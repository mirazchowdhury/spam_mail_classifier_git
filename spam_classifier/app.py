from flask import Flask, render_template
import json
import os

app = Flask(__name__)


@app.route('/')
def index():
    emails = []
    data_path = os.path.join(os.getcwd(), "data.json")

    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            emails = json.load(f)

    return render_template('index.html', emails=emails)


if __name__ == '__main__':
    app.run(debug=True)