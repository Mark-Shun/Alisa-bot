from tinydb import TinyDB, Query

class DataBase:
    def __init__(self):
        self.roles_db = TinyDB("data/roles.json")
        self.query = Query()
    
    def try_out(self):
        self.roles_db.truncate()
        self.insert_role('Character roles', 'Alisa Main')
        self.insert_role('Character roles', 'Alisa Sub')
        self.insert_role('Region roles', 'NA-EAST')
        self.insert_role('Region roles', 'NA-WEST')
        self.insert_role('Region roles', 'EU-EAST')
        self.remove_role('NA-EAST')
        print(self.roles_db.all())
    def insert_role(self, category, role):
        self.roles_db.insert({'category' : f'{category}', 'role' : f'{role}'})
    def remove_role(self, role):
        self.roles_db.remove(self.query.role == role)
    def get_roles(self):
        return self.roles_db.all()

test_db = DataBase()

test_db.try_out()
