class User:
    def __init__(self, username, password, full_name):
        self.__username = username
        self.__password = password
        self.__full_name = full_name
    
    def username(self):
        return self.__username
        
    def full_name(self):
        return self.__full_name    

    def __repr__(self):
        return "User with username " + self.__username + "password: " + self.__password + " full name: " + self.__full_name
        
