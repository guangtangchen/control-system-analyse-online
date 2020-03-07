#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Version : 1.5
# @Time    : 2019/12/25
# @Author  : GT
# 根轨迹小程序的服务器端

from flask import Flask, request, jsonify
import requests
import datetime
import os
from control import *
import matplotlib.pylab as plt

APP_ID = 'your_appid'
SECRET_KEY = 'your_key'
genguiji_record = '/genguiji/record/record.csv'


# 写入记录
def write_genguiji(username, msg):
    with open(genguiji_record, 'a') as f:
        f.write(datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S") + ', ' + username + ', ' + msg + '\n')


app = Flask(__name__)


@app.route('/draw_genguiji')
def genguiji():
    """ 绘制5个图 """
    def draw_rlocus(sys):
        plt.close()
        rlocus(sys)
        plt.title('Rlocus')
        plt.savefig(path+datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")+'rlocus.png', dpi=300)

    def draw_bode(sys):
        plt.close()
        bode(sys)
        plt.savefig(path+datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")+'bode.png', dpi=200)

    def draw_nyquist(sys):
        plt.close()
        nyquist([sys])
        plt.title('Nyquist')
        plt.savefig(path+datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")+'nyquist.png', dpi=300)

    def draw_step(sys):
        t, r = step_response(sys)
        plt.close()
        plt.plot(t, r, 'blue', linewidth=0.7)
        plt.plot([i for i in t], [1 for i in t], 'r', linewidth=0.5)
        plt.title('Step Response')
        plt.savefig(path+datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")+'step.png', dpi=300)

    def draw_impulse(sys):
        plt.close()
        t, r = impulse_response(sys)
        plt.plot(t, r, 'blue', linewidth=0.7)
        plt.plot([i for i in t], [0 for i in t], 'r', linewidth=0.5)
        plt.title('Impulse Response')
        plt.savefig(path+datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")+'impulse.png', dpi=300)

    tf_data = str(request.values.get('tf_data'))
    username = str(request.values.get('openid'))
    user_list = os.listdir('/genguiji')
    try:
        if username in user_list:    # 第一次登录小程序的用户需要建立一个用户文件夹保存数据
            write_genguiji(username, '已登陆,'+tf_data)
        else:
            os.makedirs('/genguiji/' + username)
            write_genguiji(username, '第一次登录,'+tf_data)
    except:
        return jsonify(['', 'Sorry, your name is not qualified to use this service...'])
    path = r'/genguiji/' + username + '/'
    file_list = os.listdir(path)
    for file in file_list:
        os.remove(path+file)
    try:
        try:   # 对中文逗号和英文逗号进行处理
            try:
                num, den = tf_data.split(',')
            except:
                num, den = tf_data.split('，')
            num = num.split(' ')
            den = den.split(' ')
        except:
            return jsonify(["", '输入非法，请检查是否为英文状态输入以及是否满足上述文字要求'])
        try:
            num.remove('')
        except:
            pass
        try:
            den.remove('')
        except:
            pass
        try:
            for i in range(len(num)):
                num[i] = float(num[i])
            for i in range(len(den)):
                den[i] = float(den[i])
        except:
            return jsonify(['', '数字无法转换！'])
        try:
            sys = tf(num, den)
        except:
            return jsonify(['', '传递函数生成失败'])
        try:
            draw_bode(sys)
        except:
            return jsonify(['', '波特图绘制失败'])
        try:
            draw_step(sys)
            draw_nyquist(sys)
            draw_rlocus(sys)
            draw_impulse(sys)
        except:
            return jsonify(['', '不符合传递函数基本规律，无法绘制！'])
        try:
            filename = os.listdir(path)
            for i in range(len(filename)):
                filename[i] = 'https://your_domin/genguiji_img/' + username + '/' + filename[i]
        except:
            return jsonify(['', '文件解析错误'])
        return jsonify([filename, '点击图片可进行放大保存等操作'])
    except:
        return jsonify(['', '未知错误'])


@app.route('/genguiji_get_openid', methods=['GET', 'POST'])
def genguiji_get_openid():
    """
    获取登录用户的openid
    """
    code = request.values.get('code')
    parmas = {
        'appid': APP_ID,
        'secret': SECRET_KEY,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    r = requests.get(url, params=parmas)
    openid = r.json().get('openid', '')
    write_genguiji(openid, '已登陆')     # 写入日志
    user_list = os.listdir('/genguiji')
    if openid in user_list:
        pass
    else:   # 第一次登录小程序的用户需要建立一个用户文件夹
        os.makedirs('/genguiji/' + openid)
        write_genguiji(openid, '已建立用户文件夹')
    return jsonify([openid, '服务器连接成功！'])


if __name__ == '__main__':
    app.run()





