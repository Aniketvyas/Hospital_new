from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse ,JsonResponse
from .models import appointments , doctors , patient , receptionist
from django.contrib.auth.models import User , auth 
from django.core.mail import send_mail
from django.conf import settings
import random 
import datetime as dt
from datetime import *
from django.contrib import messages
import json
from django.core import serializers
from django.conf import settings


# Importing Required Module
from reportlab.pdfgen import canvas
# Creating Canvas
# Imported for backwards compatibility and for the sake
# of a cleaner namespace. These symbols used to be in
# django/core/mail.py before the introduction of email
# backends and the subsequent reorganization (See #10355)





#from datetime import datetime

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    print(request,"hell" ,id)
    return render(request,'about.html')

def services(request):
    print(request,"hell" ,id)
    return render(request,'services.html')
def appointment(request):
    return render(request,'appointment.html')
def lab(request):
    return render(request,'lab_reports.html')
def blood(request):
    return render(request,'blood_availability.html')
def medical(request):
    return render(request,'medical_certificate.html')
def contact(request):
    return render(request,'contact.html')


def red(request,id):
    print(request,"hello",id)
    if id==1:
        return redirect('/')
    elif id==2:
        #return HttpResponse("hello")
        return redirect('/about')
    elif id==3:
        return redirect('/services')
    elif id==4:
        return redirect('/appointment')
    elif id==5:
        return redirect('/lab')
    elif id==6:
        return redirect('/blood')
    elif id==7:
        return redirect('/medical')
    elif id==8:
        return redirect('/contact')
   
    elif id==9:
        return render(request,'receptionist.html')
   
def index1(request):
    appointment = appointments.objects.all().count()
    docto = doctors.objects.all().count()
    return render(request,'index.html',{'appointment':appointment,'docto':docto})



def book(request):
    if request.method == 'POST':
        app_id=random.randint(1000,9999)
        name = request.POST['name']
        age = request.POST['age']
        location= request.POST['location']
        pincode = request.POST['pincode']
        a = request.POST['email']
        gender = request.POST['gender']
        slot_date = request.POST['date']
        doctor_name=request.POST['doc_name']
        request.session['doctor_name']=doctor_name
        request.session['slot_date']=slot_date
        request.session['patient_appointment_id']=app_id
        datetimeobject= datetime.strptime(slot_date,'%d-%m-%Y')
        slot_date = datetimeobject.strftime('%Y-%m-%d')
        c_date = dt.datetime.now().strftime('%d-%m-%Y')
        c_date= datetime.strptime(c_date,'%d-%m-%Y')
        now = datetime.now()
        doc_id=""
        print("else me")
        print(a,type(a))

        if gender in ['m','f','M','F'] and datetimeobject>=c_date:
            slot_date = datetimeobject.strftime('%Y-%m-%d')
            c_date = dt.datetime.now().strftime('%Y-%m-%d')
            print(doc_id)
            db=appointments(
                doctor_id=doctors.objects.get(doctor_id=doctor_name),
                patient_appointment_id=app_id,
                patient_email = patient.objects.get(patient_id=a),
                patient_name = name,
                patient_age=age,
                patient_gender=gender,
                slot_date=slot_date,
                created_at=c_date,
                udated_at=c_date,
                status="pending")
            print("migration")
            db.save()
            print("db saved")
                
            return redirect("patient/timeslot/50",{'doc':doctor_name})
                        #counter=0

            #send_mail=(subject,message,from_email,to_list,fail_silently=True)
        else:
            docs= doctors.objects.all()   
            print(docs,gender , datetimeobject,c_date) 
            messages.info(request , "invalid credentials")
            return render(request,'booking.html' , {'docs':docs})
            
   

        #send_mail=(subject,message,from_email,to_list)
      
    else:   
        docs= doctors.objects.all()   
        print(docs)  
        return render(request,'booking.html', {'docs' : docs})

def locate(request):
    if request.method =="POST":
        city = request.POST['city']
        code = request.POST['pincode']
        docs = doctors.objects.filter(location=city,pincode=code)
        return render(request,'dashboard_all.html',{'docs':docs,'doctors':1})
    else:
        return render(request,'dashboard_all.html')

def track(request):
    p = patient.objects.filter(id=request.user)
    if p.exists() :
        return redirect('/patient')
    else:
        messages.error(request,'You Must Login to continue')
        return redirect('/accounts/login')

    

def timeslot(request,id):
    print(id)
    docs = request.session.get('doctor_name')
    da = request.session.get('slot_date')
    id1 = request.session.get('patient_appointment_id')
    print("id1",docs)
    datetimeobject= datetime.strptime(da,'%d-%m-%Y')
    da = datetimeobject.strftime('%Y-%m-%d')

    doc = doctors.objects.filter(doctor_id=docs)
    for i in doc:
        x = i.id
    time1 = dt.time(11,00,00)
    time = dt.time(2,00,00)
    time.strftime("%H-%M-%S")
    u = request.user.username
    print("u",u)
    if id:
        if id==1:
            time = dt.time(9,1,00)
            time = time.strftime("%H:%M:%S")
            print(time)
            print(time,type(time))
            if appointments.objects.filter(doctor_id=x,slot_date=da,slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                print("user",u)
                if patient.objects.filter(patient_id=u):
                    return redirect('/patient')
                elif receptionist.objects.filter(recep_id=u):
                    return redirect('/receptionist')
                else:
                    return redirect('/')
        elif id==2:
            time = dt.time(9, 15, 00)
            time.strftime("%H-%M-%S")
            print(time)
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u):
                    return redirect('/patient')
                    
                else:
                   return redirect('/receptionist')
        elif id==3:
            time = dt.time(9,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                print("entry Done")
                if patient.objects.filter(patient_id=u):
                    return redirect('/patient')
                else:
                    return redirect('/receptionist')
        elif id==4:
            time = dt.time(9,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==5:
            time = dt.time(10,00,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==6:
            time = dt.time(10,15,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==7:
            time = dt.time(10,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da,slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==8:
            time = dt.time(10,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==9:
            time = dt.time(11,00,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da,slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==10:
            time = dt.time(11,15,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==11:
            time = dt.time(11,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da,slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==12:
            time = dt.time(11,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==13:
            time = dt.time(13,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==14:
            time = dt.time(13,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==15:
            time = dt.time(14,00,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==16:
            time = dt.time(14,15,00)
            time.strftime("%H-%M-%S")
            print(time)

            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==17:
            time = dt.time(14,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==18:
            time = dt.time(14,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id == 19:
            time = dt.time(15,00,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                print("if")
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                print("esle")
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==20:
            time = dt.time(15,15,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==21:
            time = dt.time(15,30,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==22:
            time = dt.time(15,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==23:
            time = dt.time(17,00,00)
            time.strftime("%H-%M-%S")
            print("time",time)
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==24:
            time = dt.time(17,15,00)
            time.strftime("%H-%M-%S")
            print(time)
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id ==25:
            time = dt.time(17,30,00)
            time.strftime("%H-%M-%S")
            print(time)
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==26:
            time = dt.time(17,45,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==27:
            time = dt.time(18,15,00)
            time.strftime("%H-%M-%S")
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==28:
            time = dt.time(18,30,00)
            time.strftime("%H-%M-%S")
            print(time)
            if appointments.objects.filter(doctor_id=x , slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        elif id==29:
            time = dt.time(18,45,00)
            time.strftime("%H-%M-%S")
            print(time)
            if appointments.objects.filter(doctor_id=x,slot_date=da , slot_time=time).exists():
                messages.info(request,'time is already taken')
                return redirect("/patient/timeslot/50")
            else:
                appointments.objects.filter(patient_appointment_id = id1).update(slot_time=time,status="pending")
                if patient.objects.filter(patient_id=u).exists():
                    return redirect('/patient')
             
                else:
                    return redirect('/receptionist')
        else:
            return render(request,'timeslot.html')



def dashboard(request):
    return render(request,'dashboard_all.html')


def patient_dash(request):
    docs = doctors.objects.all()
    u=request.user.username     
    print(u)
    previous = appointments.objects.filter(patient_email=patient.objects.get(patient_id=u)).order_by('-created_at')
    print(previous)
    return render(request,'dashboard_all.html',{'docs':docs,'appointment':previous,'patients':1})

def prescription(request,id):
    if id:
        print(id)
        pres = appointments.objects.filter(patient_appointment_id=id)
    return render(request,'view_prescription.html',{'pres':pres,})


#------------------------------------PATIENT DASHBOARD----------------------------------
def receptionists(request):
    pending = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="pending").order_by('-created_at')
    done = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="done")
    print("fdhygfd",pending)
    appointment = appointments.objects.all()
    print(appointment)
    count = appointments.objects.filter(slot_date=dt.datetime.now().date()).count()
    don = appointments.objects.filter(status="done",slot_date=dt.datetime.now().date()).count()
    pendings = appointments.objects.filter(status="pending").count()
    total = appointments.objects.filter(status='done').count()
    
    context={'pending':pending,
    'done':done,
    'receptionist':1,
    'count':count,
    'don':don,
    'total':total,
    'pendings':pendings,
    'docs':doctors.objects.all()
    }
    return render(request,'dashboard_all.html',context)



def requestUpdate(request):
    if request.method == 'POST':
        app_id= request.POST['patient_ID']
        name = request.POST['name']
        age = request.POST['age']
        a = request.POST['email']
        gender = request.POST['gender']
        slot_date = request.POST['date']
        doctor_name=request.POST['doc_name']
        request.session['doctor_name']=doctor_name
        request.session['slot_date']=slot_date
        request.session['patient_appointment_id']=app_id
        datetimeobject= datetime.strptime(slot_date,'%d-%m-%Y')
        slot_date = datetimeobject.strftime('%Y-%m-%d')
        c_date = dt.datetime.now().strftime('%d-%m-%Y')
        c_date= datetime.strptime(c_date,'%d-%m-%Y')
        now = datetime.now()
        if gender in ['m','f','M','F'] and datetimeobject>=c_date:
            slot_date = datetimeobject.strftime('%Y-%m-%d')
            c_date = dt.datetime.now().strftime('%Y-%m-%d')
            db=appointments.objects.filter(patient_appointment_id=app_id).update(
                doctor_id=doctors.objects.get(doctor_id=doctor_name),
                patient_appointment_id=app_id,
                patient_email = patient.objects.get(patient_id=a),
                patient_name = name,
                patient_age=age,
                patient_gender=gender,
                slot_date=slot_date,
                udated_at=dt.datetime.now().date(),
                status="pending")
            return redirect("/patient/timeslot/50",{'doc':doctor_name})
                        #counter=0

            #send_mail=(subject,message,from_email,to_list,fail_silently=True)
        else:
            docs= doctors.objects.all()   
            print(docs,gender , datetimeobject,c_date) 
            messages.info(request , "invalid credentials")
            return render(request,'booking.html' , {'docs':docs})
            




def requestDelete(request,id):
    appointments.objects.filter(patient_appointment_id=id).delete()
    print("Request deleted succcessfully")
    return redirect('/receptionist')
    


def addPatient(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['email']
        password1 = request.POST['password']
        password = request.POST['password1']
        phn_no = request.POST['phone']
        gender = request.POST['gender']
        age=request.POST['age']
        total = request.POST['total']
        outstanding = request.POST['outstanding']
        paid= request.POST['paid']

        if(password == password1):
            print("password match")
            if(User.objects.filter(username=username).exists()):
                messages.info(request,'E-Mail Exists try different one..!!')
                return redirect('/receptionist')
            else:
                user = User.objects.create_user(username=username , password=password)
                user.save();
                patient(patient_id=username,first_name=name,phone_no=phn_no,gender=gender,age=age).save()
                a= patient.objects.get(patient_id=username)
                individual_outstandings(
                    patient_id=a,updated_on=dt.datetime.now().date(),outstanding=outstanding,paid=paid,amount=total,created_on=dt.datetime.now().date()).save()
                return redirect('/receptionist')
        else:
            message.error(request,"password didn't match")
              
                


#------------DOCTOR DASHBOARD ___________________________

def doc_dash(request):
    appointment = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="pending")
    appointment_done = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="done")
    count = appointments.objects.filter(slot_date=dt.datetime.now().date()).count()
    done = appointments.objects.filter(status="done",slot_date=dt.datetime.now().date()).count()
    pending = appointments.objects.filter(status="pending").count()
    total = appointments.objects.filter(status='done').count()
    print(appointment)
    context={'doctors':1,
    'apps':appointment,
    'count':count,
    "done":done,
    'completed':appointment_done,
    'pending':pending , 
    'total':total}
    return render(request , 'dashboard_all.html',context)



def nextall(request):
    appointment_done = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="pending")
    count = appointments.objects.filter(slot_date=dt.datetime.now().date()).count()
    done = appointments.objects.filter(status="done",slot_date=dt.datetime.now().date()).count()
    pending = appointments.objects.filter(status="pending").count()
    total = appointments.objects.filter(status='done').count()
    appointment= appointments.objects.filter(doctor_id=doctors.objects.get(doctor_id=request.user))
    context={'doctors':1,
    'nextall':1,
    'app':appointment,
    'count':count,
    "done":done,
    'completed':appointment_done,
    'pending':pending , 
    'total':total,}
    return render(request , 'dashboard_all.html',context)



def previousall(request):
    appointment_done = appointments.objects.filter(slot_date = datetime.now().strftime('%Y-%m-%d'),status="done")
    count = appointments.objects.filter(slot_date=dt.datetime.now().date()).count()
    done = appointments.objects.filter(status="done",slot_date=dt.datetime.now().date()).count()
    pending = appointments.objects.filter(status="pending").count()
    total = appointments.objects.filter(status='done').count()
    appointment= appointments.objects.filter(doctor_id=doctors.objects.get(doctor_id=request.user))
    context={'doctors':1,
    'previousall':1,
    'app':appointment,
    'count':count,
    "done":done,
    'completed':appointment_done,
    'pending':pending , 
    'total':total,}
    return render(request , 'dashboard_all.html',context)


def appointment_doctor_view(request,id):
    id=int(id)
    print(id,type(id))
    if request.method == "POST":
        med = request.POST['medicine']
        print(med,type(med))
        appointments.objects.filter(patient_appointment_id=id).update(prescription=med,status="done")
        return redirect('/doctor')
    else:
        app=appointments.objects.filter(patient_appointment_id=id)
        return render(request,'prescription.html',{'apps':app})



def doctorupdate(request):
    if request.method == "POST":
        name= request.POST['name']
        email= request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']
        status =request.POST['status']
        if status=="Active":
            status =True
        else:
            status=False
        doctors.objects.filter(doctor_id=email).update(
            doctor_id=email,
            name=name,
            gender=gender,
            status = status
        )
        return redirect('/hr')






def invoiceGenerator(request):
    # Creating Canvas
    c = canvas.Canvas("invoice1.pdf",pagesize=(200,250),bottomup=0)
    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10,40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("aniket.jpg",0,0,width=50,height=30)
    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10,-40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",10)
    # Inserting the name of the company
    c.drawCentredString(125,20,"XYS Hosptal")
    # For under lining the title
    c.line(70,22,180,22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold",5)
    c.drawCentredString(125,30,"Block No. 101, Triveni Apartments, Pitam Pura,")
    c.drawCentredString(125,35,"New Delhi - 110034, India")
    # Changing the font size for Specifying GST Number of firm

    # Line Seprating the page header from the body
    c.line(5,45,195,45)
    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold",8)
    c.drawCentredString(100,55,"INVOICE")
    # This Block Consist of Costumer Details
    c.roundRect(15,63,170,40,10,stroke=1,fill=0)
    c.setFont("Times-Bold",5)
    c.drawRightString(70,70,"INVOICE No. :")
    c.drawRightString(70,80,"DATE :")
    c.drawRightString(70,90,"CUSTOMER NAME :")
    c.drawRightString(70,100,"PHONE No. :")
    c.roundRect(15,108,170,130,10,stroke=1,fill=0)
    c.line(15,120,185,120)
    c.drawCentredString(25,118,"SR No.")
    c.drawCentredString(75,118,"Payment DESCRIPTION")
    c.drawCentredString(173,118,"TOTAL")
    # Drawing table for Item Description
    c.line(15,210,185,210)
    c.drawRightString(30,130,'1')
    c.line(35,108,35,220)
    c.drawRightString(80,130,str(payment))
    c.line(115,108,115,220)
    c.drawRightString(178,130,str(total))
    c.line(135,108,135,220)

    c.line(160,108,160,220)

    # Declaration and Signature
    c.line(15,220,185,220)
    c.line(100,220,100,238)
    c.drawString(20,225,"We declare that above mentioned")
    c.drawString(20,230,"information is true.")
    c.drawString(20,235,"(This is system generated invoive)")
    c.drawRightString(180,235,"Authorised Signatory")
    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()
def check(request):
    us = request.user.username
    if patient.objects.filter(patient_id=us).exists():
        return redirect('/patient')
    elif doctors.objects.filter(doctor_id=us).exists():
        return redirect('/doctor')
    elif receptionist.objects.filter(recep_id=us).exists():
        return redirect('/receptionist')
    else:
        return redirect('/')

#<----------------------Receptionist copied-------------------------->
'''def receptionist(request):
    return render(request, "receptionist/dashboard.html", {})



def receptionist_dev(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(hours=4)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = u
    obj = Appointment.objects.filter(date__gte=vdate, startTime__gte=vtime, status_id=1)

    return render(request, "receptionist/receptionist_dev.html", {'object': obj, 'userName': userName})



def receptionist_appointment_history(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(6 * 365 / 12)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = u
    obj = Appointment.objects.filter(date__gte=vdate,status__in=(1,3,4)).order_by('-date')
    context = {
        'object': obj,
        'userName': userName,
        'title': "Appointments"
    }

    return render(request, "receptionist/appointment_history.html", context)


def receptionist_appointment_history_archive(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(6 * 365 / 12)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = u
    obj = Appointment.objects.all().order_by('-date')
    context = {
        'object': obj,
        'userName': userName,
        'title': "Archived Appointments"
    }

    return render(request, "receptionist/appointment_history.html", context)

'''

#<-------------------------------------Receptionist ------------------------------------>

