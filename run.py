from flaskblog import create_app

app = create_app()

if __name__ == '__main__':  # debug=True when we run the script directly. Lets us update the page w/o restarting webapp.
    app.run(debug=True)
