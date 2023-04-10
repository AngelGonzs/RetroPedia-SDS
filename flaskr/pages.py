from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flaskr import user
from flask import Response
import base64
import re
import requests
from flaskr.backend import Backend


def make_endpoints(app, backend):
    backend = Backend()
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.

        greeting = "Welcome to RetroPedia! we're still working on the name"  # adds a greeting to the wikipedia
        return render_template("main.html", greeting=greeting)

    # TODO(Project 1): Implement additional routes according to the project requirements.

    def fetch_pages():
        # Fetch the list of page names from the backend
        pages = backend.get_all_page_names()

        # Define the new page names with their corresponding user-friendly names
        new_pages = {
            "Super Mario Bros (1985)": "Super Mario Bros. 1985",
            "PacMan (1980)": "Pac-Man 1980",
            "Tetris (1984)": "Tetris 1984",
            "Donkey Kong (1981)": "Donkey Kong 1981",
            "Space Invaders (1978)": "Space Invaders 1978",
            "The Legend of Zelda (1986)": "The Legend of Zelda 1986",
            "Sonic the Hedgehog (1991)": "Sonic the Hedgehog 1991",
            "Street Fighter II (1991)": "Street Fighter II 1991",
            "Final Fantasy VII (1997)": "Final Fantasy VII 1997",
            "GoldenEye 007 (1997)": "GoldenEye 007 1997"
        }

        # Modify the keys in the new_pages dictionary to make them URL-safe and append them to the pages list
        pages += [
            re.sub(r'\W+', '-', page).strip('-') for page in new_pages.keys()
        ]

        # Create a list of user-friendly page names and zip them with the URL-safe page names
        pretty_page_names = []
        page_links = []
        for page in pages:
            # Check if the page is a new page or an existing page
            if page in new_pages.values():
                # If the page is a new page, get the corresponding URL-safe page name from the new_pages dictionary
                url_page = [k for k, v in new_pages.items() if v == page][0]
            else:
                # If the page is an existing page, make it URL-safe
                url_page = re.sub(r'\W+', '-', page).strip('-')
            pretty_page_names.append(page)
            page_links.append(url_for('page', page_path=url_page))

        # Combine the two lists and pass them to the template
        pages = list(zip(pretty_page_names, page_links))

        # Return the updated list of page names
        return pages

    @app.route("/pages/<path:page_path>")
    def page(page_path):
        # Convert the URL-safe page path back to the original page name
        page_name = page_path.replace('-', ' ')

        # Check if the page exists in the backend
        if backend.get_wiki_page(page_name):
            # Fetch the text associated with the page from the GCS content bucket and render the "page.html" template
            text = fetch_page_text(
                page_name
            )  # This is a function that retrieves the text for the specified page
            return render_template("page.html", page_name=page_name, text=text)

        # Check if the page name is "Super Mario Bros. (1985)" and render the appropriate template
        if page_name == "Super Mario Bros 1985":
            return render_template("super_mario_bros.html")

        # Check if the page name is "Pac-Man (1980)" and render the appropriate template
        if page_name == "PacMan 1980":
            return render_template("pac_man.html")

        # Check if the page name is "Tetris (1984)" and render the appropriate template
        if page_name == "Tetris 1984":
            return render_template("tetris.html")

        # Check if the page name is "Donkey Kong (1981)" and render the appropriate template
        if page_name == "Donkey Kong 1981":
            return render_template("donkey_kong.html")

        # Check if the page name is "Space Invaders (1978)" and render the appropriate template
        if page_name == "Space Invaders 1978":
            return render_template("space_invaders.html")

        # Check if the page name is "The Legend of Zelda (1986)" and render the appropriate template
        if page_name == "The Legend of Zelda 1986":
            return render_template("zelda.html")

        # Check if the page name is "Sonic the Hedgehog (1991)" and render the appropriate template
        if page_name == "Sonic the Hedgehog 1991":
            return render_template("sonic.html")

        # Check if the page name is "Street Fighter II (1991)" and render the appropriate template
        if page_name == "Street Fighter II 1991":
            return render_template("street_fighter.html")

    @app.route("/pages")
    def page_index():
        # Fetch a list of pages from the GCS content bucket and render the "page_index.html" template
        pages = fetch_pages()
        if not pages:
            message = "No pages available."
            return render_template("page_index.html", message=message)
        else:
            return render_template("page_index.html", pages=pages)

    def fetch_page_text(page_name):
        # Fetch the text associated with the page from the backend
        text = backend.get_wiki_page(page_name)
        return text

    @app.route('/image/<name>')
    def fetch_images(name):
        backend = Backend()
        img_bytes = backend.get_image(name)

        if img_bytes is not None:
            # If the image data was successfully retrieved, return a Flask Response object that sends the image data
            return Response(img_bytes, mimetype='image/jpeg')

        else:
            # If the image data could not be retrieved, return a 404 error
            return 'Image not found', 404

    @app.route("/about")
    def about():
        # Fetch the image data for each team member
        TEAM_MEMBERS = ['Cambrell', 'Samuel', 'Angel']
        author_images = {}
        for name in TEAM_MEMBERS:
            image_name = f"{name.lower().replace(' ', '_')}.jpg"
            img_bytes = backend.get_image(image_name)
            if img_bytes is not None:
                author_images[name] = base64.b64encode(
                    img_bytes.getvalue()).decode('utf-8')

        # Render the "about.html" template with the author images
        return render_template("about.html", author_images=author_images)

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # Get the uploaded file from the request object
            file = request.files['file']

            if not file:
                flash("Please enter a file to upload")
                return redirect(url_for('upload_file'))

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

    @app.route('/login', methods=["POST", "GET"])
    def login():

        if request.method == "POST":

            user_ID = request.form["username"]
            user_password = request.form["password"]

            if not user_ID or not user_password:
                flash(
                    "One or more fields haven't been filled, please do so to proceed"
                )
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

    @app.route("/signup", methods=["POST", "GET"])
    def signup():
        if request.method == "POST":

            username = request.form["username"]
            password = request.form["password"]

            # Check if either of the fields have not been filled
            if not username or not password:
                flash(
                    "One or more fields haven't been filled, please do so to proceed"
                )
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
