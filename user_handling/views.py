from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import User
from django.contrib.auth.models import auth
from accounts.models import Profile
from .forms import *
from datetime import datetime, date

# Create your views here.
def register(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		fname = request.POST['fname']
		fname = fname.capitalize()
		lname = request.POST['lname']
		lname = lname.capitalize()
		user_type = request.POST.get('user_type')
		if password1 == password2:
			if not User.objects.filter(username=username).exists():
				user = User.objects.create_user(username=username, password=password1, first_name=fname, last_name=lname, email=email, staff_status=user_type)
				p = Profile.objects.create(user=user)
				p.save()
				user.save()
				messages.success(request, f'{fname} your account created successfully. Now you can login here.')
				return redirect('login')
			else:
				messages.info(request, f'Username {username} already taken')
				return render(request, 'user_handling/register.html', {'fname': fname, 'lname': lname})
		else:
			messages.info(request, 'Both password not match')
			context = {
				'fname': fname, 
				'lname': lname,
				'uname': username,
				'email': email
			}
			return render(request, 'user_handling/register.html', context)

	elif request.user.is_authenticated:
		return redirect('home')

	else:
		return render(request, 'user_handling/register.html', {'title': 'Register'})

def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request, f'Welcome {user.first_name} {user.last_name}')
			return redirect('profile')
		else:
			messages.info(request, 'Invalid credentials')
			return redirect('login')

	elif request.user.is_authenticated:
		return redirect('home')

	else:
		return render(request, 'user_handling/login.html')

def profile(request):
	if not request.user.is_authenticated:
		return redirect('register')
	else:
		latest_application = ApplicationForLeave.objects.filter(employee=request.user).order_by('-date_posted')
		context = {
			'latest_application': latest_application,
		}
		return render(request, 'user_handling/profile.html', context)

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		messages.success(request, f'Loggout successfully')
		return redirect('login')
	else:
		return redirect('register')

def leave_application(request, usrname):
	if not request.user.is_authenticated:
		return redirect('register')
	
	elif request.method == "POST":
		description = request.POST.get('description')
		start_date = request.POST.get('start_date').replace('-', '/').split('/')
		new_start_date = start_date[2] + '/' + start_date[1] + '/' + start_date[0]
		start_date = datetime.strptime(new_start_date, '%d/%m/%Y')

		end_date = request.POST.get('end_date').replace('-', '/').split('/')
		new_end_date = end_date[2] + '/' + end_date[1] + '/' + end_date[0]
		end_date = datetime.strptime(new_end_date, '%d/%m/%Y')

		number_of_leaves = end_date - start_date
		number_of_leaves = number_of_leaves.days

		user = User.objects.get(username=usrname)
		
		if ApplicationForLeave.objects.filter(employee=user).exists():
			latest_app = ApplicationForLeave.objects.filter(employee=user).order_by('-id')[0]
			now = date.today()
			allowed = False
			if latest_app.end_date < now:
				allowed = True

			if user.leave_pending > 0 and number_of_leaves <= user.leave_pending and allowed:
				leave_available = user.leave_pending
				application = ApplicationForLeave(
						employee = user,
						start_date = start_date,
						end_date = end_date,
						description = description,
					)
				application.save()
				messages.success(request, 'Application is submitted. Now manager will do whatever he wants to do.')
				return redirect('profile')

			else:
				messages.info(request, 'You are not eligible for this. Contact manger ASAP')
				return redirect('profile')
		
		else:
			if number_of_leaves <= user.leave_pending:
				application = ApplicationForLeave(
						employee = user,
						start_date = start_date,
						end_date = end_date,
						description = description,
					)
				
				application.save()
				messages.success(request, 'Application is submitted. Now manager will do whatever he wants to do.')
				return redirect('profile')
			else:
				messages.info(request, 'You are not eligible for this')
				return redirect('profile')


	else:
		leave_form = ApplicationForLeaveForm()
		return render(request, 'user_handling/leave_application.html')

def employee_dashborad(request):
	if request.user.staff_status == 'employee':
		
		all_applications = ApplicationForLeave.objects.filter(employee=request.user).all()
		context = {
			'all_applications': all_applications,
			'title': 'Dashboard',
		}
		return render(request, 'user_handling/emp_dashboard.html', context)
	else:
		return redirect('home')

def home(request):
	return render(request, 'user_handling/home.html')

def manager_dashboard(request):
	if request.user.staff_status == 'manager':
		
		all_applications = ApplicationForLeave.objects.all().order_by('-date_posted')
		context = {
			'all_applications': all_applications,
			'title': 'Dashboard',
		}
		return render(request, 'user_handling/manager_dashboard.html', context)
	else:
		return redirect('home')

def handle_app_status(request, id):
	if not request.user.is_authenticated:
		return redirect('home')
	elif request.method == "POST":
		status = request.POST.get('status')
		app = ApplicationForLeave.objects.get(id=id)
		if status == 'approved':
			user = User.objects.get(username=app.employee)
			app.application_status = status
			leave_pending = user.leave_pending
			number_of_leaves = app.end_date - app.start_date
			user.leave_pending = leave_pending - number_of_leaves.days
			print(user.leave_pending)
			user.save()
			app.save()
			return redirect('manager_dashboard')

		app = ApplicationForLeave.objects.get(id=id)
		app.application_status = status
		app.save()
		return redirect('manager_dashboard')
	else:
		return redirect('manager_dashboard')

def admin_dashboard(request):
	if request.user.staff_status != 'employee' and request.user.staff_status != 'manager':
		
		all_applications = ApplicationForLeave.objects.all()
		context = {
			'all_applications': all_applications,
		}
		return render(request, 'user_handling/admin_dashboard.html', context)
	else:
		return redirect('home')
