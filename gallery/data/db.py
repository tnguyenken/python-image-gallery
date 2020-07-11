import psycopg2
import json
#from gallery.aws.secrets import get_secret_postgres

connection = None

"""
In previous modules, we used a secrets manager to obtain the correct information to access our database.
In module 6, we pass environment variables into a docker container to access our database. This part of our project
has become code that is no longer used.

def get_secret():
    jsonString = get_secret_postgres()
    return json.loads(jsonString)

def get_password(secret):
    return secret['password']

def get_host(secret):
    return secret['host']

def get_username(secret):
    return secret['username']

def get_dbname(secret):
    return secret['database_name']
"""

def connect():
    global connection
    pg_host = 'mod6-ig-database.crpyrfmdbkk5.us-east-1.rds.amazonaws.com'
    ig_database = 'image_gallery'
    ig_user = 'image_gallery'
    ig_passwd = 'simple'
    # secret = get_secret()
    # connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
    # connection = psycopg2.connect(host=$PG_HOST, dbname=$IG_DATABASE, user=$IG_USER, password=$IG_PASSWD)
    connection = psycopg2.connect(host=pg_host, dbname=ig_database, user=ig_user, password=ig_passwd)
    connection.set_session(autocommit=True)

def execute(query, args=None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def list_users():
    res = execute('select username from users')
    user_list = []
    for row in res:
        for i in range(len(row)):
            user_list.append(row[i])
    return user_list

def add_user(username, password, full_name):
    res = execute("insert into users values (%s, %s, %s)", (username,password,full_name,))
    return res

def edit_user(username, password, full_name):
    if password and full_name is not None:
        res = execute("update users set password=%s, full_name=%s where username=%s", (password,full_name,username,))
    elif password == '':
        res = execute("update users set full_name=%s where username=%s", (full_name,username,))
    else:
        res = execute("update users set password=%s  where username=%s", (password,username,))

def delete_user(username, confirm):
    if confirm == 'Delete {}'.format(username):
        res = execute('delete from users where username=%s', (username,))
