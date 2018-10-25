from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:homework@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "1234abcd"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125), unique=True)
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25)) 
    password = db.Column(db.String(25))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password,blogs):
        self.username = username
        self.password = password
        self.blogs = blogs

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login') 

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('Password is incorrect, or user does not exist', 'error')
            
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newblog')
        else:
            flash('Fields cannot be left blank', 'error')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect ('/blogs')

@app.route ('/')
def index():
    return redirect ("/blogs")    

@app.route ('/blogs', methods=['POST', "GET"])
def blog():

   post_id = request.args.get('id')

   if post_id:
       #post_id_int = int(post_id)
       name = Blog.query.get(post_id)
       return render_template('bloglist.html',title="Blogz",content="",name=name)

   blogs = Blog.query.all()
   return render_template('bloglist.html',title="Blogz",content=blogs,name="")

@app.route('/newblog', methods=['POST', "GET"]) 
def newblog():

    if request.method == 'POST':
        blog_name = request.form['name']
        blog_content = request.form['content'] 
        owner = request.form["owner_id"]
        
        existing_blog = Blog.query.filter_by(title=blog_name).first()
        
        if not existing_blog:
            new_blog = Blog(blog_name,blog_content,owner)
            db.session.add(new_blog)
            db.session.commit()
            session ['blog_name'] = blog_name

            return redirect("/blogs?id={0}".format(new_blog.id))
        else:
            flash ('Field cannot be left blank', 'error')
    
    return render_template('newblog.html')

   
 
if __name__ == '__main__':
    app.run()