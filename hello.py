#!/usr/bin/env python
from flask import Flask, redirect, request
import json
import random
import string

app = Flask(__name__)


@app.route("/mydebug")
def state():
    count = read_data()
    return json.dumps(count)

@app.route("/")
def set_user():
    user = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return redirect("/{}".format(user))

@app.route("/<user>")
def inc(user):
    count = read_data()
    if user in count.keys():
        count[user] += 1
    else:
        count[user] = 1
    persist_data(count)
    return """Hi {0} <br /> 
    <b>{1}!</b>
    <form method="get" action="/set/{0}">
    <input type="text" name="cnt" />
    <input type="submit">
    </form>
    <hr />
    <form method="get" action="/{0}">
    <button type="submit"> Inc </button>
    </form>
    """.format(user, count[user])

@app.route("/<user>/<cnt>")
def set_count(user, cnt):
    count = read_data()
    count[user] = int(cnt)
    persist_data(count)
    return redirect("/{}".format(user))

@app.route("/set/<user>")
def set_it(user):
    count = read_data()
    cnt = request.args.get('cnt')
    count[user] = int(cnt)
    persist_data(count)
    return redirect("/{}".format(user))

def persist_data(count):
    data = json.dumps(count)
    text_file = open("data.txt", "w")
    text_file.write(data)
    text_file.close()

def read_data():
    try:
        text_file = open("data.txt", "r")
        count = json.loads(text_file.read())
        text_file.close()
    except:
        count = {}
    return count


if __name__ == "__main__":
    app.run(debug=True)

