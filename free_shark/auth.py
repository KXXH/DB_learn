from flask import (Blueprint, flash, g, render_template,
                   request, session, redirect, url_for, render_template_string, current_app)
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.exceptions import Forbidden
from free_shark.forms import login_form,student_form
from free_shark.models import user
from free_shark.models import student
from flask_principal import identity_loaded,UserNeed,RoleNeed,identity_changed,Identity,AnonymousIdentity
from flask_login import login_user,login_required,logout_user,current_user
from free_shark.resources.user_resource.user_register_resource import SendActivationEmailPermission

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/login',methods=("GET","POST"))
def login():
    form=login_form.LoginForm()
    if form.validate_on_submit():
        c_user=user.User.attempt_login(form.data['username'],form.data['password'])   #需要按需加载用户信息
        print("is blocked?",c_user.is_blocked)
        if c_user.is_blocked and c_user.is_authenticated():
                flash("你已被封禁, 最近的封禁记录: 因 %s 被封号至 %s " % (c_user.active_block_list[0].reason,c_user.active_block_list[0].end_time) ,"warning")
        elif c_user.is_authenticated():
            login_user(c_user,remember=form.data['remember'])  #需要加入next跳转
            if c_user.is_forbid:
                flash("你还没有激活账户,请快去<a href='/auth/send_activation'>激活</a>!","warning")
            if c_user.is_admin:
                flash("尊敬的管理员, 请前往<a href='/admin/user'>页面</a>管理系统!","success")
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(c_user.id))
            next = request.args.get('next')
            print(next)
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            flash("Hi %s!" % c_user.username,"success")
            return redirect(next or url_for('auth.login'))
            
            #return render_template_string("Hi {{ current_user.username }}!")   #需要修改模板
        else:
            flash("wrong password!","danger")
    return render_template("login.html",form=form)

@bp.route("/editUser")
def editUser():
    targets=request.args.get("target")
    usernameInputEnable=True
    passwordInputEnable=True
    emailInputEnable=True
    if targets is not None:
        targets=targets.split(",")
        if "username" not in targets:
            usernameInputEnable=False
        if "password" not in targets:
            passwordInputEnable=False
        if "email" not in targets:
            emailInputEnable=False
    return render_template("edit_userinfo.html",
        usernameInputEnable=usernameInputEnable,
        passwordInputEnable=passwordInputEnable,
        emailInputEnable=emailInputEnable
        )

@bp.route("/register",methods=("GET",))
def register():
    if current_user.is_authenticated:
        logout()


    return render_template("register.html")

send_email_permission=SendActivationEmailPermission()


@bp.route("/send_activation")
@send_email_permission.require(403)
def send_activation():
    return render_template("send_activation_email.html")



@bp.route("/activation/<token>")
def activation(token):
    c_user=user.User.get_user_by_token(token)
    if c_user is None or not c_user.is_forbid:
        return redirect(url_for("auth.login"))
    else:
        login_user(c_user)  #需要加入next跳转
        c_user.status=1
        identity_changed.send(current_app._get_current_object(),
                                identity=Identity(c_user.id))
    return render_template("activation_success.html")


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


