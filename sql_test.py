from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_sql.db'  #这里可以使用其他数据库
db = SQLAlchemy(app) #数据库初始化


# 新建 Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)   #主键
    content = db.Column(db.String(200),nullable=False)  #待办事项内容
    completed = db.Column(db.Integer, default=0) #完成状态
    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)  #创建时间
    
    def __repr__(self):
        return '<Task %r>' % self.id     #%r和%s比，较为简单和直接

if __name__ == '__main__':
    cards = [{'card_no': '1402', 'card_name': '联通乐丰卡', 'plan_detail': '115G通用流量+100分钟通话', 'addition': '', 'monthly_cost': '29元', 'full_name': '1402 | 联通乐丰卡29元包115G通用流量+100分钟通话', 'detail_url': 'http://ka.05321888.com/ka/taocan/1402.html'}, 
    {'card_no': '1401', 'card_name': '联通祥和卡', 'plan_detail': '105G通用流量+200分钟通话', 'addition': '', 'monthly_cost': '29元', 'full_name': '1401 | 联通祥和卡29元包105G通用流量+200分钟通话', 'detail_url': 'http://ka.05321888.com/ka/taocan/1401.html'}, 
    {'card_no': '1400', 'card_name': '电信星空卡', 'plan_detail': '70G通用+30G定向+通话0.1元/分钟', 'addition': '', 'monthly_cost': '19元', 'full_name': '1400 | 电信星空卡19元包70G通用+30G定向+通话0.1元/分钟', 'detail_url': 'http://ka.05321888.com/ka/taocan/1400.html'}]
    newTodo = Todo(content="这是新的代办事项")
    try:
        db.session.add(newTodo)
        db.session.commit()
    except:
        print('录入流量卡存在问题！')
