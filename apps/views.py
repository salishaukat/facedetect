from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import  LostOne, Contact
from django.core.files.storage import FileSystemStorage


def index(request):
    contact = Contact.objects.all()
    return render(request, 'index.html', {"contacts":contact})


def lostone(request):
    user = None
    if request.method == 'POST' and request.FILES['person_pic1']:
        person_pic1 = request.FILES['person_pic1']
        
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email')
        contact_number = request.POST.get('lost_one_contact_number')
        age = request.POST.get('age')
        status = request.POST.get('status')
        area = request.POST.get('lost_one_area')
        country = request.POST.get('country')
    
        fs = FileSystemStorage(location='collection/'+first_name+last_name)
        person_pic1 = fs.save(person_pic1.name, person_pic1)
        person_pic1 = fs.url(person_pic1)
        try:
            person_pic2 = request.FILES['person_pic2']
            person_pic2 = fs.save(person_pic2.name, person_pic2)
            person_pic2 = fs.url(person_pic2)
        except:
            person_pic2 = None
        try:
            person_pic3 = request.FILES['person_pic3']
            person_pic3 = fs.save(person_pic2.name, person_pic3)
            person_pic3 = fs.url(person_pic3)
        except:
            person_pic3 = None
        name = request.POST.get('name')
        country = request.POST.get('contact_area')
        contact_number1 = request.POST.get('contact_1')
        contact_number2 = request.POST.get('contact_2')
        address = request.POST.get('address')
        note = request.POST.get('note')
        contact_area = request.POST.get('contact_area')

        lost_one_object = LostOne.objects.create(first_name=first_name, last_name=last_name, email_address=email_address, contact_number=contact_number,  person_pic1=person_pic1,
                                                 person_pic2=person_pic2, person_pic3=person_pic3, age=age, area=area, country=country)
        contact = Contact.objects.create(name=name, contact_number1=contact_number1,
                                         contact_number2=contact_number2, address=address, note=note, lost_one=lost_one_object, area=contact_area)


    return render(request, '5-rescuer.html', {'n' : range(1,100),'user':user})