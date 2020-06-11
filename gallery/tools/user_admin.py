from db_package import db

def main():
    db.connect()

    while True:
        print("1) List users")
        print("2) Add user")
        print("3) Edit user")
        print("4) Delete user")
        print("5) Quit")
        command = input("Enter command> ")
        
        try:
            if int(command) == 1:
                db.list_users()
            if int(command) == 2:
                db.add_user()
            if int(command) == 3:
                db.edit_user()
            if int(command) == 4:
                db.delete_user()
            if int(command) == 5:
                print()
                break
        except ValueError as e:
            print('\nPlease enter a valid entry\n')

if __name__ == '__main__':
    main()


