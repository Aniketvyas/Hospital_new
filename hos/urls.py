from django.urls import path 
from . import views

urlpatterns=[
    path('test',views.invoiceGenerator),
    path('<int:id>/',views.red),
    path('about',views.about),
    path('',views.index1),
    path('services',views.services),
    path('appointment',views.appointment),
    path('lab',views.lab),
    path('blood',views.blood),
    path('contact',views.contact),
    path('medical',views.medical),
    path('book',views.book),
    path('track',views.track),
    path('patient/',views.patient_dash,name="patient"),
    path('prescription/<int:id>',views.prescription),
    #path('patient/PreviousLabReports',views.LabReports),
    #path('uploadFile',views.upload),
    path('receptionist/',views.receptionists),
    path('receptionist/update',views.requestUpdate),
    path('receptionist/<int:id>/delete',views.requestDelete),
    path('receptionist/addPatient',views.addPatient),
    path('doctor',views.doc_dash,name="doctor"),
    path('nextall',views.nextall),
    path('previousall',views.previousall),
    path('appointment_view/<int:id>',views.appointment_doctor_view),
    path('locate',views.locate),
   # path('patient/timeslot',views.timeslot),
    path('check',views.check),
    path('patient/timeslot/<int:id>',views.timeslot,name="timeslot"),
    path('1/<int:id>/',views.red),
    path('2/<int:id1>/',views.red),
    path('3/<int:id1>/',views.red),
    path('4/<int:id1>/',views.red),
    path('5/<int:id1>/',views.red),
    path('6/<int:id1>/',views.red),
    path('7/<int:id1>/',views.red),
    path('8/<int:id1>/',views.red),
    path('9/<int:id1>/',views.red),
]

