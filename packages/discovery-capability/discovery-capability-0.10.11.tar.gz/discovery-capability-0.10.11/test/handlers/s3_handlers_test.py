import unittest
import os
from pathlib import Path
import shutil
import ast
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from ds_core.properties.property_manager import PropertyManager
from ds_capability import *
from ds_capability.components.commons import Commons

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class TemplateTest(unittest.TestCase):

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
        os.environ['HADRON_PM_TYPE'] = 'parquet'
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
        s3_in = 's3://project-hadron-cs-repo/domain/synthetic/source/synthetic_sample.parquet'
        s3_out = 's3://project-hadron-cs-repo/domain/synthetic/persist/synthetic_sample.parquet'
        fe = FeatureEngineer.from_memory()
        _ = fe.set_source_uri(s3_in)
        _ = fe.set_persist_uri(s3_out)
        tbl = fe.load_source_canonical()
        tprint(tbl)
        fe.save_persist_canonical(tbl)


    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")

def tprint(t: pa.table, headers: [str, list] = None, d_type: [str, list] = None, regex: [str, list] = None):
    _ = Commons.filter_columns(t.slice(0, 10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
