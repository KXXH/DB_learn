from free_shark.db import get_db,abort
import time


class Order:
    def __init__(self,**kwargs):
        self._id=kwargs.get('id',None)
        self._commodity_id=kwargs.get('commodity_id',None)
        self._buyer_id=kwargs.get('buyer_id',None)
        self._seller_id=kwargs.get('seller_id',None)
        self._status=kwargs.get('status',None)
        self._create_time=kwargs.get('create_time',None)
        print("到这里了！！！！！！！！！")
    
    @staticmethod
    def add_order(**kwargs):
        ord=Order(**kwargs) 
        db = get_db()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 创建时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print(create_time)
        sql = "INSERT INTO order(id,commodity_id,buyer_id,seller_id,status,create_time) VALUES (%s,%s,%s,%s,%s)"
        try:
            # 执行sql语句
            print("执行sql语句")
            cursor.execute(sql,(ord._id,ord._commodity_id,ord._buyer_id,ord._seller_id,ord._status,create_time))
            # 提交到数据库执行
            print("提交到数据库执行")
            db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            db.rollback()
            raise e
        # 关闭数据库连接
        db.close()
    
    def delete_order(self):
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "DELETE FROM order WHERE id = %s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close()

    @staticmethod
    def create_ord_from_rows(row):
        ord=Order(id=row[0],commodity_id=row[1],buyer_id=row[2],seller_id=row[3],status=row[4],create_time=row[5])
        return ord

    @staticmethod
    def get_order_by_id(id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT* FROM order WHERE id = %s',str(id))
            results = cursor.fetchone()
            if results is None:
                return None
            ord=Order.create_ord_from_rows(results)
        except Exception as e:
            print ("Error: unable to fetch data")
            print (e)
            raise e
        return ord
        db.close()

    @staticmethod
    def get_order_by_commodity_id(commodity_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('SELECT* FROM order WHERE commodity_id = %s',str(commodity_id))
            results = cursor.fetchone()
            if results is None:
                return None
            ord=Order.create_ord_from_rows(results)
        except Exception as e:
            print ("Error: unable to fetch data")
            print (e)
            raise e
        return ord
        db.close()

    @property
    def update_status(self):
        return self._status

    @update_status.setter
    def update_status(self,new_val):
        self._status=new_val
        db = get_db()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        # 创建时间
        sql = "UPDATE order SET status=%s WHERE id=%s"
        try:
            # 执行sql语句
            cursor.execute(sql,(self._status,self._id))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
            # 关闭数据库连接
        db.close() 