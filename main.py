from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:**B1r2y3B$$@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner_id = owner

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(30))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

'''
# require users to login if not currently in a session.
# uncomment once sessions are added
@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')
'''

#@app.route('/', methods=['POST'])
#def index():
'''
if request.method == 'POST':
    task_name = request.form['task']
    new_task = Task(task_name)
    db.session.add(new_task)
    db.session.commit()

tasks = Task.query.filter_by(completed=False).all()
completed_tasks = Task.query.filter_by(completed=True).all()
return render_template('todos.html',title="Get It Done!", 
    tasks=tasks, completed_tasks=completed_tasks)
'''
#   return pass

@app.route('/blog', methods=['GET'])
def view_blog():
    #TODO - display all blog posts from newest to oldest
    #TODO - only display blog posts that are owned by the user
    blog_entries = Blog.query.all()
    return render_template('blog.html',blog_view=blog_entries) 

@app.route('/newpost', methods=['POST'])
def add_new_post():
    #TODO - submit new blog post
    #TODO - After submitted the app displays(redirect) the main blog page /blog to view the new post
    #TODO - Blog must have title and body, if false return newpost.html with helpful error message and any previously entered content

    return view_blog() 



if __name__ == '__main__':
    app.run()