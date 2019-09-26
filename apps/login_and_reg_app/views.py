from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.utils.dateparse import parse_date
from .models import User
from django.contrib import messages # line added during the implementation of validation .
import bcrypt 


def index(request):
    request.session.flush()
    if request.method == "GET":
        return render(request, "login_and_reg_app/index.html")

    if request.method == "POST":
        return render(request, "login_and_reg_app/index.html")

# On POST: Processing view- no rendering of html
# On GET: Render the html page
def register(request):
    if request.method == "GET":
        return render(request, "login_and_reg_app/index.html")

    elif request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
        else:
            #if passwords match:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash
            print(pw_hash)
            user = User.objects.create(last_name=request.POST['last_name'], first_name=request.POST['first_name'], email=request.POST['email'], password_hash=pw_hash)
            #----- MODIFY NEXT LINE TO REUSE -----
            request.session['current_user']= user.email
            request.session['user']=user.first_name
            request.session['user_id'] = user.id
            return redirect("/success")  # never render on a post, always redirect!
        return redirect('/register')

def success(request):
    try:
        if request.session['current_user'] == "":
            return redirect('/')
        else:
            return render(request, "login_and_reg_app/success.html")
    except:
        return redirect('/')


def validate_login(request):
    request.session.flush()
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), user.password_hash.encode()):
                print("password match")
                request.session['current_user']=user.email
                request.session['user']=user.first_name
                request.session['user_id'] = user.id
                return redirect("/success") 
            else:
                print("failed password")
                messages.error(request, "Wrong password was provided")
                return redirect('/register')
        except:
            print ("user not found")
            messages.error(request, "Username not found")
            return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')



# # Transacional view- no rendering of html
# def login(request):
#     user = User.objects.filter(email=request.POST['email'])
#     if user:  # note that we take advantage of truthiness here: an empty list will return false
#         logged_user = user[0]
#         if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
#             request.session['userid'] = logged_user.id
#             return redirect('/success')
#     return redirect("/")


