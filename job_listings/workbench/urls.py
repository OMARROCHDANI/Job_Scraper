
from django.urls import include, path
from workbench import views
urlpatterns = [
    
    path('',views.workbench, name='workbench'),
    path('save_job/<int:job_id>/', views.save_job, name='save_job'),
 



]
