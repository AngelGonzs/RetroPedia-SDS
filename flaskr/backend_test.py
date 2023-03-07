from flaskr.backend import backend

# TODO(Project 1): Write tests for Backend methods.
backend = backend.Backend()

"""
Cases to be tested for the sign_up:
    1. The sign up goes perfectly well and the username is stored in the password-bucket
    2. The sign up goes bad, username already exits, so the login will be unsuccesful

    *3. User forgets to fill either of the fields, thus the user will be sent back to signup page
        This case is handled in the frontend so idk how exactly to test it
"""
def test_sign_up(username, password):

    
    succesful_signup = backend.sign_up(username, password)
    pass



"""
Cases to be tested for the sign_in:
    1. Sign In goes just well, the username blob already exists and the password mathces
    2. Sign In goes wrong, either the username or password could be wrong
"""
def test_sign_in(username, password):

    successful_signin = backend.sign_in(username,password)
    pass



"""
Cases to test for Flask_Login:
    1. Goes well, current_user will be authenticated
    2. Goes wrong, current user will NOT be authenticated

"""
def test_flask_login(user_ID):

    pass


"""
Cases to test for get_wiki_page:
    1. The page name is found, and the html file is returned
    2. The page name is not found, and nothing is returned
"""
def test_get_wiki_page(name):
    name = input("Enter html file name (No file extension): ")
    res = backend.get_wiki_page(name)
    assert res.name == name + ".html"
    
    #Test 2
    name = input("Enter html file name (No file extension): ")
    res = backend.get_wiki_page(name)
    assert res == None