from flask import jsonify, render_template, request, redirect, make_response, session, url_for
import jwt
from .models.todo import Users, Todo
from . import app, db
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
from datetime import datetime, timedelta
from .wrappers.authenticate import token_required

@app.route("/")
@token_required
def index(current_user):
    try:
        return render_template("index.html", todo=Todo.getAllForID(Users.getOne(current_user['user'].email)['user'].id), token=session['x-access-token'])
    except:
        return redirect("/login")

@app.route("/todos")
@token_required
def todos(current_user):
    return jsonify({"result": Todo.getAllForID(Users.getOne(current_user['user'].email)['user'].id),})
    

@app.route("/todo", methods=["POST"])
@token_required
def addTask(current_user):
    todo = Todo(task=request.get_json()['task'],
    created=datetime.utcnow(),
    status=request.get_json()['status'],
    user_id=Users.getOne(current_user['user'].email)['user'].id)
    todo.add()
    try:
        return jsonify({"result": Todo.getAllForID(Users.getOne(current_user['user'].email)['user'].id)})
    except BaseException as e:
        return jsonify({"result": None})

@app.route("/remove-todo", methods=["DELETE"])
@token_required
def removeTask(current_user):
    try:
        Todo.delete(request.get_json()['id'])
    except BaseException:
        pass
    return jsonify({"result": Todo.getAllForID(Users.getOne(current_user['user'].email)['user'].id)})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", register=False)
    
    if not request.form.get('email') or not request.form.get('password'):
        return render_template("login.html", register=False, error={"status": True, "text": "Invalid Form Submission"})

    user = Users.getOne(request.form.get("email"))
    if not user["exists"]:
        return render_template("login.html", register=False, error={"status": True, "text": "User does not exist"})

  
    if check_password_hash(user["user"].hashcode, request.form.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'email': user['user'].email,
            'username': user['user'].username,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, 'secret-key', algorithm='HS256')
        session['x-access-token'] = token
        return redirect(url_for("index"))
    return render_template("login.html", register=False, error={"status": True, "text": "Password is wrong"})


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html", register=True)
    else:
        if request.form.get('password') != request.form.get('confirm-password'):
            return render_template("login.html", register= True, error={"status": True, "text": "Passwords do not Match"})
        
        if not request.form.get('username') or not request.form.get('password') or not request.form.get('confirm-password'):
            return render_template("login.html", register= True, error={"status": True, "text": "Invalid Form Submission"})

        userExists = Users.getOne(request.form.get("email"))
        if userExists["exists"]:
            return render_template("login.html", register= True, error={"status": True, "text": "User already exists"})

        try:
            user = Users(email = request.form.get("email"), username = request.form.get("username"), hashcode = generate_password_hash(request.form.get("password")),)
            user.add()
            return redirect("/login")
        except BaseException as e:
            print(e)
            return render_template("login.html", register= True, error={"status": True, "text": "Something went wrong"}) 

@app.route("/sign-out")
@token_required
def signOut(current_user):
    return redirect("/login")

if __name__ == "__main__":
    db.create_all()
    app.run()