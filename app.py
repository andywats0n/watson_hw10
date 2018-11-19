from flask import Flask, render_template

app = Flask(__name__)


@app.route("/scrape")
def home():
    from scrape_mars import scrape
    data = scrape()
    return render_template("index.html", name='home', data=data)


if __name__ == "__main__":
    app.run(debug=True)
