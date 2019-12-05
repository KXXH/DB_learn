from free_shark.models.commodity import Commodity
from flask import (Blueprint,flash,g,render_template,request,session,current_app,redirect,url_for,render_template_string,send_from_directory,Response)
from free_shark.entity.Page import Page
from free_shark.util.json_help import make_json
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
import requests
import uuid
import os
import sys
import time
import re
from flask_login import login_user,login_required,logout_user,current_user

bp=Blueprint('commodity',__name__,url_prefix='/commodity')

@bp.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        current = request.args.get('current') or 1
        current = int(current)
        commodity_name = request.args.get('commodity_name') or None
        commodity_type = request.args.get('commodity_type') or None
        print(commodity_name)
        print(commodity_type)
        r = Commodity.search_commodity(-1,0,sys.maxsize,1,commodity_type,commodity_name)
        # 设置分页
        page = Page()
        page.current = current
        page.rows = r
        page.path = '/hello'
        offset = page.get_offset()
        coms = Commodity.search_commodity(-1,offset,page.limit,0,commodity_type,commodity_name)
        return render_template("commodity.html", commodities=coms,page=page)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def remove_html(s):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',s)
    return dd

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def solve_photo(file):
    if file.filename == '':
        return ''
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 得到文件后缀名
        suffix = filename.split(".")[-1]
        # 自定义一个文件名
        filename = str(uuid.uuid1()).replace('-','') + '.' + suffix
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        photo_url = '/static/image/' + filename
        return photo_url
    else:
        return 2

@login_required
@bp.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        c = Commodity()
        if 'photo1' not in request.files:
            flash('No file part')
            return make_json(500,'no photo')
        file1 = request.files['photo1']
        r = solve_photo(file1)
        if r == 2:
            return make_json(500,'wrong type')
        else:
            c.commodity_photo_url1 = r

        file2 = request.files['photo2']
        r = solve_photo(file2)
        if r == 2:
            return make_json(500,'wrong type')
        else:
            c.commodity_photo_url2 = r

        file3 = request.files['photo3']
        r = solve_photo(file3)
        if r == 2:
            return make_json(500,'wrong type')
        else:
            c.commodity_photo_url3 = r

        file4 = request.files['photo4']
        r = solve_photo(file4)
        if r == 2:
            return make_json(500,'wrong type')
        else:
            c.commodity_photo_url4 = r

        file5 = request.files['photo5']
        r = solve_photo(file5)
        if r:
            return make_json(500,'wrong type')
        else:
            c.commodity_photo_url5 = r
        
        new_commodity_name = request.form['new_commodity_name']
        c.commodity_name = remove_html(new_commodity_name)

        new_commodity_type = request.form['new_commodity_type']
        c.commodity_type = remove_html(new_commodity_type)

        new_commodity_price = request.form['new_commodity_price']
        c.price = float(new_commodity_price)

        new_commodity_introduction = request.form['new_commodity_introduction']
        c.commodity_introduction = remove_html(new_commodity_introduction)

        # 整合时再取
        c.owner_student_id = '123123123'

        if c.add_commodity() == 1:
            return make_json(200,'success')



        
