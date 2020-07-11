from . import db
from .user import User
from .user_dao import UserDAO

class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    def get_users(self):
         result = []
         cursor = db.execute("select username,password,full_name from users")
         for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
         return result

    def delete_user(self, username):
        db.execute("delete from users where username=%s", (username,))

    def edit_user(self, username, password, full_name):
        if len(password) != 0 and len(full_name) != 0:
            res = db.execute("update users set password=%s, full_name=%s where username=%s", (password,full_name,username,))
        elif len(password) == 0:
            res = db.execute("update users set full_name=%s where username=%s", (full_name,username,))
        elif len(full_name) == 0:
            res = db.execute("update users set password=%s  where username=%s", (password,username,))

    def add_user(self, username, password, full_name):
        db.execute("insert into users values (%s,%s,%s)", (username,password,full_name))

    def get_user_by_username(self, username):
        cursor = db.execute("select username,password,full_name from users where username=%s", (username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return User(row[0], row[1], row[2])
