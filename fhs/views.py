# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from forms import UserProfileForm, UserForm, PageForm, CategoryForm
from models import Category, Page

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import bing_search
import healthfinder_search
from bs4 import BeautifulSoup
import urllib2
from textstat.textstat import textstat
from textblob import TextBlob
import html_parser

def add_category(request):
    if request.method == "POST":
        category_form = CategoryForm(data = request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user = request.user
            category.save()
            return HttpResponseRedirect('/fhs/')
        else:
            print category_form.errors

    category_form = CategoryForm()
    print "return that form"
    return render(request, "fhs/add_category.html", {'category_form': category_form})

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/fhs/')

def index(request):
    public_categories = Category.objects.filter(shared=True)

    return render(request, 'fhs/index.html', {'public_categories': public_categories})

def register(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'fhs/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(username=username, password=password)


        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/fhs/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your fhs account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:

        return render(request, 'fhs/login.html', {})

def search(request):


    results_from_bing = []
    results_from_healthgov = []
    results_from_medline = []
    context_dict = {}
    result_list = []
    categories = Category.objects.filter(user=request.user)
    query = None
    age = None
    gender = "male"

    if request.method == 'POST':
        query = request.POST['query'].strip()
        age = request.POST['age']
        gender = request.POST['gender']

        if query and age and gender:
            # Run our Bing function to get the results list!

            results_from_bing = bing_search.run_query(query)
            results_from_healthgov = healthfinder_search.run_query(query, age, gender)

    context_dict['query'] = query
    context_dict['age'] = age
    context_dict['gender'] = gender
    context_dict['results_from_bing'] = results_from_bing
    context_dict['results_from_healthgov'] = results_from_healthgov
    context_dict['results_from_medline'] = results_from_medline
    context_dict['categories'] = categories

    return render(request, 'fhs/search.html', context_dict)

    #         result_list = run_query(query)
    #
    # return render(request, 'fhs/search.html', {'result_list': result_list, 'categories': categories})

def save_page(request):
    if request.method == 'POST':

        url = request.POST['url']
        title = request.POST['title']
        summary = request.POST['summary']
        category = Category.objects.get(name=request.POST['category'])


        html_file = urllib2.urlopen(url)
        html_doc = html_file.read()
        html_file.close()
        soup = BeautifulSoup(html_doc, 'html.parser')

        if request.POST['source'] == 'healthgov':


            content = soup.select(".entry-content-top")
            content.append(soup.select(".entry-content-main"))
            content.append(soup.select(".page"))
            content_string = ""

            for div in content:
                content_string += str(div)

            content_string = html_parser.strip_tags(content_string)
            content_string = unicode(content_string, "utf-8")

            testimonial = TextBlob(content_string)

            polarity = testimonial.sentiment.polarity
            subjectivity = testimonial.sentiment.subjectivity

            flesh_score = textstat.flesch_reading_ease(content_string)

            page = Page(category = category, title = title, summary = summary, url = url, flesch_score = flesh_score, sentiment_score = polarity, subjectivity_score = subjectivity)
            page.save()

        elif request.POST['source'] == 'bing':
            soup = html_parser.strip_tags(soup)
            soup = unicode(soup, "utf-8")
            page = Page(category = category, title = title, summary = summary, url = url)
            page.save()

        else:
            page = Page(category = category, title = title, summary = summary, url = url)
            page.save()
    else:
        # If the request was not a POST, display the form to enter details.
        return HttpResponseRedirect('/fhs/')

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return HttpResponse("")


def about(request):
    return render(request, 'fhs/about.html', {})

def privacy(request):
    return render(request, 'fhs/privacy.html', {})

def terms(request):
    return render(request, 'fhs/terms.html', {})
