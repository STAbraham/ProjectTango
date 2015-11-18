from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the forms
    class Meta:
        # Provides an assocation between the ModelForm and
        # the Model that it is helping support
        model = Category
        fields = ['name']

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(widget=forms.widgets.TextInput, max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provides an association between the ModelForm and the Model
        model = Page
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present
        # Some fields may allow NULL values, so we may not want/need to include them...
        # Here, we are hiding the foreign key, which relates the Page to the Category
        # We can either exclude the category field from the form
        exclude = ['category']
        # or specify the fields to include (i.e. not include the category field)
        # equivalent alternative: fields = ('title','url','views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data['url']

        # If url is not empty and doesn't start with 'http://', then prepend
        # 'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data


"""
Following forms are deprecated because we have refactored to use Django Registration Redux
App, which comes with it's own forms implementation for registering. Preserved below for
educational/infromational purposes
"""
# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['website', 'picture']