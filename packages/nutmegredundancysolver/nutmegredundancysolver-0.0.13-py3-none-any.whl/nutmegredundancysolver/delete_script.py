from pymongo import MongoClient

ATLAS_URI='mongodb+srv://james2:vatVRC5XhsRL6KPV@cluster0.lh8qz.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(ATLAS_URI)
test_collection=client['test_db'].get_collection('candidate_collection')
unittest_collection=client['test_db'].get_collection('unittest_candidate_collection')
prod_collection=client['prod_db'].get_collection('candidate_collection')

if __name__=='__main__':
    for collection in [test_collection, prod_collection, unittest_collection]:
        try:
            delete_count=len([collection.delete_many({"IsDuplicate":True})])
            print(f"deleted {delete_count} documents from {collection.collection_name}")
        except Exception as exc:
            print(exc)