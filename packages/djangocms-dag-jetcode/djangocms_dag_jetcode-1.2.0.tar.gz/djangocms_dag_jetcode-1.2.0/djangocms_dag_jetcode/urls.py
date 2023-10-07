from django.urls import path

from djangocms_dag_jetcode import views


app_name = "djangocms-dag-jetcode"

urlpatterns = [path("<int:pk>/style.css", views.get_css, name="css")]
