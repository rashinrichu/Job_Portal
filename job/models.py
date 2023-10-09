from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Employee(models.Model):
    
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    education_level = models.CharField(max_length=100)
    skills = models.TextField()
    experience = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    image=models.ImageField(upload_to='jobseeker/',blank=True,null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer', null=True, blank=True)    
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    company_description = models.TextField()
    website = models.URLField()
    image=models.ImageField(upload_to='employer/',blank=True,null=True)


    def __str__(self):
        return self.company_name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
class JobListing(models.Model):
    KEYWORD_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('remote', 'Remote'),
        ('freelance', 'Freelance'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('entry-level', 'Entry-level'),
        ('senior-level', 'Senior-level'),
        ('remote-friendly', 'Remote-friendly'),
        ('temporary', 'Temporary'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    keyword = models.CharField(max_length=20, choices=KEYWORD_CHOICES)
    vacancies=models.IntegerField(null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    
class ApplyJob(models.Model):
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"Job Listing: {self.job_listing}, Employee: {self.employee}"




#chat between admin and users employees and employers
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    reply_to = models.ForeignKey('Notification', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"From: {self.sender.username} - To: {self.recipient.username}"

    @classmethod
    def get_chat_between_employer_and_employee(cls, employer, employee):
    
        employer_to_employee = cls.objects.filter(sender=employer, recipient=employee, admin=False)
        employee_to_employer = cls.objects.filter(sender=employee, recipient=employer, admin=False)
        admin_messages_to_employee = cls.objects.filter(sender__is_superuser=True, recipient=employee)
        admin_messages_from_employee = cls.objects.filter(sender=employee, recipient__is_superuser=True)

        return employer_to_employee | employee_to_employer | admin_messages_to_employee | admin_messages_from_employee

class InterviewSchedule(models.Model):
    apply_job = models.ForeignKey(ApplyJob, on_delete=models.CASCADE,null=True,blank=True)
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Job Listing: {self.job_listing}, Employee: {self.employee}, Date: {self.date}, Time: {self.time}"
    
   
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reply_to = models.ForeignKey('ChatMessage', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message    


class GroupChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_group_messages')
    recipients = models.ManyToManyField(User, related_name='received_group_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username}"


class GroupChatReply(models.Model):
    group_message = models.ForeignKey(GroupChatMessage, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_message_replies')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username} - To: {self.group_message.sender.username}"

#admin messages to  employee employers and all
class ImportantNotification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications',null=True)
    recipients = models.ManyToManyField(User, related_name='received_notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return self.message
