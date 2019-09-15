from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import  LostOne, Contact, UserProfile
from django.core.files.storage import FileSystemStorage
import ntpath
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from trueface.recognition import FaceRecognizer
from trueface.video import VideoStream
import cv2


def search(request):
    user_role = UserProfile.objects.filter(user=request.user.id)
    contact = None
    if request.POST.get('search_name'):
        name = request.POST.get('search_name')
        contact = Contact.objects.filter(lost_one__name__contains=name)
    
    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})

def get_all(request):
    user_role = UserProfile.objects.filter(user=request.user.id)
    contact = None
    contact = Contact.objects.all()
    
    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})


def pic_search(request):
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

            fr.create_collection('collection', 'collection.npz', return_features=False)

            #vcap = VideoStream(src=0).start()
            vcap = cv2.imread('./'+person_pic1)
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

                    contact = Contact.objects.filter(lost_one__folder_name__contains=identity['predicted_label'])
        
        except Exception as e:
            print("in except =====================")
            print(str(e))

    return render(request, 'index.html', {"contacts":contact, "user":request.session["username"]})                

def advance_search(request):
    contact = None
    tags = {}
    if request.POST.get('first_name'):
        tags.update({'lost_one__first_name__contains':request.POST.get('first_name')})
    if request.POST.get('area'):
        tags.update({'lost_one__area__contains':request.POST.get('area')})
    if request.POST.get('country'):
        tags.update({'lost_one__country__contains':request.POST.get('country')})
    if request.POST.get('status'):
        tags.update({'lost_one__status__contains':request.POST.get('status')})
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
        lostones = LostOne.objects.all()
        return render(request, 'home.html', {"lostones":lostones, "user":None})
    elif request.session['username'] is not None:
        return redirect('search')



def lostone(request, lost_one_id=None):
    contact = None
    
    if request.method == 'POST':
        try:
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
                person_pic3 = fs.save(person_pic2.name, person_pic3)
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
            contact_area = request.POST.get('contact_area')

            try:
                person_pic1 = request.FILES['person_pic1']
                person_pic1 = fs.save(person_pic1.name, person_pic1)
                person_pic1 = fs.url(person_pic1)
                person_pic1 = ntpath.basename(person_pic1)
                person_pic1 = path + '/' + person_pic1
            except:
                if lost_one_id:
                    person_pic1 = None

            
            if lost_one_id:
                print("lost_one --------------------------- found")
                lost_one_object = LostOne.objects.get(id=lost_one_id)
                if person_pic1:
                    lost_one_object.person_pic1 = person_pic1
                if person_pic2:
                    lost_one_object.person_pic2 = person_pic2
                if person_pic3:
                    lost_one_object.person_pic2 = person_pic3
                lost_one_object.first_name = request.POST.get('first_name')
                lost_one_object.last_name = request.POST.get('last_name')
                lost_one_object.email_address = request.POST.get('email')
                lost_one_object.contact_number = request.POST.get('lost_one_contact_no')
                lost_one_object.age = request.POST.get('age')
                lost_one_object.status = request.POST.get('status')
                lost_one_object.area = request.POST.get('lost_one_area')
                lost_one_object.country = request.POST.get('country')
                lost_one_object.save()
                
                contact_object = Contact.objects.get(id=lost_one_id)
                contact_object.name = request.POST.get('name')
                contact_object.contact_area = request.POST.get('contact_area')
                contact_object.contact_number1 = request.POST.get('contact_1')
                contact_object.contact_number2 = request.POST.get('contact_2')
                contact_object.address = request.POST.get('address')
                contact_object.note = request.POST.get('note')
                contact_object.contact_area = request.POST.get('contact_area')
                contact_object.save()
                return redirect('index')
            else:
                lost_one_object = LostOne.objects.create(gender=gender, name=first_name+ ' ' +last_name, folder_name=first_name+last_name,first_name=first_name, last_name=last_name, email_address=email_address, contact_number=contact_number,  person_pic1=person_pic1,
                                                         person_pic2=person_pic2, person_pic3=person_pic3, age=age, area=area, country=country, status=status)
                
                rescued = True if request.POST.get('rescued') else False
                died = True if request.POST.get('died') else False
                contact = Contact.objects.create(rescued=rescued, died=died, name=name, contact_number1=contact_number1,
                                                 contact_number2=contact_number2, address=address, note=note, lost_one=lost_one_object, area=contact_area)
                return redirect('index')
            
            
        except Exception as e:
            print (e)

    elif lost_one_id:
        contact = Contact.objects.filter(lost_one=lost_one_id).first()
        return render(request, '5-rescuer.html', {'n' : range(1,100), "user":request.session["username"], 'contact':contact})


    return render(request, '5-rescuer.html', {'n' : range(1,100), "user":request.session["username"]})

def login(request):

    if request.method == 'POST':
        #print("email----------------", username)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        #print ("user",type(username.username))
        if user:
            #print ("test-----------------------------")
            request.session['username'] = request.POST['username']
            #print ("test1-----------------------------")
            request.session['password'] = request.POST['password']
        return redirect('get_all')
    return render(request, 'login.html')

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