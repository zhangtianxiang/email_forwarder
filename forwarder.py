# -*- coding: utf-8 -*-
# title:
# by ztx
# blog.csdn.net/hzoi_ztx

import _thread

from flask import Flask, jsonify, request, make_response
from flask_mail import Mail, Message


RECEIVERS = ['ztx97@qq.com']
FORWARDER_PASS = ''
DEBUG = False
HOST = '127.0.0.1'
PORT = 5050


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'tianxiang971016@gmail.com'
app.config['MAIL_PASSWORD'] = FORWARDER_PASS

mail = Mail(app)


def send_email_sync(title='Empty Title',sender='tianxiang971016@gmail.com',receivers=['ztx97@qq.com'],content='Empty content'):
    print('[msg_sender sending]')
    print('title:',title,'sender:',sender,'receivers:',receivers,'content:',content)
    msg = Message(title, sender=sender, recipients=receivers)
    msg.body = content
    with app.app_context():
        mail.send(msg)
    print('[msg_sender sent]')


def send_email_async(title='Empty Title',sender='tianxiang971016@gmail.com',receivers=['ztx97@qq.com'],content='Empty content'):
    _thread.start_new_thread(send_email_sync,(title,sender,receivers,content))


def allow_cross_response(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,Content-Type'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response


@app.route('/')
def index():
    return 'ztx email forwarder running'


@app.route('/api/send_email_async',methods=['POST'])
def api_send_email_async():
    name = request.form.get('name')
    replyemail = request.form.get('replyemail')
    message = request.form.get('message')
    if not name:
        return allow_cross_response(make_response(jsonify({'state':1,'message':'Empty name'})))
    if not message:
        message = ''
    else:
        message += '\n'
    message += 'From '+name
    if replyemail:
        message += '('+replyemail+')'
    send_email_async(title='祝你生日快乐！',sender='admin@forwarder.com',receivers=RECEIVERS,content=message)
    return allow_cross_response(make_response(jsonify({'state':0,'message':'sent'})))


@app.route('/api/send_email_sync',methods=['POST'])
def api_send_email_sync():
    name = request.form.get('name')
    replyemail = request.form.get('replyemail')
    message = request.form.get('message')
    if not name:
        return allow_cross_response(make_response(jsonify({'state':1,'message':'Empty name'})))
    if not message:
        message = ''
    else:
        message += '\n'
    message += 'From '+name
    if replyemail:
        message += '('+replyemail+')'
    send_email_sync(title='祝你生日快乐！',sender='admin@forwarder.com',receivers=RECEIVERS,content=message)
    return allow_cross_response(make_response(jsonify({'state':0,'message':'sent'})))


if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=DEBUG)