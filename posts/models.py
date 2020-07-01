from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from profiles.models import profile
from itertools import count


# Create your models here.
def uploaded_loc(instance ,filename):
    return "{}{}".format(instance.id,filename)



class Blog(models.Model):
    TAGS = (
        ('Ed', 'education'),
        ('Tr', 'travel'),
        ('Te', 'Technology'),
        ('Bo', 'Books'),
        ('De', 'Default'),
    )
    name = models.CharField(max_length= 30, db_index=True)
    author = models.ForeignKey(profile, on_delete=models.CASCADE, blank = False, null=False)
    slug = models.SlugField(unique=True,blank=True)  # slug inherits from charfield and has default max_length of 50
    photo = models.ImageField(upload_to='users', null=True, blank=True) # base class of  FileField which can store all files
    text = models.TextField(blank=False, null=False)
    tags = models.CharField(default='De', max_length=2,choices=TAGS)
    updated_stamp = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True,db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("view_blog", kwargs={"slug":self.slug})

    class Meta:
        ordering=['-timestamp']


    def generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in count(1):   # count is from itertools and maintains the value of i
            if not Blog.objects.filter(slug = slug_candidate).exists():
                break
            slug_candidate = "{}-{}".format(slug_original,i)  # here i is used instead of pf to make url robust ad some randomness

        self.slug = slug_candidate


    def save(self, *args, **kwargs):
        if not self.pk:
            self.generate_slug()
        super().save(*args,**kwargs)