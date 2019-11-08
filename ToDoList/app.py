from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['Task']
        new_task = Todo(content = task_name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return "There was an error adding the task/n{}".format(e)
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks = tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_be_deleted = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_be_deleted)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return "There was an error: {}".format(e)

@app.route("/update/<int:id>", methods = ['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        
        print(str(task))
        task.content = request.form['Task']
        try:
            db.session.commit()
        except Exception as e:
            return "there was an error updating the task :{}".format(e)
    else:
        return render_template("update.html", task = task)
    return redirect("/")
        
if __name__ == "__main__":
    app.run(debug = True)