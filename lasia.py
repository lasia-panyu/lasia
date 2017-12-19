# -- coding: utf-8 --

"""
  注意:传入的格式要符合下列
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

@app.route('/forward',methods=['POST','GET'])
def forward():
    if (request.method == 'GET'):
        print request.method
    return url_for('index', portId=100)

@app.route('/')
def bsb(name=None):
    return render_template('lasia.html', name=u"马中马")

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


