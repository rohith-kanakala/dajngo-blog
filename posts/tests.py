from django.test import TestCase

# Create your tests here.
from .models import Blog

class BlogModelTests(TestCase):
    def test_blog_content_empty(self):
        B = Blog(name = "tests", text = "", tags = "Books")
        x =False
        if B.text =="":
           x = True
        self.assertIs(x, False)
