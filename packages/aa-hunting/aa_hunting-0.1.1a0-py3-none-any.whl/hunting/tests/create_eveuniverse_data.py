from eveuniverse.tools.testdata import ModelSpec, create_testdata

from django.test import TestCase

from . import test_data_filename


class CreateEveUniverseTestData(TestCase):
    def test_create_testdata(self):
        testdata_spec = [
            ModelSpec("EveStation", ids=[60003760]),
        ]
        create_testdata(testdata_spec, test_data_filename())
