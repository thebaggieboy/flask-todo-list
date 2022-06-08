from email.policy import default
from enum import unique
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return self.id

# Routes 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        task_title = request.form['title']
        task_content = request.form['content']
        
        new_task = Todo(title=task_title, content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
        


    

@app.route('/task/<int:id>/', methods=['GET', 'POST'])
def task(id):
    task = Todo.query.get_or_404(id)
    return render_template('task_details.html', task=task)


@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        redirect('/')
    except:
        return "There was a problem deleting that task."

    return render_template('delete_task.html', task=task)
    

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.title = request.form['title']
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    return render_template('update_task.html', task=task)





if __name__ == "main":
    app.run(debug=True)


