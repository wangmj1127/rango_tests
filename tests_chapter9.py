# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import os

#Chapter 4
from django.contrib.staticfiles import finders

#Chapter 5
from rango.models import Page, Category
import populate_rango
import test_utils

#Chapter 6
from rango.decorators import chapter6

#Chapter 7
from rango.decorators import chapter7
from rango.forms import CategoryForm, PageForm

#Chapter 8
from django.template import loader
from django.conf import settings
from rango.decorators import chapter8
import os.path

#Chapter 9
from rango.models import User, UserProfile
from rango.forms import UserForm, UserProfileForm
from selenium.webdriver.common.keys import Keys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from rango.decorators import chapter9

# ===== Chapter 9
class Chapter9ModelTests(TestCase):
    def test_user_profile_model(self):
        # Create a user
        user, user_profile = test_utils.create_user()

        # Check there is only the saved user and its profile in the database
        all_users = User.objects.all()
        self.assertEquals(len(all_users), 1)

        all_profiles = UserProfile.objects.all()
        self.assertEquals(len(all_profiles), 1)

        # Check profile fields were saved correctly
        all_profiles[0].user = user
        all_profiles[0].website = user_profile.website

class Chapter9ViewTests(TestCase):

    @chapter9
    def test_registration_form_is_displayed_correctly(self):
        #Access registration page
        response = self.client.get(reverse('register'))

        # Check if form is rendered correctly
        # self.assertIn('<h1>Register with Rango</h1>', response.content)
        self.assertIn('Rango says: <strong>register here!</strong><br />'.lower(), response.content.lower())

        # Check form in response context is instance of UserForm
        self.assertTrue(isinstance(response.context['user_form'], UserForm))

        # Check form in response context is instance of UserProfileForm
        self.assertTrue(isinstance(response.context['profile_form'], UserProfileForm))

        user_form = UserForm()
        profile_form = UserProfileForm()

        # Check form is displayed correctly
        self.assertEquals(response.context['user_form'].as_p(), user_form.as_p())
        self.assertEquals(response.context['profile_form'].as_p(), profile_form.as_p())

        # Check submit button
        self.assertIn('type="submit" name="submit" value="Register"', response.content)

    @chapter9
    def test_login_form_is_displayed_correctly(self):
        #Access login page
        response = self.client.get(reverse('login'))

        #Check form display
        #Header
        self.assertIn('<h1>Login to Rango</h1>'.lower(), response.content.lower())

        #Username label and input text
        self.assertIn('Username:', response.content)
        self.assertIn('input type="text" name="username" value="" size="50"', response.content)

        #Password label and input text
        self.assertIn('Password:', response.content)
        self.assertIn('input type="password" name="password" value="" size="50"', response.content)

        #Submit button
        self.assertIn('input type="submit" value="submit"', response.content)

    @chapter9
    def test_login_provides_error_message(self):
        # Access login page
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})

        try:
            self.assertIn('wronguser', response.content)
        except:
            self.assertIn('wrongpass', response.content)

    @chapter9
    def test_login_redirects_to_index(self):
        # Create a user
        test_utils.create_user()

        # Access login page via POST with user data
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'test1234'})

        # Check it redirects to index
        self.assertRedirects(response, reverse('index'))

    @chapter9
    def test_upload_image(self):
        # Create fake user and image to upload to register user
        image = SimpleUploadedFile("testuser.jpg", "file_content", content_type="image/jpeg")
        response = self.client.post(reverse('register'),
                         {'username': 'testuser', 'password':'test1234',
                          'email':'testuser@testuser.com',
                          'website':'http://www.testuser.com',
                          'picture':image } )

        # Check user was successfully registered
        self.assertIn('thank you for registering!'.lower(), response.content.lower())
        user = User.objects.get(username='testuser')
        user_profile = UserProfile.objects.get(user=user)
        path_to_image = './profile_images/testuser.jpg'

        # Check file was saved properly
        self.assertTrue(os.path.isfile(path_to_image))

        # Delete fake file created
        default_storage.delete('./profile_images/testuser.jpg')
