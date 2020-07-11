class UserDAO:
    def get_users(self):
        raise Exception("Must be implemented")
    
    def delete_user(self, username):
        raise Exception("Must be implemented")

    def create_user(self, username, password, full_name):
        raise Exception("Must be implemented")

    def edit_user(self, username):
        raise Exception("Must be implemented")
