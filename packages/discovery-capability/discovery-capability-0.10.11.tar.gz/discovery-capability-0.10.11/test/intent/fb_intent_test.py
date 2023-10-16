import unittest
import os
from pathlib import Path
import shutil
import ast
from pprint import pprint

import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from ds_capability.sample.sample_data import MappedSample

from ds_capability import FeatureBuild
from ds_capability.intent.feature_build_intent import FeatureBuildIntent
from ds_core.properties.property_manager import PropertyManager

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

    def test_for_smoke(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        self.assertEqual((100, 6), tbl.shape)
        self.assertCountEqual(['cat', 'num', 'int', 'bool', 'date', 'string'], tbl.column_names)
        tbl = tools.get_synthetic_data_types(100, inc_nulls=True, prob_nulls=0.03)
        self.assertEqual((100, 19), tbl.shape)

    def test_event_event_singleton(self):
        fb = FeatureBuild.from_env('task1', has_contract=False)
        fb.set_persist_uri("event://task1_outcome")
        tbl = fb.tools.get_synthetic_data_types(size=10)
        # pprint(pm_view('feature_build', 'task1', 'intent'))
        fb.run_component_pipeline()
        h = fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST)
        self.assertEqual(tbl.column_names, h.event_manager.get('task1_outcome').column_names)
        result = fb.load_persist_canonical()
        self.assertEqual(tbl.column_names, result.column_names)
        self.assertEqual(tbl.shape, result.shape)

    def test_run_intent_pipeline(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        # reload the properties
        fb = FeatureBuild.from_env('test')
        _ = tools.get_synthetic_data_types(size=10, inc_nulls=True)
        result = fb.tools.run_intent_pipeline()
        self.assertEqual((10, 19), result.shape)
        _ = tools.correlate_number(result, header='num')
        result = fb.tools.run_intent_pipeline(canonical=result)
        self.assertEqual((10, 20), result.shape)
        _ = tools.build_profiling(result, profiling='quality')
        pprint(pm_view('feature_build', 'test', 'intent'))
        result = fb.tools.run_intent_pipeline(canonical=result)
        self.assertEqual((21, 4), result.shape)

    def test_run_intent_pipeline_order(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        # reload the properties
        fb = FeatureBuild.from_env('test')
        _ = tools.get_synthetic_data_types(size=10, inc_nulls=True, intent_order=0)
        _ = tools.correlate_number(_, header='num', intent_order=1)
        _ = tools.build_profiling(_, profiling='quality', intent_order=1)
        pprint(pm_view('feature_build', 'test', 'intent'))
        result = fb.tools.run_intent_pipeline()
        self.assertEqual((21, 4), result.shape)

    def test_run_intent_pipeline_canonical(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        # reload the properties
        fb = FeatureBuild.from_env('test')
        tbl = tools.get_synthetic_data_types(size=10, inc_nulls=True, save_intent=False)
        _ = tools.correlate_number(tbl, header='num')
        _ = tools.build_profiling(_, profiling='quality')
        pprint(pm_view('feature_build', 'test', 'intent'))
        result = fb.tools.run_intent_pipeline(canonical=tbl)
        self.assertEqual((21, 4), result.shape)
        # get number of columns from the summary
        self.assertEqual(str(20), result.column('summary').slice(7, 1).to_pylist()[0])

    def test_run_intent_pipeline_intent_level(self):
        fb = FeatureBuild.from_env('test', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        # reload the properties
        fb = FeatureBuild.from_env('test')
        tbl = tools.get_synthetic_data_types(size=10, inc_nulls=True, save_intent=False)
        _ = tools.correlate_number(tbl, header='num', intent_level='quantity')
        _ = tools.build_profiling(_, profiling='quality', intent_level='quantity')
        pprint(pm_view('feature_build', 'test', 'intent'))
        result = fb.tools.run_intent_pipeline(canonical=tbl, intent_level='quantity')
        self.assertEqual((21, 4), result.shape)
        # get number of columns from the summary
        self.assertEqual(str(20), result.column('summary').slice(7, 1).to_pylist()[0])

    #
    def test_get_noise(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_noise(10, num_columns=3)
        self.assertEqual((10, 3), tbl.shape)
        self.assertEqual(['A', 'B', 'C'], tbl.column_names)
        tbl = tools.get_noise(10, num_columns=3, name_prefix='P_')
        self.assertEqual(['P_A', 'P_B', 'P_C'], tbl.column_names)

    def test_get_sample_map(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        print(tools.sample_map)
        # tools.get_sample_map('us_persona', size=10, )
        i = tools.sample_inspect('us_persona')
        print(i)

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))

def pm_view(capability: str, task: str, section: str=None):
    uri = os.path.join(os.environ['HADRON_PM_PATH'], f"hadron_pm_{capability}_{task}.parquet")
    tbl = pq.read_table(uri)
    tbl = tbl.column(0).combine_chunks()
    result = ast.literal_eval(tbl.to_pylist()[0]).get(capability,{}).get(task,{})
    return result.get(section, {}) if isinstance(section, str) and section in result.keys() else result


if __name__ == '__main__':
    unittest.main()
