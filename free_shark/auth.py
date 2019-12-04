from flask import (Blueprint,flash,g,render_template,request,session,redirect,url_for,render_template_string,current_app)
from werkzeug.security import check_password_hash,generate_password_hash
from free_shark.forms import login_form,student_form
from free_shark.models import user
try:
    from models import student
except ModuleNotFoundError:
    from .models import student
from flask_principal import identity_loaded,UserNeed,RoleNeed,identity_changed,Identity,AnonymousIdentity
from flask_login import login_user,login_required,logout_user,current_user

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=("GET","POST"))
def register():
    return "register"

@bp.route('/login',methods=("GET","POST"))
def login():
    form=login_form.LoginForm()
    if form.validate_on_submit():
        c_user=user.User.attempt_login(form.data['username'],form.data['password'])   #需要按需加载用户信息
        if c_user.is_authenticated():
            login_user(c_user)  #需要加入next跳转
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(c_user.id))
            return render_template_string("Hi {{ current_user.username }}!")   #需要修改模板
        else:
            return "wrong password!"
    return render_template("login.html",form=form)


@bp.route('/test',methods=("GET","POST"))
def test():
    form=student_form.StudentForm()
    data ={}
    if form.validate_on_submit():
        print("form_data=",form.data)
        stu=student.Student.get_student_real_name(form.data['real_name'])
        stu.update_college=form.data['college']
        data = {
        "real_name": stu._real_name,
        "college": stu._college,
        "user_id": stu._user_id,
        "school_number": stu._school_number,
        "banji": stu._banji,
        "contact": stu._contact
        }
        #return "已更新！！！！！"
    return render_template("testStudent.html",form=form,data=data)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(),
                        identity=AnonymousIdentity())
    return redirect("/hello")


