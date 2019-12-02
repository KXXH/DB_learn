from free_shark.db import get_db,abort
import time


class Student():
    def __init__(self,user_id,school_number,real_name,college,banji,contact):
        self.__username=user_id
        self.__school_number=school_number
        self.__real_name=real_name
        self.__college=college
        self.__banji=banji
        self.__contact=contact
        print("到这里了！！！！！！！！！")
    
    @staticmethod
    def add_student(user_id,school_number,real_name,college,banji,contact):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = "INSERT INTO student(user_id,school_number,real_name,college,banji,contact,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            print("执行sql语句")
            cursor.execute(sql,(user_id,school_number,real_name,college,banji,contact,create_time))
            # 提交到数据库执行
            print("提交到数据库执行")
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            abort(500)
        # 关闭数据库连接
        db.close()
    
    def delete_student(id):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "DELETE FROM student WHERE id = %s"
        try:
            # 执行sql语句
            cursor.execute(sql,(id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close()

   @staticmethod
    def create_stu_from_rows(row):
        stu=Student(user_id=row[1],school_number=row[2],real_name=row[3],college=row[3],banji=row[4],activation=row[5],contact=row[6])
        return stu

    @staticmethod
    def query_student(id):
        db = get_db()
        cursor = db.cursor()
        #sql = "SELECT* FROM student WHERE id = %s"
        try:
            # 执行sql语句
            print("执行sql语句")
            print(id)
            cursor.execute('SELECT* FROM student WHERE id = %s',str(id))
            print("提交到数据库执行")
            results = cursor.fetchone()
            if result is None:
                return None
            stu=Student.create_stu_from_rows(result)
            print ("user_id=%s,school_number=%s,real_name=%s,college=%s,banji=%s,contact=%s" % (user_id,school_number,real_name,college,banji,contact))
        except:
            print ("Error: unable to fetch data")
            abort(500)
            # 关闭数据库连接
        return stu
        db.close()

    def update_student(id):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = "UPDATE student SET user_id=%s,school_number=%s,real_name=%s,college=%s,banji=%s,contact=%s,create_time=%s" % (user_id,school_number,real_name,college,banji,contact,create_time)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close() 

#Student.add_student("1","2016141441125","PDD","CS","1","buzhidao")      