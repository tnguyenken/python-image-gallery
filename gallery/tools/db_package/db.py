import psycopg2

db_host = "demo-database26.crpyrfmdbkk5.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())
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

def main():
    connect()

    while True:
        print("1) List users")
        print("2) Add user")
        print("3) Edit user")
        print("4) Delete user")
        print("5) Quit")
        command = input("Enter command> ")

        if int(command) == 1:
            list_users()
        if int(command) == 2:
            add_user()
        if int(command) == 3:
            edit_user()
        if int(command) == 4:
            delete_user()
        if int(command) == 5:
            break

if __name__ == '__main__':
    main()
