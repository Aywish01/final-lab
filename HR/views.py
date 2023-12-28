import os  # Add this import statement at the beginning

from django.shortcuts import render, reverse
from .models import User, Employee, Complaints, Feedback
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime
import dateutil.parser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import nltk

sid = SentimentIntensityAnalyzer()


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/HR/home/')
            else:
                return HttpResponseRedirect("Account Disabled")
        else:
            print("Invalid credentials: {0}, {1}".format(username, password))
            return HttpResponseRedirect("Invalid login credentials")
    else:
        return render(request, 'HR/login.html', {})


@login_required(redirect_field_name='/HR/login/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/HR/home/')


def home(request):
    context = {}
    return render(request, 'HR/home.html', context)


def employee_profile(request):
    context = {}
    try:
        user = User.objects.get(username=request.user.username)
        emp = Employee.objects.get(emp=user)
        context["emp"] = emp
    except:
        pass
    return render(request, 'HR/employee_profile.html', context)


def employee_complaints(request):
    context = {}
    if request.method == 'POST':

        try:
            user = User.objects.get(username=request.user.username)
            emp = Employee.objects.get(emp=user)
            dt = dateutil.parser.parse(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
            complaint = Complaints(id=None, subject=request.POST.get('subject'), complaint_text=request.POST.get('text'), date_time=dt, complainant=emp.name, complaint=user)
            complaint.save()
        except:
            pass

    return render(request, 'HR/employee_complaints.html', context)


def employee_feedback(request):
    context = {}
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user.username)
            emp = Employee.objects.get(emp=user)
            try:
                feed = Feedback.objects.get(feed=user)
                feed.delete()
            except:
                pass
            dt = dateutil.parser.parse(datetime.now().strftime("%d/%m/%y %H:%M:%S"))
            data = request.POST.get('message')
            y = sid.polarity_scores(data)

            if y['compound'] >= 0.6:
                pol = "Extremely Positive"
            elif y['compound'] < 0.6 and y['compound'] >= 0.2:
                pol = "Positive"
            elif y['compound'] < 0.2 and y['compound'] >= -0.2:
                pol = "Neutral"
            elif y['compound'] < -0.2 and y['compound'] >= -0.6:
                pol = "Negative"
            else:
                pol = "Extremely Negative"
            feedback = Feedback(id=None, feedback_text=data, respondent=emp.name, polarity=pol, date_time=dt, feed=user)
            feedback.save()
        except:
            pass

    return render(request, 'HR/employee_feedback.html', context)


def dashboard(request):
    context = {}
    profiles = []
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        employees = Employee.objects.all()
        for emp in employees:
            profiles.append(emp)
    context["profiles"] = profiles
    return render(request, 'HR/dashboard.html', context)


def complaints(request):
    context = {}
    comp = []
    user = User.objects.get(username=request.user.username)
    if user.is_superuser:
        complaint = Complaints.objects.all()
        for i in complaint:
            comp.append(i)
    else:
        complaint = Complaints.objects.filter(complaint=user)
        for i in complaint:
            comp.append(i)
    context['complaints'] = comp

    return render(request, 'HR/complaints.html', context)


def pie_chart(reviews, label, graph_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)

    fig, ax = plt.subplots()
    ax.pie(reviews, labels=label, explode=(0.05, 0.05, 0.05, 0.05, 0.05),
           autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')

    # Use forward slashes in the file path
    graph_path = graph_path.replace('\\', '/')
    
    # Save the figure to the specified path
    fig.savefig(graph_path)
    plt.close(fig)



def feedback(request):
    context = {}
    rev = [0, 0, 0, 0, 0]
    feedbacks = []
    users = User.objects.all()
    for user in users:
        try:
            feed = Feedback.objects.get(feed=user)
            emp = Employee.objects.get(emp=user)
            feedbacks.append([emp, feed])
            if feed.polarity == 'Extremely Positive':
                rev[0] += 1
            elif feed.polarity == 'Positive':
                rev[1] += 1
            elif feed.polarity == 'Neutral':
                rev[2] += 1
            elif feed.polarity == 'Negative':
                rev[3] += 1
            else:
                rev[4] += 1

        except Feedback.DoesNotExist:
            pass  # Handle the specific exception for Feedback not found

    context["employees"] = feedbacks
    labels = ['Extremely Positive', 'Positive', 'Neutral', 'Negative', 'Extremely Negative']
    
    # Use os.path.join to create file paths
    graph_path = os.path.join("static", "HR", "graph.png")
    pie_chart(rev, labels, graph_path)  # Updated function call

    return render(request, 'HR/feedback.html', context)

def about(request):
    context = {}
    return render(request, 'HR/about.html', context)
