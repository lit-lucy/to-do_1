from flask import Flask, render_template, request, session, url_for, redirect
from flask_session import Session
import datetime

app = Flask(__name__) 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/", methods=["GET"])
def index():
	"""renders the main page, started the first time should start new session"""
	current_date = datetime.date.today()
	if session.get("notes") is None:
		session["notes"] = []
	if session.get("finished") is None:
		session["finished"] = []
	return render_template("index.html", current_date=current_date,notes=session["notes"],finished=session["finished"])

@app.route("/add", methods=["POST"])
def add():
	"""adds task to the list"""
	if session.get("notes") is None:
		session["notes"] = []

	note = request.form.get("note")
	session["notes"].append(note)

	return redirect(url_for('index',notes=session["notes"]))


@app.route("/delete", methods=["POST"])
def delete():
	"""deletes tasks from current list"""
	index = int(request.form.get("index"))
	del session["notes"][index]


	return redirect(url_for('index'))

@app.route("/done", methods=["POST"])
def done():
	"""moves tasks to done list"""
	if session.get("finished") is None:
		session["finished"] = []
	index = int(request.form.get("done"))
	session["finished"].append(session["notes"][index])
	del session["notes"][index]

	return redirect(url_for('index',finished=session["finished"]))



