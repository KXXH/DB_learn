from flask import (Blueprint,flash,g,render_template,request,session,redirect,url_for,render_template_string)
from werkzeug.security import check_password_hash,generate_password_hash
try:
    from forms import login_form
except ModuleNotFoundError:
    from .forms import login_form
    
try:
    from models import user
except ModuleNotFoundError:
    from .models import user

try:
    from models import student
except ModuleNotFoundError:
    from .models import student

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
        c_user=user.User.attempt_login(form.data['username'],form.data['password'])   #需要按需加载用户信息
        if c_user.is_authenticated():
            login_user(c_user)  #需要加入next跳转
            return render_template_string("Hi {{ current_user.username }}!")   #需要修改模板
        else:
            return "wrong password!"
    return render_template("login.html",form=form)


@bp.route('/test',methods=("GET","POST"))
def test():
    #c_student = student.Student("1","2016141441125","PDD","CS","1","buzhidao")
    #student.Student.add_student("1","2016141441125","PDD","CS","1","buzhidao")
    student.Student.query_student(1)
    return "login required!"    #加入界面

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/hello")