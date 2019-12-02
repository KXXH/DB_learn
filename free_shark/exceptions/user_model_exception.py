class UserModelException(Exception):
    pass
class UserEmailInvalid(UserModelException):
    def __init__(self,wrong_email):
        self.wrong_email=wrong_email