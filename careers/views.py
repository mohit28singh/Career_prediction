
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
import numpy as np 
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io, base64
from django.core.files.storage import FileSystemStorage


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
# model = joblib.load('careercounselling.pkl')
# print(type(model))

def CarResult(request):
    if request.method == 'POST':
        # Get the ratings from the form
        rate_database_fundamentals = int(request.POST.get('1'))
        rate_computer_architecture = int(request.POST.get("b"))
        rate_Distributed_Computing_Systems = int(request.POST.get('3'))
        cyber_security_rating = int(request.POST.get('4'))
        rate_networking = int(request.POST.get('5'))
        rate_development = int(request.POST.get('6'))
        rate_programming_skills = int(request.POST.get('7'))
        project_management = int(request.POST.get('8'))
        computer_forensics_fundamentals = int(request.POST.get('9'))
        rate_technical_communication = int(request.POST.get('10'))
        rate_ai_ml = int(request.POST.get('11'))
        rate_se = int(request.POST.get('12'))
        rate_Business_Analysis = int(request.POST.get('13'))
        rate_communication_skills = int(request.POST.get('14'))
        rate_data_science = int(request.POST.get('15'))
        rate_Troubleshooting_skills = int(request.POST.get('16'))
        rate_graphic_designing = int(request.POST.get('17'))

        # Prepare the input data as a numpy array
        new_data = [[rate_database_fundamentals, rate_computer_architecture, rate_Distributed_Computing_Systems,
                     cyber_security_rating, rate_networking, rate_development, rate_programming_skills,
                     project_management, computer_forensics_fundamentals, rate_technical_communication, rate_ai_ml,
                     rate_se, rate_Business_Analysis, rate_communication_skills, rate_data_science,
                     rate_Troubleshooting_skills, rate_graphic_designing]]
        new_data = np.array(new_data)

        # Load the saved model
        loaded_model = joblib.load('careercounselling.pkl')

        # Get the probabilities of the new data belonging to each class
        proba = loaded_model.predict_proba(new_data)

        # Get the indices of the top 3 matches in descending order of probability
        top3_matches = np.argsort(proba[0])[::-1][:3]

        # Create a list of the top 3 match labels
        top3_labels = [loaded_model.classes_[i] for i in top3_matches]

        # Create a horizontal bar chart with the top 3 matches
        fig, ax = plt.subplots(figsize=(6, 3))
        bars = plt.barh(np.arange(3), proba[0][top3_matches], tick_label=top3_labels)
        plt.xlim(0, 1)
        plt.xlabel('Probability')
        plt.title('Top Career Matches')
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 0.02, bar.get_y() + bar.get_height()/2, '{:.1f}%'.format(width*100))


        # Adjust the spacing between subplots
        fig.subplots_adjust(left=0.4, bottom=0.1, right=0.95, top=0.9)

        # Convert the Matplotlib chart to a base64-encoded string for embedding in the template
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Pass the data to the template
        return render(request, 'result.html', {'chart_data': chart_data})
#      if request.method == 'POST':
#         rate_database_fundamentals = request.POST.get('1')
#         rate_computer_architecture = request.POST.get("b")
#         rate_Distributed_Computing_Systems = request.POST.get('3')
#         cyber_security_rating = request.POST.get('4')
#         rate_networking = request.POST.get('5')
#         rate_development = request.POST.get('6')
#         rate_programming_skills = request.POST.get('7')
#         project_management = request.POST.get('8')
#         computer_forensics_fundamentals = request.POST.get('9')
#         rate_technical_communication = request.POST.get('10')
#         rate_ai_ml = request.POST.get('11')
#         rate_se = request.POST.get('12')
#         rate_Business_Analysis = request.POST.get('13')
#         rate_communication_skills = request.POST.get('14')
#         rate_data_science = request.POST.get('15')
#         rate_Troubleshooting_skills = request.POST.get('16')
#         rate_graphic_designing = request.POST.get('17')

#         print(rate_database_fundamentals)
#         print(rate_computer_architecture)
#         print(rate_Distributed_Computing_Systems)
#         print(cyber_security_rating)
#         print(rate_networking)
#         print(rate_development , rate_programming_skills ,project_management ,computer_forensics_fundamentals ,rate_technical_communication ,  rate_ai_ml)
#         print(rate_se ,rate_Business_Analysis ,rate_communication_skills , rate_data_science, 
#         rate_Troubleshooting_skills 
#         ,rate_graphic_designing )
#         skills = {
#     'rate_database_fundamentals': rate_database_fundamentals,
#     'rate_computer_architecture': rate_computer_architecture,
#     'rate_Distributed_Computing_Systems': rate_Distributed_Computing_Systems,
#     'cyber_security_rating': cyber_security_rating,
#     'rate_networking': rate_networking,
#     'rate_development': rate_development,
#     'rate_programming_skills': rate_programming_skills,
#     'project_management': project_management,
#     'computer_forensics_fundamentals': computer_forensics_fundamentals,
#     'rate_technical_communication': rate_technical_communication,
#     'rate_ai_ml': rate_ai_ml,
#     'rate_se': rate_se,
#     'rate_Business_Analysis': rate_Business_Analysis,
#     'rate_communication_skills': rate_communication_skills,
#     'rate_data_science': rate_data_science,
#     'rate_Troubleshooting_skills': rate_Troubleshooting_skills,
#     'rate_graphic_designing': rate_graphic_designing
# }

    #  testdata=pd.DataFrame({'x':skills}).transpose()
    #  resultdata=model.predict(testdata)[0]
    #  resultdata1= round(resultdata * 100, 2)
    #  return render(request, 'result.html', {'resultdata':resultdata,'resultdata1':resultdata1})
      # Make predictions using the trained model
     #dont delete it its for backup
     #dont delete it its for backup
     #dont delete it its for backup
     #dont delete it its for backup