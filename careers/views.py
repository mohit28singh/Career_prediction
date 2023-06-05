
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

import re
import nltk
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect

nltk.download("punkt")

dataScience_keywords = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep learning', 'flask', 'streamlit', 'numpy', 'pandas', 'scikit-learn', 'matplotlib', 'data analysis', 'data visualization', 'statistics', 'data mining', 'natural language processing', 'computer vision', 'neural networks', 'linear regression', 'logistic regression', 'decision trees', 'random forests', 'gradient boosting', 'clustering', 'dimensionality reduction', 'time series analysis']

webDevelopment_keywords = ['react', 'django', 'node.js', 'react.js', 'php', 'laravel', 'magento', 'wordpress', 'javascript', 'angular.js', 'c#', 'flask', 'HTML', 'CSS', 'responsive design', 'RESTful APIs', 'version control', 'UX/UI design', 'front-end development', 'back-end development', 'database management', 'web security', 'user experience']

android_keywords = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy', 'Java', 'Android Studio', 'Android SDK', 'mobile app development', 'UI design', 'UX design', 'Firebase', 'RESTful APIs', 'SQLite', 'MVC pattern', 'material design', 'push notifications', 'memory management', 'performance optimization']

ios_keywords = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode', 'Objective-C', 'iOS SDK', 'Core Data', 'Auto Layout', 'App Store submission', 'push notifications', 'memory management', 'user interface design', 'user experience design', 'widget development', 'localization']

uiux_keywords = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyboards', 'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator', 'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign', 'indesign', 'wireframing', 'solid grasp', 'user research', 'user experience design', 'visual design', 'interaction design', 'usability testing']




recommended_skills_dict ={
    'Data Science': ['numpy', 'pandas', 'scikit-learn', 'matplotlib', 'tensorflow', 'keras', 'pytorch', 'sql', 'big data', 'data visualization',
                     'natural language processing', 'deep learning', 'time series analysis', 'feature engineering', 'data preprocessing',
                     'model evaluation', 'ensemble methods', 'cross-validation', 'dimensionality reduction', 'cluster analysis',
                     'hyperparameter tuning', 'data wrangling', 'data mining', 'statistical analysis', 'predictive modeling'],
    'Web Development': ['HTML', 'CSS', 'JavaScript', 'React', 'Django', 'Node.js', 'Express.js', 'Vue.js', 'Angular', 'RESTful APIs',
                        'MERN stack', 'LAMP stack', 'front-end development', 'back-end development', 'responsive web design',
                        'version control (Git)', 'UI/UX principles', 'web performance optimization', 'SEO'],
    'Android Development': ['Java', 'Android Studio', 'Kotlin', 'Android SDK', 'Firebase', 'RESTful APIs', 'SQLite', 'MVVM architecture',
                            'material design', 'Google Play Store submission', 'push notifications', 'background tasks',
                            'unit testing', 'debugging', 'memory management', 'performance optimization'],
    'iOS Development': ['Swift', 'Xcode', 'Objective-C', 'iOS SDK', 'Core Data', 'Auto Layout', 'CocoaPods', 'App Store submission',
                        'push notifications', 'Core Animation', 'Core Graphics', 'memory management', 'UI/UX guidelines',
                        'localization', 'In-App Purchases', 'widget development'],
    'UI/UX Design': ['Adobe XD', 'Figma', 'Sketch', 'InVision', 'user research', 'wireframing', 'prototyping', 'user personas',
                     'information architecture', 'interaction design', 'visual design', 'usability testing', 'design thinking',
                     'responsive design', 'typography', 'color theory', 'motion design', 'user-centered design'],
}

courses_dict = {
    'Data Science': [
        ['Machine Learning Crash Course by Google', 'https://developers.google.com/machine-learning/crash-course'],
        ['Machine Learning A-Z by Udemy', 'https://www.udemy.com/course/machinelearning/'],
        ['Machine Learning by Andrew NG', 'https://www.coursera.org/learn/machine-learning'],
        ['Data Scientist Master Program of Simplilearn (IBM)', 'https://www.simplilearn.com/big-data-and-analytics/senior-data-scientist-masters-program-training'],
        ['Data Science Foundations: Fundamentals by LinkedIn', 'https://www.linkedin.com/learning/data-science-foundations-fundamentals-5'],
        ['Data Scientist with Python', 'https://www.datacamp.com/tracks/data-scientist-with-python'],
        ['Programming for Data Science with Python', 'https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104'],
        ['Programming for Data Science with R', 'https://www.udacity.com/course/programming-for-data-science-nanodegree-with-R--nd118'],
        ['Introduction to Data Science', 'https://www.udacity.com/course/introduction-to-data-science--cd0017'],
        ['Intro to Machine Learning with TensorFlow', 'https://www.udacity.com/course/intro-to-machine-learning-with-tensorflow-nanodegree--nd230']
    ],
    'Web Development': [
        ['Django Crash course', 'https://youtu.be/e1IyzVyrLSU'],
        ['Python and Django Full Stack Web Developer Bootcamp', 'https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp'],
        ['React Crash Course', 'https://youtu.be/Dorf8i6lCuk'],
        ['ReactJS Project Development Training', 'https://www.dotnettricks.com/training/masters-program/reactjs-certification-training'],
        ['Full Stack Web Developer - MEAN Stack', 'https://www.simplilearn.com/full-stack-web-developer-mean-stack-certification-training'],
        ['Node.js and Express.js [Free]', 'https://youtu.be/Oe421EPjeBE'],
        ['Flask: Develop Web Applications in Python', 'https://www.educative.io/courses/flask-develop-web-applications-in-python'],
        ['Full Stack Web Developer by Udacity', 'https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044'],
        ['Front End Web Developer by Udacity', 'https://www.udacity.com/course/front-end-web-developer-nanodegree--nd0011'],
        ['Become a React Developer by Udacity', 'https://www.udacity.com/course/react-nanodegree--nd019']
    ],
     'Android Development': [
        ['Android Development for Beginners', 'https://youtu.be/fis26HvvDII'],
        ['Android App Development Specialization', 'https://www.coursera.org/specializations/android-app-development'],
        ['Associate Android Developer Certification', 'https://grow.google/androiddev/#?modal_active=none'],
        ['Become an Android Kotlin Developer by Udacity', 'https://www.udacity.com/course/android-kotlin-developer-nanodegree--nd940'],
        ['Android Basics by Google', 'https://www.udacity.com/course/android-basics-nanodegree-by-google--nd803'],['The Complete Android Developer Course', 'https://www.udemy.com/course/complete-android-n-developer-course/'],
['Building an Android App with Architecture Components', 'https://www.linkedin.com/learning/building-an-android-app-with-architecture-components'],
['Android App Development Masterclass using Kotlin', 'https://www.udemy.com/course/android-oreo-kotlin-app-masterclass/'],
['Flutter & Dart - The Complete Flutter App Development Course', 'https://www.udemy.com/course/flutter-dart-the-complete-flutter-app-development-course/'],
['Flutter App Development Course [Free]', 'https://youtu.be/rZLR5olMR64']
],
'iOS Development': [
['IOS App Development by LinkedIn', 'https://www.linkedin.com/learning/subscription/topics/ios'],
['iOS & Swift - The Complete iOS App Development Bootcamp', 'https://www.udemy.com/course/ios-13-app-development-bootcamp/'],
['Become an iOS Developer', 'https://www.udacity.com/course/ios-developer-nanodegree--nd003'],
['iOS App Development with Swift Specialization', 'https://www.coursera.org/specializations/app-development'],
['Mobile App Development with Swift', 'https://www.edx.org/professional-certificate/curtinx-mobile-app-development-with-swift'],
['Swift Course by LinkedIn', 'https://www.linkedin.com/learning/subscription/topics/swift-2'],
['Objective-C Crash Course for Swift Developers', 'https://www.udemy.com/course/objectivec/'],
['Learn Swift by Codecademy', 'https://www.codecademy.com/learn/learn-swift'],
['Swift Tutorial - Full Course for Beginners [Free]', 'https://youtu.be/comQ1-x2a1Q'],
['Learn Swift Fast - [Free]', 'https://youtu.be/FcsY1YPBwzQ']
],
'UI/UX Design': [
['Google UX Design Professional Certificate', 'https://www.coursera.org/professional-certificates/google-ux-design'],
['UI / UX Design Specialization', 'https://www.coursera.org/specializations/ui-ux-design'],
['The Complete App Design Course - UX, UI and Design Thinking', 'https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
['UX & Web Design Master Course: Strategy, Design, Development', 'https://www.udemy.com/course/ux-web-design-master-course-strategy-design-development/'],
['The Complete App Design Course - UX, UI and Design Thinking', 'https://www.udemy.com/course/the-complete-app-design-course-ux-and-ui-design/'],
['DESIGN RULES: Principles + Practices for Great UI Design', 'https://www.udemy.com/course/design-rules/'],
['Become a UX Designer by Udacity', 'https://www.udacity.com/course/ux-designer-nanodegree--nd578'],
['Adobe XD Tutorial: User Experience Design Course [Free]', 'https://youtu.be/68w2VwalD5w'],
['Adobe XD for Beginners [Free]', 'https://youtu.be/WEljsc2jorI'],
['Adobe XD in Simple Way', 'https://learnux.io/course/adobe-xd']
]
}
def courserecommendation(matching_keyword):
    recommended_courses = []
    if matching_keyword:
        recommended_courses = courses_dict.get(matching_keyword, [])
        recommended_courses = [
            f'<a href="{course[1]}">{course[0]}</a>'
            for course in recommended_courses
        ]
    return ', '.join(recommended_courses)


import re

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

    # Define the phone number pattern for 10 digits
    phone_number_pattern = r'\b\d{10,12}\b'

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

    # Check for the presence of a phone number using regular expression
    phone_numbers = re.findall(phone_number_pattern, text)
    phone_number = phone_numbers[0] if phone_numbers else ""

    # Store the extracted data in a dictionary
    extracted_data = {
        "Name": name_section.strip() if name_section else "",
        "Email": email,
        "Skills and Technologies": list(unique_skills),
        "Number of Pages": num_pages,
        "Phone Number": phone_number,
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

from .forms import PDFUploadForm
@login_required(login_url='/')
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
    print(extracted_data)
    print(extracted_data.get("Email"))
    print(extracted_data.get("Phone Number"))
    skills = extracted_data.get("Skills and Technologies", [])
    skills = [skill.strip() for skill in skills]
    skills = list(set(skills))
    print(skills)
    
    # Check if fields are accessible
    messages = []
    if not extracted_data.get("Name", ""):
        messages.append("Name field is empty or invalid type!")
    if not extracted_data.get("Email", ""):
        messages.append("Email field is empty or invalid type!")
    if not extracted_data.get("Skills and Technologies", []):
        messages.append("Skills field is either empty or not in the right format")
    if not extracted_data.get("Phone Number", ""):
        messages.append("Phone number is missing or inaccessible")
    print(messages)
    
    matching_keyword = get_matching_keyword(skills)
    recommended_skills = []
    if matching_keyword:
        recommended_skills = recommended_skills_dict.get(matching_keyword, [])
            
    # Get the recommended courses for the matching keyword
    recommended_courses = []
    if matching_keyword:
        recommended_courses = courserecommendation(matching_keyword)
    
    # Generate recommendations for missing fields
    missing_fields_recommendations = []
    if not skills:
        missing_fields_recommendations.append("Skills section is either empty or does not contain relevant skills. We recommend including key skills and technologies that are relevant to your desired job profile. Highlighting your skills can greatly enhance your resume and increase your chances of success.")
    if not extracted_data.get("Email", ""):
        missing_fields_recommendations.append("Email address is either missing or not recognized. Please ensure that the email address is provided in a valid format (e.g., example@example.com) or try reformatting it according to  ATS system.")
    if not extracted_data.get("Phone Number", ""):
        missing_fields_recommendations.append("Phone number is either missing or not recognized.Please ensure that the phone number is provided in a recognized format or try reformatting it according to our ATS system..")
    all_fields_present = extracted_data.get("Email") and skills and extracted_data.get("Phone Number")
    return render(request, 'pdf_detail.html', {'pdf': pdf, 'document_name': document_name, 'extracted_data': extracted_data,
                                                'matching_keyword': matching_keyword, 'skills': skills,
                                                'recommended_skills': recommended_skills,
                                                'recommended_courses': recommended_courses, 'messages': messages,
                                                'missing_fields_recommendations': missing_fields_recommendations,'all_fields_present': all_fields_present
                                                })

def home(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    return render(request, 'main.html', {'user': user})
def homepage(request):
    return render(request, 'main.html')
def redirect_to_mohit_linkedin(request):
    return redirect('https://www.linkedin.com/in/mohit-singh-210036185/')

def redirect_to_prachi_linkedin(request):
    return redirect('https://www.linkedin.com/in/prachi-singh-9044b31ab/')


def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
             messages.error(request, 'Passwords do not match')
             return redirect('/')
        
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        
        return HttpResponse('<script>alert("User created successfully!"); window.location.href = "/";</script>')
    
    return redirect('/')



from django.contrib import messages
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid password')
            return redirect('/')
            
    return redirect('login')

def LogoutPage(request):
     logout(request)
     return render(request,'main.html')
 


@login_required(login_url='/')
def careerprediction(request):
    if request.user.is_authenticated:
        return render(request, 'services.html')
    else:
        messages.warning(request, 'Please login to access this page.')
        return render(request, 'main.html')

def course(request):
    return render(request,"course.html")

from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact_message = ContactMessage.objects.create(name=name, email=email, message=message)
        print(contact_message)

        success_message = 'Your message has been sent successfully. We will get back to you soon!'
        return render(request, 'contact.html', {'success_message': success_message})

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
@login_required(login_url='/')
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
# print(type(model))c

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