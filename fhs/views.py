# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import UserProfileForm, UserForm, CategoryForm, EmailForm
from models import Category, Page
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import bing_search
import healthfinder_search, medlinePlus
from save_page_helper import *
from django.http import JsonResponse
import merge_by_relevance

from django.contrib.auth import views

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def delete_category(request):
    if request.is_ajax():
        category_id = request.POST['cat_id']
        try:
            print "do we get here"
            theCategory=Category.objects.get(id = category_id)
            theCategory.delete()
            json_response={ "response": "Success"}
        except:
            json_response={"response": "Failure"}
    return JsonResponse(json_response)


def delete_page(request):
    if request.is_ajax():
        category_id = request.POST['cat_id']
        page_title = request.POST['page_title']
        try:
            theCategory = Category.objects.get(id=category_id)
            thePage = Page.objects.filter(title=page_title, category=theCategory)[0]
            thePage.delete()
            pages_count = len(Page.objects.filter(category=theCategory))
            json_response = {"response": "Success", 'pages_count':pages_count}
        except:
            json_response = {"response": "Failure"}
        return JsonResponse(json_response)


def track_category(request):
    cat_id = None
    url = '/fhs/'
    if request.method == 'GET':
        if 'cat_id' in request.GET:
            cat_id = request.GET['cat_id']
            try:
                category = Category.objects.get(id = cat_id)
                user = request.user
                if category.user != user:
                    category.views += 1
                    category.save()
                url = '/fhs/category/{}/{}/'.format(category.slug, cat_id)

            except:
                pass
    return redirect(url)


@login_required(login_url='/fhs/login/')
def add_category(request):

    if request.is_ajax():
        name = request.POST['name'].strip()
        description = request.POST['description']
        shared = request.POST['shared']

        if shared == "false":
            shared = False
        else:
            shared = True

        category = Category(user=request.user, name=name, description=description, shared=shared)

        # Saves it
        category.save()

        id = category.id

        category_url = Category.objects.get(id=id).slug

        return JsonResponse({"response":"Success", "category": category_url, "category_id": id })


    if request.method == "POST":
        category_data = request.POST
        category_data['name'] = category_data['name'].strip()
        if category_data['name'] == "":
            return render(request, "fhs/add_category.html", {"invalid": True})

        category_form = CategoryForm(data=category_data)
        if category_form.is_valid():
            try:
                category = category_form.save(commit=False)
                category.user = request.user
                category.save()

                return HttpResponseRedirect('/fhs/profile/'+request.user.username)
            except:
                return render(request, "fhs/add_category.html", {"existent": True})
        else:
            return render(request, "fhs/add_category.html", {"existent": True})

    return render(request, "fhs/add_category.html", {})


def category(request, category_name_slug, id):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug, id=id)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)[::-1]

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
        public_categories = Category.objects.filter(shared=True)
    else:
        public_categories = Category.objects.filter(shared=True)[:5]

    return render(request, 'fhs/index.html', {'public_categories': public_categories})


def register(request):

    email_in_db = False
    registered = False
    username_taken = False
    name = None
    email = None
    age = None
    gender = None

    if request.method == 'POST':
        user_data = request.POST
        user_data['username'] = user_data['username'].strip()
        user_form = UserForm(data=user_data)
        profile_form = UserProfileForm(data=request.POST)
        name = user_data['username']
        email = user_data['email']
        age = user_data['age']

        gender = user_data['gender']


        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # c heck if email is in the database
            email_to_be_checked = user.email
            # if no user has this email, the query will result in an error, then
            # the except statement will be executed, resulting in a successful registration
            try:
                test_user = User.objects.get(email=email_to_be_checked)
                email_in_db = True
            except User.DoesNotExist:
                # save user and user_profile, and sign in the user with the non-hashed password
                non_hashed_password = user.password
                user.set_password(non_hashed_password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user

                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                profile.save()
                registered = True
                # In the end, log the user into the system
                theUser = authenticate(username=user.username, password=non_hashed_password)
                login(request, theUser)
        else:
            # convert the errors into a json format
            user_form_errors = json.loads(user_form.errors.as_json())
            # check if the user_form error was raised because someone tried to register with a username that is already in the dbs
            if user_form_errors.has_key("username") and \
                user_form_errors['username'][0]['message'] == "User with this Username already exists.":
                username_taken = True

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'fhs/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered,
             'email_in_db':email_in_db, 'username_taken':username_taken, "name": name, "email": email, "age": age, "gender": gender})


def user_login(request):
    name = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = username
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/fhs/search/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your fhs account is disabled.")
        else:

            return render(request, 'fhs/login.html', {"invalid": True, "name": name})

    else:

        return render(request, 'fhs/login.html', {"name": name})


@login_required(login_url='/fhs/login/')
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

    display = True

    if request.method == 'POST':
        checked_box = request.POST.get('search-target', None)
        query = request.POST['query'].strip()
        # search for me
        if checked_box == "on":
            age = UserProfile.objects.get(user = request.user).age
            gender = UserProfile.objects.get(user = request.user).gender
            display=True
        else:
            age = request.POST['age']
            gender = request.POST['gender']
            display=False

        if query and age and gender:
            # Run our Bing function to get the results list!

            results_from_bing = bing_search.run_query(query)
            results_from_healthgov = healthfinder_search.run_query(query, age, gender)
            results_from_medline = medlinePlus.run_query(query)
            results_mashup = merge_by_relevance.merge(results_from_bing, results_from_medline, results_from_healthgov)
    context_dict['query'] = query
    context_dict['age'] = age
    context_dict['gender'] = gender
    context_dict['results_from_bing'] = results_from_bing
    context_dict['results_from_healthgov'] = results_from_healthgov
    context_dict['results_from_medline'] = results_from_medline
    context_dict['categories'] = categories
    context_dict['public_categories'] = public_categories
    context_dict['results_mashup'] = results_mashup
    context_dict['display'] = display

    return render(request, 'fhs/search.html', context_dict)


# Newly written save_page view, below it, commented, is the old one
def save_page(request):
    if request.method == 'POST':
        print request.POST
        url = request.POST['url']
        title = request.POST['title']
        summary = request.POST['summary']
        id = request.POST['id']
        print id
        category = Category.objects.get(id=id)
        print category
        source = request.POST['source']
        flesh_score = request.POST['flesh_score']
        polarity = request.POST['polarity']
        subjectivity = request.POST['subjectivity']
        # Checks if we already have the same page in the category
        try:
            existent_page = Page.objects.filter(title=title, category=category)
        except:
            existent_page = None

        if not existent_page:

            page = Page(category=category, title=title, summary=summary, url=url, source=source,
                    flesch_score=flesh_score, sentiment_score=polarity,
                    subjectivity_score=subjectivity)

            # Saves it
            page.save()

            json_response = {"response": "Success", "category_id": category.id, 'category': category.slug}
            return JsonResponse(json_response)

        else:
            json_response = {"response": "Existent page", "category": category.slug, "category_id": category.id}
            return JsonResponse(json_response)

    else:
        # If the request was not a POST, display the form to enter details.
        return HttpResponseRedirect('/fhs/search/')


def about(request):
    return render(request, 'fhs/about.html', {})


def privacy(request):
    return render(request, 'fhs/privacy.html', {})


def terms(request):
    return render(request, 'fhs/terms.html', {})


@login_required(login_url='/fhs/login/')
def profile(request, user):
    context_dict={}
    try:
        cat_list = get_category_list()
        user_can_edit=False
        userp = User.objects.get(username=user)

        context_dict = {'cat_list': cat_list}

        try:
            up = UserProfile.objects.get(user=userp)
        except:
            up = None

        context_dict['user'] = userp
        context_dict['userprofile'] = up

        if userp == User.objects.get(username=request.user):
            categories = Category.objects.filter(user=userp)
            deleted = False
            user_can_edit = True
            if request.method == "POST":
                some_var = request.POST.getlist('dependable')

                for id in some_var:
                    try:
                        Category.objects.get(id=id).delete()
                        deleted = True
                        print "hello"
                    except:
                        print "here?"
                        deleted = False
            context_dict['deleted'] = deleted
        else:
            categories = Category.objects.filter(user=userp, shared=True)
        context_dict['user_can_edit'] =user_can_edit
        context_dict['categories'] = categories
    except User.DoesNotExist:
        pass
    return render(request, 'fhs/profile.html', context_dict)


@login_required(login_url='/fhs/login/')
def editprofile(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        email = request.POST['email']
        try:
            existent_email = User.objects.get(email=email)
        except:
            existent_email = None

        if existent_email:
            return render(request, 'fhs/editprofile.html',{"existent": True})

        form = EmailForm(data=request.POST, instance=request.user)
        picform = UserProfileForm(data=request.POST, instance=request.user)
        try:
            up = UserProfile.objects.get(user=request.user)
        except:
            up = None
        if form.is_valid() and picform.is_valid():
            if email:
                user = form.save(commit=False)
                user.save()
            if 'picture' in request.FILES:
                up.picture = request.FILES['picture']
                up.save()
            return HttpResponseRedirect('/fhs/profile/'+user.username)
    else:
        return render(request, 'fhs/editprofile.html',{})


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
        return render(request, 'fhs/index_cats.html', {'cats': cat_list })


@login_required(login_url='/fhs/login/')
def change_password(request):
    form = PasswordReset(user=request.user)

    if request.method == 'POST':
        form = forms.PasswordReset(request.user,request.POST)
        if form.is_valid():
            the_form = form.save(commit=False)
            update_session_auth_hash(request, form.user)
        else:

            return render(request, 'fhs/changepassword.html', {
        'form': form,
        'error': True
    })

    return render(request, 'fhs/changepassword.html', {
        'form': form,
    })


def update_category_state(request):
    if request.is_ajax():
        id = request.POST['id']
        if request.POST['state'] == "true":
            state = True
        else :
            state = False

        try:
            category = Category.objects.get(id=id)
            category.shared = state
            category.save()
            return HttpResponse("Success")
        except:
            return HttpResponse("Error")

    return HttpResponseRedirect("/fhs/")
