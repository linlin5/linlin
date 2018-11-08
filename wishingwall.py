#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from tornado import web, ioloop, httpserver
import time
import json

# 留言存在全局变量中
MESSAGES = [
    {'id': 1,'name':'零零', 'time':'2018-11-07', 'content':'来来来，一起许下愿望吧~', 'num': 1}
]

#首页模块
class MainPageHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        #self.write("HELLO")
        self.render('index.html', messages=MESSAGES)
        #渲染前端页面的函数

#许愿
class WishHandler(web.RequestHandler):
    # 返回许愿界面
    def get(self, *args, **kwargs): # 对应http get 请求
        #第一次访问许愿页面
        self.render('wish.html')

    # 接收前端传递的数据，post 请求
    def post(self, *args, **kwargs): # 对应http post 请求
        #获取前端传递的数据
        content = self.get_argument('content',default=None)
        #print(context)
        name = self.get_argument('name', default=None)
        #print(name)
        if not name:
            name = '匿名'
        if content: # 敏感词汇 过滤
            # 添加 每个人的愿望
            MESSAGES.append({
                'name': name,
                'content': content,
                'id': len(MESSAGES) + 1,
                'num': len(MESSAGES) + 1,
                'time': time.strftime('%Y-%m-%d')
            })
            # 跳转
            self.redirect('/') #跳转到首页面
        else:
            self.write('内容不能为空')


#设置
settings = {
    'template_path':'templates', # 设置模板文件的路径
    'static_path':'statics'#设置静态文件路径
}

#路由分配
application = web.Application([
    (r"/", MainPageHandler),
    (r"/wish", WishHandler),
    ], **settings)


if __name__ =='__main__':
    http_server = httpserver.HTTPServer(application)
    http_server.listen(1001)
    ioloop.IOLoop.current().start()

####打开网页：http://127.0.0.1:8080/





