from collections import OrderedDict
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from .fetch import *

from .models import *


def start_app(request):
    return render(request, 'index.html')


def login_page(request):
    if(request.user.is_authenticated):
        return redirect('/dailytask/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if(user == None):
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        login(request, user)
        return redirect('dailytask')
    return render(request, 'login.html')


def register_page(request):
    if(request.user.is_authenticated):
        return redirect('/dailytask/')
    if request.method == 'POST':
        email = request.POST['email']
        cf_handle = request.POST['discord_handle']
        username = request.POST['username']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        cat1 = request.POST.get('CP1')
        cat2 = request.POST.get('CP2')
        # cat3 = request.POST.get('DSA1')
        # cat4 = request.POST.get('DSA2')
        cat5 = request.POST.get('CP3')
        id = len(Customer.objects.all())+1
        if(len(User.objects.filter(username=username)) > 0):
            return render(request, 'register.html', {'error': 'Username already exists'})
        if(cat1 == None and cat2 == None and cat5 == None):
            return render(request, 'register.html', {'error': 'Please select atleast one category'})
        if(password1 != password2):
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if(len(User.objects.filter(email=email)) > 0):
            return render(request, 'register.html', {'error': 'Email already exists'})
        if(len(phone) != 10):
            return render(request, 'register.html', {'error': 'Invalid phone number'})
        person = User(id=id, email=email,
                      username=username, password=password1)
        person.set_password(password1)
        person.save()
        op1 = (cat1 == 'on')
        op2 = (cat2 == 'on')
        # op3 = (cat3=='on')
        # op4 = (cat4=='on')
        op5 = (cat5 == 'on')
        student = Customer(email=email, cf_handle=cf_handle, username=person, phone=phone,
                           CP1=op1, CP2=op2, CP3=op5, DSA1=False, DSA2=False)
        student.save()
        return redirect('/login/')
    return render(request, 'register.html')


def customer(request, pk_test):
    student = Customer.objects.get(id=pk_test)
    context = {
        "username": student.username,
        "category": student.category,
    }
    # return render(request, 'index.html')
    return render(request, 'customer.html', {'context': context})


@login_required(login_url='login')
def resources_page(request):
    all_resources = []
    customer = Customer.objects.get(username=request.user.id)
    if(Customer.objects.get(username=request.user.id).CP1):
        all_resources.append(Resources.objects.filter(category='CP1'))
    if(Customer.objects.get(username=request.user.id).CP2):
        all_resources.append(Resources.objects.filter(category="CP2"))
    if(Customer.objects.get(username=request.user.id).CP3):
        all_resources.append(Resources.objects.filter(category="CP3"))
    if(Customer.objects.get(username=request.user.id).DSA1):
        all_resources.append(Resources.objects.filter(category="DSA1"))
    if(Customer.objects.get(username=request.user.id).DSA2):
        all_resources.append(Resources.objects.filter(category="DSA2"))
    alllinks = {}
    for resources in all_resources:
        for temp in resources:
            local = {
                'link': temp.link,
                'slides': temp.slides
            }
            alllinks[temp.description] = local
    alllinks = OrderedDict(reversed(list(alllinks.items())))
    return render(request, 'resources.html', {'alllinks': alllinks})


@login_required(login_url='login')
def dailytask_page(request):
	dailytask = {}
	all_tasks = []
	category = ""
	handle = Customer.objects.get(username=request.user.id).cf_handle
	if(Customer.objects.get(username=request.user.id).CP1):
		category = 'CP1'
		all_tasks.append(DailyTask.objects.filter(category='CP1'))
	if(Customer.objects.get(username=request.user.id).CP2):
		category = 'CP2'
		all_tasks.append(DailyTask.objects.filter(category="CP2"))
	if(Customer.objects.get(username=request.user.id).CP3):
		category = 'CP3'
		all_tasks.append(DailyTask.objects.filter(category="CP3"))
	if(Customer.objects.get(username=request.user.id).DSA1):
		all_tasks.append(DailyTask.objects.filter(category="DSA1"))
	if(Customer.objects.get(username=request.user.id).DSA2):
		all_tasks.append(DailyTask.objects.filter(category="DSA2"))
	time = datetime.datetime.now()
	delta = datetime.timedelta(2)
	time = time-delta
	alllinks = {}
	for dailytask in all_tasks:
		for temp in dailytask:
			current = (temp.date_created)
			current = datetime.datetime(current.year, current.month, current.day)
			if(time < current):
				done=fetch_call(handle,category,temp.link)
				local={}
				if done:
					local = {
						'link': temp.link,
						'done' : {'answer': 'done'}
						}
				else: 
					local = {
						'link': temp.link,
						'done': None,
					}
				alllinks[temp.description] = local
	alllinks = OrderedDict(reversed(list(alllinks.items())))
	return render(request, 'dailytask.html', {'alllinks': alllinks})


@login_required(login_url='login')
def leaderboard_page(request):
	all_scores = []
	category = ""
	# current user ki category
	if(Customer.objects.get(username=request.user.id).CP1):
		category = 'CP1'
	if(Customer.objects.get(username=request.user.id).CP2):
		category = 'CP2'
	if(Customer.objects.get(username=request.user.id).CP3):
		category = 'CP3'

	# all users ki category
	for student in Customer.objects.all():
		if(category == 'CP1' and student.CP1):
			current_score = get_lb1(student.cf_handle)
			if(current_score >= student.score1):
				student.score1 = current_score
				student.save()
			all_scores.append([student.score1, student.cf_handle])
		if(category == 'CP2' and student.CP2):
			current_score = get_lb2(student.cf_handle)
			if(current_score >= student.score2):
				student.score2 = current_score
				student.save()
			all_scores.append([student.score2, student.cf_handle])
		if(category == 'CP3' and student.CP3):
			current_score = get_lb3(student.cf_handle)
			if(current_score >= student.score3):
				student.score3 = current_score
				student.save()
			all_scores.append([student.score3, student.cf_handle])

	# sorting and taking top 3
	all_scores.sort(reverse=True)
	# print(all_scores)
	sendingvalues = {}
	index = min(3, len(all_scores))
	for i in range(min(3, len(all_scores))):
		temp = {}
		for j in range(index):
			temp[j] = j
		index -= 1
		sendingvalues[all_scores[i][1]] = {
			'star': temp, 'score': all_scores[i][0]}

	# print(sendingvalues)
	if(Customer.objects.get(username=request.user.id).cf_handle not in sendingvalues.keys()):
		if(Customer.objects.get(username=request.user.id).CP3):
			sendingvalues['Your score'] = {
				'star': {}, 'score': Customer.objects.get(username=request.user.id).score3}
		elif(Customer.objects.get(username=request.user.id).CP2):
			sendingvalues['Your score'] = {
				'star': {}, 'score': Customer.objects.get(username=request.user.id).score2}
		elif(Customer.objects.get(username=request.user.id).CP1):
			sendingvalues['Your score'] = {
				'star': {}, 'score': Customer.objects.get(username=request.user.id).score1}
	return render(request, 'leaderboard.html', {'leaderboard': sendingvalues})


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


def contact_page(request):
    return render(request, 'contactus.html')


def team_page(request):
    return render(request, 'team.html')


@login_required(login_url='login')
def allq_page(request):
    dailytask = {}
    all_tasks = []
    if(Customer.objects.get(username=request.user.id).CP1):
        all_tasks.append(DailyTask.objects.filter(category='CP1'))
    if(Customer.objects.get(username=request.user.id).CP2):
        all_tasks.append(DailyTask.objects.filter(category="CP2"))
    if(Customer.objects.get(username=request.user.id).CP3):
        all_tasks.append(DailyTask.objects.filter(category="CP3"))
    if(Customer.objects.get(username=request.user.id).DSA1):
        all_tasks.append(DailyTask.objects.filter(category="DSA1"))
    if(Customer.objects.get(username=request.user.id).DSA2):
        all_tasks.append(DailyTask.objects.filter(category="DSA2"))
    alllinks = {}
    for dailytask in all_tasks:
        for temp in dailytask:
            local = {
                'link': temp.link,
            }
            alllinks[temp.description] = local
    alllinks = OrderedDict(reversed(list(alllinks.items())))
    return render(request, 'allques.html', {'alllinks': alllinks})
