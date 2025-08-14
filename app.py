from flask import Flask, redirect, request, render_template,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import smtplib
from dotenv import load_dotenv
import os
from flask import jsonify
import cloudinary
import cloudinary.uploader
from flask_migrate import Migrate

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_API_SECRET")
)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = Flask(__name__)
UPLOAD_FOLDER_POST = 'static/posts'
UPLOAD_FOLDER_DOPS = 'static/dops'
UPLOAD_FOLDER = 'static/dp'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_POST'] = UPLOAD_FOLDER_POST
app.config['UPLOAD_FOLDER_DOPS'] = UPLOAD_FOLDER_DOPS
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_POST, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DOPS, exist_ok=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

class Gooners(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    dateadded = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100))
    DOB = db.Column(db.String(100))
    dp = db.Column(db.String(200))
    

    posts = db.relationship('Posts',backref = 'user', lazy = True)
    dops = db.relationship('Dops',backref = 'user', lazy = True)

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.String(200))
    post_caption = db.Column(db.String(1000))
    
    user_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)

    comments = db.relationship("Comments", backref="post", cascade="all, delete-orphan")  # define here


class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_text = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=True)

    user = db.relationship('Gooners', backref='comments', lazy=True)

    
class Dops(db.Model):
    dops_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dops = db.Column(db.String(200))
    dops_caption = db.Column(db.String(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    

    comments = db.relationship("DopsComments", backref="dop", cascade="all, delete-orphan")

class DopsComments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    dops_id = db.Column(db.Integer, db.ForeignKey('dops.dops_id'), nullable=False)

    user = db.relationship('Gooners', backref='dops_comments')
    
class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    dateadded = db.Column(db.DateTime, default=datetime.utcnow)
    final_status = db.Column(db.String(200), default="pending")
    
    follower = db.relationship('Gooners', foreign_keys=[follower_id], backref='following')
    following = db.relationship('Gooners', foreign_keys=[following_id], backref='followers')

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('gooners.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer,db.ForeignKey('gooners.user_id'),nullable=False)
    status = db.Column(db.String(200),default="pending")
    dateadded = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('Gooners',foreign_keys=[sender_id],backref='sent_requests')
    receiver = db.relationship('Gooners',foreign_keys=[receiver_id],backref='received_requests')

@app.route("/comments/<int:post_id>", methods=["POST", "GET"])
def comments(post_id):
    user_id = session.get("user_id")
    if request.method == "POST":
        comment = request.form["comment"]
        
        new_comment = Comments(
            comment_text=comment,
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(new_comment)
        db.session.commit()
    comment = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamp.desc()).all()    
    return render_template("comments.html", comment=comment, post_id = post_id)


@app.route("/dopcomments/<int:dops_id>", methods=["POST","GET"])
def dopscomments(dops_id):
    user_id = session.get("user_id")
    if request.method == "POST":
        comment = request.form["comments"]
        new_comment = DopsComments(comment_text = comment, dops_id =dops_id, user_id = user_id)

        db.session.add(new_comment)
        db.session.commit()
        return redirect(f"/dops/{dops_id}")
    comments = DopsComments.query.filter_by(dops_id=dops_id).order_by(DopsComments.timestamp.desc()).all()
    return render_template("dopscomments.html",comments=comments,dops_id=dops_id)

@app.route("/deletecomment/<int:comment_id>", methods=["POST", "GET"])
def commentdelete(comment_id):
    user_id = session.get("user_id")
    delete_comment = Comments.query.get_or_404(comment_id)
    if user_id == delete_comment.user_id:
        post_id = delete_comment.post_id
        db.session.delete(delete_comment)
        db.session.commit()
        return redirect(f"/post/{post_id}")
    else:
        return redirect(f"/post/{delete_comment.post_id}")

@app.route("/dops",methods=["POST","GET"])
def dops():
 user_id = session.get("user_id")
 if not user_id:
     return redirect("/login")
 if request.method == "POST":
     file = request.files["dops"]
     caption = request.form["caption"]
     if file:
         result = cloudinary.uploader.upload(file, folder="goongram/dops", resource_type="video")
         image_url = result['secure_url']
         user = Gooners.query.filter_by(user_id = user_id).first()
         new_dop = Dops(dops=image_url,dops_caption = caption,user_id = user.user_id)
         db.session.add(new_dop)
         db.session.commit()
         return redirect("/profile")
 return render_template("dops.html")        
 
         
@app.route("/post1", methods=["POST", "GET"])
def post1():
    user_name = session.get("user_name")
    if not user_name:
        return redirect("/login")
    if request.method == "POST":
        file = request.files["post1"]
        caption = request.form["caption"]
        if file:
            result = cloudinary.uploader.upload(file, folder="goongram/posts")
            image_url = result['secure_url']
            
            user = Gooners.query.filter_by(user_name=user_name).first()
            new_post = Posts(post = image_url, post_caption = caption,user_id = user.user_id)
            
            db.session.add(new_post)
            db.session.commit()

            return redirect("/profile")

    return render_template("post.html")

@app.route("/deletepost/<int:post_id>")
def deletepost(post_id):
    id = Posts.query.get_or_404(post_id)
    db.session.delete(id)
    db.session.commit()
    return redirect("/profile")

@app.route("/deletedops/<int:dops_id>")
def deletedops(dops_id):
    id = Dops.query.get_or_404(dops_id)
    db.session.delete(id)
    db.session.commit()
    return redirect("/profile")

@app.route("/dops/<int:dops_id>")
def opendops(dops_id):
    user_id = session.get("user_id")
    comments = DopsComments.query.filter_by(dops_id=dops_id).order_by(DopsComments.comment_id).all()
    user = Gooners.query.filter_by(user_id=user_id).first()
    dops = Dops.query.get_or_404(dops_id)
    
    return render_template("dopsopen.html",comments=comments,user=user,dops=dops)


@app.route("/dp", methods=["POST", "GET"])
def dp():
    user_name = session.get("user_name")
    if not user_name:
        return redirect("/login")

    if request.method == "POST":
        file = request.files["img"]
        if file:
            
            result = cloudinary.uploader.upload(file, folder="goongram/dp")
            image_url = result['secure_url']  # permanent URL

            
            gooner = Gooners.query.filter_by(user_name=user_name).first()
            gooner.dp = image_url
            session["image_url"] = image_url
            db.session.commit()

            return redirect("/profile")

    return render_template("dp.html")



@app.route("/profile", methods=["POST", "GET"])
def profile():
    user_id = session.get("user_id")
    if "user_id" not in session:
        return redirect("/login")
    user = Gooners.query.get(session["user_id"])
    posts = Posts.query.filter_by(user_id = user_id).order_by(Posts.post_id.desc()).all()
    dops = Dops.query.filter_by(user_id = user_id).order_by(Dops.dops_id.desc()).all()
    return render_template("profile.html", user=user,posts = posts,dops=dops)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def postopen(post_id):
    user_id = session.get("user_id")
    post = Posts.query.get_or_404(post_id)
    comments = Comments.query.filter_by(post_id=post_id).all()
    user = Gooners.query.filter_by(user_id=user_id).first()
    post_author = post.user
    return render_template("postopen.html", post=post, comments=comments,user = user,post_author = post_author)

@app.route("/name", methods=["POST", "GET"])
def name():
    if request.method == "POST":
        name = request.form["name"]
        user = Gooners.query.get(session["user_id"])
        if user:
            user.name = name  
            db.session.commit()
            return redirect("/DOB")
        else:
            return "Error adding name"
    return render_template("name.html")


@app.route("/DOB", methods=["POST", "GET"])
def DOB():
    if request.method == "POST":
        dob = request.form["DOB"]
        user = Gooners.query.get(session["user_id"])
        if user:
            user.DOB = dob  
            db.session.commit()
            return redirect("/gooners")
        else:
            return "Failed to add DOB"
    return render_template("DOB.html")

@app.route("/allreq")
def allreq():
    reqs = Requests.query.order_by(Requests.id.desc()).all()
    return render_template("adminreqs.html",reqs=reqs)

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/")
def home():
    print(">>> Entered / route")  # to see if we even reach here
    try:
        # Your original code here
        return render_template("index.html")
    except Exception as e:
        import traceback
        print("ERROR in / route:", e)
        traceback.print_exc()
        return f"Error: {e}", 500


@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        session["user_name"] = user_name
        gooner = Gooners.query.filter_by(user_name=user_name, user_password=user_password).first()
        if gooner:
            message = f"{user_name} Just logged in"
            session["user_id"] = gooner.user_id
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login(EMAIL_USER,EMAIL_PASS)
            server.sendmail(EMAIL_USER,EMAIL_USER,message)
            
            if gooner.name and gooner.DOB:
                return redirect("/gooners")
            else:
                return redirect("/name")
        else:
            return "Invalid Credentials (or) Gooner Not Registered !!!"
    

    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    user_name = session.get("user_name")
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_password = request.form["user_password"]
        
        existing_user = Gooners.query.filter_by(user_name=user_name).first()
        if existing_user:
            return redirect("/login")
        
        new_gooner = Gooners(user_password=user_password, user_name=user_name)
        db.session.add(new_gooner)
        db.session.commit()
        client_message = f"Dear {user_name}, Welcome to Dopameme, Post Away!"
        admin_message = f"Greetings BatMan, {user_name} has just taken part in the Dopameme initiative!"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, user_name, client_message)
        server.sendmail(EMAIL_USER, EMAIL_USER, admin_message)
        return redirect("/login")

    return render_template("register.html")

@app.route("/search",methods = ["POST","GET"])
def search():
    user_name = session.get("user_name")
    if request.method == "POST":
       name = request.form["name"]
       search_name = Gooners.query.filter(Gooners.name.ilike(f"%{name}%")).all()
       return render_template("search_results.html",search_name = search_name,query=name)
    return render_template("search.html")

@app.route("/suggest") #VIBECODED   
def suggest():
    query = request.args.get("query", "")
    results = Gooners.query.filter(Gooners.name.ilike(f"{query}%")).limit(5).all()
    suggestions = [{"name": u.name, "user_name": u.user_name} for u in results]
    return jsonify(suggestions)

@app.route("/dopsdisplay")
def dopsdisplay():
    user_id = session.get("user_id")
    user = Gooners.query.filter_by(user_id=user_id).first()
    dops = Dops.query.order_by(Dops.dops_id.desc()).all()
    comments = DopsComments.query.order_by(DopsComments.comment_id.desc()).all()
    return render_template("dopsdisplay.html",user=user,dops=dops,comments=comments)

@app.route("/addfollower/<int:sender_id>/<int:receiver_id>")
def addfollower(sender_id, receiver_id):
    receiver = Gooners.query.filter_by(user_id=receiver_id).first()
    sender = Gooners.query.filter_by(user_id=sender_id).first()
    request = Requests.query.filter_by(sender_id=sender_id,receiver_id=receiver_id).first()

    if not request:
        new_request = Requests(sender_id=sender_id, receiver_id=receiver_id, status="pending")
        db.session.add(new_request)
        db.session.commit()
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(EMAIL_USER,EMAIL_PASS)
        server.sendmail(EMAIL_USER,{receiver.user_name},f"{sender.name} sent a follow request")
    return render_template("ReqSent.html")

@app.route("/approvefollower/<int:sender_id>/<int:receiver_id>")
def approvefollower(sender_id, receiver_id):

    remove = Requests.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).first_or_404()    
    receiver = Gooners.query.filter_by(user_id=receiver_id).first()
    sender = Gooners.query.filter_by(user_id=sender_id).first()
    follower = Followers.query.filter_by(follower_id=sender_id,following_id=receiver_id).first()
    if not follower:
        new_follower = Followers(follower_id=sender_id,following_id=receiver_id,final_status="accepted")
        db.session.add(new_follower)
        db.session.delete(remove)
        db.session.commit()
    return render_template("approvefollower.html")


@app.route("/all_requests")
def all_requests():
    receiver_id = session["user_id"]
    requests = Requests.query.filter_by(receiver_id=receiver_id).order_by(Requests.id.desc()).all()
    return render_template("requests.html", requests=requests)

@app.route("/all_followers/<int:user_id>")
def all_followers(user_id):
    followers = Followers.query.filter_by(following_id=user_id).order_by(Followers.id.desc()).all()
    return render_template("followers.html", followers=followers)



@app.route("/profile/<int:user_id>")
def profile_open(user_id):
    if "user_id" not in session:
        return redirect("/login")

    current_user_id = session["user_id"]

    user = Gooners.query.get_or_404(user_id)
    images = Posts.query.filter_by(user_id=user_id).order_by(Posts.post_id.desc()).all()
    dops = Dops.query.filter_by(user_id=user_id).order_by(Dops.dops_id.desc()).all()

    
    follower = Followers.query.filter_by(
        follower_id=current_user_id, 
        following_id=user_id
    ).first()

    request = Requests.query.filter_by(
        sender_id=current_user_id, 
        receiver_id=user_id
    ).first()

    if follower:

        return render_template("profileopen.html", user=user, images=images, dops=dops)
    else:
        
        return render_template("sendreq.html", user=user, follower=follower, request=request, sender_id=current_user_id)




@app.route("/delete/<int:user_id>")
def delete(user_id):
   
    delete_gooner = Gooners.query.get_or_404(user_id)
    try:
        db.session.delete(delete_gooner)
        db.session.commit()
    except:
        return f"Failed to Delete Gooner id {user_id}"
    return redirect("/database")

@app.route("/dashboard")    
def dashboard():
    user_name = session.get("user_name")
    user_id = session.get("user_id")
    dops = Dops.query.order_by(Dops.dops_id.desc()).all()
    posts = Posts.query.order_by(Posts.post_id.desc()).all()
    user = Gooners.query.order_by(Gooners.dateadded).all()
    comments = Comments.query.order_by(Comments.comment_id.desc()).all()
    return render_template("dashboard.html", posts = posts, user = user,comments = comments,dops=dops)

@app.route("/gooners")
def gooners():
    present = Gooners.query.order_by(Gooners.dateadded.desc()).all()
    return render_template("present.html", present = present)

@app.route("/database")
def database():
    new_gooner = Gooners.query.order_by(Gooners.dateadded.desc()).all()
    return render_template("Database.html", new_gooner=new_gooner)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    #app.run(debug=True)
