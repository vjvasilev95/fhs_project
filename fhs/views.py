from django.shortcuts import render
from django.http import HttpResponse
from forms import UserProfileForm, UserForm, PageForm, CategoryForm
from models import Category

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import bing_search
import healthfinder_search

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

    result_list = []
    categories = Category.objects.filter(user=request.user)


    if request.method == 'POST':
        #print request.POST['query'].strip()
        query = request.POST['query'].strip()
        age = request.POST['age']
        gender = request.POST['gender']

        if query:
            # Run our Bing function to get the results list!

            results_from_bing = bing_search.run_query(query)
            results_from_healthgov = healthfinder_search.run_query(query, age, gender)

    #print results_from_bing

    return render(request, 'fhs/search.html', {'results_from_bing': results_from_bing,
                                               'results_from_healthgov':results_from_healthgov,
                                               'results_from_medline' : results_from_medline,
                                               'categories': categories,
                                               })

    #         result_list = run_query(query)
    #
    # return render(request, 'fhs/search.html', {'result_list': result_list, 'categories': categories})

def save_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            try:
                category = Category.objects.get(name=form.cleaned_data.get('category'))
            except Category.DoesNotExist:
                cat = None

            page = form.save(commit=False)
            page.category = category
            page.save()
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        return HttpResponseRedirect('/fhs/')

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return HttpResponseRedirect('/fhs/')


def about(request):
    return render(request, 'fhs/about.html', {})

def privacy(request):
    return render(request, 'fhs/privacy.html', {})

def terms(request):
    return render(request, 'fhs/terms.html', {})
