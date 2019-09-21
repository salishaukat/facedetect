from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
import ntpath
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from trueface.recognition import FaceRecognizer
from trueface.video import VideoStream
import cv2
from django.shortcuts import redirect, reverse
import time
from django.http import JsonResponse
from random import randint
from itertools import chain
import sys
import base64
import numpy as np
from django.views.decorators.csrf import csrf_protect

fr = FaceRecognizer(ctx='cpu',
                    fd_model_path='./fd_model',
                    fr_model_path='./model-tfv2/model.trueface',
                    params_path='./model-tfv2/model.params',
                    license='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbW90aW9uIjpudWxsLCJmciI6dHJ1ZSwicGFja2FnZV9pZCI6bnVsbCwiZXhwaXJ5X2RhdGUiOiIyMDE5LTA5LTI3IiwidGhyZWF0X2RldGVjdGlvbiI6bnVsbCwibWFjaGluZXMiOiI1IiwiYWxwciI6bnVsbCwibmFtZSI6IkpvaG4gQnJpZGdld2F0ZXIiLCJ0a2V5IjoibmV3IiwiZXhwaXJ5X3RpbWVfc3RhbXAiOjE1Njk1NDI0MDAuMCwiYXR0cmlidXRlcyI6dHJ1ZSwidHlwZSI6Im9mZmxpbmUiLCJlbWFpbCI6ImpvaG5iQGJsdWVzdG9uZS5uZXR3b3JrIn0._B9h-H4sZ5tQBslIVZtM1b2Y4_-TSN1e4dAo6KAp0nU'
                    )
fr.create_collection('collection', 'collection.npz', return_features=False)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def live(request):
    return render(request, 'live.html')

def search(request, id=None):
    if 'username' not in request.session:
        request.session["username"] = None
    if request.session["username"]:
        if "reporter" in request.session["role"]:
            return redirect('reports')
    user_role = UserProfile.objects.filter(user=request.user.id)
    contact = None
    if id:
        contact = Shelter.objects.filter(lost_one=id)
        print("search ============== contact1")
        print(contact)
        if not contact:
            print("search ============== contact1")
            contact = Contact.objects.filter(lost_one=id)    
            print(contact)
    if request.POST.get('search_name'):
        name = request.POST.get('search_name')
        contact_data = None
        shelter_data = None
        shelter_data = Shelter.objects.filter(lost_one__name__icontains=name)
        contact_data = Contact.objects.filter(lost_one__name__icontains=name).exclude(lost_one__in=shelter_data.values('lost_one'))
        contact = list(chain(contact_data, shelter_data))

    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})

def get_all(request):
    if 'username' not in request.session:
        request.session["username"] = None
    if request.session["username"]:
        if "reporter" in request.session["role"]:
            return redirect('reports')
    user_role = UserProfile.objects.filter(user=request.user.id)
    contact_data = None
    shelter_data = None
    shelter_data = Shelter.objects.all()
    contact_data = Contact.objects.exclude(lost_one__in=shelter_data.values('lost_one'))
    contact = list(chain(contact_data, shelter_data))

    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})

def live_search(request):
    if 'username' not in request.session:
        request.session["username"] = None
    print("in function live ==============")
    contact = None

    fr = FaceRecognizer(ctx='cpu',
                        fd_model_path='./fd_model',
                        fr_model_path='./model-tfv2/model.trueface',
                        params_path='./model-tfv2/model.params',
                        license='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbW90aW9uIjpudWxsLCJmciI6dHJ1ZSwicGFja2FnZV9pZCI6bnVsbCwiZXhwaXJ5X2RhdGUiOiIyMDE5LTA5LTI3IiwidGhyZWF0X2RldGVjdGlvbiI6bnVsbCwibWFjaGluZXMiOiI1IiwiYWxwciI6bnVsbCwibmFtZSI6IkpvaG4gQnJpZGdld2F0ZXIiLCJ0a2V5IjoibmV3IiwiZXhwaXJ5X3RpbWVfc3RhbXAiOjE1Njk1NDI0MDAuMCwiYXR0cmlidXRlcyI6dHJ1ZSwidHlwZSI6Im9mZmxpbmUiLCJlbWFpbCI6ImpvaG5iQGJsdWVzdG9uZS5uZXR3b3JrIn0._B9h-H4sZ5tQBslIVZtM1b2Y4_-TSN1e4dAo6KAp0nU'
                        )

    fr.create_collection('collection', 'collection.npz', return_features=False)

    vcap = VideoStream(src=0).start()
    t_end = time.time() + 60 * 0.5
    while time.time() < t_end:
    #while(True):
        frame = vcap.read()
        frame = cv2.resize(frame, (640, 480))
        bounding_boxes, points, chips = fr.find_faces(frame,
                                                  return_chips=True,
                                                  return_binary=True)
        if bounding_boxes is None:
                continue
        for i, chip in enumerate(chips):
            identity = fr.identify(chip,
                                   threshold=0.3,
                                   collection='./collection.npz')
            print("========================")
            print(identity)
            if identity['predicted_label'] != None:
                contact = Contact.objects.filter(lost_one__folder_name__contains=identity['predicted_label'])
                print (contact)
                break
        if contact:
            print('==============================')
            print('in if contact')
            # vcap.stopped = True
            # vcap.stream.release()
            break
        else:
            print('==============================')
            print('in else contact')

            continue
    vcap.stopped = True
    vcap.stream.release()
    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})

def pic_search(request):
    if 'username' not in request.session:
        request.session["username"] = None
    print("in function ==============")
    contact = None
    if request.method == 'POST' and request.FILES['person_pic1']:
        try:
            person_pic1 = request.FILES['person_pic1']     
            
            fs = FileSystemStorage(location='search/')
            person_pic1 = fs.save(person_pic1.name, person_pic1)
            person_pic1 = fs.url(person_pic1)
            person_pic1 = ntpath.basename(person_pic1)
            person_pic1 = 'search' + '/' + person_pic1

            fr = FaceRecognizer(ctx='cpu',
                                fd_model_path='./fd_model',
                                fr_model_path='./model-tfv2/model.trueface',
                                params_path='./model-tfv2/model.params',
                                license='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbW90aW9uIjpudWxsLCJmciI6dHJ1ZSwicGFja2FnZV9pZCI6bnVsbCwiZXhwaXJ5X2RhdGUiOiIyMDE5LTA5LTI3IiwidGhyZWF0X2RldGVjdGlvbiI6bnVsbCwibWFjaGluZXMiOiI1IiwiYWxwciI6bnVsbCwibmFtZSI6IkpvaG4gQnJpZGdld2F0ZXIiLCJ0a2V5IjoibmV3IiwiZXhwaXJ5X3RpbWVfc3RhbXAiOjE1Njk1NDI0MDAuMCwiYXR0cmlidXRlcyI6dHJ1ZSwidHlwZSI6Im9mZmxpbmUiLCJlbWFpbCI6ImpvaG5iQGJsdWVzdG9uZS5uZXR3b3JrIn0._B9h-H4sZ5tQBslIVZtM1b2Y4_-TSN1e4dAo6KAp0nU'
                                )

            #fr.create_collection('collection', 'collection.npz', return_features=False)

            #vcap = VideoStream(src=0).start()
            vcap = cv2.imread('./'+person_pic1)
            print (vcap)
            #while(True):
                #frame = vcap.read()
            frame = vcap
            frame = cv2.resize(frame, (640, 480))
            bounding_boxes, points, chips = fr.find_faces(frame,
                                                      return_chips=True,
                                                      return_binary=True)
            for i, chip in enumerate(chips):
                identity = fr.identify(chip,
                                       threshold=0.3,
                                       collection='./collection.npz')
                print('=======identity=======')
                print(identity)
                print(identity['predicted_label'])
                if identity['predicted_label'] != None:
                    contact_data = None
                    shelter_data = None
                    shelter_data = Shelter.objects.filter(lost_one__folder_name__contains=identity['predicted_label'])
                    contact_data = Contact.objects.filter(lost_one__folder_name__contains=identity['predicted_label']).exclude(lost_one__in=shelter_data.values('lost_one'))
                    contact = list(chain(contact_data, shelter_data))
                    print (contact)
        
        except Exception as e:
            print("in except =====================")
            print(str(e))

    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})                

def advance_search(request):
    if 'username' not in request.session:
        request.session["username"] = None
    contact = None
    tags = {}
    if request.POST.get('first_name'):
        tags.update({'lost_one__first_name__icontains':request.POST.get('first_name')})
    if request.POST.get('last_name'):
        tags.update({'lost_one__last_name__icontains':request.POST.get('last_name')})
    if request.POST.get('contact_no'):
        tags.update({'lost_one__contact_number__icontains':request.POST.get('contact_no')})        
    if request.POST.get('area'):
        tags.update({'lost_one__area__icontains':request.POST.get('area')})
    if request.POST.get('country'):
        tags.update({'lost_one__country__icontains':request.POST.get('country')})
    if request.POST.get('status'):
        tags.update({'lost_one__status__icontains':request.POST.get('status')})
    male = request.POST.get('male') if request.POST.get('male') else None
    female = request.POST.get('female') if request.POST.get('female') else None
    if male:
        tags.update({'lost_one__gender__contains':"male"})
    elif female:
        tags.update({'lost_one__gender__contains':"female"})
     # Your dict with fields
    or_condition = Q()
    for key, value in tags.items():
        or_condition.add(Q(**{key: value}), Q.OR)
    contact = Contact.objects.filter(or_condition)
    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})

def index(request):
    if 'username' not in request.session or request.session['username'] is None:
        request.session['username'] = None
        lostones = LostOne.objects.order_by("-id")[:10]
        sponsors = Sponsor.objects.filter(active=True)
        return render(request, 'home.html', {"lostones":lostones, "sponsors":sponsors, "user":None})
    if request.session["username"]:
        if "reporter" in request.session["role"]:
            return redirect('reports')
        else:
            return redirect('search')

def sponsor(request):
    if 'username' not in request.session:
        request.session["username"] = None
    sponsor = None    
    print("in sponsor =============================")
    if request.method == 'POST' and request.FILES['company_logo']:
        print("in sponsor =============================")
        try:
            sid = random_with_N_digits(6)
            company_logo = request.FILES['company_logo']
            name = request.POST.get('name')
            company_name = request.POST.get('company_name')
            email_address = request.POST.get('email_address')
            contact_number = request.POST.get('contact_number')
            fs = FileSystemStorage(location='collection/company/')
            company_logo = fs.save(company_logo.name, company_logo)
            company_logo = fs.url(company_logo)
            company_logo = ntpath.basename(company_logo)
            company_logo = '/collection/company/' + company_logo

            sponsor_object = Sponsor.objects.create(sid=sid, name=name, company_name=company_name, email_address=email_address, contact_number=contact_number, company_logo=company_logo)
                        
        except Exception as e:
            print (e)
    else:
        try:
            name = request.POST.get('name')
            company_name = request.POST.get('company_name')
            email_address = request.POST.get('email_address')
            contact_number = request.POST.get('contact_number')

            sponsor_object = Sponsor.objects.create(name=name, company_name=company_name, email_address=email_address, contact_number=contact_number)
                        
        except Exception as e:
            print (e)        
    return redirect('index')
    #return render(request, 'home.html', {'n' : range(1,100), "user":request.session["username"]})


def lostone(request, lost_one_id=None):
    if 'username' not in request.session:
        request.session["username"] = None
    if request.session["username"]:
        if "reporter" in request.session["role"]:
            return redirect('reports')
    contact = None


    if request.method == 'POST':

        uid = random_with_N_digits(6)
        shelter_id = random_with_N_digits(6)
        lost_one_id = request.POST.get('lost_one_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email')
        contact_number = request.POST.get('lost_one_contact_no')
        age = request.POST.get('age')
        status = request.POST.get('status')
        area = request.POST.get('lost_one_area')
        country = request.POST.get('country')
        male = request.POST.get('male') if request.POST.get('male') else None
        female = request.POST.get('female') if request.POST.get('female') else None
        if male:
            gender = 'male'
        elif female:
            gender = 'female'
        shelter_status = None
        rescued = request.POST.get('rescued') if request.POST.get('rescued') else None
        died = request.POST.get('died') if request.POST.get('died') else None
        if rescued:
            shelter_status = 'rescued'
        elif died:
            shelter_status = 'died'

        path = '/collection/'+first_name+last_name
        fs = FileSystemStorage(location='collection/'+first_name+last_name)


        try:
            person_pic2 = request.FILES['person_pic2']
            person_pic2 = fs.save(person_pic2.name, person_pic2)
            person_pic2 = fs.url(person_pic2)
            person_pic2 = ntpath.basename(person_pic2)
            person_pic2 = path + '/' + person_pic2
        except:
            person_pic2 = None
        try:
            person_pic3 = request.FILES['person_pic3']
            person_pic3 = fs.save(person_pic3.name, person_pic3)
            person_pic3 = fs.url(person_pic3)
            person_pic3 = ntpath.basename(person_pic3)
            person_pic3 = path + '/' + person_pic3
        except:
            person_pic3 = None
        name = request.POST.get('name')
        contact_area = request.POST.get('contact_area')
        contact_number1 = request.POST.get('contact_1')
        contact_number2 = request.POST.get('contact_2')
        address = request.POST.get('address')
        note = request.POST.get('note')

        try:
            person_pic1 = request.FILES['person_pic1']
            person_pic1 = fs.save(person_pic1.name, person_pic1)
            person_pic1 = fs.url(person_pic1)
            person_pic1 = ntpath.basename(person_pic1)
            person_pic1 = path + '/' + person_pic1
        except:
            person_pic1 = None


        if lost_one_id:
            lost_one_object = LostOne.objects.get(id=lost_one_id)
            shelter = Shelter.objects.filter(lost_one=lost_one_id).first()
            if shelter:
                shelter.shelter = request.POST.get('name')
                shelter.area = request.POST.get('contact_area')
                shelter.contact_number1 = request.POST.get('contact_1')
                shelter.contact_number2 = request.POST.get('contact_2')
                shelter.address = request.POST.get('address')
                shelter.note = request.POST.get('note')
                shelter.status = shelter_status
                lost_one_object.status = shelter_status
                if person_pic1:
                    print(person_pic1)
                    lost_one_object.person_pic1 = person_pic1
                shelter.save()
                lost_one_object.save()
                shelter_obj = Shelter.objects.filter(lost_one=lost_one_id)

            else:
                shelter = Shelter.objects.create(shelter_id=shelter_id, status=shelter_status, shelter=name, contact_number1=contact_number1,
                                                 contact_number2=contact_number2, address=address, note=note, lost_one=lost_one_object, area=contact_area)
                if person_pic1:
                    print(person_pic1)
                    lost_one_object.person_pic1 = person_pic1
                lost_one_object.status = shelter_status
                lost_one_object.save()

                shelter_obj = Shelter.objects.filter(lost_one=lost_one_id)
                print("=======shle in else =======")
                print(shelter_obj)
            return render(request, 'index.html', {"contacts":shelter_obj, "user":request.session["username"]})
            #return redirect('get_all')
        else:
            lost_one_object = LostOne.objects.create(uid=uid, gender=gender, name=first_name+ ' ' +last_name, folder_name=first_name+last_name,first_name=first_name, last_name=last_name, email_address=email_address, contact_number=contact_number,  person_pic1=person_pic1,
                                                     person_pic2=person_pic2, person_pic3=person_pic3, age=age, area=area, country=country, status=status)
            fr.create_collection('collection', 'collection.npz', return_features=False)
            
            if request.session['username'] is None:
                contact = Contact.objects.create(name=name, contact_number1=contact_number1,
                                                 contact_number2=contact_number2, address=address, note=note, lost_one=lost_one_object, area=contact_area)
                contact_obj = Contact.objects.filter(lost_one__name__contains=first_name+' '+last_name)
                print(contact_obj)
                return render(request, 'index.html', {"contacts":contact_obj, "user":request.session["username"], "created":"success"})

            else:
                shelter = Shelter.objects.create(shelter_id=shelter_id, status=shelter_status, shelter=name, contact_number1=contact_number1,
                                                     contact_number2=contact_number2, address=address, note=note, lost_one=lost_one_object, area=contact_area)
                shelter_obj = Shelter.objects.filter(lost_one__name__contains=first_name+' '+last_name)
                print(shelter_obj)
                return render(request, 'index.html', {"contacts":shelter_obj, "user":request.session["username"], "created":"success"})                

            #return redirect('get_all')
            
    elif ('username' not in request.session or request.session['username'] is None) and lost_one_id:
        return redirect('lostone')

    elif lost_one_id:
        contact = Shelter.objects.filter(lost_one=lost_one_id).first()
        shelter = True
        if contact is None:
            contact = Contact.objects.filter(lost_one=lost_one_id).first()
            shelter = False
        return render(request, 'lostone.html', {'n' : range(1,100), "user":request.session["username"], 'contact':contact, 'shelter':shelter, 'allow_shelter':True})
    
   
    
    


    return render(request, 'lostone.html', {'n' : range(1,100), "user":request.session["username"]})

def login(request):

    if request.method == 'POST':
        #print("email----------------", username)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        #print ("user",type(username.username))
        if user:
            print(user,"----------------------")
            #print ("test-----------------------------")
            request.session['username'] = request.POST['username']
            #print ("test1-----------------------------")
            request.session['password'] = request.POST['password']
            role = UserProfile.objects.filter(user=user).first()
            request.session['role'] = None
            print(role,"----------------------")
            if role:
                request.session['role'] = role.role
                if "reporter" in role.role:
                    return redirect('reports')
            return redirect('get_all')
        else:
            print("in else")
            return render(request, 'home.html', {"username":request.POST['username'],'user':None})
    return render(request, 'home.html')

def logout(request):
   try:
      request.session['username'] = None
   except:
      pass
   return redirect('index')

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def comments(request):
    if 'username' not in request.session:
        request.session["username"] = None
    if request.method == 'POST':
        if request.session['username']:
            name = request.session['username']
        else:
            name = request.POST.get('comment_name')
        comments = request.POST.get('comment')
        print("--------------------",request.POST.get('lost_one'))
        lost_one_object = LostOne.objects.get(id=request.POST.get('lost_one'))
        id = Comments.objects.create(name=name, comment=comments, lost_one=request.POST.get('lost_one'))
    return render(request, 'login.html')

def reports(request, search=None):
    if 'username' not in request.session:
        request.session["username"] = None
    if request.session["username"]:
        if "reporter" in request.session["role"]:
            if search:
                if search.lower() == 'oc':
                    contacts = Contact.objects.exclude(lost_one__country__in=['Canada','Bahamas','United States of America'])
                else:
                    contacts = Contact.objects.filter(Q(lost_one__status__contains=search) | Q(name__contains=search) | Q(lost_one__area__contains=search) | Q(lost_one__country__contains=search))
            else:
                contacts = Contact.objects.all()
            return render(request, 'reports.html',{'contacts':contacts,'search':search})
    return redirect('index')

def get_all_lost_one(request, lost_one_id=None):
    try:
        lostone = LostOne.objects.filter(id=lost_one_id).values()[0]
    except:
        lostone = None
    try:
        contact = Contact.objects.filter(lost_one=lost_one_id).values()[0]
    except:
        contact = None
    try:
        shelter = Shelter.objects.filter(lost_one=lost_one_id).values()[0]
    except:
        shelter = None
    print(lostone)
   
    return JsonResponse({'lostone':lostone,'contact':contact, 'shelter':shelter})

@csrf_protect
def get_face_from_image(request):
    contact=None
    if request.method == 'POST':
        image = request.POST.get('image')
        #print(image)

        imagen_decodificada = base64.b64decode(image)

        img_name = str(random_with_N_digits(6))+'.png'
        output = open(img_name, 'wb')

        output.write(imagen_decodificada)

        output.close()
        vcap = cv2.imread(img_name)

        fr = FaceRecognizer(ctx='cpu',
                            fd_model_path='./fd_model',
                            fr_model_path='./model-tfv2/model.trueface',
                            params_path='./model-tfv2/model.params',
                            license='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbW90aW9uIjpudWxsLCJmciI6dHJ1ZSwicGFja2FnZV9pZCI6bnVsbCwiZXhwaXJ5X2RhdGUiOiIyMDE5LTA5LTI3IiwidGhyZWF0X2RldGVjdGlvbiI6bnVsbCwibWFjaGluZXMiOiI1IiwiYWxwciI6bnVsbCwibmFtZSI6IkpvaG4gQnJpZGdld2F0ZXIiLCJ0a2V5IjoibmV3IiwiZXhwaXJ5X3RpbWVfc3RhbXAiOjE1Njk1NDI0MDAuMCwiYXR0cmlidXRlcyI6dHJ1ZSwidHlwZSI6Im9mZmxpbmUiLCJlbWFpbCI6ImpvaG5iQGJsdWVzdG9uZS5uZXR3b3JrIn0._B9h-H4sZ5tQBslIVZtM1b2Y4_-TSN1e4dAo6KAp0nU'
                            )

        #fr.create_collection('collection', 'collection.npz', return_features=False)


        frame = vcap
        frame = cv2.resize(frame, (640, 480))
        bounding_boxes, points, chips = fr.find_faces(frame,
                                                      return_chips=True,
                                                      return_binary=True)
        for i, chip in enumerate(chips):
            identity = fr.identify(chip,
                                   threshold=0.3,
                                   collection='./collection.npz')
            print ("----------------------------------------",identity['predicted_label'])
            if identity['predicted_label'] != None:
                contact_data = None
                shelter_data = None
                shelter_data = Shelter.objects.filter(lost_one__folder_name__contains=identity['predicted_label'])
                contact_data = Contact.objects.filter(lost_one__folder_name__contains=identity['predicted_label'])
                print(shelter_data)
                if shelter_data:
                    contact = shelter_data.values()[0]
                else:
                    contact = contact_data.values()[0]
                print(contact)
                #contact = Contact.objects.filter(lost_one__folder_name__contains=identity['predicted_label']).values()[0]
                print(contact)
    return JsonResponse({'contact': contact})