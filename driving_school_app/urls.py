from django.urls import include, path
from . import views


urlpatterns = [

    
    path('',views.home,name="home"),
    path('logout',views.logout,name="logout"),
    path('logout1',views.logout1),
    path('login',views.login_form,name="login"),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('new_password/<uname>',views.new_password,name='new_password'),



    path('driving_school_register',views.driving_school_register,name="driving_school_register"),
    path('user_register',views.user_register,name="user_register"),
    path('adminhome',views.adminhome,name="adminhome"),
   path('managecategory',views.managecategory,name="managecategory"),
   path('categoryupdate/<catid>',views.categoryupdate,name="categoryupdate"),
   path('categorydelete/<catid>',views.categorydelete,name="categorydelete"),
   path('viewdrivingschool',views.viewdrivingschool,name="viewdrivingschool"),
   path('viewtrainer/<tid>',views.viewtrainer,name="viewtrainer"),
   path('admin_view_users',views.admin_view_users,name="admin_view_users"),
   path('admin_view_complaints',views.admin_view_complaints,name="admin_view_complaints"),
   path('admin_send_reply/<id>',views.admin_send_reply,name="admin_send_reply"),
   path('adminaccept_driving/<did>/<lid>',views.adminaccept_driving,name="adminaccept_driving"),
   path('adminreject_driving/<did>/<lid>',views.adminreject_driving,name="adminreject_driving"),
   path('admin_view_licence_req',views.admin_view_licence_req,name="admin_view_licence_req"),
    path('admin_view_driving_req',views.admin_view_driving_req,name="admin_view_driving_req"),


   path('drivingschoolhome',views.drivingschoolhome,name="drivingschoolhome"),
   path('managetrainer',views.managetrainer,name="managetrainer"),
   path('trainerdelete/<id>',views.trainerdelete,name="trainerdelete"),
   path('trainerupdate/<id>',views.trainerupdate,name="trainerupdate"),
   path('viewqueries',views.viewqueries,name="viewqueries"),
   path('sendqueries/<id>',views.sendqueries,name="sendqueries"),
   path('drivingview_request',views.drivingview_request,name="drivingview_request"),
   path('drivingaccept_req/<id>',views.drivingaccept_req,name="drivingaccept_req"),
   path('drivingreject_req/<id>',views.drivingreject_req,name="drivingreject_req"),
   path('drivingassign_trainer/<oid>',views.drivingassign_trainer,name="drivingassign_trainer"),
   path('drivingassign/<id>/<oid>',views.drivingassign,name="drivingassign"),
   path('drivingview_lrequest',views.drivingview_lrequest,name="drivingview_lrequest"),
   path('drivingaccept_lreq/<id>',views.drivingaccept_lreq,name="drivingaccept_lreq"),
   path('drivingreject_lreq/<id>',views.drivingreject_lreq,name="drivingreject_lreq"),





   path('trainerhome',views.trainerhome,name="trainerhome"),
   path('managetutorial',views.managetutorial,name="managetutorial"),
   path('deletetutorial/<id>',views.deletetutorial,name="deletetutorial"),
   path('viewassignedusers',views.viewassignedusers,name="viewassignedusers"),
   path('trainerupdatestatus/<id>',views.trainerupdatestatus,name="trainerupdatestatus"),
   path('trainerchatwith_user/<pid>',views.trainerchatwith_user),
   path('trainer_send_queries',views.trainer_send_queries,name="trainer_send_queries"),


   path('userhome',views.userhome,name="userhome"),
   path('user_send_complaint',views.user_send_complaint,name="user_send_complaint"),
   path('user_view_tutorial',views.user_view_tutorial),
   path('user_send_driving_req',views.user_send_driving_req),
   path('usermake_payment/<oid>/<total>',views.usermake_payment,name="usermake_payment"),
   path('user_send_license_req',views.user_send_license_req),
   path('user_makepayment/<oid>/<total>',views.user_makepayment,name="user_makepayment"),
   path('userview_trainer',views.userview_trainer),
   path('userchatwith_trainer/<pid>',views.userchatwith_trainer),
   path('driving_viewuser',views.driving_viewuser),
   path('user_view_drivingschool',views.user_view_drivingschool),
   path('userview_invoice/<id>/<amt>',views.userview_invoice,name="userview_invoice"),
   path('userviewl_invoice/<id>/<amt>',views.userviewl_invoice,name="userviewl_invoice"),









  





]