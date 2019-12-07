from flask import Blueprint,render_template,flash,current_app,request
from flask.views import MethodView
from free_shark.utils import admin_login_required
from free_shark.models.user import User

bp=Blueprint('admin',__name__,url_prefix='/admin')

@bp.route('/user',methods=("GET",))
@admin_login_required
def user_admin():
    flash("Hi, 尊敬的管理员","success")
    return render_template("admin/user.html")


class AdminView(MethodView):

    default_page_num=1
    default_page_size=20

    def get_target(self):
        raise NotImplementedError()

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self,**context):
        return render_template(self.get_template_name(),**context)

    @admin_login_required
    def get(self):
        method=request.args.get("method")
        target=self.get_target()
        if not method:
            ans,count=target.search(page_size=self.default_page_size,page_num=self.default_page_num)
            print(ans)
            return self.render_template(ans=ans,count=count)
        


class UserAdminView(AdminView):

    def get_template_name(self):
        return "admin/user.html"

    def get_target(self):
        return User

    

bp.add_url_rule('/userTest',view_func=UserAdminView.as_view("admin_view"))