from django.contrib import admin
from .models import Employee, Employer, Category, JobListing, InterviewSchedule, Notification, ImportantNotification, ChatMessage, GroupChatMessage, GroupChatReply,ApplyJob

admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(Category)
admin.site.register(ApplyJob)

admin.site.register(JobListing)
admin.site.register(InterviewSchedule)
admin.site.register(Notification)
admin.site.register(ImportantNotification)
admin.site.register(ChatMessage)
admin.site.register(GroupChatMessage)
admin.site.register(GroupChatReply)
