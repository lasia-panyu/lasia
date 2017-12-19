# -- coding: utf-8 --

"""
  注意:传入的格式要符合下列
  我的设计原则是如果前台能处理的逻辑，坚决不让他在后台执行。
  1.对于一个curd的程序，后台处理显的多余且累赘还浪费成本。但是乐死如果花2w比花5k更让人高兴，当我没说。
 {"type":'SELECT',"field":['name','desc'],"tn":'product',"cause":{"id":1}}

"""
from flask import Flask
from flask import Flask,url_for
from flask import request
from flask import render_template
import json
import BsbEntity

app = Flask(__name__)
bsbEntity=BsbEntity.BsbEntity()
bsbDict={"type": 'sqltype', "field": [], "tn": 'tablename', "cause": {}}

#当前台传入符合格式的dict时，可直接返回想要数据，必要时可以添加
@app.route('/bsbDetail/<user_id>')
def bsbDetail(user_id):
    bsbDict['type']='SELECT'
    bsbDict['field'].append('*')
    bsbDict['tn'].append('tb_account_info')
    dict=bsbEntity.execSql(**bsbDict)
    print
    return render_template('detail.html', bsbDict)

@app.route('/post/<int:portId>')
def index(portId):
    return 'index page'+str(portId)


#返回一个你想要的界面，我当然非常赞成单页面程序
#以文件传文件 好办法好吧（恭喜您发现嘲讽1）
@app.route('/forward',methods=['POST','GET'])
def forward():
    if (request.method == 'GET'):
        print request.method
    return url_for('index', portId=100)


#url 跳转，本次迭代暂无设计
@app.route('/')
def bsb(name=None):
    return render_template('lasia.html', name=u"马中马")


#url ajx前台交互模式
@app.route('/bsbjson',methods=['POST'])
def bsbjson():
    a = request.get_data()
    dict1 = a
    print dict1
    dict1=eval(dict1)
    dict1['field'] = ['*']
    dict1['cause'] = {}
    return json.dumps(bsbEntity.execSql(**dict1))


if __name__ == '__main__':
    app.run()


