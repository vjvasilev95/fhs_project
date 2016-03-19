# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from forms import UserProfileForm, UserForm, CategoryForm
from models import Category, Page
from models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import bing_search
import healthfinder_search, medlinePlus
from save_page_helper import *
from django.http import JsonResponse
import merge_by_relevance
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def track_category(request):
    cat_id = None
    url = '/fhs/'
    if request.method == 'GET':
        if 'cat_id' in request.GET:
            cat_id = request.GET['cat_id']
            try:
                category = Category.objects.get(id = cat_id)
                category.views += 1
                category.save()
                url = '/fhs/category/{}'.format(category.slug)
            except:
                pass
    return redirect(url)

def add_category(request):

    if request.is_ajax():
        name = request.POST['name']
        description = request.POST['description']
        shared = request.POST['shared']
        if (shared == "false"):
            shared = False
        else:
            shared = True

        existent_category = Category.objects.filter(name = name)

        if not existent_category:
            #Create a new category
            category = Category(user = request.user, name=name, description=description, shared=shared)

            #Saves it
            category.save()

            return HttpResponse("Success")
        else:
            return HttpResponse("Existent category")

    if request.method == "POST":
        category_form = CategoryForm(data=request.POST)
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


def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'fhs/category.html', context_dict)

def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/fhs/')

def index(request):
    if request.user.is_authenticated():
        public_categories = Category.objects.filter(shared=True).order_by('-views')
    else :
        public_categories = Category.objects.filter(shared=True).order_by('-views')[:5]
    return render(request, 'fhs/index.html', {'public_categories': public_categories})

def register(request):

    email_in_db = False
    registered = False
    username_taken = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            #check if email is in the database
            email_to_be_checked = user.email
            #if no user has this email, the query will result in an error, then
            #the except statement will be executed, resulting in a successful registration
            try:
                test_user = User.objects.get(email=email_to_be_checked)
                email_in_db = True
            except User.DoesNotExist:
                #save user and user_profile, and sign in the user with the non-hashed password
                non_hashed_password = user.password
                user.set_password(non_hashed_password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                profile.save()
                registered = True
                #In the end, log the user into the system
                theUser = authenticate(username=user.username, password=non_hashed_password)
                login(request, theUser)
        else:
            #convert the errors into a json format
            user_form_errors = json.loads(user_form.errors.as_json())
            #check if the user_form error was raised because someone tried to register with a username that is already in the dbs
            if user_form_errors.has_key("username") and \
                user_form_errors['username'][0]['message'] == "User with this Username already exists.":
                username_taken = True
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'fhs/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
             'email_in_db':email_in_db, 'username_taken':username_taken})


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

@login_required
def search(request):


    results_from_bing = []
    results_from_healthgov = []
    results_from_medline = []
    context_dict = {}
    results_mashup = []
    categories = Category.objects.filter(user=request.user)
    public_categories = Category.objects.filter(shared=True)
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
            results_from_medline = medlinePlus.run_query(query)

            results_mashup = merge_by_relevance.merge(results_from_bing, results_from_medline, results_from_healthgov)
            print len(results_mashup)
    context_dict['query'] = query
    context_dict['age'] = age
    context_dict['gender'] = gender
    context_dict['results_from_bing'] = results_from_bing
    context_dict['results_from_healthgov'] = results_from_healthgov
    context_dict['results_from_medline'] = results_from_medline
    context_dict['categories'] = categories
    context_dict['public_categories'] = public_categories
    context_dict['results_mashup'] = results_mashup

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

        #Checks if we already have the same page in the category
        try:
            existent_page = Page.objects.filter(title=title, category=category)
        except:
            existent_page = None

        if not existent_page:

            #Strips the page out of unnecessary html tags and content
            try:
                content = filter_content(request.POST['source'], url)
            except ValueError as e:
                json_response = {"response": "Problem while fetching the resource"}
                return JsonResponse(json_response)

            #Calculates the flesh score, sentiment score and subjectivity score of the content
            stats = calculate_stats(content)

            #Creates a new page
            page = Page(category = category, title = title, summary = summary, url = url,
                    flesch_score = stats['flesh_score'], sentiment_score = stats['polarity'], subjectivity_score = stats['subjectivity'])

            #Saves it
            page.save()

            json_response = {"response": "Success", "category": category.slug}
            return JsonResponse(json_response)

        else:
            json_response = {"response": "Existent page", "category": category.slug}
            return JsonResponse(json_response)


    else:
        # If the request was not a POST, display the form to enter details.
        return HttpResponseRedirect('/fhs/')


def about(request):
    return render(request, 'fhs/about.html', {})

def privacy(request):
    return render(request, 'fhs/privacy.html', {})

def terms(request):
    return render(request, 'fhs/terms.html', {})


@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    public_categories = Category.objects.filter(user=request.user)
    return render(request, 'fhs/profile.html', {"profileuser":user, 'public_categories': public_categories})

def editprofile(request):
    user = User.objects.get(username=request.user)
    return render(request, 'fhs/editprofile.html', {"profileuser":user})

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with).exclude(shared=False)
    if max_results > 0:
        if cat_list.count() > max_results:
            cat_list = cat_list[:max_results]

    return cat_list

def suggest_category(request):

    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    cat_list = get_category_list(8, starts_with)

    if request.GET['page'] == "search":
        return render(request, 'fhs/cats.html', {'cats': cat_list })
    else:
        print "I am here"
        return render(request, 'fhs/index_cats.html', {'cats': cat_list })

