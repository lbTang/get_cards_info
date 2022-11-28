from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  #这里可以使用其他数据库
db = SQLAlchemy(app) #数据库初始化


# 新建 Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)   #主键
    content = db.Column(db.String(200),nullable=False)  #待办事项内容
    completed = db.Column(db.Integer, default=0) #完成状态
    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)  #创建时间
    
    def __repr__(self):
        return '<Task %r>' % self.id     #%r和%s比，较为简单和直接


@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return '录入任务存在问题！'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '删除存在问题！'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return '修改出现问题！'
    else:
        return render_template('update.html',task=task)


if __name__ == "__main__":
    app.run(debug=True)

