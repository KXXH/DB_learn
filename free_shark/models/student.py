from db import get_db
import time
import pymysql

class Student():
    def __init__(self,user_id,school_number,real_name,college,banji,contact):
        self.__username=user_id
        self.__school_number=school_number
        self.__real_name=real_name
        self.__college=college
        self.__banji=banji
        self.__contact=contact
        print("到这里了！！！！！！！！！")
    
    def add_student(user_id,school_number,real_name,college,banji,contact):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = """INSERT INTO student(user_id,school_number,real_name,college,banji,contact,create_time) VALUES (user_id,school_number,real_name,college,banji,contact,create_time)"""
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

    def delete_student(id):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "DELETE FROM student WHERE id = %s" % (id)
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

    def query_student(id):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "SELECT FROM student WHERE id = %s" % (id)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            results = cursor.fetchall()
            for row in results:
                user_id = row[0]
                school_number = row[1]
                real_name = row[2]
                college = row[3]
                banji = row[4]
                contact = row[5]
                # 打印结果
                print ("user_id=%s,school_number=%s,real_name=%s,college=%s,banji=%s,contact=%s" % (user_id,school_number,real_name,college,banji,contact))
        except:
            print ("Error: unable to fetch data")
            # 关闭数据库连接
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

        