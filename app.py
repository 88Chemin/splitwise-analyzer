from copy import deepcopy

from flask import Flask, render_template, redirect, session, url_for, request
from splitwise import Splitwise
import config as Config
import datetime

import wallstreet
from wallstreet import payment_matrix, simplify_matrix

app = Flask(__name__)
app.secret_key = "test_secret_key"


@app.route("/")
def home():
    if 'access_token' in session:
        return redirect(url_for("analyzer"))
    return render_template("home.html")


@app.route("/login")
def login():

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session['secret'] = secret
    return redirect(url)


@app.route("/authorize")
def authorize():

    if 'secret' not in session:
        return redirect(url_for("home"))

    oauth_token    = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,session['secret'],oauth_verifier)
    session['access_token'] = access_token

    return redirect(url_for("analyzer"))


@app.route("/friends")
def friends():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    friends = sObj.getFriends()
    return render_template("friends.html", friends=friends)


@app.route("/analyze")
def analyzer():
    if 'access_token' not in session:
        return redirect(url_for("home"))

    sObj = Splitwise(Config.consumer_key,Config.consumer_secret)
    sObj.setAccessToken(session['access_token'])

    groups = sObj.getGroups()
    group = [ x for x in groups if x.name == "88 Chemin 2018"][0]
    group.members.sort(key=wallstreet.get_index_for_dude)

    expenses = sObj.getExpenses(group_id=group.id, limit=10000, dated_after=datetime.datetime(2017,5, 1))
    matrix = payment_matrix(expenses)
    wallstreet.print_matrix(matrix)
    simplified_matrix = simplify_matrix(deepcopy(matrix))
    wallstreet.print_matrix(simplified_matrix)
    return render_template("payment_matrix.html", users=group.members, matrix=matrix, simplified_matrix=simplified_matrix)


if __name__ == "__main__":
    app.run(threaded=True,debug=True, host='0.0.0.0')
