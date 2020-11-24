from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from urllib import request
from datetime import date
from urllib.parse import unquote
from datetime import datetime
import hashlib
import os
import requests
import urllib3
import ssl


urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

Base = declarative_base()
engine = create_engine('sqlite:///db', echo=False)
Session = sessionmaker(bind=engine)


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    src = Column(String, nullable=False)
    save_date = Column(Date, nullable=False)
    publication_date = Column(Date, nullable=True)
    downloaded = Column(Boolean, default=False)
    hash_md5 = Column(String)

    @staticmethod
    def check_exists_by_title(title):
        return bool(Document.query().filter_by(title=title).scalar())

    @staticmethod
    def query():
        session = Session()
        query = session.query(Document)
        session.close()
        return query

    def __init__(self, title, src, pub_date=None):
        self.title = title
        self.publication_date = datetime.strptime(pub_date, '%d/%m/%Y') if pub_date is not None else None
        self.src = src
        self.save_date = date.today()
        self.hash_md5 = hashlib.md5(title.encode()).hexdigest()

    def save(self):
        session = Session()
        session.add(self)

        try:
            session.commit()
            return self.id
        except Exception as ex:
            print(ex)
            session.rollback()
        finally:
            session.close()

    def __repr__(self):
        return self.title

    def download(self, path='downloads'):
        try:
            headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
            request = requests.get(self.src, headers=headers, timeout=10000, stream=True, verify=False)
            src = unquote(os.path.basename(self.src ))
            path = os.path.join(path, src)

            with open(path, 'wb') as fh:
                for chunk in request.iter_content(1024 * 1024):
                    fh.write(chunk)

            self.downloaded = True
            self.save()
        except Exception as ex:
            print(ex)
         
def remove_duplicates(documents):
    saved_documents = Document.query().all()
    saved_hash = list(map(lambda c: c.hash_md5, saved_documents))
    new_documents = [x for x in documents if x.hash_md5 not in saved_hash]
    return new_documents

Base.metadata.create_all(engine)
