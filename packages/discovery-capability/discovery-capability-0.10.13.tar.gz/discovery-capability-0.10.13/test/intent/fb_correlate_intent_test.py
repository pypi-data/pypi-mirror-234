import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureBuild
from ds_capability.components.commons import Commons
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
        tbl = tools.get_synthetic_data_types(100)
        self.assertEqual((100, 6), tbl.shape)

    def test_correlate_discrete_intervals(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        result = tools.correlate_discrete_intervals(tbl, header='num', to_header='num')
        self.assertEqual(5, pc.count(result.column('num').combine_chunks().dictionary).as_py())
        result = tools.correlate_discrete_intervals(tbl, header='num', categories=['low', 'mid', 'high'], to_header='num')
        self.assertCountEqual(['high', 'mid', 'low'], result.column('num').combine_chunks().dictionary.to_pylist())
        result = tools.correlate_discrete_intervals(tbl, header='num', granularity=[0.25,0.5,0.75],
                                                    categories=['0%->25%', '25%->50%', '50%->75%', '75%->100%'], to_header='num')
        self.assertCountEqual(['0%->25%', '25%->50%', '50%->75%', '75%->100%'], result.column('num').combine_chunks().dictionary.to_pylist())

    def test_correlate_on_condition(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(1000, seed=101)
        # check no zeros
        self.assertEqual(0, pc.sum(pc.equal(tbl.column('num').combine_chunks(), 0)).as_py())
        # check three zeros
        result = tools.correlate_on_condition(tbl, header='num', other='num',
                                              condition=[(4, 'greater', 'or'), (-2, 'less', None)], value=0, to_header='num')
        self.assertEqual(383, pc.sum(pc.equal(result.column('num').combine_chunks(), pa.scalar(0.0))).as_py())
        # check string
        result = tools.correlate_on_condition(tbl, header='cat', other='cat',
                                              condition=[(pa.array(['INACTIVE', "SUSPENDED"]), 'is_in', None)], value='N/A', to_header='target')
        self.assertEqual(228, pc.count(pc.index_in(result.column('target').combine_chunks(), pa.array(['N/A'])).drop_null()).as_py())
        # check headers
        result = tools.correlate_on_condition(tbl, header='num', other='num',
                                              condition=[(4, 'greater', 'or'), (-2, 'less', None)],
                                              value=0, default=1, to_header='target')
        self.assertEqual(617, pc.sum(result.column('target')).as_py())
        result = tools.correlate_on_condition(tbl, header='num', other='num',
                                              condition=[(4, 'greater', 'or'), (-2, 'less', None)],
                                              value=0, default="@num", to_header='target')
        self.assertEqual(result.column('target').slice(2, 4), result.column('num').slice(2, 4))
        # check null
        tbl = tools.get_synthetic_data_types(1000, inc_nulls=True, seed=101)
        result = tools.correlate_on_condition(tbl, header='num_null', other='num_null',
                                              condition=[(None, 'is_null', None)],
                                              value=0, default="@num_null", to_header='target')
        self.assertGreater(tbl.column('num_null').null_count, 0)
        self.assertEqual(0, result.column('target').null_count)

    def test_correlate_column_join(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(10, seed=101)
        result = tools.correlate_column_join(tbl, header='cat', others='string', sep=': ', to_header='compound')
        self.assertCountEqual(['cat', 'num', 'int', 'bool', 'date', 'compound'], result.column_names)
        self.assertEqual("PENDING: Smokeys Gate", result.column('compound').combine_chunks()[0].as_py())
        result = tools.correlate_column_join(tbl, header='cat', others='string', sep=': ', to_header='cat')
        self.assertCountEqual(['cat', 'num', 'int', 'bool', 'date'], result.column_names)
        self.assertEqual("PENDING: Smokeys Gate", result.column('cat').combine_chunks()[0].as_py())
        tbl = tools.get_synthetic_data_types(1000, inc_nulls=True, seed=101)
        result = tools.correlate_column_join(tbl, header='cat', others=['cat_null', 'string_null'], sep='-', to_header='compound')
        self.assertGreater(result.column('compound').combine_chunks().null_count, 0)

    def test_correlate_column_join_constant(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(10, seed=101)
        result = tools.correlate_column_join(tbl, header='PI', others='int', to_header='compound')
        self.assertTrue(pc.all(pc.match_like(result.column('compound'),"PI__")).as_py())
        self.assertEqual(['cat', 'num', 'bool', 'date', 'string', 'compound'], result.column_names)
        result = tools.correlate_column_join(tbl, header='int', others=['-PI-', 'date'], to_header='int')
        self.assertTrue(pc.all(pc.match_like(result.column('int'),"__-PI-20%")).as_py())
        self.assertEqual(['cat', 'num', 'bool', 'string', 'int'], result.column_names)
        result = tools.correlate_column_join(tbl, header='int', others=['-PI-', 'date'], drop_others=False, to_header='compound')
        self.assertEqual(['cat', 'num', 'int', 'bool', 'date', 'string', 'compound'], result.column_names)

    def test_correlate_date_diff(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        sample_size = 10
        tbl = tools.get_datetime(start=-30, until=-14, ordered=True, ignore_time=True, size=sample_size, to_header='creationDate')
        tbl = tools.correlate_dates(tbl, header="creationDate", ignore_time=True, offset={'days': 10}, to_header='processDate')
        result = tools.correlate_date_diff(tbl, 'creationDate', 'processDate', to_header='diff')
        self.assertEqual(10, pc.divide(pc.sum(result.column('diff')),tbl.num_rows).as_py())

    def test_correlate_dates_jitter(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        sample_size = 10
        tbl = tools.get_datetime(start=-30, until=-14, ordered=True, ignore_time=True, size=sample_size, to_header='creationDate')
        tbl = tools.correlate_dates(tbl, header="creationDate", ignore_time=True, offset={'days': 10}, jitter=1, jitter_units='D', to_header='processDate')
        tprint(tbl)

    def test_correlate_dates_choice(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(10)
        sample_size = 10
        tbl = tools.get_datetime(start=-30, until=-14, ordered=True, ignore_time=True, size=sample_size, to_header='creationDate')
        tbl = tools.correlate_dates(tbl, header="creationDate", ignore_time=True, offset={'days': 10},
                                                 choice=4, jitter=1, jitter_units='D', to_header='processDate')
        tbl = tools.correlate_date_diff(tbl, 'creationDate', 'processDate', to_header='diff', precision=0)
        tprint(tbl)

    def test_correlate_dates(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        arr = pa.array(pd.to_datetime(['2019/01/30', '2019/02/12', '2019/03/07', '2019/03/07']), pa.timestamp('us'))
        tbl = pa.table([arr], names=['dates'])
        # offset
        result = tools.correlate_dates(tbl, 'dates', offset=2, date_format='%Y/%m/%d', to_header='offset')
        self.assertEqual(['2019/02/01', '2019/02/14', '2019/03/09', '2019/03/09'], result.column('offset').to_pylist())
        result = tools.correlate_dates(tbl, 'dates', offset=-2, date_format='%Y/%m/%d', to_header='offset')
        self.assertEqual(['2019/01/28', '2019/02/10', '2019/03/05', '2019/03/05'], result.column('offset').to_pylist())
        result = tools.correlate_dates(tbl, 'dates', offset={'years': 1, 'months': 2}, date_format='%Y/%m/%d', to_header='offset')
        self.assertEqual(['2020/03/30', '2020/04/12', '2020/05/07', '2020/05/07'], result.column('offset').to_pylist())
        result = tools.correlate_dates(tbl, 'dates', offset={'years': -1, 'months': 2}, date_format='%Y/%m/%d', to_header='offset')
        self.assertEqual(['2018/03/30', '2018/04/12', '2018/05/07', '2018/05/07'], result.column('offset').to_pylist())
        # jitter
        result = tools.correlate_dates(tbl, 'dates', jitter=2, jitter_units='D', to_header='jitter', seed=31)
        loss = tools.correlate_date_diff(result, first_date='dates', second_date='jitter', to_header='diff')
        self.assertEqual([-1, 1, 1, -2], loss.column('diff').to_pylist())

    def test_correlate_date_min_max(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        arr = pa.array(pd.to_datetime(['2017/12/14', '2017/12/20', '2018/01/18', '2017/12/27']), pa.timestamp('us'))
        tbl = pa.table([arr], names=['dates'])
        # control
        result = tools.correlate_dates(tbl, 'dates', jitter=5, jitter_units='D', date_format='%Y/%m/%d', to_header='maxmin', seed=31)
        self.assertEqual("2017/12/12", pc.min(result.column('maxmin')).as_py())
        self.assertEqual("2018/01/21", pc.max(result.column('maxmin')).as_py())
        # min
        result = tools.correlate_dates(tbl, 'dates', jitter=5, jitter_units='D', min_date="2017/12/24", date_format='%Y/%m/%d', to_header='maxmin', seed=31)
        self.assertEqual("2017/12/24", pc.min(result.column('maxmin')).as_py())
        self.assertEqual("2018/01/21", pc.max(result.column('maxmin')).as_py())
        # max
        result = tools.correlate_dates(tbl, 'dates', jitter=5, jitter_units='D', max_date="2018/01/01", date_format='%Y/%m/%d', to_header='maxmin', seed=31)
        self.assertEqual("2017/12/12", pc.min(result.column('maxmin')).as_py())
        self.assertEqual("2018/01/01", pc.max(result.column('maxmin')).as_py())

    def test_correlate_date_as_delta(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        arr = pa.array(pd.to_datetime(['2018/01/30', '2019/02/12', '2019/03/07', '2020/03/07']), pa.timestamp('us'))
        tbl = pa.table([arr], names=['dates'])
        # control
        result = tools.correlate_dates(tbl, 'dates', now_delta='Y', date_format='%Y/%m/%d', to_header='delta', seed=31)
        self.assertEqual([5,4,4,3], result.column('delta').to_pylist())


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))

def tprint(t: pa.table, headers: [str, list]=None, d_type: [str, list]=None, regex: [str, list]=None):
    _ = Commons.filter_columns(t.slice(0,10), headers=headers, d_types=d_type, regex=regex)
    print(Commons.table_report(_).to_string())

if __name__ == '__main__':
    unittest.main()
