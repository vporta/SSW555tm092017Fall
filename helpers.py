from math import floor
from datetime import datetime
import validate

def is_deceased(row_death):
    """ Check if an individual is dea and return a Boolean val. """
    try:
        row_death = str(row_death)
        if not row_death:
            return False
        else:
            return True
    except ValueError:
        print('Invalid type.')


def list_deceased(indi_list):
    """ This function loops through the individual list and prints
        names of deceased people. """
    for row in indi_list:
        if is_deceased(row["DEAT"]):
            print('US29: Deceased: {0}, {1}'.format(row["NAME"], row['DEAT']))


def find_living_people_ids(individuals):
    """ Find all living people, then return a list of their ID and Name. """
    living_people_ids = []
    for person in individuals:
        if is_deceased(person["DEAT"]):
            continue
        else: 
            living_people_ids.append([person["ID"],person["NAME"]])

    return living_people_ids


def get_currently_married(families):
    """ Takes a list of families as a parameter and checks if they are 
        currently married by looking for an empty MARR, DIV row. Returns
        a list of couple IDs. """
    couple_ids = []
    for family in families:
        if family["MARR"] != '' and family["DIV"] == '':
            couple_ids.extend([family["HUSB"], family["WIFE"]])

    return couple_ids


def get_living_married(families, individuals):
    """ Return a list of living married people. """
    couple_ids = get_currently_married(families)
    living_people_ids = find_living_people_ids(individuals)
    living_married_people = []
    
    for living_person in living_people_ids:
        if living_person[0] in couple_ids:
            print("US30: Living married person: {}".format(living_person[1]))
            living_married_people.append([living_person[0],living_person[1]])
    
    return living_married_people


def list_living_single(individuals, families):
    """ List people over 30 years old who have never been married. 
        Compare the ID of married people to living people over 30. 
        If the person's ID is NOT IN the married people list, return the ID. """

    wife = None
    husb = None
    living_people_ids = [] # all living people
    family_ids = [] # all married or formerly married people
    living_single_people_over_30 = []

    for person in find_living_people_ids(individuals):
        living_people_ids.append(person[0])

    for family in families:
        wife = family["WIFE"]
        husb = family["HUSB"]
        family_ids.extend([wife, husb])

    for ID in living_people_ids:
        age = int(validate.get_age(individuals, ID))
        if age > 30 and ID not in family_ids:
            living_single_people_over_30.append(ID)

    for person in find_living_people_ids(individuals):
        if person[0] in living_single_people_over_30:
            print("US31: List of living single people over 30: {}".format(person[1]))

            
def date_compare(date1, date2):
    """ This routine compares 2 dates in the Exact format 
        and returns true if the early date is before thelater date
        otherwise, returns false
        by default, the later date is set to today.
    """
    early_date = datetime.strptime(date1, '%d %b %Y').date()
    if date2 == '':
        late_date = datetime.now().date()
    else:
        late_date = datetime.strptime(date2, '%d %b %Y').date()

    if early_date < late_date:
        return True
    else:
        return False


def get_name(list, id):
    """ Get the name for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["NAME"]
    return "Unknown"


def get_last_name(list, id):
    name = get_name(list, id)
    names = name.split('/')

    if len(names) > 1:
        return names[-2]
    else:
        return "Unknown"


def get_birth(list, id):
    """ Get the birth date for an individual.  """
    for row in list:
        if row["ID"] == id:
            return row["BIRT"]
    return "Unknown"


def calculate_years(date1, date2):
    # this returns the number of years between 2 exact format dates
    first_date = datetime.strptime(date1, '%d %b %Y').date()
    second_date = datetime.strptime(date2, '%d %b %Y').date()

    years = (first_date - second_date).days / 365
    return floor(abs(years))