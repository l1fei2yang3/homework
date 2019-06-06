from django.urls import path

from userapp import views

app_name="userapp"
urlpatterns = [
    path('login/',views.login ,name="login"),
    path('getcaptcha/',views.getcaptcha ,name="getcaptcha"),
    path('loginlogic/',views.loginlogic ,name="loginlogic"),
    path('regist/',views.regist,name="regist"),
    path('registlogic/',views.registlogic,name="registlogic"),
    path('checkname/',views.checkname,name="checkname"),
    path('checkImg/',views.checkImg,name="checkImg"),
]
