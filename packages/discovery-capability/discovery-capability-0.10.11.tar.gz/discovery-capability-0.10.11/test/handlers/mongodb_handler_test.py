import unittest
import os
from datetime import datetime
from pathlib import Path
import shutil
import pyarrow as pa
import pyarrow.compute as pc
from ds_core.handlers.abstract_handlers import ConnectorContract
from ds_core.properties.property_manager import PropertyManager
from ds_capability import FeatureBuild


class MongodbHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'json'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_handler_default(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        tbl = fb.tools.get_number(1_000_000, 10_000_000, canonical=tbl, at_most=1, size=tbl.num_rows, column_name='_id')
        fb.set_persist_uri("mongodb://admin:admin@localhost:27017/")
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        self.assertFalse(fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST).exists())
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertTrue(fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST).exists())
        self.assertEqual((1000, 7), result.shape)
        self.assertEqual(['_id', 'cat', 'num', 'int', 'bool', 'date', 'string'], result.column_names)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_sort(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=10, seed=101)
        uri = "mongodb://admin:admin@localhost:27017/?project={'cat':1, 'num':1, '_id':0}&sort=[('num', 1)]"
        fb.set_persist_uri(uri=uri).save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        c = result.column('num').combine_chunks()
        self.assertEqual(pc.min(c), c[0])
        self.assertEqual(pc.max(c), c.slice(len(c)-1)[0])

    def test_handler_query(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://admin:admin@localhost:27017/?collection=${collection}&find={}&project={'cat':1, 'num':1}"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual((1000, 2), result.shape)
        self.assertEqual(['cat', 'num'], result.column_names)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_find_limit(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://admin:admin@localhost:27017/?collection=${collection}&find={}&project={'cat':1, 'num':1, '_id':0}&limit=2&spip=2"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual((2, 2), result.shape)
        self.assertEqual(['cat', 'num'], result.column_names)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_aggregate(self):
        os.environ['HADRON_AGG'] = """
        [
            {"$match": { 
                "cat": { "$eq": "ACTIVE" },
            }},
            {"$project": {
                "_id":0,
                "cat":1,  
                "num":1, 
                "int":1, 
            }},
            {'$limit':50}
        ]
        """
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        uri = "mongodb://admin:admin@localhost:27017/?aggregate=${HADRON_AGG}"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual(['cat', 'num', 'int'], result.column_names)
        self.assertEqual(['ACTIVE'], pc.unique(result.column('cat')).to_pylist())
        self.assertEqual(50, result.num_rows)

    def test_connector_contract(self):
        os.environ['HADRON_ADDITION'] = 'myAddition'
        os.environ['HADRON_AGG'] = """
        [
            {"$match": { 
                "creditProfile": { "$ne": None },
                #"creditProfile.creditScore": { "$ne": None }
            }},
            {"$project": {
                "customerCategory":1,  
                "customerSubCategory":1, 
                "customerType":1, 
                "organizationChildRelationship": {
                    "$cond": {
                        "if": {"$isArray": "$organizationChildRelationship"},
                        "then": "$organizationChildRelationship",
                        "else": [
                            {
                                "organization": {
                                    "_id": None,
                                    "referredType": None
                                },
                                "relationshipType": None
                            }
                        ]
                    }},
                "riskCategory":1, 
                "status": 1,
                "creditProfile": 1, 
                "deniedList.isDenied": 1, 
                "deniedList.validFor.startDateTime": 1,
                "engagedParty": 1
            }},
            {'$limit':2000}
        ]
        """
        uri = "mongodb://admin:admin@localhost:27017/?database=hadron_docs&collection=records&aggregate=${HADRON_AGG}"
        cc = ConnectorContract(uri=uri, module_name='', handler='', addition='${HADRON_ADDITION}')
        print(f"raw_uri = {cc.raw_uri}")
        print(f"uri = {cc.uri}")
        print(f"raw_kwargs = {cc.raw_kwargs}")
        print(f"address = {cc.address}")
        print(f"schema = {cc.schema}")
        print(f"hostname = {cc.hostname}")
        print(f"port = {cc.port}")
        print(f"username = {cc.username}")
        print(f"password = {cc.password}")
        print(f"path = {cc.path}")
        print(f"database = {cc.path[1:]}")
        print(f"query")
        extra = cc.query.pop('extra', None)
        print(f" extra = {extra}")
        find = cc.query.pop('find', None)
        print(f" mongo_find = {find}")
        aggregate = cc.query.pop('aggregate', None)
        print(f" mongo_aggregate = {aggregate}")
        collection = cc.query.pop('collection', None)
        print(f" collection = {collection}")
        print(f"kwargs")
        addition = cc.kwargs.get('addition', None)
        print(f" addition = {addition}")

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")



if __name__ == '__main__':
    unittest.main()
