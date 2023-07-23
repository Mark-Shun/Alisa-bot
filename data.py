from tinydb import TinyDB, Query
import warnings
from exceptions import InvalidInsertRole, InvalidRemoveRole, DuplicateRole

standard_roles = [
    {"category": "Character roles", "role": "Alisa Main"},
    {"category": "Character roles", "role": "Alisa Sub"},
    {"category": "Region roles", "role": "NA-EAST"},
    {"category": "Region roles", "role": "NA-WEST"},
    {"category": "Region roles", "role": "EU-EAST"},
    {"category": "Region roles", "role": "EU-WEST"},
    {"category": "Region roles", "role": "OCE"},
    {"category": "Region roles", "role": "MEA"},
    {"category": "Region roles", "role": "EAST-ASIA"},
    {"category": "Region roles", "role": "SOUTH-ASIA"},
    {"category": "Region roles", "role": "SEA"},
    {"category": "Platform roles", "role": "PC"},
    {"category": "Platform roles", "role": "PS4"},
    {"category": "Platform roles", "role": "XBOX"},
    {"category": "Misc roles", "role": "Guest"},
    {"category": "Misc roles", "role": "Streamer"}
]

class RolesDataBase:
    roles_dict = {}
    def __init__(self):
        self.roles_db = TinyDB("data/roles.json")
        self.query = Query()
        if len(self.roles_db) == 0:
            warnings.warn("data/roles.json file seems to be empty, filling it up pre-configured standard roles.")
            self.roles_db.insert_multiple(standard_roles)
        self.db_to_dict()

    def db_to_dict(self):
        self.roles_dict.clear()
        db = self.get_database()
        for entry in db:
            self.roles_dict[entry['category']] = []
        for entry in db:
            self.roles_dict[entry['category']].append(entry['role'])
    def try_out(self):
        # self.roles_db.truncate()
        # self.roles_db.insert_multiple(standard_roles)
        #self.insert_role("Character roles", "Alisa Main")
        # print(self.roles_dict)
        return
    def is_duplicate(self, role):
        return self.roles_db.contains(self.query['role']==role)
    def add_role(self, category, role):
        if(role == 'Admin' or role == 'Mod'):
            raise InvalidInsertRole(f"I'm not allowed to assign {role} to regular members.")
        elif(not(self.is_duplicate(role))):
            self.roles_db.insert({'category' : f'{category}', 'role' : f'{role}'})
        else:
            raise DuplicateRole(f"The role {role} already exists in the list.")
    def remove_role(self, role):
        if(not(self.is_duplicate(role))):
            raise InvalidRemoveRole(f"The role {role} is not present in the database.")
        self.roles_db.remove(self.query.role == role)
    def get_database(self):
        return self.roles_db.all()
    def get_dictionary(self):
        return self.roles_dict
    #TODO Perhaps change to outputting with dictionary results
    def search_category(self, category_val):
        result = self.roles_db.search(self.query.category == category_val)
        return result

test_db = RolesDataBase()

test_db.try_out()
# test_result = test_db.get_roles()
# print(test_result)
print(test_db.search_category('Character roles'))