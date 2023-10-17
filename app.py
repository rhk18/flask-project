from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
with app.app_context():
    db=SQLAlchemy(app)


class User(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),nullable=False)
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.email}"

    

@app.route('/',methods=['GET','POST'])
def createUser():
    if request.method=='POST':
        email=request.form['email']
        first_name=request.form['first']
        last_name=request.form['last']
        password=request.form['pass']
        user=User(email=email,first_name=first_name,last_name=last_name,password=password)
        db.session.add(user)
        db.session.commit()
    allusers=User.query.all()
    return render_template('index.html',allusers=allusers)
    

@app.route('/users')
def users():
    allusers=User.query.all()
    return render_template("users.html",allusers=allusers)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def updateUser(sno):
    user=User.query.filter_by(sno=sno).first()
    if request.method=="POST":
        email=request.form['email']
        first_name=request.form['first']
        last_name=request.form['last']
        password=request.form['pass']
        if user.password==password:
            user.email=email
            user.first_name=first_name
            user.last_name=last_name
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        else:
            return "wrong password"


    return render_template("update.html",user=user)

@app.route('/delete/<int:sno>')
def deleteUser(sno):
    user=User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)

