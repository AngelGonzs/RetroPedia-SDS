from flask import render_template, redirect, url_for, request


def make_endpoints(app, backend):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.

        greeting = "Welcome to RetroPedia! we're still working on the name" # adds a greeting to the wikipedia
        return render_template("nav_bar.html", greeting = greeting)

    # TODO(Project 1): Implement additional routes according to the project requirements.

    def fetch_pages():
        # Fetch the list of page names from the backend
        pages = backend.get_all_page_names()

        # Append the new pages to the list
        pages += ["page1", "page2", "page3"]

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


    @app.route("/signup", methods = ["POST", "GET"])
    def signup():
        if request.method == "POST":
            backend.sign_up()
            return render_template("about.html")
        return render_template("signup.html")


    @app.route("/login", methods = ["POST","GET"])
    def login():
        if request.method == "POST":
            backend.sign_in()
            return render_template("about.html")

        return render_template("login.html")