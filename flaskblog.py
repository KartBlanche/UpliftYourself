from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")  # Each successive @app.route is a different way to get to the same page.
def hello():  # Each @app.route above uses this same function.
    return render_template('home.html', posts=posts)  # returns the html code from the home.html file


@app.route("/about")
def about():
    return render_template('about.html', title='About')  # returns the html code from the about.html file


if __name__ == '__main__':  # debug=True when we run the script directly. Lets us update the page w/o restarting webapp.
    app.run(debug=True)
