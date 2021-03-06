import unittest
from inspect import signature
from project import Gedcom
from validate import valid_month, valid_lifetime, validate_genders
from validate import validate_males, validate_marriages, validate_ids
from validate import validate_marriage_dates, validate_marriage_divorce
from validate import validate_name_birth
from helpers import date_compare, is_deceased, calculate_years, get_name
from helpers import get_last_name, get_birth, get_recent_deaths
from helpers import get_death, get_living_married, find_living_people_ids
from helpers import get_currently_married, list_living_single, get_name_id
from helpers import get_name_id_list, get_recent_births, valid_divorce
from helpers import siblings, get_mom, get_dad, create_family_dict
from helpers import find_duplicate_children, process_partial_dates
from helpers import get_age, sort_siblings

TEST_FILE_NAME = 'data/testing.ged'
gedcom = Gedcom(TEST_FILE_NAME)
individuals = gedcom.individual
families = gedcom.family


class TestProject(unittest.TestCase):

    def test_create_family_dict(self):
        """ Test create_family_dict(fam, ind). """
        sig = signature(create_family_dict)
        params = len(sig.parameters)
        self.assertEqual(params, 2)
        self.assertEqual(create_family_dict(families, individuals),
                         "Anomaly US25: Duplicate child name and birthday: [('Jane', '9 FEB 2010')]")

    def test_find_duplicate_children(self):
        """ Test find_duplicate_children(children_list). """
        sig = signature(find_duplicate_children)
        params = len(sig.parameters)
        self.assertEqual(params, 1)

    def test_process_partial_dates(self):
        """ Test process_partial_dates(date). """
        sig = signature(process_partial_dates)
        params = len(sig.parameters)
        self.assertEqual(params, 1)
        self.assertEqual(process_partial_dates('JUL 1988'), '1 JUL 1988')
        self.assertEqual(process_partial_dates('1988'), '1 JAN 1988')

    def test_date_compare(self):
        """ Testing the date_compare function  """
        self.assertEqual(date_compare('10 SEP 2017', ''), True)
        self.assertTrue(date_compare('10 SEP 2017', ''))
        self.assertEqual(date_compare('10 SEP 2018', '10 SEP 2017'), False)
        self.assertEqual(date_compare('20 SEP 2017', '10 SEP 2018'), True)

    def test_is_deceased(self):
        """ Testing the is_deceased function  """
        self.assertEqual(is_deceased(''), False)
        self.assertEqual(is_deceased('11 SEP 1998'), True)
        self.assertEqual(is_deceased('18 MAR 2007'), True)
        self.assertFalse(is_deceased(''), True)
        self.assertTrue(is_deceased('18 MAR 2007'), True)

    def test_life_duration(self):
        """ Testing if life duration is less than 150 years"""
        self.assertTrue(valid_lifetime('01 JAN 1980', '01 JAN 2020'))
        self.assertTrue(valid_lifetime('01 JAN 1985', '01 JAN 2020'))
        self.assertFalse(valid_lifetime('01 JAN 1000', '01 JAN 1150'))
        self.assertFalse(valid_lifetime('01 JAN 1500', '01 JAN 2520'))
        self.assertFalse(valid_lifetime('01 JAN 1000', '01 JAN 2220'))

    def test_get_age(self):
        """ Testing the get_age function  """
        self.assertEqual(get_age(individuals, '@I1@'), 117)
        self.assertEqual(get_age(individuals, '@I3@'), 78)
        self.assertEqual(get_age(individuals, '@I4@'), 80)

    def test_valid_month(self):
        """ Testing is month is valid """
        self.assertTrue(valid_month('01 JAN 1980'))
        self.assertTrue(valid_month('01 FEB 1980'))
        self.assertTrue(valid_month('01 MAR 1980'))
        self.assertFalse(valid_month('01 JAM 1980'))
        self.assertFalse(valid_month('01 ABC 1980'))

    def test_validate_genders(self):
        """ validate_genders(families, individuals):
            if husband and wife genders accurate, return True
        """
        self.assertFalse(validate_genders(families, individuals))

    def test_validate_males(self):
        """ Testing male last name validation """
        self.assertFalse(validate_males(families, individuals))

    def test_validate_marriages(self):
        """ If duplicate spouses found, returns false """
        self.assertTrue(validate_marriages(families, individuals))

    def test_calculate_years(self):
        """ Testing the calculate_years function  """
        self.assertEqual(calculate_years('09 FEB 1962', '11 SEP 2017'), 55)
        self.assertEqual(calculate_years('10 SEP 1969', '11 SEP 1999'), 30)
        self.assertEqual(calculate_years('23 OCT 1989', '11 SEP 2017'), 27)

    def test_valid_lifetime(self):
        """ Testing the valid_lifetime function  """
        self.assertEqual(valid_lifetime('11 SEP 1998', '11 SEP 1999'), True)
        self.assertEqual(valid_lifetime('11 SEP 1898', '11 SEP 1999'), True)
        self.assertEqual(valid_lifetime('11 SEP 1798', '11 SEP 1999'), False)

    def test_get_name(self):
        """ Testing the get_name function  """
        self.assertEqual(get_name(individuals, '@I1@'), 'Bob /Jones/')
        self.assertEqual(get_name(individuals, '@I2@'), 'Mary /Smith/')

    def test_get_last_name(self):
        """ Testing the get_last_name function  """
        self.assertEqual(get_last_name(individuals, '@I1@'), 'Jones')
        self.assertEqual(get_last_name(individuals, '@I2@'), 'Smith')

    def test_get_birth(self):
        """ Testing the get_age function  """
        self.assertEqual(get_birth(individuals, '@I1@'), '1 JAN 1900')
        self.assertEqual(get_birth(individuals, '@I3@'), '18 FEB 1939')

    def test_get_recent_deaths(self):
        """ Testing the get_recent_deaths function  """
        mock_data = [{'BIRT': '9 FEB 1962', 'SEX': 'F', 'ID': 'p1',
                      'DEAT': '20 OCT 2017', 'NAME': 'Bob /Jones/'}]
        self.assertEqual(get_recent_deaths(mock_data), ['Bob /Jones/'])

    def test_get_recent_births(self):
        """ Testing the get_recent_births function  """
        mock_data = [{'BIRT': '20 OCT 2017', 'SEX': 'F', 'ID': 'p1',
                      'DEAT': '9 FEB 1962', 'NAME': 'Andrew /Stewart/'}]
        self.assertEqual(get_recent_births(mock_data), ['Andrew /Stewart/'])

    def test_get_death(self):
        """ Testing the get_age function  """
        self.assertEqual(get_death(individuals, '@I1@'), '1 JAN 2051')
        self.assertEqual(get_death(individuals, '@I3@'), '')

    def test_get_living_married(self):
        """ Test the living married function to return a list """
        families = list()
        individuals = list()
        self.assertEqual(get_living_married(families, individuals), [])

    def test_find_living_people_ids(self):
        """ Test the living_single(individuals) function """
        individuals = list()
        self.assertEqual(find_living_people_ids(individuals), [])

    def test_get_currently_married(self):
        """ Test the get_currently_married(families) function """
        families = list()
        self.assertEqual(get_currently_married(families), [])

    def test_unique_id(self):
        """ Test the validate_ids function"""
        self.assertFalse(validate_ids(families, individuals))

    def list_living_single(self):
        """ Test the list_living_single(families, individuals) function """
        individuals = list()
        families = list()
        self.assertEqual(list_living_single(families, individuals), [])
        self.assertEqual(list_living_single(families, individuals), [])

    def test_get_name_id(self):
        """ Testing the get_name_id function """
        self.assertEqual(get_name_id(individuals[0]), 'Bob /Jones/ (@I1@)')
        self.assertEqual(get_name_id(individuals[1]), 'Mary /Smith/ (@I2@)')
        self.assertEqual(get_name_id(individuals[2]),
                         'Thelma Lucella /Philbrook/ (@I3@)')

    def test_get_name_id_list(self):
        """ Testing the get_name_id function """
        self.assertEqual(get_name_id_list(individuals, '@I1@'),
                         'Bob /Jones/ (@I1@)')
        self.assertEqual(get_name_id_list(individuals, '@I2@'),
                         'Mary /Smith/ (@I2@)')
        self.assertEqual(get_name_id_list(individuals, '@I3@'),
                         'Thelma Lucella /Philbrook/ (@I3@)')

    def test_validate_marriage_dates(self):
        self.assertEqual(validate_marriage_dates(families[0], individuals),
                         'no marriage')
        self.assertEqual(validate_marriage_dates(families[1], individuals),
                         'no error')
        self.assertEqual(validate_marriage_dates(families[4], individuals),
                         'after wife')
        self.assertEqual(validate_marriage_dates(families[3], individuals),
                         'after husband')

    def test_validate_marriage_divorce(self):
        self.assertEqual(validate_marriage_divorce(families[0]), 'no marriage')
        self.assertEqual(validate_marriage_divorce(families[1]), 'no error')
        self.assertEqual(validate_marriage_divorce(families[2]),
                         'after divorce')

    def test_birth_name(self):
        bad_data = [{'BIRT': '05 OCT 2017', 'SEX': 'F', 'ID': 'p1',
                     'DEAT': '9 FEB 1962', 'NAME': 'Constance Joan /Lewis/'},
                    {'BIRT': '05 OCT 2017', 'SEX': 'F', 'ID': 'p1',
                     'DEAT': '9 FEB 1962', 'NAME': 'Constance Joan /Lewis/'}]
        good_data = [{'BIRT': '05 OCT 2017', 'SEX': 'F', 'ID': 'p1',
                      'DEAT': '9 FEB 1962', 'NAME': 'Constance Joan /Lewis/'},
                     {'BIRT': '05 OCT 2017', 'SEX': 'F', 'ID': 'p1',
                      'DEAT': '9 FEB 1962', 'NAME': 'Constance Jean /Lewis/'}]
        self.assertTrue(validate_name_birth(good_data))
        self.assertFalse(validate_name_birth(bad_data))

    def test_valid_divorce(self):
        self.assertTrue(valid_divorce(families[0], individuals))
        self.assertTrue(valid_divorce(families[2], individuals))
        self.assertFalse(valid_divorce(families[5], individuals))

    def test_get_mom(self):
        self.assertEqual(get_mom('@I5@', families), '@I3@')
        self.assertNotEqual(get_mom('@I5@', families), '@I4@')
        self.assertEqual(get_mom('@I3@', families), 'unknown')

    def test_get_dad(self):
        self.assertEqual(get_dad('@I5@', families), '@I4@')
        self.assertNotEqual(get_dad('@I5@', families), '@I3@')
        self.assertEqual(get_dad('@I3@', families), 'unknown')

    def test_siblings(self):
        self.assertFalse(siblings('@I1@', '@I5@', families))
        self.assertTrue(siblings('@I5@', '@I7@', families))
        self.assertFalse(siblings('@I1@', '@I2@', families))
        self.assertFalse(siblings('@I3@', '@I2@', families))

    def test_sibling_order(self):
        """ Ensure siblings are ordered by age """
        self.assertEqual(families[1]['CHIL'], ['@I5@', '@I7@'])
        sort_siblings(families[1]['CHIL'], individuals)
        self.assertEqual(families[1]['CHIL'], ['@I7@', '@I5@'])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
