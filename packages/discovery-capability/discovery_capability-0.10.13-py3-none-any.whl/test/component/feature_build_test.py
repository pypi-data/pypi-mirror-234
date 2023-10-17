import unittest
import os
from pathlib import Path
import shutil
import ast
from datetime import datetime
from pprint import pprint

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from ds_core.handlers.event_handlers import EventPersistHandler

from ds_capability.intent.feature_build_intent import FeatureBuildIntent
from ds_core.properties.property_manager import PropertyManager

from ds_capability import FeatureBuild

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class FeatureBuilderTest(unittest.TestCase):

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

    def test_run_intent_pipeline(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        _ = tools.get_synthetic_data_types(size=10, inc_nulls=True, intent_level='simulator')
        _ = tools.correlate_number(_, header='num', intent_level='data_quality', intent_order=0)
        _ = tools.build_profiling(_, profiling='quality', intent_level='data_quality', intent_order=1)
        # pprint(pm_view('feature_build', 'test', 'intent'))
        fb.run_component_pipeline(intent_levels=['simulator', 'data_quality'])
        result = fb.load_persist_canonical()
        self.assertEqual((21, 4), result.shape)
        # get number of columns from the summary
        self.assertEqual(str(20), result.column('summary').slice(7, 1).to_pylist()[0])

    def test_run_intent_pipeline_event_manager(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        fb.set_persist_uri('event://task')
        _ = tools.get_synthetic_data_types(size=10, inc_nulls=True, intent_level='simulator')
        _ = tools.correlate_number(_, header='num', intent_level='data_quality', intent_order=0)
        _ = tools.build_profiling(_, profiling='quality', intent_level='data_quality', intent_order=1)
        # pprint(pm_view('feature_build', 'test', 'intent'))
        fb.run_component_pipeline(intent_levels=['simulator', 'data_quality'])
        result = fb.load_persist_canonical()
        self.assertEqual((21, 4), result.shape)
        # get number of columns from the summary
        self.assertEqual(str(20), result.column('summary').slice(7, 1).to_pylist()[0])
        h = fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST)
        self.assertIsInstance(h,EventPersistHandler)

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")


def get_table():
    num = pa.array([1.0, None, 5.0, -0.46421, 3.5, 7.233, -2], pa.float64())
    val = pa.array([1, 2, 3, 4, 5, 6, 7], pa.int64())
    date = pc.strptime(["2023-01-02 04:49:06", "2023-01-02 04:57:12", None, None, "2023-01-02 05:23:50", None, None],
                       format='%Y-%m-%d %H:%M:%S', unit='ns')
    text = pa.array(["Blue", "Green", None, 'Red', 'Orange', 'Yellow', 'Pink'], pa.string())
    binary = pa.array([True, True, None, False, False, True, False], pa.bool_())
    cat = pa.array([None, 'M', 'F', 'M', 'F', 'M', 'M'], pa.string()).dictionary_encode()
    return pa.table([num, val, date, text, binary, cat], names=['num', 'int', 'date', 'text', 'bool', 'cat'])


def pm_view(capability: str, task: str, section: str = None):
    uri = os.path.join(os.environ['HADRON_PM_PATH'], f"hadron_pm_{capability}_{task}.parquet")
    tbl = pq.read_table(uri)
    tbl = tbl.column(0).combine_chunks()
    result = ast.literal_eval(tbl.to_pylist()[0]).get(capability, {}).get(task, {})
    return result.get(section, {}) if isinstance(section, str) and section in result.keys() else result


if __name__ == '__main__':
    unittest.main()
