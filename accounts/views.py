from django.shortcuts import render,redirect , reverse
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User , auth
from hos.models import doctors , appointments, patient , receptionist
from hos.models import receptionist
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from django.urls import reverse
# Create your views here.
#-----------------------------------------LOGIN-----------------------------------------
def index(request):
    if request.method == 'POST':
        type=request.POST['type']
        username = request.POST['email']
        passw = request.POST['password']
        print(type)
        user= auth.authenticate(username=username ,password=passw)
        print('authenticated',user is not None)
        if type =='patient' and user is not None:
            if patient.objects.filter(patient_id=username).exists():
                print("user is not none")
                auth.login(request,user)
                return redirect('/patient/')
            else:
                messages.info(request,'Patient Does Not Exist')
                return redirect('/accounts/login')
        elif type =='doctor' and user is not None:
            if doctors.objects.filter(doctor_id=username):
                print("sdf")
                auth.login(request,user)
                return redirect('/doctor')
            else:
                messages.info(request,'Doctor Does Not Exist')
                return redirect('/accounts/login')
        elif type=="receptionist" and user is not None :
            if receptionist.objects.filter(recep_id=username):
                auth.login(request,user)
                return redirect('/receptionist')
            else:
                messages.info(request,'Receptionist Does Not Exist')
                return redirect('/accounts/login')
        else:
            print('else')
            messages.info(request,'invalid credentials') 
            return redirect('/accounts/login')

    else:
        return render(request , 'login.html')




#--------------------------------------REGISTRATION-------------------------------------------    



def logout(request):
    print('logout me')
    auth.logout(request)
    return redirect('/')

def patient_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_nam = request.POST['last_name']
        username = request.POST['email']
        password1 = request.POST['password']
        password = request.POST['password1']
        phn_no = request.POST['phn_no']
        gender = request.POST['gender']
        age=request.POST['age']
        type= request.POST['type']
      
        
        #lol.append(username)
        if(password == password1):
            print("password match")
            if(User.objects.filter(username=username).exists()):
                messages.info(request,'E-Mail Exists try different one..!!')
                return redirect('/accounts/register')
            else:
                user = User.objects.create_user(username=username , password=password,first_name=first_name , last_name=last_nam)
                user.save();
              
                if type=="patient":
                    patient(patient_id=username,first_name=first_name,last_name=last_nam,phone_no=phn_no,gender=gender,age=age).save()
                    return redirect('/accounts/login') 
                elif type=="doctor":
                    doctors( doctor_id = username,
                        name = first_name + last_nam,
                        department = 'none',
                        gender = gender,
                        status = 1).save()

                    return redirect('/accounts/login')
                                
               
               
        else:
            messages.info(request,'password must match')
            return redirect('/accounts/register')


    return render(request,'register.html')







































