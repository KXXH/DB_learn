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

bp=Blueprint('comorder',__name__,url_prefix='/comorder')

@bp.route('/order',methods=("GET","POST"))
def order():
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