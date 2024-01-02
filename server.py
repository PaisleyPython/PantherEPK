from flask import Flask, render_template
print("hello")


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/spec.html")
def spec():
    return render_template("spec.html")


@app.route("/tour.html")
def tour():
    return render_template("tour.html")


@app.route("/images.html")
def images():
    return render_template("images.html")


# @app.route("/test.html")
# def test():
#     return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
