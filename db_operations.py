import pymongo
import certifi
import pandas as pd

class MongoDBManagement:
    def __init__(self, username, password):
        try:
            self.username = username
            self.password = password
            self.uri = f"mongodb+srv://{self.username}:{self.password}@cluster0.99jtb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        except Exception as e:
            raise Exception("__init__: Something went wrong on initiation process\n" + str(e))
    

    def get_mongodb_clientobj(self):
        try:
            mongo_client = pymongo.MongoClient(self.uri, tlsCAFile=certifi.where())
            return mongo_client
        except Exception as e:
            raise Exception("get_mongodb_clientobj: Something went wrong on creation of client object\n" + str(e))

    '''
        #closing mongo_db connection explicitly is not required as it is handled by MongoClient() for auto connection 

        def close_mongodb_connection(self, mongo_client):
        try:
            mongo_client.close()
        except Exception as e:
            raise Exception("close_mongodb_connection: Something went wrong on closing connection\n" + str(e))
    '''



    def is_database_present(self, db_name):
        try:
            mongo_client = self.get_mongodb_clientobj()
            if db_name in mongo_client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception("is_database_present: Failed to check database existence \n" + str(e))

    
    def fetch_database(self, db_name):
        try:
            mongo_client = self.get_mongodb_clientobj()
            database = mongo_client[db_name]
            return database
        except Exception as e:
            raise Exception(f"fetch_database: Failed on creating database\n" + str(e))


    def drop_database(self, db_name):
        try:
            mongo_client = self.get_mongodb_clientobj()
            if db_name in mongo_client.list_database_names():
                mongo_client.drop_database(db_name)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"drop_database: Failed to delete database {db_name}\n" + str(e))


    def fetch_collection(self, collection_name, db_name):
        try:
            database = self.fetch_database(db_name)
            return database[collection_name]
        except Exception as e:
            raise Exception(f"fetch_collection: Failed to get the database list.")


    def is_collection_present(self, collection_name, db_name):
        try:
            database = self.fetch_database(db_name=db_name)
            if collection_name in database.list_collection_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"is_collection_present: Failed to check collection\n" + str(e))

    
    def drop_collection(self, collection_name, db_name):
        try:
            database = self.fetch_database(db_name)
            if collection_name in database.list_collection_names():
                database[collection_name].drop()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"drop_collection: Failed to drop collection {collection_name}")  

    
    def insert_record(self, collection_name, db_name, record):
        try:
            return self.fetch_collection(collection_name, db_name).insert_one(record)
        except Exception as e:
            raise Exception("insert_record: Error inserting record")


    def insert_records(self, collection_name, db_name, records):
        try:
            return self.fetch_collection(collection_name, db_name).insert_many(records)
        except Exception as e:
            raise Exception("insert_records: Error inserting records")

    
    def find_record(self, collection_name, db_name):
        try:
            return self.fetch_collection(collection_name, db_name).find_one()
        except Exception as e:
            raise Exception("find_record: Error in fetching first record")


    def find_records(self, collection_name, db_name, query=None):
        try:
            if query is not None:
                return self.fetch_collection(collection_name, db_name).find(query)
            else:
                return self.fetch_collection(collection_name, db_name).find()
        except Exception as e:
            raise Exception("find_records: Error in fetching records with provided query")


    def update_one_record(self, collection_name, db_name, filter=None, new_value=None):
        try:
            return self.fetch_collection(collection_name, db_name).update_one(filter,new_value)
        except Exception as e:
            raise Exception("update_one_record: Error in updating record with provided filter")
        

    def update_records(self, collection_name, db_name, filter=None, new_value=None):
        try:
            return self.fetch_collection(collection_name, db_name).update(filter,new_value)
        except Exception as e:
            raise Exception("update_records: Error in updating records with provided filter")


    def delete_record(self, collection_name, db_name, query=None):
        try:
            if query is not None:
                return self.fetch_collection(collection_name, db_name).delete_one(query)
            else:
                return self.fetch_collection(collection_name, db_name).delete_one({})
        except Exception as e:
            raise Exception("delete_record: Error in deleting record with provided query")


    def delete_records(self, collection_name, db_name, query=None):
        try:
            if query is not None:
                return self.fetch_collection(collection_name, db_name).delete_many(query)
            else:
                return self.fetch_collection(collection_name, db_name).delete_many({})
        except Exception as e:
            raise Exception("delete_records: Error in deleting records with provided query")
    

    def collection_to_dataframe(self, collection_name, db_name):
        try:
            df = pd.Dataframe(self.find_records(collection_name, db_name))
            return df
        except Exception as e:
            raise Exception(f"collection_to_dataframe: Failed to get DatFrame from provided collection and database.\n" + str(e))


    def dataframe_to_collection(self, collection_name, db_name, df):
        try:
            records = df.to_dict(orient='records')
            return self.insert_records(collection_name, db_name, records)
        except Exception as e:
            raise Exception(f"collection_to_dataframe: Failed to get DatFrame from provided collection and database.\n" + str(e))