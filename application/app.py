from flask import jsonify, render_template, request, redirect, session, url_for
import jwt
from models import app
from models.todo import Users, Todo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from wrappers.authenticate import token_required

# Landing page for authorized  users
@app.route("/")
# wrapper function to handle validating the Authenticity of the Token in session 
@token_required
def index(current_user):
    try:
        email = current_user['user'].email
        # Render the landing page - along with the session token and the Users's Todods
        return render_template("index.html", todo=Todo.getAllForID(Users.getOne(email)['user'].id), token=session['x-access-token'])
    except:
        # Redirect user to login, Invalid Session Token
        return redirect("/login")

# Get Token
@app.route("/token", methods=["POST"])
def getToken():
    # Server side validation of the Username and Password
    if not request.get_json().get('email') or not request.get_json().get('password'):
        return jsonify({"code": 405, "token": None, "message": "Invalid Form Submission"})

    # Check if User exists
    user = Users.getOne(request.get_json().get("email"))
    if not user["exists"]:
        return {"code": 404, "token": None, "message": "User does not exist"}

    # Validate password provided
    if check_password_hash(user["user"].hashcode, request.get_json().get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'email': user['user'].email,
            'username': user['user'].username,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return {"code": 200, "token": token, "message": ""}
    # Invalided password provided
    return {"code": 405, "token": None, "message": "Password is wrong"}

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Accesses the login page
    if request.method == "GET":
        return render_template("login.html", register=False)
    
    # Server side validation of the Username and Password
    if not request.form.get('email') or not request.form.get('password'):
        return render_template("login.html", register=False, error={"status": True, "text": "Invalid Form Submission"})

    # Check if User exists
    user = Users.getOne(request.form.get("email"))
    if not user["exists"]:
        return render_template("login.html", register=False, error={"status": True, "text": "User does not exist"})

    # Validate password provided
    if check_password_hash(user["user"].hashcode, request.form.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'email': user['user'].email,
            'username': user['user'].username,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        # Store token in a flask session 
        session['x-access-token'] = token
        # Redirect to landing page
        return redirect(url_for("index"))
    # Invalided password provided
    return render_template("login.html", register=False, error={"status": True, "text": "Password is wrong"})

# User registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    # Accesses the Registration Page
    if request.method == "GET":
        return render_template("login.html", register=True)
    
    # Server side validation
    if not request.form.get('username') or not request.form.get('password') or not request.form.get('confirm-password'):
        return render_template("login.html", register= True, error={"status": True, "text": "Invalid Form Submission"})
    
    # Validate registration passwords match
    if request.form.get('password') != request.form.get('confirm-password'):
            return render_template("login.html", register= True, error={"status": True, "text": "Passwords do not Match"})
    
    # Check if user already exists
    userExists = Users.getOne(request.form.get("email"))
    if userExists["exists"]:
        return render_template("login.html", register= True, error={"status": True, "text": "User already exists"})
    
    try:
        user = Users(email = request.form.get("email"), username = request.form.get("username"), hashcode = generate_password_hash(request.form.get("password")),)
        user.add()
        return redirect("/login")
    except BaseException as e:
        return render_template("login.html", register= True, error={"status": True, "text": "Something went wrong"}) 
        
# Sign Out Handler
@app.route("/sign-out")
@token_required
def signOut(current_user):
    try:
        # Removes the token from flask session
        del session['x-access-token']
    except:
        pass
    # Return user to login page
    return redirect("/login")

# REST Endpoint - GET All Todo Tasks
@app.route("/todos")
@token_required
def todos(current_user):
    user = Users.getOne(current_user['user'].email)['user']
    try:
        return {"code": 200, "message": "", "result": Todo.getAllForID(user.id)}
    except BaseException as e:
        return jsonify({"code": 404, "message": str(e), "result": []})
    
# REST Endpoint - POST New Todo Tasks
@app.route("/todo", methods=["POST"])
@token_required
def addTask(current_user):
    try:
        # Get current users email
        email = current_user['user'].email

        # Create Todo Task
        todo = Todo(task=request.get_json()['task'],
        created=datetime.utcnow(),
        status=request.get_json()['status'],
        user_id=Users.getOne(email)['user'].id)
        todo.add()

        # Return All Todos for current user only
        return {"code": 200, "message": "", "result": Todo.getAllForID(Users.getOne(email)['user'].id)}
    except BaseException as e:
        # Return empty list
        return {"code": 404, "message": str(e), "result": []}


# REST Endpoint - DELETE Existsing Todo Tasks
@app.route("/remove-todo", methods=["DELETE"])
@token_required
def removeTask(current_user):
    try:
        email = current_user['user'].email
        # Delete requested todo id
        Todo.delete(request.get_json().get('id'))
        # Return remaining Todos for current user
        return {"code": 200, "message": "", "result": Todo.getAllForID(Users.getOne(email)['user'].id)}
    except BaseException as e:
        # Return empty list
        return {"code": 404, "message": str(e), "result": []}



if __name__ == "__main__":
    db.create_all()
    app.run()