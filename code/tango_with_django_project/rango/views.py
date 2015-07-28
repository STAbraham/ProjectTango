from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
#Import the Category model
from rango.models import Category, Page

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    # Excercise 7.4 Modify the index page to also include the top 5 most viewed pages.
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    visits = int(request.COOKIES.get('visits', '1'))

    reset_last_visit_time = False
    response = render(request, 'rango/index.html', context_dict)

    # Does teh cookie last_visit exist?
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)


  #  return HttpResponse("Rango says hey there world! <br> If you want to learn more about Rango, please visit our <a href='/rango/about/'>About</a> page")

def about(request):
    return render(request, 'rango/about.html')

def category(request, category_name_slug):
    # Create a context dictionary, specific to category view, which we
    # will pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception
        # So the .get() method returns a model instance (object) or raises an exception
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance (object).
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # This is necessary for the if statement that we perform in the category
        # template, where we confirm that the category being called upon exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category; there is no
        # matching category_name_slug. If this occurs, we don't do anything
        # The template displays the "no category" message for us
        # Slight Modification
        context_dict['category_slug'] =  category_name_slug
        pass

    # Now go render the reponse and return it to the client
    return render(request, 'rango/category.html' , context_dict)

@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # If the supplied form contained errors, making it NOT valid, print these
            # errors to the terminal
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details
        # (i.e. upon first load)
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    # A HTTP POST?
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method =='POST':
        form = PageForm(request.POST)
        # Is the Form Valid?
        if form.is_valid():
            # Save the new page to the DB
            if cat:
                page = form.save(commit=False)
                page.category = cat
                # page.views = 0 from original, but doesn't seem necessary
                page.save()
            # Return user to category page; Tango with Django suggests a redirect
            # would be better here but does not show how to implement
            return category(request, category_name_slug)
        else:
            # Show any errors if the form is not valid
            print form.errors
    else:
        # If the request was a GET, render using the add_page template
        form = PageForm()

    # Need to pass category slug directly in the event that the cat does not exist,
    # but rango/category/<category_name_slug>/add_page has been navigated to
    context_dict = {'form': form, 'category': cat, 'category_slug': category_name_slug}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # A boolean value for telling the template whether the registration was succesful
    # Set to False initially. Code changes value to True when registartion logic is completed successfully
    registered = False

    # If it's a HTTP POST, we're interested in processing form data
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both User UserForm and UserProfileForm
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's for data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we initially set commit = False
            # Same technique we used in the add_page() view, as we had to set the category ourselves
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user # profile.user comes from our UserProfile model

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance to the DB
            profile.save()

            # Update our variable to tell the template registeration was succesful
            registered = True

        # Invalid form or forms - mistakes or something else
        # Print problems to the terminal.
        # They'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors

    # If it's NOT and HTTP POST (i.e. if it's a GET), we'll render our two MOdelForm instances
    # These forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template to depending on context.
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):

    #If the request is a HTTP POST, pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user
        # This information is obtained from the login form
            # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
            # because  the request.POST.get('<variable>') returns None if the value does not exist,
            # while the request.POST['<variable>'] will raise a KeyError exception
            # we used the request.POST['variable'] method in the vote view of the Django Tutorial App
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, then no user with matching credentials was found.
        if user:
            # Is the account active?
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                # An inactive account was used - no logging in
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request, 'rango/login.html', {'error_message': "You have supplied an incorrect username or password. Please try again!"})

    # The request is not a HTTP POST, sp display the login form.
    # In other words, we're assuming this is a HTTP GET
    else:
        # No context variables pass to the template sustem, hence the blank dictionary object
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view whereby they can logout
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('rango:index'))







