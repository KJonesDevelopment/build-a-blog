from flask import Flask, request, redirect, render_template
import jinja2
import os
import re
import cgi
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route("/", methods=["POST", "GET"])
def index():    
    entries = Blog.query.all()
    return render_template('blogsetup.html', entries = entries)

class Blog(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    tagline = db.Column(db.String(43))
    body = db.Column(db.String(20000))

    def __init__(self, id, title, tagline, body):
        self.title = title
        self.tagline = tagline
        self.body = body

    def __repr__(self):
        return self.title 


@app.route("/addentry", methods=["POST", "GET"])
def hello():
    return render_template('addentry.html')

@app.route("/thankyou", methods=["POST", "GET"])
def thankyou():
    if request.method == "POST":
        title = request.form['title']
        titleError = verifyTitle(title)
        entry = request.form['body']
        entryError = veryifyEntry(entry)
        if title != titleError:
            return render_template('addentry.html', titleError=titleError, entry=entry, entryError=entryError)
        tagline = verifyTag(request.form['tagline'], entry)
        newEntry = Blog(id, title, tagline, entry)
        db.session.add(newEntry)
        db.session.commit()
        return render_template('thankyou.html', title=title)
    return "I'm sorry, please navigate back to the main page"

def veryifyEntry(entry):
    if len(entry) < 1: 
        return "Please enter a body"
    return "" 

def verifyTitle(title): 
    if len(title) < 1: 
        return "Please enter a title"    
    return title

def verifyTag(tagline, entry):
    if len(tagline) < 1: 
        entry = entry[:40]+"..."
        return entry
    return tagline

@app.route("/blog")
def blogpage():
    blogid = request.args.get("id")
    blog = Blog.query.get(blogid)
    blog.body = '<br>'.join(blog.body.split('\n'))
    return render_template("blog.html", blog = blog)

    
if __name__ == "__main__": 
    app.run()
