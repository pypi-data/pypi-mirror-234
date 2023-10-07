import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureBuild
from ds_capability.intent.feature_build_intent import FeatureBuildIntent
from ds_core.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class FeatueBuildDiffTest(unittest.TestCase):

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
        # os.environ['HADRON_PM_TYPE'] = 'json'
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
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        fb.set_source_uri('./working/source/hadron_synth_origin.pq')
        fb.add_connector_uri('sample', './working/source/hadron_synth_other.pq')
        tbl = fb.load_source_canonical()
        result = tools.build_difference(tbl, other='sample', on_key='unique')
        for c in result.column_names:
            if c == 'num':
                self.assertEqual(5, pc.sum(result.column(c)).as_py())
            elif c == 'int':
                self.assertEqual(2, pc.sum(result.column(c)).as_py())
            elif c == 'unique':
                self.assertLess(result.num_rows, pc.sum(result.column(c)).as_py())
            else:
                self.assertEqual(0, pc.sum(result.column(c)).as_py())

    def test_pipeline(self):
        fb = FeatureBuild.from_env('tester', has_contract=False)
        tools: FeatureBuildIntent = fb.tools
        fb.set_source_uri('./working/source/hadron_synth_origin.pq')
        fb.add_connector_uri('sample', './working/source/hadron_synth_other.pq')
        tbl = fb.load_source_canonical()
        _ = tools.build_difference(tbl, other='sample', on_key='unique', intent_level='diff')
        fb.run_component_pipeline()
        result = fb.load_persist_canonical()
        self.assertEqual((10,7), result.shape)

    def test_model_no_difference(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        fb.add_connector_uri('sample', './working/data/sample.parquet')
        tbl = tools.get_synthetic_data_types(10, inc_nulls=False)
        fb.save_canonical('sample', tbl)
        tbl = tools.build_difference(tbl, other='sample', on_key='int', drop_zero_sum=True)
        self.assertEqual(['int'], tbl.column_names)
        self.assertEqual(0, tbl.num_rows)

    def test_model_difference_num(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data=    {"A": list("ABCDEFG"), "B": [1, 2, 5, 5, 3, 3, 1], 'C': [0,  2, 3, 3, 3, 2, 1], 'D': [0, 2, 0, 4, 3, 2, 1]})
        target = pa.table(data={"A": list("ABCDEFG"), "B": [1, 2, 5, 4, 3, 3, 1], 'C': [11, 2, 3, 4, 3, 2, 1], 'D': [0, 2, 0, 4, 3, 2, 1]})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        # normal
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=False)
        self.assertEqual((7,4), result.shape)
        # drop zero rows
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=True)
        self.assertEqual((2,3), result.shape)
        self.assertEqual(['A', 'D'], result.column('A').to_pylist())
        self.assertEqual([0,1], result.column('B').to_pylist())
        self.assertEqual([1,1], result.column('C').to_pylist())

    def test_model_difference_str(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data=    {"A": list("ABCDEFG"), "B": ['B', 'C', 'A', 'A', 'F', 'E', 'G'], 'C': ['L', 'L',  'M', 'N', 'J', 'K', 'M']})
        target = pa.table(data={"A": list("ABCDEFG"), "B": ['B', 'C', 'D', 'A', 'F', 'E', 'G'], 'C': ['L', 'FX', 'M', 'N', 'P', 'K', 'M']})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        # tests
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=False)
        self.assertEqual((7,3), result.shape)
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=True)
        self.assertEqual((3,3), result.shape)
        self.assertEqual(['B', 'C', 'E'], result.column('A').to_pylist())
        self.assertEqual([0,1,0], result.column('B').to_pylist())
        self.assertEqual([1,0,1], result.column('C').to_pylist())

    def test_model_difference_unmatched(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data={"X": list("ABCDEFGHK"),"Y": list("ABCABCABC"),  "B": ['B','C','A','A','F','E','G','X','Y'],'C': ['L','L','M','N','J','K','M','X','Y']})
        target = pa.table(data={"X": list("ABCDEFGX"),"Y": list("ABCABCAB"),"B": ['B','C','D','A','F','E','G','P'],    'C': ['L','FX','M','N','P','K','M','P'],"D": list("XYZXYZXY")})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.add_connector_uri('unmatched', uri='working/data/unmatched.csv')
        fb.save_canonical('target', target)
        # test
        self.assertEqual((9, 4), df.shape)
        self.assertEqual((8, 5), target.shape)
        result = tools.build_difference(df, 'target', on_key=['X', 'Y'], drop_zero_sum=True, unmatched_connector='unmatched')
        self.assertEqual((3,4), result.shape)
        unmatched = fb.load_canonical('unmatched')
        self.assertEqual((3,4), result.shape)
        self.assertEqual(['left_only', 'left_only', 'right_only', ], unmatched.column('found_in').to_pylist())
        self.assertEqual(['H', 'K', 'X', ], unmatched.column('X').to_pylist())

    def test_model_difference_unmatched_data(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        fb.set_source_uri('working/source/hadron_synth_origin.pq')
        fb.add_connector_uri('target', uri='working/source/hadron_synth_other.pq')
        fb.add_connector_uri('unmatched', uri='working/data/unmatched.csv')
        # data
        df = fb.load_source_canonical()
        target = fb.load_canonical('target')
        self.assertEqual(((12, 10), (15, 8)), (df.shape, target.shape))
        # test
        _ = tools.build_difference(df, 'target', on_key=['unique'], drop_zero_sum=True, unmatched_connector='unmatched')
        unmatched = fb.load_canonical('unmatched')
        self.assertEqual((7, 12), unmatched.shape)
        column = unmatched.column('found_in')
        mapping = pc.equal(column, "left_only")
        self.assertEqual(2, column.filter(mapping).length())
        mapping = pc.equal(column, "right_only")
        self.assertEqual(5, column.filter(mapping).length())

    def test_model_difference_equal(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data=    {"X": list("ABCDEFG"), "Y": list("RSTUVWX"), "B": ['B', 'C', 'A', 'A', 'F', 'E', 'G'], 'C': ['L', 'L',  'M', 'N', 'J', 'K', 'M']})
        target = pa.table(data={"X": list("ABCDEFG"), "Y": list("RSTUVWX"), "B": ['B', 'C', 'A', 'A', 'F', 'E', 'G'], 'C': ['L', 'L',  'M', 'N', 'J', 'K', 'M']})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        # identical
        result = tools.build_difference(df, 'target', on_key='X')
        self.assertEqual((7,4), result.shape)
        result = tools.build_difference(df, 'target', on_key='X', drop_zero_sum=True)
        self.assertEqual((0,1), result.shape)
        self.assertEqual(['X'], result.column_names)
        result = tools.build_difference(df, 'target', on_key=['X', 'Y'], drop_zero_sum=True)
        self.assertEqual((0,2), result.shape)
        self.assertCountEqual(['Y','X'], result.column_names)

    def test_model_difference_multi_key(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data=    {"X": list("ABCDEFG"), "Y": list("RSTUVWX"), "B": ['B', 'C', 'A', 'A', 'F', 'E', 'G'], 'C': ['L', 'L',  'M', 'N', 'J', 'K', 'M']})
        target = pa.table(data={"X": list("ABCDEFG"), "Y": list("RSTUVWX"), "B": ['B', 'C', 'D', 'A', 'F', 'E', 'G'], 'C': ['L', 'FX', 'M', 'N', 'P', 'K', 'M']})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        # one key
        result = tools.build_difference(df, 'target', on_key=['X'])
        self.assertTrue(all((v is None) or isinstance(v, str) for v in result.column('X').to_pylist()))
        self.assertFalse(all((v is None) or isinstance(v, str) for v in result.column('Y').to_pylist()))
        # two keys
        result = tools.build_difference(df, 'target', on_key=['X', 'Y'])
        self.assertTrue(all((v is None) or isinstance(v, str) for v in result.column('X').to_pylist()))
        self.assertTrue(all((v is None) or isinstance(v, str) for v in result.column('Y').to_pylist()))


    def test_model_difference_order(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data={"A": list("ABCDEFG"), "B": list("ABCFCBA"), 'C': list("BCDECFB"), 'D': [0, 2, 0, 4, 3, 2, 1]})
        target = pa.table(data={"A": list("ABCDEFG"), "B": list("BBCDCAA"), 'C': list("BCDECFB"), 'D': [0, 2, 0, 4, 1, 2, 1]})
        _ = target.to_pandas().sample(frac = 1)
        target = pa.Table.from_pandas(_)
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=True)
        self.assertEqual((4,3), result.shape)
        self.assertEqual(['A', 'B', 'D'], result.column_names)

    def test_model_difference_drop(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data={"A": list("ABCDEFG"), "B": list("ABCFCBA"), 'C': list("BCDECFB"), 'D': [0, 2, 0, 4, 3, 2, 1]})
        target = pa.table(data={"A": list("ABCDEFG"), "B": list("BBCDCAA"), 'C': list("BCDECFB"), 'D': [0, 2, 0, 4, 1, 2, 1]})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        result = tools.build_difference(df, 'target', on_key='A', drop_zero_sum=True)
        self.assertEqual((4,3), result.shape)
        self.assertEqual(['A', 'B', 'D'], result.column_names)

    def test_model_difference_summary(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data={"X":  list("ABCDEFG"),    "Y": list("ABCDEFG"), "B": [1, 2, 3, 4, 3, 3, 1], 'C': [0, 2, 0, 4, 3, 2, 1]})
        target = pa.table(data={"X": list("ABCDEFG"), "Y": list("ABCDEFG"), "B": [1, 2, 5, 4, 3, 3, 1], 'C': [1, 2, 3, 4, 3, 2, 1]})
        fb.add_connector_persist('target', uri_file='target.csv')
        fb.save_canonical('target', target)
        # summary connector
        fb.add_connector_persist('summary', uri_file='summary.csv')
        _ = tools.build_difference(df, 'target', on_key='X', summary_connector='summary')
        result = fb.load_canonical('summary')
        self.assertEqual(result.shape, (6,2))
        self.assertEqual(result.column('Attribute').to_pylist(), ['matching','left_only','right_only','B','C','Y'])
        self.assertEqual(result.column('Summary').to_pylist(), [7,0,0,1,2,0])
        _ = tools.build_difference(df, 'target', on_key='X', summary_connector='summary', drop_zero_sum=True)
        result = fb.load_canonical('summary')
        self.assertEqual(result.shape, (5,2))
        self.assertEqual(result.column('Attribute').to_pylist(), ['matching','left_only','right_only','B','C'])
        self.assertEqual(result.column('Summary').to_pylist(), [7,0,0,1,2])

    def test_model_difference_detail(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        df = pa.table(data={"X":  list("CBADEFG"), "Y":  list("ABCDEFG"), "B": [1, 2, 3, 4, 3, 3, 1], 'C': [0, 2, 0, 4, 3, 2, 1]})
        target = pa.table(data={"X": list("CBADEFG"), "Y":  list("ABCDEFG"), "B": [1, 2, 5, 4, 3, 3, 1], 'C': [1, 2, 3, 4, 3, 2, 1]})
        fb.add_connector_persist('target', uri_file='working/data/target.csv')
        fb.save_canonical('target', target)
        # detail connector
        fb.add_connector_persist('detail', uri_file='detail.csv')
        _ = tools.build_difference(df, 'target', on_key='X', detail_connector='detail')
        result = fb.load_canonical('detail')
        self.assertEqual(result.shape, (2,5))
        self.assertEqual(result.column_names, ['X', 'B_x', 'B_y', 'C_x', 'C_y'])
        # self.assertEqual(result.loc[0].values.tolist(), ['A', '3', '5', 0, 3])
        _ = tools.build_difference(df, 'target', on_key=['X', 'Y'], detail_connector='detail')
        result = fb.load_canonical('detail')
        self.assertEqual(result.shape, (2,6))
        self.assertEqual(result.column_names, ['X', 'Y', 'B_x', 'B_y', 'C_x', 'C_y'])
        # self.assertEqual(result.loc[0].values.tolist(), ['A', 'C', '3', '5', 0, 3])


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
