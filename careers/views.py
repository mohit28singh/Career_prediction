
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
import joblib
import pandas as pd
reloadModel=joblib.load('careerlast.pkl')
print(type(reloadModel))
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
def Technical_wri(request):
    return render (request,'Technical_writer.html')
def Graphic_Designer(request):
    return render (request,'Graphic_Designer.html')
def TermsConditons(request):
    return render(request, 'Terms&Condition.html')
def CarResult(request):
    if request.method == 'POST':
       rate_Database_Fundamentals= request.POST.get('rate_Database Fundamentals')
       rate_Computer_Architecture=request.POST.get('rate_Computer_Architecture')
       rate_Distributed_Computing_Systems=request.POST.get('rate_Distributed Computing Systems')
       rate_Cyber_Security=request.POST.get('rate_Cyber Security')
       rate_Networking=request.POST.get('rate_Networking')
       rate_Development=request.POST.get('rate_Development')
       rate_Programming_Skills=request.POST.get('rate_Programming Skills')
       rate_Project_Management=request.POST.get('rate_Project Management')
       rate_Computer_Forensics_Fundamentals=request.POST.get('rate_Computer Forensics Fundamentals')
       rate_Technical_Communication=request.POST.get('rate_Technical Communication')
       rate_AI_ML=request.POST.get('rate_AI ML')
       rate_se=request.POST.get('rate_se')
       rate_Business_Analysis=request.POST.get('rate_Business Analysis')
       rate_Communication_skills=request.POST.get('rate_Communication skills')
       rate_Data_Science=request.POST.get('rate_Data Science')
       rate_Troubleshooting_skills=request.POST.get('rate_Troubleshooting skills')
       rate_graphic_designing=request.POST.get('rate_graphic_designing')
       temp={}
       temp['rate_database_fundamentals']=rate_Database_Fundamentals
       temp['rate_Computer_Architecture']=rate_Computer_Architecture
       temp['Distributed_Computing_Systems']=rate_Distributed_Computing_Systems
       temp['rate_Cyber_Security']=rate_Cyber_Security
       temp['rate_Networking']=rate_Networking
       temp['rate_Development']=rate_Development
       temp['rate_Programming_Skills']=rate_Programming_Skills
       temp['rate_Project_Management']=rate_Project_Management
       temp['rate_Computer_Forensics_Fundamentals']=rate_Computer_Forensics_Fundamentals
       temp['rate_Technical_Communication']=rate_Technical_Communication
       temp['rate_AI_ML']=rate_AI_ML
       temp['rate_se']=rate_se
       temp['rate_Business_Analysis']=rate_Business_Analysis
       temp['rate_Communication_skills']=rate_Communication_skills
       temp['rate_Data_Science']=rate_Data_Science
       temp['rate_Troubleshooting_skills']=rate_Troubleshooting_skills
       temp['rate_graphic_designing']=rate_graphic_designing
       print(temp)
    testdata=pd.DataFrame({'x':temp}).transpose()
    resultdata=reloadModel.predict(testdata)[0]
    context={'resultdata':resultdata}
    return render(request, 'result.html', context)