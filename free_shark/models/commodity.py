from free_shark.db import get_db

class Commodity:
    def __init__(self,**kwargs):
        self._id = kwargs.get('id',None)
        self._commodity_name = kwargs.get('commodity_name', None)
        self._commodity_type = kwargs.get('commodity_type', None)
        self._owner_student_id = kwargs.get('owner_student_id', None)
        self._price = kwargs.get('price', None)
        self._commodity_introduction = kwargs.get('commodity_introduction', None)
        self._commodity_photo_url1 = kwargs.get('commodity_photo_url1', None)
        self._commodity_photo_url2 = kwargs.get('commodity_photo_url2', None)
        self._commodity_photo_url3 = kwargs.get('commodity_photo_url3', None)
        self._commodity_photo_url4 = kwargs.get('commodity_photo_url4', None)
        self._commodity_photo_url5 = kwargs.get('commodity_photo_url5', None)
        self._create_time = kwargs.get('create_time', None)

    @property
    def id(self):
        return self._id

    @property
    def commodity_name(self):
        return self._commodity_name
    
    @property
    def commodity_type(self):
        return self._commodity_type
    
    @property
    def owner_student_id(self):
        return self._owner_student_id
    
    @property
    def price(self):
        return self._price
    
    @property
    def commodity_introduction(self):
        return self._commodity_introduction
    
    @property
    def commodity_photo_url1(self):
        return self._commodity_photo_url1
    
    @property
    def commodity_photo_url2(self):
        return self._commodity_photo_url2
    
    @property
    def commodity_photo_url3(self):
        return self._commodity_photo_url3
    
    @property
    def commodity_photo_url4(self):
        return self._commodity_photo_url4
    
    @property
    def commodity_photo_url5(self):
        return self._commodity_photo_url5
    
    @property
    def create_time(self):
        return self._create_time



    @commodity_name.setter
    def commodity_name(self,new_commodity_name):
        self._commodity_name = new_commodity_name
    
    @commodity_type.setter
    def commodity_type(self,new_commodity_type):
        self._commodity_type = new_commodity_type
    
    @owner_student_id.setter
    def owner_student_id(self,new_owner_student_id):
        self._owner_student_id = new_owner_student_id
    
    @price.setter
    def price(self,new_price):
        self._price = new_price
    
    @commodity_introduction.setter
    def commodity_introduction(self,new_commodity_introduction):
        self._commodity_introduction = new_commodity_introduction
    
    @commodity_photo_url1.setter
    def commodity_photo_url1(self,new_commodity_photo_url1):
        self._commodity_photo_url1 = new_commodity_photo_url1
    
    @commodity_photo_url2.setter
    def commodity_photo_url2(self,new_commodity_photo_url2):
        self._commodity_photo_url2 = new_commodity_photo_url2
    
    @commodity_photo_url3.setter
    def commodity_photo_url3(self,new_commodity_photo_url3):
        self._commodity_photo_url3 = new_commodity_photo_url3
    
    @commodity_photo_url4.setter
    def commodity_photo_url4(self,new_commodity_photo_url4):
        self._commodity_photo_url4 = new_commodity_photo_url4
    
    @commodity_photo_url5.setter
    def commodity_photo_url5(self,new_commodity_photo_url5):
        self._commodity_photo_url5 = new_commodity_photo_url5
    
    @create_time.setter
    def create_time(self,new_create_time):
        self._create_time = new_create_time

    

#       上架商品
#       传入一个Commodity实例进行上架，为实例方法
    
    def add_commodity(self):
        sql = "insert into commodity(commodity_name,commodity_type,owner_student_id,price,\
            commodity_introduction,commodity_photo_url1,commodity_photo_url2,commodity_photo_url3,\
            commodity_photo_url4,commodity_photo_url5,create_time) \
            VALUES('%s','%s','%s',%.2f,'%s','%s','%s','%s','%s','%s','%s')" % (
                self._commodity_name, self._commodity_type, self._owner_student_id, self._price,
                self._commodity_introduction, self._commodity_photo_url1,self._commodity_photo_url2,
                self._commodity_photo_url3, self._commodity_photo_url4, self._commodity_photo_url5, self._create_time)
        
        try:
            db = get_db()
            cursor = db.cursor()
            print(sql)
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        db.close()

#       删除商品
#       传入商品id进行删除，为静态方法

    def delete_commodity_by_id(id):
        sql = "delete from commodity where id = %d" % (id)

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        db.close()

#       搜索商品
#       需要传入用户id（为-1时表示搜索全部），商品种类，商品名称
#       需要改进 加入模糊搜索。。
    def search_commodity(owner_student_id, commodity_type=None, commodity_name=None):
        r = []
        if commodity_type != None and commodity_name!= None:
            if owner_student_id == -1:
                sql = "SELECT * FROM commodity \
                    WHERE commodity_type LIKE '%%%s%%'\
                    AND commodity_name LIKE '%%%s%%' \
                    order by create_time desc " % (commodity_type, commodity_name)
            else:
                sql = "SELECT * FROM commodity \
                    WHERE commodity_type LIKE '%%%s%%'\
                    AND owner_student_id = '%s' \
                    AND commodity_name LIKE '%%%s%%' \
                    order by create_time desc" % (commodity_type, owner_student_id, commodity_name)

        elif commodity_type == None and commodity_name != None:
            if owner_student_id == -1:
                sql = "SELECT * FROM commodity \
                    WHERE commodity_name LIKE '%%%s%%' \
                    order by create_time desc " % (commodity_name)
            else:
                sql = "SELECT * FROM commodity \
                    WHERE owner_student_id = '%s' \
                    AND commodity_name LIKE '%%%s%%' \
                    order by create_time desc" % (owner_student_id, commodity_name)
        elif commodity_type != None and commodity_name == None:
            if owner_student_id == -1:
                sql = "SELECT * FROM commodity \
                    WHERE commodity_type LIKE '%%%s%%'\
                    order by create_time desc " % (commodity_type)
            else:
                sql = "SELECT * FROM commodity \
                    WHERE commodity_type LIKE '%%%s%%'\
                    AND owner_student_id = '%s' \
                    order by create_time desc" % (commodity_type, owner_student_id)
        else:
            if owner_student_id == -1:
                sql = "SELECT * FROM commodity \
                    order by create_time desc "
            else:
                sql = "SELECT * FROM commodity \
                    WHERE owner_student_id = '%s' \
                    order by create_time desc" % (owner_student_id)

        db = get_db()
        cursor = db.cursor()
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            commodity_name = row[1]
            commodity_type = row[2]
            owner_student_id = row[3]
            price = row[4]
            commodity_introduction = row[5]
            commodity_photo_url1 = row[6]
            commodity_photo_url2 = row[7]
            commodity_photo_url3 = row[8]
            commodity_photo_url4 = row[9]
            commodity_photo_url5 = row[10]
            create_time = row[11]

            commodity = Commodity(
                id=id, commodity_name=commodity_name, commodity_type=commodity_type,owner_student_id=owner_student_id,
                price=price, commodity_introduction=commodity_introduction, commodity_photo_url1=commodity_photo_url1,
                commodity_photo_url2=commodity_photo_url2,commodity_photo_url3=commodity_photo_url3,commodity_photo_url4=commodity_photo_url4,
                commodity_photo_url5=commodity_photo_url5, create_time=create_time)

            r.append(commodity)

        db.close()
        return r

#       是否需要加入更新操作？
#       还是加入把

    def update_commodity(self):
        sql = "update commodity set commodity_name = '%s',commodity_type='%s',owner_student_id='%s',price=%.2f,\
            commodity_introduction='%s',commodity_photo_url1='%s',commodity_photo_url2='%s',commodity_photo_url3='%s',\
            commodity_photo_url4='%s',commodity_photo_url5='%s',create_time='%s' \
            where id = %d" % (
                self._commodity_name, self._commodity_type, self._owner_student_id, self._price,
                self._commodity_introduction, self._commodity_photo_url1,self._commodity_photo_url2,
                self._commodity_photo_url3, self._commodity_photo_url4, self._commodity_photo_url5, self._create_time,self._id)
        
        try:
            db = get_db()
            cursor = db.cursor()
            print(sql)
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        db.close()