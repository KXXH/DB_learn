from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,username,password):
        super().__init__()
        self.__username=username
        self.__password=password
        if self.__username=="user" and self.__password=="pass":
            self.__activite_flag=True
        else:
            self.__activite_flag=False
    
    def get_id(self):
        return '3'