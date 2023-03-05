from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flaskr import user


def make_endpoints(app, backend):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.

        greeting = "Welcome to RetroPedia! we're still working on the name" # adds a greeting to the wikipedia
        return render_template("main.html", greeting = greeting)

    # TODO(Project 1): Implement additional routes according to the project requirements.

    def fetch_pages():
        # Fetch the list of page names from the backend
        pages = backend.get_all_page_names()

        # Define the new page names
        new_pages = [
            "Super Mario Bros. (1985)",
            "Pac-Man (1980)",
            "Tetris (1984)",
            "Donkey Kong (1981)",
            "Space Invaders (1978)",
            "The Legend of Zelda (1986)",
            "Sonic the Hedgehog (1991)",
            "Street Fighter II (1991)",
            "Final Fantasy VII (1997)",
            "GoldenEye 007 (1997)"
        ]

        # Append the new pages to the list
        pages += new_pages

        # Return the updated list of page names
        return pages
    
    @app.route("/pages")
    def page_index():
    # Fetch a list of pages from the GCS content bucket and render the "page_index.html" template
        pages = fetch_pages() # This function retrieves a list of page names
        if not pages:
            message = "No pages available."
            return render_template("page_index.html", message=message)
        else:
            return render_template("page_index.html", pages = pages)

    

    def fetch_page_text(page_name):
    # This function should fetch the text associated with the specified page from the GCS content bucket and return it
        return f"This is the text for page {page_name}."

    @app.route("/pages/<page_name>")
    def page(page_name):
    # Fetch the text associated with the page from the GCS content bucket and render the "page.html" template
        text = fetch_page_text(page_name) # This is a function that retrieves the text for the specified page
        return render_template("page.html", page_name = page_name, text = text)

    def fetch_images():
    # This function should fetch a list of image URLs for each author from the GCS content bucket and return them
    # For this example I'm returning a list of static image URLs
        return ['https://example.com/author1.jpg', 'https://example.com/author2.jpg', 'https://example.com/author3.jpg']

    @app.route("/about")
    def about():
    # Fetch a list of author images from the GCS content bucket and render the "about.html" template
        author_images = fetch_images()  # This is a function that retrieves a list of image URLs
        return render_template("about.html", author_images = author_images)
    
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # Get the uploaded file from the request object
            file = request.files['file']

            # Upload the file to Cloud Storage
            backend.upload(file)

            # Redirect to the upload page after the upload is complete
            return redirect(url_for('upload_file'))

        # Render the upload page template on GET requests
        return render_template('upload.html')





    # Ahead, we will work with the Flask Login

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_ID):

        #Lookup the user by the ID and if it exists return it, otherwise return None

        user_exists = backend.get_user(user_ID)
        if user_exists:
            return user.User(user_ID)
        return None

    @app.route('/login',methods = ["POST", "GET"])
    def login():

        if request.method == "POST":

            user_ID = request.form["username"]
            user_password = request.form["password"]

            if not user_ID or not user_password:            
                flash("One or more fields haven't been filled, please do so to proceed")
                return redirect(url_for('login'))

            successful_login = backend.sign_in(user_ID, user_password)

            if successful_login: 
                # If the user is logged in successfully,
                # we will log the user with Flask

                new_user = user.User(user_ID)
                login_user(new_user)
                # Now that the user is logged in, 
                # We can use current_user to refer
                # to the user logged in

                
                flash('You were successfully logged in')
                return redirect(url_for("home"))


            else:
                # If the login isn't succesful, we should
                # redirect the user to the login page and
                # let them know that their was a mistake
        
                flash('Invalid email or password')
                return redirect(url_for('login'))


        return render_template("login.html")

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))


    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        if request.method == "POST":

            username = request.form["username"]
            password = request.form["password"]

            # Check if either of the fields have not been filled
            if not username or not password:            
                flash("One or more fields haven't been filled, please do so to proceed")
                return render_template("signup.html")

            prefixed_password = "" + password

            succesful_signup = backend.sign_up(username, prefixed_password)

            if succesful_signup:
                new_user = user.User(username)
                login_user(new_user)
                return redirect(url_for("home"))

            else:
                flash("Username already exists, try a different one!")
                return redirect(url_for("signup"))

        return render_template("signup.html")