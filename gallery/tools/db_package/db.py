import psycopg2
import json
from secrets import get_secret_postgres

connection = None

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

def connect():
    global connection
    secret = get_secret()
    connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))
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
    res = execute('select * from users')
    width = 11
    print('\nusername   password   full name')
    print('-------------------------------')
    for row in res:
        for i in range(len(row)):
            print(row[i].ljust(width), end='')
        print()
    print()

def add_user():
    username = input('\nUsername> ')
    password = input('Password> ')
    full_name = input('Full name> ')
    try:
        res = execute("insert into users values (%s, %s, %s)", (username,password,full_name,))
        print()
    except psycopg2.errors.UniqueViolation as e:
        print('\nError: user with username {Username} already exists\n'.format(Username=username))

def edit_user():
    username = input('\nUsername to edit> ')
    check_entry = execute('select username from users where username=%s', (username,))
    if check_entry.fetchone() == None:
        print('\nNo such user.\n')
    else:
        password = input('New password (press enter to keep current)> ')
        full_name = input('New full name (press enter to keep current)> ')
        print()
        res = execute("update users set password=%s where username=%s", (password,username,))

def delete_user():
    username = input('\nEnter username to delete> ')
    confirm = input('\nAre you sure you want to delete {Username}?(Yes/No) '.format(Username=username))

    if confirm == 'Yes':
        res = execute('delete from users where username=%s', (username,))
        print('\nDeleted.\n')
