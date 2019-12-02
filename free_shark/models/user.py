from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import re
try:
    from db import get_db,close_db,db_required,abort,get_db_with_dict_cursor
    from exceptions.db_exception import DB_Exception
    from exceptions.user_model_exception import UserModelException,UserEmailInvalid
except ModuleNotFoundError:
    from ..db import get_db,close_db,db_required,abort,get_db_with_dict_cursor
    from ..exceptions.db_exception import DB_Exception
    from ..exceptions.user_model_exception import UserModelException,UserEmailInvalid

class User(UserMixin):

    def __init__(self,**kwargs):
        super().__init__()
        self._id=kwargs.get('id',None)
        self._username=kwargs.get('username',None)
        self._password=kwargs.get('password',None)
        self._salt=kwargs.get('salt',None)
        self._email=kwargs.get('email',None)
        self._activation=kwargs.get('activation',None)
        self._type=kwargs.get('type',None)
        self._status=kwargs.get('status',None)
        self._create_time=kwargs.get('create_time',None)
        self._activite_flag=False
    
    def is_authenticated(self):
        return self._activite_flag

    def user_id_not_none(func):
        def wrapper(self,*args,**kwargs):
            if self.id is None:
                print('User id should not None!')
                abort(500)
            else:
                func(self,*args,**kwargs)
        return wrapper

    def login(self):
        self._activite_flag=True

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self,new_val):
        self._username=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET username=%s WHERE id=%s",(self._username,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()
    
    @property
    def password(self):
        return self._password
    
    def check_password(self,password):
        return check_password_hash(self.password,password)

    @password.setter
    def password(self,new_val):
        self._password=generate_password_hash(new_val)
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET password=%s WHERE id=%s",(self._password,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()

    @property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self,new_val):
        self._salt=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET salt=%s WHERE id=%s",(self._salt,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self,new_val):
        pattern=r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"   #邮箱仅允许字母数字下划线和横杠
        if not re.match(pattern,new_val):
            raise UserEmailInvalid(new_val)
        self._email=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET email=%s WHERE id=%s",(self._email,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()


    @property
    def activation(self):
        return self._activation
    
    @activation.setter
    def activation(self,new_val):
        self._activation=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET activation=%s WHERE id=%s",(self._activation,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()


    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self,new_val):
        self._type=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET type=%s WHERE id=%s",(self._type,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()

    @property
    def status(self):
        return self._status
    
    @status.setter
    @user_id_not_none
    def status(self,new_val):
        self._status=new_val
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("UPDATE user SET status=%s WHERE id=%s",(self._status,self._id))
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()


    @property
    def create_time(self):
        return self._create_time
    

    def delete_user(self):
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE id=%s",self._id)
            db.commit()
        except:
            db.rollback()
            abort(500)
        db.close()

    @staticmethod
    def create_user_from_rows(row):
        user=User(id=row[0],username=row[1],password=row[2],salt=row[3],email=row[4],activation=row[5],type=row[6],status=row[7],create_time=row[8])
        return user

    @staticmethod
    def get_user_by_id(id):
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT * FROM user WHERE id=%s',str(id))
        result = cursor.fetchone()  #由于id的唯一性，至多只有一个结果
        if result is None:
            return None
        user=User.create_user_from_rows(result)
        cursor.close()
        db.close()
        return user

    @staticmethod
    def get_user_by_username(username):
        db=get_db()
        cursor=db.cursor()
        cursor.execute('SELECT * FROM user WHERE username=%s',str(username))
        result = cursor.fetchone()  #由于username的唯一性，至多只有一个结果
        if result is None:
            return None
        user=User.create_user_from_rows(result)
        cursor.close()
        db.close()
        return user

    @staticmethod
    def attempt_login(username,password):
        user = User.get_user_by_username(username)
        if user is None:
            return User()
        if user.check_password(password):
            user.login()
            return user
        else:
            return User()

    @staticmethod
    def create_user(**kwargs):
        user=User(**kwargs)
        db=get_db()
        cursor=db.cursor()
        try:
            cursor.execute("INSERT INTO user (username,password,salt,email,activation,type,status,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(user.username,user.password,user.salt,user.email,user.activation,user.type,user.status,user.create_time))
            db.commit()
            return User.get_user_by_username(user.username)
        except:
            db.rollback()
            abort(500)
        


    




