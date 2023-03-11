from flask import Flask, render_template, request,url_for,flash,g, redirect,session
import os
import sqlite3
from custom_tools.Configuration import Config
from custom_tools.DataBaseManager import FDataBase
from werkzeug.security import generate_password_hash,check_password_hash

# app initialization
app = Flask(__name__)

app.app_context().push()

app.config.from_object(Config)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "tmp/customDB.db")))


# --- DataBase section ---


def connect_db():
	# get connection to data base
	conn = sqlite3.connect(app.config["DATABASE"], check_same_thread=False)
	conn.row_factory = sqlite3.Row
	return conn
		
		
def create_db():
	# database generation
	db = connect_db()
	with app.open_resource('sql_db.sql', mode='r') as f:
		db.cursor().executescript(f.read())
		db.commit()
		db.close()
			
			
def get_db():
	# get database link
	if not hasattr(g, "link_db"):
		g.link_db = connect_db()
	return g.link_db


@app.teardown_appcontext
def close_db(error):
	# auto breaking connection DB
	if hasattr(g, "link_db"):
		g.link_db.close()
		
		
create_db()
db = get_db()
dbase = FDataBase(db)
		
		
# --- end DataBase section ---


# --- errors handle section ---
		
		
@app.errorhandler(404)
def Page404(error):
		return render_template ("page404.html")
		
		
# --- end error handle section ---



# ---authorization section ---	


@app.route("/authorization", methods=["GET", "POST"])
def authorization():
	# authorization form
	
	if request.method == "POST":
		# checking is log/pass acceptable
		login = request.form["loginInput"]
		password = request.form["passInput"]
		
		if dbase.searchUserBy("login", login) and dbase.searchUserBy("password", password):
			# user founded
			[[cur_user]] = dbase.getUsers({
			"login": login,
			"password": password})
			
			if cur_user:
				sess_user = [tuple(row) for row in cur_user]
				session["user"] = sess_user
				return redirect("/" + str(cur_user["id"]))
				print("redirect")
		else:
			# user is not exists
			flash("vrong data")
	
	# with both methods rendering template
	return render_template("authorization.html", reg_ref=url_for("registration"))


# --- end authorization section ---


# --- registration section ---


@app.route("/registration", methods=["GET", "POST"])
def registration():
	# registration form
	
	if request.method == "POST":
		login = request.form["loginInput"]
		password = request.form["passInput"]
		email = request.form["emailInput"] or None
		name = request.form["nameInput"]
		
		dbase.createObject([login, password, email, name])
		print("success")
	
	return render_template("registration.html")


# --- end registration section ---


# --- main page section ---


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:user_id>", methods=["GET", "POST"])
def main_page(user_id=None):
	
	#if user isn't exists - ti authorization
	if user_id and not dbase.searchUserBy("id", user_id):
		print("---redirecting---")
		return redirect("/authorization")
	
	
	offers = dbase.getData("Offer")
	for o in offers:
		print(o)
	# !!! Error on non existing user !!!
	if user_id:
		[[current_user]] = dbase.getUsers({"id": user_id})
		return render_template("main_page.html", user=current_user, offers=offers)
	
		
	return render_template("main_page.html", offers = offers)


# --- end main page section ---

# --- user profile section ---

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user_profile(user_id):
	
	if not dbase.searchUserBy("id", user_id):
		return render_template("page404.html")
	
	[current_user] = dbase.getById("User", user_id)
	
	return render_template("user_profile.html", user=current_user)

# --- end user prifile section ---



@app.route("/offer/<int:offer_id>", methods=["GET", "POST"])
def offer_page(offer_id):
	
	current_offer = dbase.getById("Offer", offer_id)
	return render_template("offer_page.html", offer_list = current_offer)

# start app
if __name__ == "__main__":
	app.run(debug=True, threaded=True)