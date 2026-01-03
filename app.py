from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///./database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db=SQLAlchemy(app)

class Message(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    message=db.Column(db.Text)
with app.app_context():
    print("Creating database...")
    db.create_all()

app.secret_key="supersecretkey"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    services_list=["Landing pages profecionales", "Formularios de contacto", "Diseño responsive", "Backend con Flask"]
    return render_template("services.html", services=services_list)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method=="POST":
        nombre=request.form["nombre"]
        email=request.form["email"]
        mensaje=request.form["mensaje"]
        
        new_message= Message(
            name=nombre,
            email=email,
            message=mensaje
        )
        db.session.add(new_message)
        db.session.commit()

        return render_template("success.html", name=nombre)
    
    return render_template("contact.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    
    mensajes=Message.query.all()
    return render_template("admin.html", mensajes=mensajes)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username=="admin" and password=="1234":
            session["admin"]=True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

if __name__ =="__main__":
    app.run(debug=True)