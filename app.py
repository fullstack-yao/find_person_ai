from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from find_person import find_person

load_dotenv()

app = Flask(__name__)


@app.route("/")
def inde():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = find_person(name=name)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
