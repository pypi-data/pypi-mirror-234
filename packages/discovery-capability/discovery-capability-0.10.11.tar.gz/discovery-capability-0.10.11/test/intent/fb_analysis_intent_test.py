import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
from ds_capability import FeatureBuild
from ds_capability.components.commons import Commons
from ds_capability.intent.feature_build_intent import FeatureBuildIntent
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
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(100, inc_nulls=True)
        fb.add_connector_uri('sample', './working/source/data_type.parquet')
        fb.save_canonical('sample', tbl)
        self.assertEqual((100, 17), tbl.shape)
        result = tools.get_analysis(1000, 'sample')
        self.assertEqual((1000, 17), result.shape)

    def test_direct_other(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        tbl = tools.get_synthetic_data_types(10, inc_nulls=True)
        result = tools.get_analysis(100, tbl)
        self.assertEqual((100, 17), result.shape)

    def test_flattened_sample(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        fb.add_connector_uri('sample', './working/source/complex_flatten_records.parquet')
        tbl = fb.load_canonical('sample')
        self.assertEqual((4, 20), tbl.shape)
        result = tools.get_analysis(6, 'sample')
        self.assertEqual((6, 20), result.shape)

    def test_complex_nested(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntent = fb.tools
        document = [
            {"_id": "I35138",
             "contactMedium": [
                {"medium": {"number": "50070028", "type": "mobile"}, "preferred": True},
                {"medium": {"emailAddress": "mail@stc.com.kw", "type": "emailAddress"}, "preferred": True}],
             "gender": "M", "familyName": "Fouad", "givenName": "Fouad", "middleName": "Fouad"},
            {"_id": "I35145",
             "contactMedium": [
                {"medium": {"emailAddress": "panneer.rajadurai.c@solutions.com.kw", "type": "EmailAddress"}, "preferred": True},
                {"medium": {"number": "51658317", "type": "mobile"}, "preferred": True},
                {"medium": {"number": "51658317", "type": "whatsapp"}, "preferred": False},
                {"medium": {"number": "51658317", "type": "telegram"}, "preferred": False},
                {"medium": {"type": "telephone"}, "role": "AlternateNumber"}],
             "gender": "M", "familyName": "Jay", "givenName": "Bhuvana", "middleName": ""},
            {"_id": "I35146",
             "contactMedium": [
                {"medium": {"emailAddress": "bhuvana.stc21@gmail.com", "type": "EmailAddress"}, "preferred": True},
                {"medium": {"type": "mobile"}, "preferred": False},
                {"medium": {"type": "whatsapp"}, "preferred": False},
                {"medium": {"type": "telegram"}, "preferred": False}],
             "gender": "F", "familyName": "CORP", "givenName": "TECNOTREE", "middleName": "LTD"},
            {"_id": "I35181",
             "contactMedium": [],
             "gender": "M", "familyName": "test", "givenName": "test", "nationality": "", "middleName": ""}
        ]
        tbl = pa.Table.from_pylist(document)
        tbl = Commons.table_flatten(tbl)
        result = tools.get_analysis(10, tbl)


    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
