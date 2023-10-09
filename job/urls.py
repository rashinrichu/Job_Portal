from django.contrib import admin
from django.urls import path,include
from job import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('jobs/',views.jobs,name='jobs'),
    path('registration_employee/',views.registration_employee,name='registration_employee'),
    path('registration_employer/',views.registration_employer,name='registration_employer'),
    path('user_login/',views.user_login,name='user_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('employee_home/',views.employee_home,name='employee_home'),
    path('employer_home/',views.employer_home,name='employer_home'),
    path('employee_profile/',views.employee_profile,name='employee_profile'),
    path('employer_profile/',views.employer_profile,name='employer_profile'),

    path('edit_employer_profile/',views.edit_employer_profile,name='edit_employer_profile'),
    path('edit_employee_profile/',views.edit_employee_profile,name='edit_employee_profile'),
    path('add_category/',views.add_category,name='add_category'),
    path('category_list/',views.category_list,name='category_list'),
    path('create_job_listing/',views.create_job_listing,name='create_job_listing'),
    path('created_jobs/',views.created_jobs,name='created_jobs'),

    path('logout/',views.logout,name='logout'),
    path('employer_list/',views.employer_list,name='employer_list'),
    path('employee_list/',views.employee_list,name='employee_list'),
    path('created_jobs_employee/',views.created_jobs_employee,name='created_jobs_employee'),

    path('delete_employer/<int:employer_id>/',views.delete_employer,name='delete_employer'),

    path('apply_job/<int:job_listing_id>/', views.apply_job, name='apply_job'),
    path('applied_jobs_employee/', views.applied_jobs_employee, name='applied_jobs_employee'),
    path('applied_jobs_employer/', views.applied_jobs_employer, name='applied_jobs_employer'),
    path('all_employees/', views.all_employees, name='all_employees'),
    path('add_category_employer/', views.add_category_employer, name='add_category_employer'),

    # path('employer_chat/<int:job_listing_id>/', views.employer_chat, name='employer_chat'),
    # path('employee_chat/<int:job_listing_id>/', views.employee_chat, name='employee_chat'),
    # path('all_messages/<int:job_listing_id>/', views.all_messages, name='all_messages'),
    # path('send_message_to_all_employees/', views.send_message_to_all_employees, name='send_message_to_all_employees'),
    path('schedule_interview/<int:job_listing_id>/<int:applied_job_id>/', views.schedule_interview, name='schedule_interview'),
    path('interview_list_employee/', views.interview_list_employee, name='interview_list_employee'),
    path('interview_schedule_employer/', views.interview_schedule_employer, name='interview_schedule_employer'),
    path('chat/<int:sender_id>/<int:recipient_id>/', views.chat_between_users, name='chat_between_users'),  
    path('all_employers_list/', views.all_employers_list, name='all_employers_list'),
    path('job_search/', views.job_search, name='job_search'),
    path('employer_job_listings/<int:employer_id>/', views.employer_job_listings, name='employer_job_listings'),
    path('group_chat/', views.group_chat, name='group_chat'),
    path('employee_chat/', views.employee_chat, name='employee_chat'),
    path('update_job_listing/<int:job_listing_id>/', views.update_job_listing, name='update_job_listing'),
    path('notification/', views.notification, name='notification'),
    path('job_listings/category/<int:category_id>/', views.job_listings_by_category, name='job_listings_by_category'),
    path('job_search_employer/', views.job_search_employer, name='job_search_employer'),
    path('private_chat/<int:recipient_id>/', views.private_chat, name='private_chat'),
    path('job_search_admin/', views.job_search_admin, name='job_search_admin'),
    # path('chat_between_admin_and_user/<int:user_id>/', views.chat_between_admin_and_user, name='chat_between_admin_and_user'),
    path('admin_messages/', views.admin_messages, name='admin_messages'),
    path('admin_messages_employer/', views.admin_messages_employer, name='admin_messages_employer'),
    path('job_listings_by_category_employee/<int:category_id>/', views.job_listings_by_category_employee, name='job_listings_by_category_employee'),
    path('job_list_admin/<int:category_id>/', views.job_list_admin, name='job_list_admin'),

]
    




