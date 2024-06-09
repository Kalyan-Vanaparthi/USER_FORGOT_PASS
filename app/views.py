from django.shortcuts import render
from app.forms import *

from django.http import HttpResponse,HttpResponseRedirect
from app.models import *

def home(request):
    if request.session.get("username"):
       
        d = {"username": request.session["username"]} 
        return render(request, "home.html", d)       

    return render(request, "home.html")

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
def user_login(request):
    if request.method == "POST":
        username = request.POST["un"]
        password = request.POST["pw"]
        if password  == "" or username == "":
            return HttpResponseRedirect(reverse("forgot"))
        
        
            
        AUTHENTICATED_USER_OBJ = authenticate(username = username, password = password)
        if AUTHENTICATED_USER_OBJ and AUTHENTICATED_USER_OBJ.is_active:
            login(request,AUTHENTICATED_USER_OBJ)
            request.session.update({"username":username})
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("<marquee> invalid creadentials </marquee>")



    return render(request, "login.html")

from django.contrib.auth.decorators import login_required

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

from django.core.mail import send_mail
def reg(request):
    EMPTY_USER_FORM_DATA = User_Form()
    EMPTY_PROFILE_FORM_DATA = Profile_Form()
    d = {"EMPTY_USER_FORM_DATA": EMPTY_USER_FORM_DATA, "EMPTY_PROFILE_FORM_DATA": EMPTY_PROFILE_FORM_DATA}
    if request.method == "POST" and request.FILES:
        NON_MODIFIED_COLLECTED_USER_FORM_DATA = User_Form(request.POST)
        NON_MODIFIED_COLLECTED_PROFILE_FORM_DATA = Profile_Form(request.POST, request.FILES)

        if NON_MODIFIED_COLLECTED_USER_FORM_DATA.is_valid()  and NON_MODIFIED_COLLECTED_PROFILE_FORM_DATA.is_valid() :

            MODIFIEDABLE_COLLECTED_USER_FORM_DATA = NON_MODIFIED_COLLECTED_USER_FORM_DATA.save(commit=False)
            pw =  NON_MODIFIED_COLLECTED_USER_FORM_DATA.cleaned_data["password"]
            
            
        
            MODIFIEDABLE_COLLECTED_USER_FORM_DATA.set_password(pw)
            MODIFIEDABLE_COLLECTED_USER_FORM_DATA.save()

            MODIFIEDABLE_COLLECTED_PROFILE_FORM_DATA = NON_MODIFIED_COLLECTED_PROFILE_FORM_DATA.save(commit=False)
            MODIFIEDABLE_COLLECTED_PROFILE_FORM_DATA.username = MODIFIEDABLE_COLLECTED_USER_FORM_DATA
            MODIFIEDABLE_COLLECTED_PROFILE_FORM_DATA.save()

            send_mail("REGISTRATION PRPCESS", 
                      f'''THANKS FOR REGISTRATION
                      Your Login creadential are 
                      username : {MODIFIEDABLE_COLLECTED_USER_FORM_DATA.username}
                      password is : {pw}''',
                      "kalyanromeo358@gmail.com",
                      [ MODIFIEDABLE_COLLECTED_USER_FORM_DATA.email],
                      fail_silently=False,)
            un =  NON_MODIFIED_COLLECTED_USER_FORM_DATA.cleaned_data
            print(un)
            d={"key":"user created successfully ☠️"}
            return render(request, "home.html",d)
            #return HttpResponse("user Created ")
        else:
            if request.session.get("username"):
                return render(request, "<h1><center><mark>Already User Existed Mawa<mark><center></h1>")
            else:
                return HttpResponse("Inavlid Creadentials")

            # #if NON_MODIFIED_COLLECTED_USER_FORM_DATA.cleaned_data.get("username")  == None:
            #     return HttpResponse("<h1><center><mark>Already User Existed Mawa<mark><center></h1>")
            # else:
            #     return HttpResponse("Inavlid Creadentials")
    return render(request, "reg.html",d)

@login_required
def profile_details(request):
    un = request.session.get("username")
    USER_OBJ = User.objects.get(username = un)
    PROFILE_OBJ = Profile.objects.get(username = USER_OBJ)
    return render(request, "profile_display.html", {"USER_OBJ": USER_OBJ,"PROFILE_OBJ": PROFILE_OBJ })

@login_required
def change_password(request):
    if request.method == "POST": 
        new_pw = request.POST["pw"]
        un = request.session.get("username")
        UO = User.objects.get(username = un)
        UO.set_password(new_pw)
        UO.save()
        return HttpResponse("password changed")
    else:
        return render(request, "change_password.html")
import random
def re_enter_pass(request):
    if request.method == "POST":
        pw = request.POST["pw"]
        User_obj2 = User.objects.get(username = un)
        User_obj2.set_password(pw)
        User_obj2.save()
        return HttpResponseRedirect(reverse("user_login"))

    return render(request, "re_enter_pass.html")
    

def otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        if int(otp) == random_number:
            return HttpResponseRedirect(reverse("re_enter_pass"))
            
        else:
            
            return HttpResponse("otp not matched")
    return render(request, "otp.html")

def forgot(request):
    if request.method == "POST":
        global random_number
        random_number = random.randint(10000, 99999)
        
        global un
        un = request.POST["un"]
        User_obj = User.objects.get(username = un)
        
        user_emaill = User_obj.email
        send_mail("FORGOT PASS WORD",
                  f'your Secreat code is {random_number}',
                  "kalyanromeo358@gmail.com",
                  [f"{user_emaill}"],
                  fail_silently=False)
        return HttpResponseRedirect(reverse('otp'))
                     
    return render(request, "forgot.html")