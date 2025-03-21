from flask import Flask, render_template, url_for, request, redirect, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# Create database and tables
# from app import db
# db.create_all()


app = Flask(__name__)
#27.0.0.1 er localhost
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://storm:ElvebakkenIM@127.0.0.1/brukerflask'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)

def __repr__(self):
    return '<Task %r>' % self.id
@app.route("/", methods=['POST', 'GET'])
def index():  
    if request.method == 'POST': #Henter info og putter i database
        task_content = request.form['content'] #Henter info fra content i index.html
        new_task = Todo(content=task_content) #Lager ny task med content

        try:
            db.session.add(new_task)
            db.session.commit() #Legger til i database
            return redirect('/') #Redirecter til index.html
        except:
            return f"ERROR"
    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #Henter informasjon fra databasen sortert i dato lagd, nyest til eldst
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR'
    else:
        return render_template('update.html', task=task)
    
@app.route('/done/<int:id>')
def mark_done(id):
    task = Todo.query.get_or_404(id)
    task.done = True  # Eller bruk 1 hvis databasen ikke støtter Boolean
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR'

if __name__ == '__main__':
    app.run(debugging=True)