import json

from flask import Flask, request, render_template

webapp = Flask(__name__)

SESSION = {}


@webapp.route("/start-session", methods=["POST"])
def ss():
    global SESSION
    SESSION = dict(request.json)
    return "200"


@webapp.route("/verify")
def verify():
    if request.args.get("hash") != SESSION["attendance hash"]:
        return "Wrong Session, retry!"
    # Bonus points to those who can reverse shell this. we can sanitize it with regex later but i wont for now
    return render_template("verify.html", hash=request.args.get("hash"))


@webapp.route("/commit", methods=["POST"])
def commit():

    SESSION["students"].append(request.form.get("rollno"))
    print(SESSION)
    return "Attendance noted"


@webapp.route("/get-state")
def get_state():
    global SESSION
    return json.dumps(SESSION)


if __name__ == '__main__':
    webapp.run(host="0.0.0.0")