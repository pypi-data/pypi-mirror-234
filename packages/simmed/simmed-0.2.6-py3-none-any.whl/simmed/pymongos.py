import os
from pymongo import MongoClient, database, collection, operations,errors

from simmed.info_base import UpdateResult


class ShardCollection(collection.Collection):
    def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None, array_filters=None, hint=None, session=None):
        row = self.find_one(filter, {'_id': 1})
        update_result = UpdateResult()
        if row is not None:
            # new_filter = {"_id": row["_id"]}
            filter["_id"] = row["_id"]
            return super().update_one(filter, update, upsert, bypass_document_validation, collation, array_filters, hint, session)
        return update_result

    def update_many(self, filter, update, upsert=False, array_filters=None, bypass_document_validation=False, collation=None, hint=None, session=None):
        rows = list(self.find(filter, {'_id': 1}))
        row_ids=list(map(lambda x: x["_id"], rows))
        update_result = UpdateResult()
        if rows is not None:
            batch_num = 50000
            batch_update_id_list = [row_ids[i:i + batch_num] for i in range(0, len(row_ids), batch_num)]
            for update_id_list in batch_update_id_list:
                filter["_id"] = {"$in": update_id_list}
                # new_filter = {"_id": {"$in": row_ids}}
                mg_update_result = super().update_many(filter, update, upsert, array_filters, bypass_document_validation, collation, hint, session)
                update_result.matched_count += mg_update_result.matched_count
                update_result.modified_count += mg_update_result.modified_count
        return update_result

    def update(self, filter, update, upsert=False, bypass_document_validation=False, collation=None, hint=None, session=None):
        self.update_one(filter, update, upsert, bypass_document_validation, collation, hint, session)

    def delete_one(self, filter, collation=None, hint=None, session=None):
        row = self.find_one(filter, {'_id': 1})
        if row is not None:
            new_filter = {"_id": row["_id"]}
            return super().delete_one(new_filter, collation, hint, session)

    def delete_many(self, filter, collation=None, hint=None, session=None):
        rows = list(self.find(filter, {'_id': 1}))
        row_ids=list(map(lambda x : x["_id"],rows))
        if rows is not None:
            new_filter = {"_id": {"$in": row_ids}}
            return super().delete_many(new_filter, collation, hint, session)

    def bulk_write(self, requests, ordered=True, bypass_document_validation=False, session=None):
        new_request = []
        for request in requests:
            if type(request) is operations.UpdateOne or type(request) is operations.DeleteOne or type(request) is operations.ReplaceOne:
                row = self.find_one(request._filter, {'_id': 1})
                if row is not None:
                    new_filter = {"_id": row["_id"]}
                    request._filter = new_filter
                    # print(request)
                    new_request.append(request)
            elif type(request) is operations.UpdateMany or type(request) is operations.DeleteMany:
                rows = list(self.find(request._filter, {'_id': 1}))
                if rows is not None:
                    new_filter = {"_id": {"$in": rows}}
                    request._filter = new_filter
                    # print(request)
                    new_request.append(request)
            else:
                new_request.append(request)
        return super().bulk_write(new_request, ordered, bypass_document_validation, session)


class ShardDatabase(database.Database):
    def __getitem__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        # print('shard db '+self.name)
        # print('shard collection:'+self.name+'.'+name)
        try:
            if name != 'admin' and os.getenv(self.name+'.'+name, None) is None:
                os.environ[self.name+'.'+name] = "1"
                self.client.admin.command(
                    'shardcollection', self.name+'.'+name, key={'_id': 1})
        except errors.OperationFailure:
            print("shardcollection exception:"+self.name+'.'+name)
        return ShardCollection(self, name)


class ShardMongoClient(MongoClient):
    # This attribute interceptor works when we call the class attributes.
    def __getitem__(self, name):
        # print('shard '+name)
        try:
            if name != 'admin' and os.getenv(name, None) is None:
                os.environ[name] = "1"
                db_admin = self.get_database('admin')
                db_admin.command('enablesharding', name)
        except errors.OperationFailure:
            print("enablesharding exception:"+name)
        return ShardDatabase(self, name)
