from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from.models import *
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from datetime import datetime
from django.contrib.auth import authenticate,login
from django.db.models import F
from .models import ChatMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


from django.conf import settings


# Create your views here.
def index(request):
    categories = Category.objects.all()
    employees = Employee.objects.all()
    job_listings = JobListing.objects.all()
    keywords = JobListing.KEYWORD_CHOICES  

    context = {
        'categories': categories,
        'keywords': keywords,
        'job_listings': job_listings,
    }

    return render(request, 'index.html', context)


def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def jobs(request):
    return render(request,'jobs.html')



from django.db.models import F

from django.db.models import Q

def employee_home(request):
    categories = Category.objects.all()
    job_listings = JobListing.objects.all()
    keywords = JobListing.KEYWORD_CHOICES

    employee = request.user.employee
    employer = Employee.objects.filter(user__employer__isnull=False).first()
    employer_id = employer.user.id if employer else None
    employee_id = employee.user.id if employee else None

    recipient_id = request.GET.get('recipient_id')  

    chat_notifications = Notification.objects.filter(
        recipient=request.user,
        employer__isnull=True,  
        reply_to__isnull=True,  
    ).order_by('-timestamp')

    context = {
        'job_listings': job_listings,
        'categories': categories,
        'keywords': keywords,
        'employee': employee,
        'employer': employer.user if employer else None,
        'employer_id': employer_id,
        'employee_id': employee_id,
        'chat_notifications': chat_notifications,
        'recipient_id': recipient_id, 
    }

    return render(request, 'employee_home.html', context)

def employer_home(request):
    job_listing_id = 1 
    categories = Category.objects.all()
    job_listings = JobListing.objects.all()

    keywords = JobListing.KEYWORD_CHOICES  

    chat_notifications = Notification.objects.filter(
        recipient=request.user,
        employer__isnull=False,  
        reply_to__isnull=True,  
    ).order_by('-timestamp')

    context = {
        'job_listings': job_listings,

        'categories': categories,
        'keywords': keywords,
        'job_listing_id': job_listing_id,
        'chat_notifications': chat_notifications,
    }

    return render(request, 'employer_home.html', context)


def admin_home(request):
    categories = Category.objects.all()
    employees = Employee.objects.all()

    job_listings = JobListing.objects.all()

    keywords = JobListing.KEYWORD_CHOICES  
    context = {
        'categories': categories,
        'keywords': keywords,
        'job_listings': job_listings,

    }
    return render(request, 'admin_home.html', context)




from django.core.mail import send_mail
from django.conf import settings

def registration_employee(request):
    default_image = settings.STATIC_URL + 'static/img/User.png'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        image = request.FILES.get('image')
        education_level = request.POST.get('education_level')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        resume = request.FILES.get('resume')
        contact_number = request.POST.get('contact_number')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('index')

        # Create the user object
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create the employee object
        employee = Employee.objects.create(
            user=user,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            education_level=education_level,
            skills=skills,
            experience=experience,
            resume=resume,
            image=image,
            contact_number=contact_number,
            date_of_birth=date_of_birth,
            gender=gender
        )
        
        # Send registration confirmation email
        subject = 'Welcome to Job Connect'
        message = f'Thank you for joining our Job Connect. Your registration as an employee was successful. We look forward to working with you.\n\nYour username: {username}\nYour password: {password}'        
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, 'Registration successful. Please log in to access your account.')
        return redirect('index')
    else:
        context = {'default_image': default_image}
        return render(request, 'index.html', context)



    





def registration_employer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        company_description = request.POST.get('company_description')
        website = request.POST.get('website')
        image = request.FILES.get('image')

        if Employer.objects.filter(company_name=company_name).exists():
            messages.error(request, 'Company name already taken')
            return redirect('index')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('index')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        employer = Employer(
            user=user,
            company_name=company_name,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            company_description=company_description,
            website=website,
            image=image
        )
        employer.save()

        subject = 'Welcome to Job Connect'
        message = f'Thank you for joining our Job Connect. Your registration as an employer was successful.\n\nYour username: {username}\nYour password: {password}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Redirect to the index page with a success message
        messages.success(request, 'Registration successful. Please log in to access your account.')
        return redirect('index')

    else:
        return render(request, 'index.html')
    
    


def user_login(request):
    success_alert = False
    error_alert = False

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                # User is an admin
                messages.success(request, 'Logged in successfully as admin!')
                success_alert = True
                return redirect('admin_home')
            else:
                try:
                    employee = user.employee
                    # User is an employee
                    messages.success(request, 'Logged in successfully as employee!')
                    success_alert = True
                    return redirect('employee_home')
                except ObjectDoesNotExist:
                    pass

                try:
                    employer = Employer.objects.get(user=user)
                    # User is an employer
                    messages.success(request, 'Logged in successfully as employer!')
                    success_alert = True
                    return redirect('employer_home')
                except ObjectDoesNotExist:
                    pass

        messages.error(request, 'Invalid username or password')
        error_alert = True

    return render(request, 'index.html', {'success_alert': success_alert, 'error_alert': error_alert})


def logout(request):
    auth.logout(request)
    return redirect('index')



@login_required
def employee_profile(request):
    employee = request.user.employee

    context = {
        'employee': employee
    }

    return render(request, 'employee_profile.html', context)



@login_required
def employer_profile(request):
    employer = Employer.objects.get(user__username=request.user.username)

    context = {
        'employer': employer
    }

    return render(request, 'employer_profile.html', context)




# edit employee profile


def edit_employee_profile(request):
    employee = request.user.employee

    if request.method == 'POST':
        employee.user.first_name = request.POST.get('first_name')
        employee.user.last_name = request.POST.get('last_name')
        employee.user.email = request.POST.get('email')
        employee.address = request.POST.get('address')
        employee.city = request.POST.get('city')
        employee.state = request.POST.get('state')
        employee.zip_code = request.POST.get('zip_code')
        employee.education_level = request.POST.get('education_level')
        employee.skills = request.POST.get('skills')
        employee.experience = request.POST.get('experience')
        employee.contact_number = request.POST.get('contact_number')
        employee.gender = request.POST.get('gender')

        date_of_birth_str = request.POST.get('date_of_birth')
        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                date_of_birth = None
        else:
            date_of_birth = None

        employee.date_of_birth = date_of_birth

        if 'image' in request.FILES:
            if employee.image:
                default_storage.delete(employee.image.name)
            image_file = request.FILES['image']
            employee.image.save(image_file.name, image_file)

        if 'resume' in request.FILES:
            if employee.resume:
                default_storage.delete(employee.resume.name)
            resume_file = request.FILES['resume']
            employee.resume.save(resume_file.name, resume_file)

        employee.user.save()
        employee.save()
        messages.success(request, 'Profile updated successfully.')

        return redirect('employee_profile')

    context = {
        'employee': employee
    }

    return render(request, 'edit_employee_profile.html', context)


#edit employer profile 


@login_required
def edit_employer_profile(request):
    employer = request.user.employer

    if request.method == 'POST':
        image = request.FILES.get('image')

        employer.company_name = request.POST.get('company_name')
        employer.contact_person_name = request.POST.get('contact_person_name')
        employer.email = request.POST.get('email')
        employer.phone_number = request.POST.get('phone_number')
        employer.address = request.POST.get('address')
        employer.city = request.POST.get('city')
        employer.state = request.POST.get('state')
        employer.zip_code = request.POST.get('zip_code')
        employer.company_description = request.POST.get('company_description')
        employer.website = request.POST.get('website')

        if image:
            employer.image = image

        employer.save()
        messages.success(request,'Profile updated successfully.')

        return redirect('employer_profile')

    context = {
        'employer': employer
    }

    return render(request, 'edit_employer_profile.html', context)

#add category
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        category = Category(name=name, description=description)
        category.save()

        return redirect('category_list')

    return render(request, 'add_category.html')


#show all category


def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category_list.html', context)


#add joblist

@login_required

def create_job_listing(request):
    if request.method == 'POST':
        try:
            employer = Employer.objects.get(user__username=request.user.username)
        except ObjectDoesNotExist:
            return redirect('error_page')

        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        keyword = request.POST.get('keyword')
        vacancies = request.POST.get('vacancies')
        expiry_date_str = request.POST.get('expiry_date')

        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)

        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()

        if expiry_date and expiry_date < timezone.now().date():
            return redirect('error_page')  
        job_listing = JobListing(
            employer=employer,
            title=title,
            category=category,
            description=description,
            requirements=requirements,
            location=location,
            salary=salary,
            keyword=keyword,
            vacancies=vacancies,
            expiry_date=expiry_date
        )
        job_listing.save()
        messages.success(request,'Job Added Success')

        return redirect('created_jobs')

    categories = Category.objects.all()
    keyword_choices = JobListing.KEYWORD_CHOICES
    context = {'categories': categories, 'keyword_choices': keyword_choices}
    return render(request, 'create_job_listing.html', context)

@login_required
def created_jobs(request):
    employer = request.user.employer
    today = timezone.now().date()
    job_listings = JobListing.objects.filter(employer=employer, expiry_date__gte=today)
    context = {'job_listings': job_listings}
    return render(request, 'created_jobs.html', context)


def created_jobs_employee(request):
    current_date = timezone.now().date()

    expired_listings = JobListing.objects.filter(expiry_date__lt=current_date)
    expired_listings.delete()

    job_listings = JobListing.objects.filter(expiry_date__gte=current_date)

    context = {'job_listings': job_listings}
    return render(request, 'created_jobs_employee.html', context)

#update job

def update_job_listing(request, job_listing_id):
    job_listing = get_object_or_404(JobListing, id=job_listing_id, employer=request.user.employer)

    if request.method == 'POST':
        job_listing.title = request.POST.get('title')
        job_listing.category_id = request.POST.get('category')
        job_listing.description = request.POST.get('description')
        job_listing.requirements = request.POST.get('requirements')
        job_listing.location = request.POST.get('location')
        job_listing.salary = request.POST.get('salary')
        job_listing.keyword = request.POST.get('keyword')
        job_listing.vacancies = request.POST.get('vacancies')

        if 'expiry_date' in request.POST:
            expiry_date = request.POST.get('expiry_date')
            try:
                job_listing.expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except ValueError:
                pass

        job_listing.save()
        messages.success(request,'Job Updated Successfully')
        return redirect('created_jobs')

    categories = Category.objects.all()
    keyword_choices = JobListing.KEYWORD_CHOICES
    context = {'job_listing': job_listing, 'categories': categories, 'keyword_choices': keyword_choices}
    return render(request, 'update_job_listing.html', context)


#message 

# @login_required
# def inbox(request):
#     received_messages = Message.objects.filter(recipient=request.user)
#     return render(request, 'inbox.html', {'messages': received_messages})

# @login_required
# def message_detail(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     if not message.is_read:
#         message.is_read = True
#         message.save()
#     return render(request, 'message_detail.html', {'message': message})

# @login_required

# def compose_message(request):
#     if request.method == 'POST':
#         recipient_username = request.POST.get('recipient')
#         recipient = get_object_or_404(User, username=recipient_username)
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')
#         message = Message(sender=request.user, recipient=recipient, subject=subject, body=body)
#         message.save()
#         return redirect('admin_home')
#     return render(request, 'admin_home.html')





#all employee

def employee_list(request):
    employees = Employee.objects.all()

    for employee in employees:
        # Get chat messages between the employee and admin
        chat_messages = ChatMessage.get_chat_between_employer_and_employee(request.user, employee.user)
        chat_messages = chat_messages.order_by('-timestamp')  # Order by timestamp in descending order (latest first)

        # Store the chat messages in a dictionary with employee ID as the key
        employee.chat_messages = chat_messages

        # Get messages sent by the employee to the admin
        employee_sent_messages = ChatMessage.objects.filter(sender=employee.user, recipient=request.user, admin=True)
        employee_sent_messages = employee_sent_messages.order_by('-timestamp')  # Order by timestamp in descending order

        employee.employee_sent_messages = employee_sent_messages

        # Get messages received by the employee from the admin
        employee_received_messages = ChatMessage.objects.filter(sender=request.user, recipient=employee.user, admin=True)
        employee_received_messages = employee_received_messages.order_by('-timestamp')  # Order by timestamp in descending order

        employee.admin_received_messages = employee_received_messages

    admin_received_messages = ChatMessage.objects.filter(recipient=request.user, admin=True)
    admin_received_messages = admin_received_messages.order_by('-timestamp')  # Order by timestamp in descending order

    context = {
        'employees': employees,
        'admin_user': request.user,
        'admin_received_messages': admin_received_messages,
    }

    return render(request, 'employee_list.html', context)



#all employer

def employer_list(request):
    employers = Employer.objects.all()
    current_user = request.user

    for employer in employers:
        admin_messages_sent_by_employer = ChatMessage.objects.filter(
            sender=current_user, recipient=employer.user, admin=True
        )
        admin_messages_received_by_employer = ChatMessage.objects.filter(
            sender=employer.user, recipient=current_user, admin=True
        )

        chat_messages = admin_messages_sent_by_employer | admin_messages_received_by_employer

        employer_messages_sent = ChatMessage.objects.filter(sender=employer.user, recipient=current_user, admin=False)
        employer_messages_received = ChatMessage.objects.filter(sender=current_user, recipient=employer.user, admin=False)

        chat_messages = chat_messages | employer_messages_sent | employer_messages_received

        employer.chat_messages = chat_messages.order_by('timestamp')

        admin_messages_received_by_employer_from_admin = ChatMessage.objects.filter(
            sender__is_superuser=True, recipient=employer.user, admin=True
        )
        employer.admin_messages_received = admin_messages_received_by_employer_from_admin

    admin_messages = ChatMessage.objects.filter(
        Q(recipient=current_user, sender__is_superuser=True) | Q(sender=current_user, recipient__is_superuser=True) | Q(sender__is_superuser=False, recipient=current_user)
    )

    context = {
        'employers': employers,
        'admin_messages': admin_messages,
    }

    return render(request, 'employer_list.html', context)


def delete_employer(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)

    if request.method == 'POST':
        employer.delete()
        return redirect('employer_list')

    context = {
        'employer': employer
    }

    return render(request, 'employer_list.html', context)



from django.db.models import Q

def all_employees(request):
    employer = request.user
    employees = Employee.objects.all()

    for employee in employees:
        sent_messages = ChatMessage.objects.filter(sender=employer, recipient=employee.user)
        received_messages = ChatMessage.objects.filter(sender=employee.user, recipient=employer)
        employee.sent_messages = sent_messages
        employee.received_messages = received_messages

    sent_group_messages = GroupChatMessage.objects.filter(sender=employer)
    received_group_messages = GroupChatMessage.objects.filter(~Q(sender=employer))

    context = {
        'employees': employees,
        'sent_group_messages': sent_group_messages,
        'received_group_messages': received_group_messages
    }

    return render(request, 'all_employees.html', context)


#apply job

def apply_job(request, job_listing_id):
    job_listing = get_object_or_404(JobListing, id=job_listing_id)
    employee = request.user.employee

    if ApplyJob.objects.filter(job_listing=job_listing, employee=employee).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('applied_jobs_employee')

    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')

        application = ApplyJob(job_listing=job_listing, employee=employee, cover_letter=cover_letter, resume=resume)
        application.save()

        messages.success(request, 'Applied Job Successfully')

        return redirect('applied_jobs_employee')

    context = {
        'job_listing': job_listing
    }
    return render(request, 'created_jobs_employee.html', context)



def applied_jobs_employer(request):
    employer = request.user.employer
    applied_jobs = ApplyJob.objects.filter(job_listing__employer=employer)

    context = {
        'applied_jobs': applied_jobs,
    }

    return render(request, 'applied_jobs.html', context)


def applied_jobs_employee(request):
    employee = request.user.employee
    applied_jobs = ApplyJob.objects.filter(employee=employee)

    context = {
        'applied_jobs': applied_jobs
    }

    return render(request, 'applied_jobs_employee.html', context)

#interview schedule 
from django.http import JsonResponse
def schedule_interview(request, job_listing_id, applied_job_id):
    job_listing = get_object_or_404(JobListing, id=job_listing_id)
    applied_job = get_object_or_404(ApplyJob, id=applied_job_id, job_listing=job_listing)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        description = request.POST.get('description')

        interview = InterviewSchedule.objects.create(
            job_listing=job_listing,
            employee=applied_job.employee,
            date=date,
            time=time,
            location=location,
            description=description
        )

        messages.success(request, 'Interview scheduled successfully.')
        return redirect('interview_schedule_employer')

    context = {
        'job_listing': job_listing,
        'applied_job': applied_job
    }
    return render(request, 'schedule_interview.html', context)
#employee  view
def interview_list_employee(request):
    employee = request.user.employee
    interviews = InterviewSchedule.objects.filter(employee=employee)

    context = {
        'interviews': interviews
    }
    return render(request, 'interview_list_employee.html', context)


#employer view
def interview_schedule_employer(request):
    employer = request.user.employer
    interviews = InterviewSchedule.objects.filter(job_listing__employer=employer)

    context = {
        'interviews': interviews
    }
    return render(request, 'interview_schedule_employer.html', context)

#message 
from django.urls import reverse


@login_required

def chat_between_users(request, sender_id, recipient_id):
    if request.method == 'POST':
        message = request.POST.get('message')
        sender = request.user
        recipient = get_object_or_404(User, id=recipient_id)

        chat_message = ChatMessage(sender=sender, recipient=recipient, message=message)
        chat_message.save()
        messages.success(request, 'Message sent successfully.')

        if hasattr(sender, 'employee'):
            return HttpResponseRedirect(reverse('all_employers_list'))
        elif hasattr(sender, 'employer'):
            return HttpResponseRedirect(reverse('all_employees'))

    sender = get_object_or_404(User, id=sender_id)
    recipient = get_object_or_404(User, id=recipient_id)

    sent_messages = ChatMessage.objects.filter(sender=sender, recipient=recipient)
    received_messages = ChatMessage.objects.filter(sender=recipient, recipient=sender)
    chat_messages = sent_messages | received_messages

    if hasattr(request.user, 'employee'):
        template = 'all_employers_list_employee.html'
    elif hasattr(request.user, 'employer'):
        template = 'all_employees.html'

    context = {
        'sender': sender,
        'recipient': recipient,
        'chat_messages': chat_messages,
    }

    return render(request, template, context)


# def send_message_to_all_employees(request):
#     if request.method == 'POST':
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')

#         # Get all employees
#         employees = Employee.objects.all()

#         # Create a message for each employee
#         for employee in employees:
#             message = EmployerMessage.objects.create(employer=request.user.employer, subject=subject, body=body)
#             message.employees.set([employee])  # Set the employees for the message

#         # Redirect or show success message
#         return redirect('employer_home')  # Redirect to the same page
#     else:
#         return render(request, 'all_employees.html')

# def employee_message(request, message_id):
#     message = EmployerMessage.objects.get(id=message_id)

#     if request.method == 'POST':
#         sender = request.user.employee
#         body = request.POST.get('body')

#         # Create a reply message
#         reply_message = EmployerMessage.objects.create(employer=message.employer, subject=message.subject, body=body, employees=sender, parent_message=message)

#         # Additional logic...

#         return redirect('employee_message', message_id=message_id)

#     context = {
#         'message': message
#     }
#     return render(request, 'employee_message.html', context)


# views.py
def all_employers_list(request):
    employers = Employer.objects.all()

    for employer in employers:
        sent_messages = ChatMessage.objects.filter(sender=request.user, recipient=employer.user)
        received_messages = ChatMessage.objects.filter(sender=employer.user, recipient=request.user)
        employer.sent_messages = sent_messages
        employer.received_messages = received_messages

    context = {
        'employers': employers,
    }

    return render(request, 'all_employers_list_employee.html', context)



#search for employee

def job_search(request):
    categories = Category.objects.all()

    keywords = JobListing.KEYWORD_CHOICES

    location = request.GET.get('location')
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword')

    job_listings = JobListing.objects.all()

    if location:
        job_listings = job_listings.filter(location__icontains=location)

    if category_id:
        job_listings = job_listings.filter(category_id=category_id)

    if keyword:
        job_listings = job_listings.filter(keyword=keyword)

    context = {
        'job_listings': job_listings,
        'categories': categories,
        'keywords': keywords,
        'location': location,
        'category_id': category_id,
        'keyword': keyword,
    }

    return render(request, 'job_search.html', context)



#employer

@login_required
def job_search_employer(request):
    categories = Category.objects.all()

    keywords = JobListing.KEYWORD_CHOICES

    location = request.GET.get('location')
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword')

    job_listings = JobListing.objects.filter(employer=request.user.employer)

    if location:
        job_listings = job_listings.filter(location__icontains=location)

    if category_id:
        job_listings = job_listings.filter(category_id=category_id)

    if keyword:
        job_listings = job_listings.filter(keyword=keyword)

    context = {
        'job_listings': job_listings,
        'categories': categories,
        'keywords': keywords,
        'location': location,
        'category_id': category_id,
        'keyword': keyword,
    }

    return render(request, 'job_search_employer.html', context)




# views.py
def employer_job_listings(request, employer_id):
    employer = get_object_or_404(Employer, id=employer_id)
    job_listings = JobListing.objects.filter(employer=employer)

    context = {
        'employer': employer,
        'job_listings': job_listings,
    }

    return render(request, 'employer_job_listings.html', context)



def group_chat(request):
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            sender = request.user
            group_message = GroupChatMessage.objects.create(sender=sender, message=message_text)

            employees = Employee.objects.all()

            for employee in employees:
                chat_message = ChatMessage(sender=sender, recipient=employee.user, message=message_text)
                chat_message.save()

            return redirect('all_employees')

    employees = Employee.objects.all()
    employer = request.user

    # Retrieve the group messages
    group_messages = GroupChatMessage.objects.all()

    # Retrieve the employee chat messages
    chat_messages = ChatMessage.objects.filter(Q(sender=employer) | Q(recipient=employer) | Q(sender__in=employees))

    context = {
        'employees': employees,
        'chat_messages': chat_messages,
        'group_messages': group_messages,  # Include the group messages in the context
    }

    return render(request, 'all_employees.html', context)


#employee chat
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import GroupChatMessage, ChatMessage

@login_required

def employee_chat(request):
    user = request.user
    group_messages = GroupChatMessage.objects.all()

    employers = Employer.objects.all()

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            sender = user
            group_message = GroupChatMessage.objects.create(sender=sender, message=message_text)

            chat_message = ChatMessage(sender=sender, recipient=user, message=message_text)
            chat_message.save()

            admin_chat_message = ChatMessage(sender=user, recipient=sender, message=message_text, admin=True)
            admin_chat_message.save()

            messages.success(request, 'Message sent successfully.')

    context = {
        'user': user,
        'group_messages': group_messages,
        'employers': employers,  
    }

    return render(request, 'employer_chat.html', context)






#all chat for admin and users(html page notification.html)
def notification(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'send':
            message = request.POST.get('message')
            recipient_option = request.POST.get('recipient_option')

            User = get_user_model()
            recipients = None

            if recipient_option == 'employees':
                recipients = User.objects.filter(employee__isnull=False)
            elif recipient_option == 'employers':
                recipients = User.objects.filter(employer__isnull=False)

            if recipients is not None:
                for recipient in recipients:
                    if recipient != request.user:  
                        sent_message = ChatMessage(sender=request.user, recipient=recipient, message=message, admin=False)
                        sent_message.save()

                        notification = Notification(recipient=recipient, employer=None, message=message, reply_to=sent_message)
                        notification.save()

            messages.success(request, 'Message sent successfully.')

            return redirect('notification')

    received_messages = ChatMessage.objects.filter(recipient=request.user, admin=False)

    sent_messages = ChatMessage.objects.filter(sender=request.user, admin=False)

    all_messages = (received_messages | sent_messages).order_by('timestamp')

    context = {
        'all_messages': all_messages,
    }

    return render(request, 'notification.html', context)




@login_required
def job_listings_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    employer = request.user.employer  # Assuming the currently logged-in user is an employer
    job_listings = JobListing.objects.filter(category=category, employer=employer)

    context = {
        'category': category,
        'job_listings': job_listings
    }

    return render(request, 'job_listings_by_category.html', context)






#chat betweeen admin and users(employee_list views.py for employees chat employers_list for employers chat)
def private_chat(request, recipient_id):
    recipient = get_object_or_404(get_user_model(), id=recipient_id)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            sender = request.user

            if sender.is_superuser:
                chat_message = ChatMessage(sender=sender, recipient=recipient, message=message_text, admin=True)
            else:
                admin_user = User.objects.filter(is_superuser=True).first()
                chat_message = ChatMessage(sender=sender, recipient=admin_user, message=message_text, admin=False)

            chat_message.save()

    user_to_user_messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient, admin=False)
    user_to_admin_messages = ChatMessage.objects.filter(sender=recipient, recipient=request.user, admin=True)
    admin_to_user_messages = ChatMessage.objects.filter(sender=request.user, recipient=recipient, admin=True)

    chat_messages = user_to_user_messages | user_to_admin_messages | admin_to_user_messages
    chat_messages = chat_messages.order_by('timestamp')

    context = {
        'recipient': recipient,
        'chat_messages': chat_messages,
    }

    if hasattr(request.user, 'employee'):
        return render(request, 'admin_messages.html', context)
    elif hasattr(request.user, 'employer'):
        return render(request, 'admin_messages_employer.html', context)
    else:
        return redirect('employer_list')
    
    
# def chat_between_admin_and_user(request, user_id):
#     user = request.user
#     recipient = get_object_or_404(get_user_model(), id=user_id)

#     if request.method == 'POST':
#         message = request.POST.get('message')

#         if user.is_superuser:
#             chat_message = ChatMessage(sender=user, recipient=recipient, message=message, admin=True)
#         else:
#             chat_message = ChatMessage(sender=user, recipient=recipient, message=message, admin=False)

#         chat_message.save()

#         if hasattr(request.user, 'employee'):
#             return redirect('admin_messages')
#         elif hasattr(request.user, 'employer'):
#             return redirect('admin_messages_employer')

#     user_to_user_messages = ChatMessage.objects.filter(sender=user, recipient=recipient, admin=False)
#     user_to_admin_messages = ChatMessage.objects.filter(sender=user, recipient=recipient, admin=True)
#     admin_to_user_messages = ChatMessage.objects.filter(sender=recipient, recipient=user, admin=True)

#     chat_messages = user_to_user_messages | user_to_admin_messages | admin_to_user_messages

#     context = {
#         'sender': user,
#         'recipient': recipient,
#         'chat_messages': chat_messages,
#     }

#     if hasattr(request.user, 'employee'):
#         return render(request, 'admin_messages.html', context)
#     elif hasattr(request.user, 'employer'):
#         return render(request, 'admin_messages_employer.html', context)



#show messages employee to admin(html page admin_messages.html)
def admin_messages(request):
    user = request.user

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            if user.is_superuser:
                chat_message = ChatMessage(sender=user, recipient=user, message=message_text, admin=True)
            else:
                admin_user = User.objects.filter(is_superuser=True).first()
                chat_message = ChatMessage(sender=user, recipient=admin_user, message=message_text, admin=False)

            chat_message.save()

            print("Message saved:", chat_message.message)

            messages.success(request, 'Message sent successfully.')
            return redirect('employee_home')

    admin_user = User.objects.filter(is_superuser=True).first()
    admin_messages = ChatMessage.objects.filter(
        Q(recipient=user, sender=admin_user) |  
        Q(sender=user, recipient=admin_user, admin=False)  
    )

    context = {
        'admin_messages': admin_messages,
        'recipient': user,
        'admin_user': admin_user,
    }

    return render(request, 'admin_messages.html', context)



#employers to admin messages(html page admin_messages_employers.html)
def admin_messages_employer(request):
    user = request.user

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            if user.is_superuser:
                chat_message = ChatMessage(sender=user, recipient=user, message=message_text, admin=True)
            else:
                admin_user = User.objects.filter(is_superuser=True).first()
                chat_message = ChatMessage(sender=user, recipient=admin_user, message=message_text, admin=False)

            chat_message.save()


            return redirect('admin_messages_employer')

    admin_user = User.objects.filter(is_superuser=True).first()
    admin_messages = ChatMessage.objects.filter(
        Q(recipient=user, sender=admin_user) | 
        Q(sender=user, recipient=admin_user, admin=False)  
    )

    context = {
        'admin_messages': admin_messages,
        'recipient': user,
    }

    return render(request, 'admin_messages_employer.html', context)

@login_required

def job_search_admin(request):
    categories = Category.objects.all()

    keywords = JobListing.KEYWORD_CHOICES

    location = request.GET.get('location')
    category_id = request.GET.get('category')
    keyword = request.GET.get('keyword')

    job_listings = JobListing.objects.all()

    if location:
        job_listings = job_listings.filter(location__icontains=location)

    if category_id:
        job_listings = job_listings.filter(category_id=category_id)

    if keyword:
        job_listings = job_listings.filter(keyword=keyword)

    context = {
        'job_listings': job_listings,
        'categories': categories,
        'keywords': keywords,
        'location': location,
        'category_id': category_id,
        'keyword': keyword,
    }

    return render(request, 'job_search_admin.html', context)


@login_required
def job_list_admin(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    job_listings = JobListing.objects.filter(category=category)

    context = {
        'category': category,
        'job_listings': job_listings
    }

    return render(request, 'job_list_admin.html', context)



def job_listings_by_category_employee(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    job_listings = JobListing.objects.filter(category=category)

    context = {
        'category': category,
        'job_listings': job_listings
    }

    return render(request, 'job_listings_by_category_employee.html', context)



def add_category_employer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        category = Category(name=name, description=description)
        category.save()

        return redirect('employer_home')

    return render(request, 'add_category_employer.html')


