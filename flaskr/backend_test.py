from flaskr import backend
import unittest
from unittest import mock, TestCase
from unittest.mock import Mock, MagicMock
import hashlib


# TODO(Project 1): Write tests for Backend methods.


# """
# Cases to be tested for the sign_up:
#     1. The sign up goes perfectly well and the username is stored in the password-bucket
#     2. The sign up goes bad, username already exits, so the login will be unsuccesful
# """
# def test_sign_up(username, password):

    
#     succesful_signup = backend.sign_up(username, password)
#     pass



# """
# Cases to be tested for the sign_in:
#     1. Sign In goes just well, the username blob already exists and the password mathces
#     2. Sign In goes wrong, either the username or password could be wrong
# """
# def test_sign_in(username, password):

#     successful_signin = backend.sign_in(username,password)
#     pass



# """
# Cases to test for Flask_Login:
#     1. Goes well, current_user will be authenticated
#     2. Goes wrong, current user will NOT be authenticated

# """
# def test_flask_login(user_ID):

#     pass



back = backend.Backend()


def test_sign_up():

    # Test for when the username doesn't exist, this should be True
    username = "test_user"
    password = "test_pw"


    bucket = MagicMock()
    blob = MagicMock()
    blob.exists.return_value = False
    bucket.blob.return_value = blob

    back.password_bucket = bucket


    result = back.sign_up(username, password)
    assert result == True


    # Test for when the username already exists, this should be False
    blob.exists.return_value = True
    result = back.sign_up(username, password)
    assert result == False




def test_sign_in_pass():

    # Test for trying to log into an existing account with the right password
    # The following is an existing User in the bucket.
    username = "angel3"
    password = "12345"

    bucket = MagicMock()
    blob = MagicMock()

    blob.exists.return_value = True
    blob.download_as_string.return_value = "12345"

    bucket.blob.return_value = blob


    result = back.sign_in(username,password)
    assert result == True



    # #  Test for when the username might be right, but the password surely isn't
    # blob.download_as_string.return_value = "You'll never get this password right, because I'm not hashed!"
    # result = back.sign_in(username,password)
    # assert result == False

    pass


"""
Cases to test for get_wiki_page:
    1. The page name is found, and the html file is returned
    2. The page name is not found, and nothing is returned
"""
def test_get_wiki_page():
    bucket = MagicMock()
    blob = MagicMock()

    html_name = "about.html"

    result = back.get_wiki_page(html_name)

    assert result == bucket.blob.get_wiki_page("about.html")

    #Test 2
    html_name = "fake_page.html"
    result = back.get_wiki_page(html_name)
    assert result == bucket.blob.get_wiki_page("fake_page.html")


