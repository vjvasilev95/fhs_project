# -*- coding: utf-8 -*-

from django.shortcuts import render
from forms import UserProfileForm, UserForm, CategoryForm
from models import Category, Page

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import bing_search
import healthfinder_search, medlinePlus
from save_page_helper import *
from django.template import RequestContext
from endless_pagination.decorators import page_template

def add_category(request):
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

    context_dict['query'] = query
    context_dict['age'] = age
    context_dict['gender'] = gender
    context_dict['results_from_bing'] = results_from_bing
    context_dict['results_from_healthgov'] = results_from_healthgov
    context_dict['results_from_medline'] = results_from_medline
    context_dict['categories'] = categories
    context_dict['public_categories'] = public_categories

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
                return HttpResponse("Problem while fetching the resource")

            #Calculates the flesh score, sentiment score and subjectivity score of the content
            stats = calculate_stats(content)

            #Creates a new page
            page = Page(category = category, title = title, summary = summary, url = url,
                    flesch_score = stats['flesh_score'], sentiment_score = stats['polarity'], subjectivity_score = stats['subjectivity'])

            #Saves it
            page.save()
        else:
            return HttpResponse("Existent page")


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

# @page_template('fhs/entry_index_page.html')  # just add this decorator
# def entry_index(
#         request, template='fhs/entry_index.html', extra_context=None):
#     context = {
#         'entries': Page.objects.all(),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#     return render(request, template, context, context_instance=RequestContext(request))