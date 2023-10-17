from django import test

from ..factories import SubdistrictFactory


class SubdistrictModelGetProvinceTest(test.TestCase):
    def setUp(self):
        self.subdistrict = SubdistrictFactory()

    def test_simple(self):
        self.assertEqual(self.subdistrict.get_province(), self.subdistrict.district.province)
