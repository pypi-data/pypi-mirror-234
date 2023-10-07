# Developing Mongo Persist Handler
import ast
import pyarrow as pa

from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler
from ds_core.handlers.abstract_handlers import HandlerFactory, ConnectorContract
from ds_capability.components.commons import Commons


class MongodbSourceHandler(AbstractSourceHandler):
    """ A mongoDB source handler"""

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the source_contract dictionary """
        # required module import
        self.mongo = HandlerFactory.get_module('pymongo')
        self.pymongo = HandlerFactory.get_module('pymongoarrow')
        self.bson = HandlerFactory.get_module('bson')
        super().__init__(connector_contract)

        _kwargs = {**self.connector_contract.kwargs, **self.connector_contract.query}
        database = _kwargs.pop('database', "hadron_db")
        self.collection_name = _kwargs.pop('collection', "records")
        self._mongo_find = ast.literal_eval(_kwargs.pop('find').replace("'", '"')) if _kwargs.get('find') else {}
        self._mongo_aggregate = ast.literal_eval(_kwargs.pop('aggregate').replace("'", '"')) if _kwargs.get('aggregate') else None
        self._mongo_project = ast.literal_eval(_kwargs.pop('project').replace("'", '"')) if _kwargs.get('project') else None
        self._mongo_limit = int(_kwargs.pop('limit').replace("'", '"')) if _kwargs.get('limit') else None
        self._mongo_skip = int(_kwargs.pop('skip').replace("'", '"')) if _kwargs.get('skip') else None
        self._mongo_sort = ast.literal_eval(_kwargs.pop('sort').replace("'", '"')) if _kwargs.get('sort') else None
        self._decode = _kwargs.pop('decode') if _kwargs.get('decode') else False

        self._if_exists = _kwargs.pop('if_exists', 'replace')
        self._file_state = 0
        self._changed_flag = True

        self._mongo_document = self.mongo.MongoClient(self.connector_contract.address)[database]
        self._mongo_collection = self._mongo_document[self.collection_name]

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['mongodb']

    def load_canonical(self, **kwargs) -> pa.Table:
        """ returns the canonical dataset based on the source contract
            The canonical in this instance is a dictionary that has the headers as the key and then
            the ordered list of values for that header
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The PandasSource Connector Contract has not been set")

        def traverse_it(it):
            if isinstance(it, list):
                for item in it:
                    traverse_it(item)
            elif isinstance(it, dict):
                if '_id' in it.keys():
                    if isinstance(it.get('_id'), self.bson.ObjectId):
                        it.update({'_id': str(it.get('_id'))})
                for key in it.keys():
                    traverse_it(it[key])

        #    else: # returns top of the tree item

        if self._mongo_aggregate is not None:
            result = list(self._mongo_collection.aggregate(self._mongo_aggregate))
            if isinstance(result[0].get('_id'), self.bson.ObjectId) or self._decode:
                traverse_it(result)
            return Commons.table_flatten(pa.Table.from_pylist(result))
        cursor = self._mongo_collection.find(self._mongo_find, self._mongo_project)
        if self._mongo_limit is not None:
            cursor.limit(self._mongo_limit)
        if self._mongo_skip is not None:
            cursor.skip(self._mongo_skip)
        if self._mongo_sort is not None:
            cursor.sort(self._mongo_sort)
        result = list(cursor)
        if isinstance(result[0].get('_id'), self.bson.ObjectId) or self._decode:
            traverse_it(result)
        return Commons.table_flatten(pa.Table.from_pylist(result))

    def exists(self) -> bool:
        """ returns True if the collection exists """
        return self.collection_name in self._mongo_document.list_collection_names()

    def has_changed(self) -> bool:
        """ returns the amount of documents in the collection
            ... if the counts change ... then the collection was probably modified ...
            ... this assumes that records are never edited/updated ... nor deleted ...
        """
        _cc = self.connector_contract
        state = self._mongo_collection.count_documents(self._mongo_find)
        if state != self._file_state:
            self._changed_flag = True
            self._file_state = state
        return self._changed_flag

    def reset_changed(self, changed: bool = False):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed


class MongodbPersistHandler(MongodbSourceHandler, AbstractPersistHandler):
    # a mongoDB persist handler

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _uri = self.connector_contract.uri
        return self.backup_canonical(canonical=canonical, collection_name=self.collection_name, **kwargs)

    def backup_canonical(self, canonical: pa.Table, collection_name: str, **kwargs) -> bool:
        """  creates a backup of the canonical to an alternative table """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _collection = self._mongo_document[collection_name]
        tbl = Commons.table_nest(canonical)
        # remove anything there as this is replaced
        _collection.delete_many({})
        resp = _collection.insert_many(tbl)
        return resp.acknowledged

    def remove_canonical(self) -> bool:
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        return self._mongo_document.drop_collection(self.collection_name)
