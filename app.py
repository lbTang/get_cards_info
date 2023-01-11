from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import datetime

from werkzeug.utils import redirect
from cards_downloader import cards_downloader


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'  #这里可以使用其他数据库
db = SQLAlchemy(app) #数据库初始化


# 新建 Model
class Phone_Card(db.Model):
    __tablename__ = "cards_info"

    card_no = db.Column(db.String(200),nullable=False,primary_key=True)  #卡编号
    card_name = db.Column(db.String(200)) #卡名
    plan_detail = db.Column(db.String(200)) #套餐详情
    addition = db.Column(db.String(200)) #附加说明
    monthly_cost = db.Column(db.String(200)) #流量卡月租
    full_name = db.Column(db.String(200)) #完整卡名
    detail_url = db.Column(db.String(200)) #流量卡链接
    card_state = db.Column(db.Integer,default=1) #卡的状态。1：生效，0：失效。
    is_published = db.Column(db.Integer,default=0) #是否已发布。0：未发布，1已发布。
    date_created = db.Column(db.DateTime,default=datetime.datetime.utcnow)  #创建时间
    date_expiration = db.Column(db.DateTime,default= datetime.datetime(2099, 12, 30, 0, 0)  # 用指定日期时间创建 datetime 对象

) #失效时间
     
    def __repr__(self):
        return '<流量卡 %r %r>' % (self.card_no,self.card_name)     #%r和%s比，较为简单和直接



@app.route('/',methods=['GET'])
def index():
    card_downloader = cards_downloader()
    cards_info = card_downloader.work()
    for card in cards_info:
        new_card = Phone_Card(card_no = card['card_no'],
                              card_name = card['card_name'],
                              full_name = card['full_name'],
                              plan_detail = card['plan_detail'],
                              addition = card['addition'],
                              monthly_cost = card['monthly_cost'],
                              detail_url = card['detail_url']
                              )
        try:
            db.session.add(new_card)
            db.session.commit()
        except:
            app.logger.error('录入流量卡存在问题！')
    cards = Phone_Card.query.all()
    sort_attr = request.args.get("sort",'')
    return render_template('index.html', cards = cards, sort_attr = sort_attr)



if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

