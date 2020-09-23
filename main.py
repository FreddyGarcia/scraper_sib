from scraper import gather_all_documents, gather_documents_1
from persistence import Document, Session, remove_duplicates

def convert_to_document(row):
    return Document(row['title'], row['src'])

def main():
    documents_dict = gather_documents_1()[:3]

    # save documents
    documents_mod = list(map(convert_to_document, documents_dict))
    new_documents = (documents_mod)

    session = Session()

    session.bulk_save_objects(new_documents)

    try:
        session.commit()
    except Exception as ex:
        session.rollback()
    finally:
        session.close()

    for doc in new_documents:
        doc.download()
    
