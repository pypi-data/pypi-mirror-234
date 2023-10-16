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

    def test_run_data_tyoe_runbook(self):
        os.environ['HADRON_PROFILING_SOURCE_URI'] = 'working/source/hadron_synth_other.pq'
        os.environ['HADRON_DATA_QUALITY_URI'] = 'working/data/quality.parquet'
        os.environ['HADRON_DATA_DICTIONARY_URI'] = 'working/data/dictionary.parquet'
        os.environ['HADRON_DATA_SCHEMA_URI'] = 'working/data/schema.parquet'

        from ds_capability import FeatureBuild
        from ds_capability.components.commons import Commons

        # feature builder
        fb = FeatureBuild.from_env('data_profiling', has_contract=False)
        tbl = fb.set_source_uri('${HADRON_PROFILING_SOURCE_URI}').load_source_canonical()
        _ = fb.set_persist_uri('event://profiling')
        _ = fb.add_connector_uri('quality', '${HADRON_DATA_QUALITY_URI}')
        _ = fb.add_connector_uri('dictionary', '${HADRON_DATA_DICTIONARY_URI}')
        _ = fb.add_connector_uri('schema', '${HADRON_DATA_SCHEMA_URI}')
        tbl = fb.tools.build_profiling(tbl, profiling='quality', connector_name='quality', intent_order=0)
        tbl = fb.tools.build_profiling(tbl, profiling='dictionary', connector_name='dictionary', intent_order=1)
        tbl = fb.tools.build_profiling(tbl, profiling='schema', connector_name='schema', intent_order=2)
        fb.run_component_pipeline()

        # c = Controller.from_env()
        # print(pm_view('controller', 'master'))
        # c.run_controller()

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


def tprint(t: pa.table, headers: [str, list] = None, d_type: [str, list] = None, regex: [str, list] = None):
    _ = Commons.filter_columns(t.slice(0, 10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
