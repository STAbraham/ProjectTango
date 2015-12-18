from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

# Overwrites the save method to incoporate the conversion of name
# to the slug field; where the whitespaces are now hyphens through
# use of the slugify method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

# Necessary for Python 2 users to establish encoding this way
# It is slightly variant for Python 3, where unicode is replaced with str
# Particularly helpful in debugging as it allows you to see field values
# as opposed to just seeing <Category: Category Object> because of encoding
# This is best practice, essentially making outputs human readable.
    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserPorfile to a User model instance.
    user = models.OneToOneField(User) # have to import the User model above from django.conrib.auth.models
    test_field = models.IntegerField(default=0)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', default="Is Anything Registering?")

    # Override the __unicode__() mehod to return something meaningful, from the linked User object
    def __unicode__(self):
        return self.user.username
