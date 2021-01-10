from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import timeago


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test1.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)

if __name__=="__main__":
    app.run(debug=False)

#################################################################################################
class Feed(db.Model):
    global db
    __tablename__='feed'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150))
    platform = db.Column(db.String(150), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    application = db.relationship('Apply')

    def daysago(self):
        now = datetime.utcnow()
        date = self.posted_on
        return timeago.format(date, now)

    def __repr__(self):
        return '<Post %r>' %self.id


class Apply(db.Model):
    __tablename__='apply'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_link = db.Column(db.String(120), unique=True, nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    

    def __repr__(self):
        return '<Application %r>' %self.id


#################################################################################################


@app.route('/', methods = ['POST','GET'])
def home_page():
    if request.method == 'POST':
        new_post = Feed(brand_name = request.form['brand_name'], platform = request.form['platform'],
        description = request.form['description'])
        db.session.add(new_post)
        db.session.commit()
        return redirect ('/')
    else:
        posts= Feed.query.order_by(Feed.posted_on.desc()).all()
        return render_template('home.html',posts=posts)


@app.route('/application_by_user', methods = ['POST','GET'])
def application_by_user():
    if request.method == 'POST':
        new_application = Apply(name = request.form['name'], email = request.form['email'], 
        profile_link = request.form['profile_link'], feed_id=request.form['feed_id'])
        db.session.add(new_application)
        db.session.commit()
        return redirect ('/')
    else:
        application=Apply.query.order_by(Apply.id).all()
        return render_template('home.html',application=application)


@app.route('/list_of_applications', methods = ['POST','GET'])
def list_of_applications():
    num=request.args.get("feed")
    candidates_list = Apply.query.filter_by(feed_id = num)
    return render_template('list_of_applications.html',list=candidates_list)









