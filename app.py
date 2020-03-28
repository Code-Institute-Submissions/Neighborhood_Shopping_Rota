import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGODB_NAME"] = os.environ.get("MONGODB_NAME",
                                            'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/new_requests')
def index():
    return render_template("index.html", foods=mongo.db.c_food.find(),
                           members=mongo.db.c_members.find(),
                           shops=mongo.db.c_shops.find(),
                           status=mongo.db.c_status.find())


@app.route('/member_reg')
def member_reg():
    return render_template("member_reg.html",
                           members=mongo.db.c_members.find())


@app.route('/requests')
def requests():
    return render_template("requests.html",
                           requests=mongo.db.c_requests.find())


@app.route('/insert_requests', methods=['POST'])
def insert_requests():
    request = mongo.db.c_requests
    requests.insert_one(request.form.to_dict())
    return redirect(url_for('requests'))


@app.route('/insert_login', methods=['POST'])
def insert_login():
    logins = mongo.db.c_user
    logins.insert_one(request.form.to_dict())
    return redirect(url_for('add_new_requests'))


@app.route('/edit_request/<request_id>')
def edit_request(request_id):
    the_request = mongo.db.c_requests.find_one({"_id": ObjectId(request_id)})
    all_members = mongo.db.c_members.find()
    all_shops = mongo.db.c_shops.find()
    all_status = mongo.db.c_status.find()
    return render_template("edit_request.html", request=the_request,
                           members=all_members, shops=all_shops,
                           status=all_status)


@app.route('/update_request/<request_id>', methods=["POST"])
def update_request(request_id):
    request = mongo.db.c_requests
    request.update({"_id": ObjectId(request_id)},
                   {'requested_by': request.form.get('requested_by'),
                    'phone': request.form.get('phone'),
                    'shop': request.form.get('shop'),
                    'date': request.form.get('date'),
                    'food': request.form.get('food'),
                    'status': request.form.get('status')
                    })
    return redirect(url_for('requests.html'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
