from django.urls import path

from empapp import views

app_name="empapp"
urlpatterns = [
    path('emplist/',views.emplist,name="emplist" ),
    path('addEmp/',views.addEmp,name="addEmp" ),
    path('addEmplogic/',views.addEmplogic,name="addEmplogic" ),
    path('deleteEmplogic/',views.deleteEmplogic,name="deleteEmplogic" ),
    path('updateEmp/',views.updateEmp,name="updateEmp" ),
    path('updateEmplogic/',views.updateEmplogic,name="updateEmplogic" ),
    path('index/',views.index,name="index" ),
    path('query/',views.query,name="query" ),
]