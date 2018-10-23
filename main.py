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
    title = db.Column(db.String(125), unique=True)
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route ('/')
def index():
    return redirect ("/blogs")

@app.route ('/blogs', methods=['POST', "GET"])
def blog():

   post_id = request.args.get('id')

   if post_id:
       #post_id_int = int(post_id)
       #TODO check if name is not blank display the one posting or (Else) display everything 9o8
       name = Blog.query.get(post_id)
       return render_template('bloglist.html',title="Blogs Page",content="",name=name)

   blogs = Blog.query.all()
   return render_template('bloglist.html',title="Blogs Page",content=blogs,name="")

@app.route('/newblog', methods=['POST', "GET"]) 
def newblog():

    if request.method == 'POST':
        blog_name = request.form['name']
        blog_content = request.form['content'] 
        
        existing_blog = Blog.query.filter_by(title=blog_name).first()
        
        if not existing_blog:
            new_blog = Blog(blog_name,blog_content)
            db.session.add(new_blog)
            db.session.commit()
            session ['blog_name'] = blog_name

            return redirect("/blogs?id={0}".format(new_blog.id))
        else:
            flash ('Field cannot be left blank', 'error')
    
    return render_template('newblog.html')

   
 
if __name__ == '__main__':
    app.run()