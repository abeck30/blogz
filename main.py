from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:bear@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "1234abcd"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route ('/')
def index():
    return redirect ("/blog")

@app.route ('/blog', methods=['POST', "GET"])
def blog():

    if request.method == 'POST':
        blog_name = request.form['name']
        blog_content = request.form['content']
        new_blog = Blog(blog_name,blog_content)
        db.session.add(new_blog)
        db.session.commit()
        
    name = Blog.query.all()
    content = Blog.query.all()
    return render_template('blog.html',title="Build-a-blog", name=name, content=content)

     #TODO - determine how to check for the same blog post
     #TODO - get blog post underneath blog name


@app.route('/newblog', methods=['POST', "GET"]) 
def newblog():
   #TODO - create error messages if fields in form are left blank
   
    return render_template('/newpost.html')
 
if __name__ == '__main__':
    app.run()