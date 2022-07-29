# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user

"""
Change class construct, queries, and db for magazine
"""

class Magazine:
    # Use a alias for the database; call in classmethods as cls.db
    # For staticmethod need to call the database name not alias
    db = "magazine_subscriptions"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Needed to create this to capture the creator of the magazine
        self.creator = None
        self.user_ids_who_subscribed = []
        self.users_who_subscribed = []

    # CRUD CREATE METHODS
    @classmethod
    def create_magazine(cls,data):
        """Create a magazine"""
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def subscribe(cls,data):
        query = "INSERT INTO subscriptions (user_id, magazine_id) VALUES (%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD READ METHODS -- Modified for many to many
    @classmethod
    def get_all_magazines(cls):
        """Get all the magazines in db"""
        query = '''SELECT * FROM magazines
                JOIN users AS creators ON magazines.user_id = creators.id
                LEFT JOIN subscriptions ON subscriptions.magazine_id = magazines.id
                LEFT JOIN users AS users_who_subscribed ON subscriptions.user_id = users_who_subscribed.id;'''
        # query = "SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_magazines = []
        for r in results:
            new_magazine = True
            users_who_subscribed_data = {
                'id': r['users_who_subscribed.id'],
                'first_name': r['users_who_subscribed.first_name'],
                'last_name': r['users_who_subscribed.last_name'],
                'email': r['users_who_subscribed.email'],
                'password': r['users_who_subscribed.password'],
                'created_at': r['users_who_subscribed.created_at'],
                'updated_at': r['users_who_subscribed.updated_at']
            }
            # Check to see if previous processed magazine, exist as current row
            num_of_magazine = len(all_magazines)
            print(num_of_magazine)
            # Check to see if we have magazines in list
            # If num_of_magazine is > 0; then we have procesed a row/magazine
            # already
            if num_of_magazine > 0:
                # Check if last magazine equals current row
                last_magazine = all_magazines[num_of_magazine-1]
                if last_magazine.id == r['id']:
                    last_magazine.user_ids_who_subscribed.append(r['users_who_subscribed.id'])
                    last_magazine.users_who_subscribed.append(user.User(users_who_subscribed_data))
                    new_magazine = False
            # Create new magazine object if magazine has not been created
            # and added to the list
            if new_magazine:
                # Create the magazine object
                magazine = cls(r)
                # Create the associated User object; include all contructors
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in magazine
                magazine.creator = one_user
                # Check to see if any user subscribed this magazine
                if r['users_who_subscribed.id']:
                    magazine.user_ids_who_subscribed.append(r['users_who_subscribed.id'])
                    magazine.users_who_subscribed.append(user.User(users_who_subscribed_data))
                    print(magazine.users_who_subscribed)
                # Append the magazine to the all_magazine list
                all_magazines.append(magazine)

        return all_magazines

    @classmethod
    def get_one_magazine(cls,data):
        """Get one magazine to display"""
        query = '''SELECT * FROM magazines
                JOIN users AS creators ON magazines.user_id = creators.id
                LEFT JOIN subscriptions ON subscriptions.magazine_id = magazines.id
                LEFT JOIN users AS users_who_subscribed ON subscriptions.user_id = users_who_subscribed.id WHERE magazines.id = %(id)s;'''
        # query = "SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        # Now due to fav; we can get back multiple rows or no rows (if no fav)
        # So we need to check for both conditions
        # First condition no results; return False
        if len(result) < 1:
            return False
        # Check if multiple rows (or fav)
        # If one row then magazine so set to True to start
        new_magazine = True
        for r in result:
            if new_magazine:
                # If this is the first row
                magazine = cls(result[0])
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in magazine
                magazine.creator = one_user
                # Set new_magazine to False once we create 
                new_magazine = False
            # if fav data associate it with user
            if r['users_who_subscribed.id']:
                users_who_subscribed_data = {
                    'id': r['users_who_subscribed.id'],
                    'first_name': r['users_who_subscribed.first_name'],
                    'last_name': r['users_who_subscribed.last_name'],
                    'email': r['users_who_subscribed.email'],
                    'password': r['users_who_subscribed.password'],
                    'created_at': r['users_who_subscribed.created_at'],
                    'updated_at': r['users_who_subscribed.updated_at']
                }
                # Create instance of user who fav
                users_who_subscribed = user.User(users_who_subscribed_data)
                # Add user to users_who_subscribed list
                magazine.users_who_subscribed.append(users_who_subscribed)
                # Add users_who_subscribed id to user_ids_who_subscribed list
                magazine.user_ids_who_subscribed.append(r['users_who_subscribed.id'])
        return magazine

    # CRUD UPDATE METHODS
    @classmethod
    def update_magazine(cls,data):
        """Update the magazine"""
        query = "UPDATE magazines SET title=%(title)s, description=%(description)s, WHERE magazines.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD DELETE METHODS
    @classmethod
    def delete_magazine(cls,data):
        """Delete magazine"""
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unsubscribe(cls,data):
        query = "DELETE FROM subscriptions WHERE user_id=%(user_id)s AND magazine_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # FORM VALIDATION
    @staticmethod
    def validate_form(magazine):
        """Validate the new magazine create form"""
        is_valid = True # We set True until False
        if len(magazine['title']) < 2:
            flash("The Title must be at least 2 characters.", "danger")
            is_valid = False
        if len(magazine['description']) < 10:
            flash("The description must be at least 10 characters.", "danger")
            is_valid = False
        return is_valid


