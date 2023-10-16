import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureEngineer
from ds_capability.intent.feature_engineer_intent import FeatureEngineerIntent
from ds_core.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class SyntheticTest(unittest.TestCase):

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
        try:
            shutil.copytree('../_test_data', os.path.join(os.environ['PWD'], 'working/source'))
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_for_smoke(self):
        fe = FeatureEngineer.from_memory()
        tools: FeatureEngineerIntent = fe.tools
        tbl = tools.get_synthetic_data_types(10)
        old_schema = tbl.schema
        fe.add_connector_uri('sample', './working/data/sample.parquet')
        fe.save_canonical('sample', tbl)
        result = fe.load_canonical('sample')
        self.assertTrue(old_schema == result.schema)

    def test_from_env(self):
        fe = FeatureEngineer.from_env('tester', has_contract=False)
        tools: FeatureEngineerIntent = fe.tools
        fe.set_persist()
        tbl = tools.get_synthetic_data_types(10)
        old_schema = tbl.schema
        fe.add_connector_uri('sample', './working/data/sample.parquet')
        fe.save_canonical('sample', tbl)
        result = fe.load_canonical('sample')
        self.assertTrue(old_schema == result.schema)

    def test_from_source(self):
        fe = FeatureEngineer.from_env('tester', has_contract=False)
        tools: FeatureEngineerIntent = fe.tools
        fe.set_source('source/hadron_synth_origin.pq')
        fe.set_persist()
        fe.run_component_pipeline()
        result = fe.load_persist_canonical()
        print(result.column_names)



    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
