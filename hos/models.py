from django.db import models

# Create your models here.

'''class admins(models.Model):
    admin_id = models.IntegerField(max_length=100 ,primary_key=True)
    #admin_id=models.ForeignKey('admin_id')
    name = models.CharField(max_length=100,)
    password = models.CharField(max_length=100,)
    created_at = models.TimeField(max_length=100,)
    updated_at = models.TimeField(max_length=100,)'''

class appointments(models.Model):
    patient_appointment_id =models.IntegerField()
    patient_email = models.ForeignKey('patient',on_delete=models.CASCADE)
    #patient_phone = models.BigIntegerField()
    patient_name = models.CharField(max_length=100,default="")
    patient_age = models.IntegerField()
    patient_gender = models.CharField(max_length=100,)
    location = models.CharField(max_length=100,blank=True)
    doctor_id = models.ForeignKey('doctors',on_delete=models.CASCADE)
    slot_date = models.DateField()
    slot_time = models.TimeField(blank=True,null=True)
    created_at = models.DateField()
    udated_at = models.DateField()
    status = models.CharField(max_length=10)
    prescription = models.CharField(max_length=2000,blank=True)


class patient(models.Model):
    patient_id = models.EmailField()
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    age = models.IntegerField()
    phone_no = models.BigIntegerField()
    gender = models.CharField(max_length=1)




'''class departments(models.Model):
    department_id = models.CharField(max_length=100,primary_key=True)
    #department_id = models.ForeignKey('department_id')
    department_name = models.CharField(max_length=100,) 
    created_at = models.DateField(max_length=100 , )
    updated_at = models.DateField(max_length=100,)'''


class doctors(models.Model):
    doctor_id = models.EmailField()
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    status = models.BooleanField()
    #phone_no = models.IntegerField(max_length=1000)



class receptionist(models.Model):
    recep_name = models.CharField(max_length=100)
    recep_id = models.EmailField()
    hospital_name = models.CharField(max_length=100)
    hospital_id = models.IntegerField()
    status = models.BooleanField()




