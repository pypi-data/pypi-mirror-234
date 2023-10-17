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
from ds_capability.intent.feature_transform_intent import FeatureTransformIntent

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

    def test_scale_normalize(self):
        tbl = pa.table([pa.array([1,2,3,4,5], pa.int64()),
                        pa.array([0,0,0,0,0], pa.int64()),
                        pa.array([1,2,None,2,1], pa.int64()),
                        pa.array([0.7, 0.223, 0.4, -0.3, -0.2], pa.float64()),
                        ], names=['int', 'zero', 'null', 'num'])
        ft = FeatureTransform.from_memory()
        tools: FeatureTransformIntent = ft.tools
        result = tools.scale_normalize(tbl)
        for c in result.columns:
            self.assertTrue(pc.greater_equal(1, pc.max(c)))
            self.assertTrue(pc.less_equal(0, pc.min(c)))
        # scale
        result = tools.scale_normalize(tbl, scalar=(4,5))
        for c in result.columns:
            self.assertTrue(pc.greater_equal(5, pc.max(c)))
            self.assertTrue(pc.less_equal(4, pc.min(c)))
        # robust
        result = tools.scale_normalize(tbl, scalar='robust')
        for c in result.columns:
            self.assertTrue(pc.greater_equal(1, pc.max(c)))
            self.assertTrue(pc.less_equal(0, pc.min(c)))

    def test_scale_standardize(self):
        tbl = pa.table([pa.array([1,2,3,4,5], pa.int64()),
                        pa.array([0,0,0,0,0], pa.int64()),
                        pa.array([1,2,None,2,1], pa.int64()),
                        pa.array([0.7, 0.223, 0.4, -0.3, -0.2], pa.float64()),
                        ], names=['int', 'zero', 'null', 'num'])
        ft = FeatureTransform.from_memory()
        tools: FeatureTransformIntent = ft.tools
        result = tools.scale_standardize(tbl)
        tprint(result)

    def test_scale_transform(self):
        tbl = pa.table([pa.array([1,2,3,4,5], pa.int64()),
                        pa.array([0.7, 0.223, 0.4, -0.3, -0.2], pa.float64()),
                        ], names=['int', 'num'])
        ft = FeatureTransform.from_memory()
        tools: FeatureTransformIntent = ft.tools
        result = tools.scale_transform(tbl, transform='log')
        tprint(result)

    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")

def pm_view(capability: str, task: str, section: str=None):
    uri = os.path.join(os.environ['HADRON_PM_PATH'], f"hadron_pm_{capability}_{task}.parquet")
    tbl = pq.read_table(uri)
    tbl = tbl.column(0).combine_chunks()
    result = ast.literal_eval(tbl.to_pylist()[0]).get(capability, {}).get(task, {})
    return result.get(section, {}) if isinstance(section, str) and section in result.keys() else result

def tprint(t: pa.table, headers: [str, list]=None, d_type: [str, list]=None, regex: [str, list]=None):
    _ = Commons.filter_columns(t.slice(0, 10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())


if __name__ == '__main__':
    unittest.main()
