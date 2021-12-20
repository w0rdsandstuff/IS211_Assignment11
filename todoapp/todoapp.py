from flask import request
from flask import Flask
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)






class Tasklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    
    
    def __init__(self, task, email, priority):
        self.task = task
        self.email = email
        self.priority = priority        


@app.route('/', methods=['POST', 'GET'])
def todolist():
    if request.method == 'POST':
        task_name = request.form['task']
        email_name = request.form['email']
        priority_name = request.form['priority']
        new_task = Tasklist(task=task_name, email=email_name, priority=priority_name)
    
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    else:
        task = Tasklist.query.order_by(Tasklist.priority)
        return render_template("to_do.html", task=task)


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)