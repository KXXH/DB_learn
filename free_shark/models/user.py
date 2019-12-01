from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,username,password):
        super().__init__()
        self.__username=username
        self.__password=password
        if self.__username=="user" and self.__password=="pass":
            print("login success!")
            self.__activite_flag=True
        else:
            print("login fail!")
            print("username=%s, pass=%s" % (self.__username,self.__password))
            self.__activite_flag=False
    
    def is_authenticated(self):
        return self.__activite_flag

    def get_id(self):
        return '3'