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
from ds_capability.components.commons import Commons
from ds_core.properties.property_manager import PropertyManager
from ds_capability import Controller, FeatureBuild
from ds_capability.intent.controller_intent import ControllerIntentModel

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

    def test_controller_runbook(self):
        # tbl = FeatureBuild.from_memory().tools.get_synthetic_data_types(size=10)
        controller: Controller = Controller.from_env('control', has_contract=False)
        register: ControllerIntentModel = controller.register
        fb1 = set_service_one()
        fb2 = set_service_two(fb1)
        # build controller
        fb_tbl = register.feature_build('task1', intent_level='fb1')
        fb_tbl = register.feature_build('task2', intent_level='fb2')
        controller.add_run_book_level(book_name='test_item', run_level='fb1', source='event1', persist='event1')
        controller.add_run_book_level(book_name='test_item', run_level='fb2', source='event1', persist='event2')
        controller.add_run_book_level(book_name='test_item', run_level='fb2', source='event1', persist=['event2', 'event3'])
        controller.add_run_book(run_levels=['fb1', 'fb2'], book_name='test_book')
        # pprint(pm_view('controller', 'control', 'run_book'))
        # pprint(pm_view('controller', 'control', 'intent'))
        controller.run_controller(run_book=['test_item', 'test_book'], run_cycle_report='tmp_report.parquet')
        result = controller.load_canonical('run_cycle_report')
        print(Commons.table_report(result).to_string())


    def test_controller(self):
        # tbl = FeatureBuild.from_memory().tools.get_synthetic_data_types(size=10)
        controller: Controller = Controller.from_env('control', has_contract=False)
        register: ControllerIntentModel = controller.register
        fb1 = set_service_one()
        fb2 = set_service_two(fb1)
        # build controller
        register.feature_build('task1')
        register.feature_build('task2', intent_level='pre-process')
        # pprint(pm_view('controller', 'control', 'intent'))
        controller.run_controller(run_cycle_report='tmp_report.parquet')
        result = controller.load_canonical('run_cycle_report')
        print(Commons.table_report(result).to_string())


    def test_raise(self):
        startTime = datetime.now()
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))
        print(f"Duration - {str(datetime.now() - startTime)}")


def set_service_one():
    fb = FeatureBuild.from_env('task1', has_contract=False)
    fb.set_persist_uri("event://task1_outcome")
    tbl = fb.tools.get_synthetic_data_types(size=10)
    _ = fb.tools.get_noise(size=10, num_columns=2, canonical=tbl)
    # pprint(pm_view('feature_build', 'task1'))
    fb.run_component_pipeline()
    return fb

def set_service_two(other: FeatureBuild):
    fb = FeatureBuild.from_env('task2', has_contract=False)
    fb.set_source_uri(other.get_persist_uri())
    fb.set_persist_uri("event://task2_outcome")
    source_tbl = fb.load_source_canonical()
    tbl = fb.tools.correlate_number(canonical=source_tbl, header='num', jitter=2, to_header='jitter')
    _ = fb.tools.correlate_column_join(tbl, header='PI', others='int', to_header='id')
    # pprint(pm_view('feature_build', 'task2'))
    fb.run_component_pipeline()
    return fb


def pm_view(capability: str, task: str, section: str=None):
    uri = os.path.join(os.environ['HADRON_PM_PATH'], f"hadron_pm_{capability}_{task}.parquet")
    tbl = pq.read_table(uri)
    tbl = tbl.column(0).combine_chunks()
    result = ast.literal_eval(tbl.to_pylist()[0]).get(capability, {}).get(task, {})
    return result.get(section, {}) if isinstance(section, str) and section in result.keys() else result


if __name__ == '__main__':
    unittest.main()
