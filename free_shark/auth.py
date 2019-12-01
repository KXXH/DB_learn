from flask import (Blueprint,flash,g,render_template,request,session,redirect,url_for)
from werkzeug.security import check_password_hash,generate_password_hash
from forms import login_form
from models import user
from flask_login import login_user,login_required,logout_user

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=("GET","POST"))
def register():
    return "register"

@bp.route('/login',methods=("GET","POST"))
def login():
    form=login_form.LoginForm()
    if form.validate_on_submit():
        print("form_data=",form.data)
        c_user=user.User(form.data['username'],form.data['password'])   #需要按需加载用户信息
        if c_user.is_authenticated():
            login_user(c_user)  #需要加入next跳转
            return "success!"   #需要修改模板
        else:
            return "wrong password!"
    return render_template("login.html",form=form)

@bp.route('/test')
@login_required
def test():
    return "login required!"    #加入界面

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/hello")