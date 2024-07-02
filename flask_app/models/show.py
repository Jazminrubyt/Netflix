from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from pprint import pprint
from flask import flash


class Show:
    _db = "netflix_db"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.date_released = data["date_released"]
        self.comments = data["comments"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the show form"""

        is_valid = True

        if len(form_data["title"].strip()) == 0:
            flash("No title entered, please enter title!")
            is_valid = False
        elif len(form_data["title"].strip()) < 2:
            flash("Title must be at least 2 characters!")
            is_valid = False
        if len(form_data["network"].strip()) == 0:
            flash("No network entered, please enter network!")
            is_valid = False
        elif len(form_data["network"].strip()) < 2:
            flash("Network must be at least 2 characters!")
            is_valid = False
        if len(form_data["comments"].strip()) == 0:
            flash("No comments entered, please enter comments!")
            is_valid = False
        elif len(form_data["comments"].strip()) < 2:
            flash("Comments must be at least 2 characters!")
            is_valid = False

        if len(form_data["date_released"].strip()) == 0:
            flash("No date entered, please enter date!")
            is_valid = False
        return is_valid

    @classmethod
    def retrieve_info(cls):
        """retrieve all shows info from database"""
        query = """
        SELECT * FROM shows 
        LEFT JOIN users ON shows.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Show._db).query_db(query)
        print("************")
        pprint(list_of_dicts)
        print("************")

        shows = []
        for show_info in list_of_dicts:
            show = Show(show_info)
            user_data = {
                "id": show_info["users.id"],
                "first_name": show_info["first_name"],
                "last_name": show_info["last_name"],
                "email": show_info["email"],
                "password": show_info["password"],
                "created_at": show_info["users.created_at"],
                "updated_at": show_info["users.updated_at"],
            }
            user = User(user_data)
            show.user = user
            shows.append(show)
        return shows

    @classmethod
    def retrieve_by_id_with_user(cls, show_id):
        """Finds one show by id and related user"""

        query = """
        SELECT * FROM shows 
        LEFT JOIN users ON shows.user_id = users.id
        WHERE shows.id = (%(show_id)s);
        """
        data = {"show_id": show_id}
        list_of_dicts = connectToMySQL(Show._db).query_db(query, data)
        pprint(list_of_dicts)
        show = Show(list_of_dicts[0])
        print(show.title)
        for each_dict in list_of_dicts:
            if each_dict["users.id"] != None:

                user_data = {
                    "id": each_dict["users.id"],
                    "first_name": each_dict["first_name"],
                    "last_name": each_dict["last_name"],
                    "email": each_dict["email"],
                    "password": each_dict["password"],
                    "created_at": each_dict["users.created_at"],
                    "updated_at": each_dict["users.updated_at"],
                }
                user = User(user_data)
                show.user = user
        return show

    @classmethod
    def create(cls, form_data):
        """insert a new show into the database"""
        query = """
        INSERT INTO shows
        (title, network, date_released, comments, user_id)
        Values
        (%(title)s,
        %(network)s,
        %(date_released)s,
        %(comments)s,
        %(user_id)s)
        """

        show_id = connectToMySQL(Show._db).query_db(query, form_data)
        return show_id

    @classmethod
    def retrieve_info_id_with_user(cls, show_id):
        """retrieve one show info from database"""
        query = """
        SELECT * FROM shows 
        Join users 
        ON shows.user_id = users.id
        WHERE shows.id = %(show_id)s;"""
        data = {"show_id": show_id}
        list_of_dicts = connectToMySQL(Show._db).query_db(query, data)
        pprint(list_of_dicts)
        show = Show(list_of_dicts[0])
        one_dict = list_of_dicts[0]
        user_data = {
            "id": one_dict["users.id"],
            "first_name": one_dict["first_name"],
            "last_name": one_dict["last_name"],
            "email": one_dict["email"],
            "password": one_dict["password"],
            "created_at": one_dict["users.created_at"],
            "updated_at": one_dict["users.updated_at"],
        }
        user = User(user_data)
        show.user = user
        return show

    @classmethod
    def update(cls, form_data):
        """Update a show by id"""

        query = """
        UPDATE shows
        SET
        title = (%(title)s),
        network = (%(network)s),
        date_released = (%(date_released)s),
        comments = (%(comments)s)
        WHERE id = %(show_id)s;
        """
        connectToMySQL(Show._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, show_id):
        """Deletes a user by id"""

        query = "DELETE FROM shows WHERE id = %(show_id)s;"
        data = {"show_id": show_id}
        connectToMySQL(Show._db).query_db(query, data)
        return
