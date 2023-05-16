
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
from django.shortcuts import render, redirect





import io
import re
import nltk
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect



dataScience_keywords = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
webDevelopment_keywords = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular js', 'c#', 'flask']
android_keywords = ['android','android development','flutter','kotlin','xml','kivy']
ios_keywords = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
uiux_keywords = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']



recommended_skills_dict = {
    'Data Science': ['numpy', 'pandas', 'scikit-learn', 'matplotlib'],
    'Web Development': ['HTML', 'CSS', 'JavaScript', 'React', 'Django'],
    'Android Development': ['Java', 'Android Studio', 'Kotlin'],
    'iOS Development': ['Swift', 'Xcode', 'Objective-C'],
    'UI/UX Design': ['Adobe XD', 'Figma', 'Sketch', 'InVision']
}
# def process_pdf(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         pdf_file = request.FILES['pdf_file']
#         instance = PDFFile(name=name, file=pdf_file)
#         instance.save()

#         # Extract key information from the PDF file
#         extracted_data = extract_information_from_pdf(pdf_file)

#         # Fetch further details from the extracted data
#         email = extracted_data.get('Email')
#         skills = extracted_data.get('Skills and Technologies')
#         num_pages = extracted_data.get('Number of Pages')

#         # Do further processing with the extracted details
#         # ...

#         # Pass the extracted data and additional details to the template for rendering
#         return render(request, 'pdf_detail.html', {'pdf_file': instance, 'name': name, 'email': email, 'skills': skills, 'num_pages': num_pages})

#     pdf_files = PDFFile.objects.all()
#     return render(request, 'upload_pdf.html', {'pdf_files': pdf_files})

def extract_information_from_pdf(pdf_file):
    # Create a BytesIO object to store the PDF file
    pdf_buffer = io.BytesIO(pdf_file.read())

    # Extract text from the PDF file
    output_string = io.StringIO()
    pdf_reader = PdfReader(pdf_buffer)

    for page in pdf_reader.pages:
        output_string.write(page.extract_text())

    # Get the text as a string
    text = output_string.getvalue()

    # Extract the section containing the name
    line_break_index = text.find('\n')
    name_section = text[:line_break_index]

    # Extract email addresses
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    email = emails[0] if emails else ""

    # Define the patterns to extract skills and technologies
    skill_patterns = [
        r'(?i)\b((?:Java|Data Structure|MongoDB|IBM Cognos|C#|Perl|ASP.NET|Excel|Python|C\+\+|JavaScript|PHP|Ruby|Swift|Objective-C)\s*(?:programming)?\s*(?:language|lang|developer)?)\b',
        r'(?i)\b((?:HTML|CSS|React|Vue\.js|Angular|Node\.js|jQuery|Bootstrap)\s*(?:developer|designer|framework|library|tool)?)\b',
        r'(?i)\b((?:SQL|MySQL|PostgreSQL|Oracle)\s*(?:database|DBA|developer|admin)?)\b',
        r'(?i)\b((?:Linux|Unix|Windows|MacOS)\s*(?:system)?\s*(?:administration|admin|developer|user)?)\b',
        r'(?i)\b((?:Git|JIRA|Trello|Slack)\s*(?:management)?\s*(?:tool|software)?)\b',
    ]

    # Create a set to store unique skills and technologies
    unique_skills = set()

    # Extract skills and technologies from the text
    remaining_text = text[line_break_index + 1:]  # Exclude the name section
    sentences = nltk.sent_tokenize(remaining_text)

    for sentence in sentences:
        # Extract skills and technologies that match the patterns
        for pattern in skill_patterns:
            matches = re.findall(pattern, sentence)
            unique_skills.update(matches)  # Add
    num_pages = len(pdf_reader.pages)

# Store the extracted data in a dictionary
    extracted_data = {
    "Name": name_section.strip() if name_section else "",
    "Email": email,
    "Skills and Technologies": list(unique_skills),
    "Number of Pages": num_pages,
}

    return extracted_data
def get_matching_keyword(skills):
    weights = {
        'Data Science': 0,
        'Web Development': 0,
        'Android Development': 0,
        'iOS Development': 0,
        'UI/UX Design': 0
    }
    
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in [keyword.lower() for keyword in dataScience_keywords]:
            weights['Data Science'] += 1
        elif skill_lower in [keyword.lower() for keyword in webDevelopment_keywords]:
            weights['Web Development'] += 1
        elif skill_lower in [keyword.lower() for keyword in android_keywords]:
            weights['Android Development'] += 1
        elif skill_lower in [keyword.lower() for keyword in ios_keywords]:
            weights['iOS Development'] += 1
        elif skill_lower in [keyword.lower() for keyword in uiux_keywords]:
            weights['UI/UX Design'] += 1
    
    # Get the category with the highest weight
    matching_keyword = max(weights, key=weights.get)
    
    return matching_keyword

from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFDocument


from django.shortcuts import render, redirect
from .forms import PDFUploadForm

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save()  # Save the form and get the PDFDocument object
            return redirect('view_pdf', pdf_id=pdf.pk)  # Redirect to the view_pdf page
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import PDFDocument

def view_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFDocument, id=pdf_id)
    document_name = pdf.Name

    # Call the extract_information_from_pdf function
    extracted_data = extract_information_from_pdf(pdf.pdf_file)
    skills = extracted_data.get("Skills and Technologies", [])
    matching_keyword = get_matching_keyword(skills)
    print(matching_keyword)
    recommended_skills = []
    if matching_keyword:
            recommended_skills = recommended_skills_dict.get(matching_keyword, [])
            print(recommended_skills)
            
            # Get the recommended courses for the matching keyword
    # recommended_courses = []
    # if matching_keyword:
    #         recommended_courses = courserecommendation(matching_keyword)


    return render(request, 'pdf_detail.html', {'pdf': pdf, 'document_name': document_name, 'extracted_data': extracted_data,'matching_keyword': matching_keyword,'recommended_skills':recommended_skills})

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

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.shortcuts import render

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
    # Create the data for the pie chart
        labels = top3_labels
        values = proba[0][top3_matches] * 100

        # Create the pie chart trace
        trace = go.Pie(
            labels=labels,
            values=values,
            hoverinfo='label+percent',
            textinfo='percent',
            textfont=dict(size=14),
            marker=dict(colors=['rgb(50, 100, 200)', 'rgb(200, 50, 100)', 'rgb(100, 200, 50)'])
        )

        # Create the layout with increased size
        layout = go.Layout(
            title='Top Career Matches',
            height=600,
            width=800
        )

        # Create the figure
        fig = go.Figure(data=[trace], layout=layout)

        # Convert the figure to HTML
        chart_data = fig.to_html()

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