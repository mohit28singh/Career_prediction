
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    return render(request, 'main.html', {'user': user})
def homepage(request):
    return render(request, 'main.html')

def SignUpPage(request):
    if request.method=='POST':
       uname=request.POST.get('username')
       email=request.POST.get('email')
       pass1=request.POST.get('password1')
       pass2=request.POST.get('password2')
       if pass1!=pass2:
          return HttpResponse("Password not same")
       else:
         my_user=User.objects.create_user(uname,email,pass1)
         my_user.save()
         return redirect('login')

    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
       username=request.POST.get('username')
       pass1=request.POST.get('password1')
       user=authenticate(request,username=username,password=pass1)
       if user is not None:
          login(request,user)
          return redirect('home')
       else:
          return HttpResponse("Wrong pw entered")
       
    return render(request,'login.html')

def LogoutPage(request):
     logout(request)
     return render(request,'main.html')


@login_required(login_url='login')
def careerprediction(request):
    return render(request, 'services.html')

def course(request):
    return render(request,"course.html")

def contact(request):
    return render(request,"contact.html")
def about(request):
    return render(request, 'about.html')
@login_required(login_url='login')
def knowledge(request):
    return render(request, 'knowledge.html')

def AIML(request):
    return render(request, 'AI_ML_Specialist.html')
def APIs(request):
    return render(request, 'API_Integration_Specialist.html')

def PenTest(request):
    return render(request, 'Penetration_Tester.html')
def AppSupport(request):
    return render(request, 'Application_Support_engineer.html')
def Business(request):
    return render (request,'Business_Analyst.html')
def Customer_service_executive(request):
    return render (request,'Customer_service_executive.html')
def Cyber_Security (request):
    return render(request,'Cyber_Security_Specialist.html')
def Databaseadmin(request):
    return render(request,'Database_Administrator.html')
def Datasci(request):
    return render(request,'Data_Scientist.html')
def Hardware_Engineer(request):
    return render(request,'Hardware_Engineer.html')
def Helpdesk_Engineer(request):
    return render (request,'Helpdesk_Engineer.html')

def Information_security(request):
    return render (request,'Information_security.html')
def Networking_engineer(request):
    return render (request,'Networking_engineer.html')
def Project_Manager(request):
    return render (request,'Project_Manager.html')
def Software_developer(request):
    return render (request,'Software_developer.html')
def Software_tester(request):
    return render (request,'Software_tester.html')
def Technical_wri (request):
    return render (request,'Technical_writer.html')
def Graphic_Designer(request):
    return render (request,'Graphic_Designer.html')
def TermsConditons(request):
    return render(request, 'Terms&Condition.html')
