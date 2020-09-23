from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine, Boolean
from sqlalchemy.orm import sessionmaker
from urllib import request
from datetime import date
import hashlib
import os

Base = declarative_base()
engine = create_engine('sqlite:///db', echo=False)
Session = sessionmaker(bind=engine)


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    src = Column(String, nullable=False)
    save_date = Column(Date, nullable=False)
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

    def __init__(self, title, src):
        self.title = title
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
            path = os.path.join(path, os.path.basename(self.src ))
            request.urlretrieve(self.src, path)
            self.downloaded = True
            self.save()
        except Exception as ex:
            pass
         
def remove_duplicates(documents):
    saved_documents = Document.query().all()
    saved_hash = list(map(lambda c: c.hash_md5, saved_documents))
    new_documents = [x for x in documents if x.hash_md5 not in saved_hash]
    return new_documents

Base.metadata.create_all(engine)
