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

    def test_run_remote_runbook(self):
        os.environ['HADRON_PROFILING_SOURCE_URI'] = 'working/source/hadron_synth_other.pq'
        os.environ['HADRON_DATA_QUALITY_URI'] = 'working/data/quality.parquet'
        os.environ['HADRON_DATA_DICTIONARY_URI'] = 'working/data/dictionary.parquet'
        os.environ['HADRON_DATA_SCHEMA_URI'] = 'working/data/schema.parquet'

        remote_uri = 'https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/contracts/pyarrow/data_profiling'
        c = Controller.from_env(uri_pm_repo=remote_uri)
        c.run_controller()

    def test_run_feature_select(self):
        fe = FeatureEngineer.from_memory()
        fe.set_persist('synthetic_data.parquet')
        tbl = fe.tools.get_synthetic_data_types(10)
        fe.save_persist_canonical(tbl)
        # test
        fs = FeatureSelect.from_env('fs_component', has_contract=False)
        fs.set_source(fe.get_persist_uri())
        fs.set_persist()
        print(fs.report_connectors().to_string())

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")


def pm_view(capability: str, task: str, section: str = None):
    uri = os.path.join(os.environ['HADRON_PM_PATH'], f"hadron_pm_{capability}_{task}.json")
    tbl = pq.read_table(uri)
    tbl = tbl.column(0).combine_chunks()
    result = ast.literal_eval(tbl.to_pylist()[0]).get(capability, {}).get(task, {})
    return result.get(section, {}) if isinstance(section, str) and section in result.keys() else result


def tprint(t: pa.table, headers: [str, list] = None, d_type: [str, list] = None, regex: [str, list] = None):
    _ = Commons.filter_columns(t.slice(0, 10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
