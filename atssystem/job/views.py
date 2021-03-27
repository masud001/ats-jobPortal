from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return render(request, 'index.html')

# admin login page function


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

# admin home page function


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


# admin shows user
def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = JobSeecker.objects.all()
    d = {'data': data}
    print(d)
    return render(request, 'view_users.html', d)
# admin shows user


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = JobSeecker.objects.get(id=pid)
    data.delete()
    return redirect('view_users')


# job seecker sign up function


def user_signup(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(
                first_name=f, last_name=l, username=e, password=p)
            JobSeecker.objects.create(
                user=user, mobile=con, image=i, gender=gen, type="JobSeecker")
            error = "no"
        except:
            error = "yes"
    d = {"error": error}
    return render(request, 'user_signup.html', d)


# job seecker log in function
def user_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['usermail']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        print(user)
        # try:
        #     if user.jobseecker_set.last().type == "Student":
        #         login(request, user)
        #         error = "no"
        #     else:
        #         print("login UN success!")
        # except:
        #     error = "yes"

        if user:
            try:
                users = JobSeecker.objects.get(user=user)
                if users.type == "JobSeecker":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"

    d = {'error': error}
    return render(request, 'user_login.html', d)

# job seecker home page after log in


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'user_home.html')


# job Seecker logout and redirect to home page.
def Logout(request):
    logout(request)
    return redirect('index')


# HR/Recruiter signup function
def recruiter_signup(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(
                first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(
                user=user, mobile=con, image=i, gender=gen, company=company, type="Recruiter", status="Pending")
            error = "no"
        except:
            error = "yes"
    d = {"error": error}
    return render(request, 'recruiter_signup.html', d)


# HR/Recruiter log in function
def recruiter_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['hremail']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        # print(user)
        # try:
        #     if user.recruiter_set.last().type == "Recruiter" and user.recruiter_set.last().status != "Pending":
        #         login(request, user)
        #         error = "no"
        #     else:
        #         print("loginsuccess!")
        # except:
        #     error = "yes"

        if user:
            try:
                users = Recruiter.objects.get(user=user)
                if users.type == "Recruiter" and users.status != "Pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"

    d = {'error': error}
    return render(request, 'recruiter_login.html', d)


# HR home page after log in
def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request, 'recruiter_home.html')
