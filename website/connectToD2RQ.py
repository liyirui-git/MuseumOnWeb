# 启动D2RQ的服务端口
# 此处给D2RQ单独建立了一个线程
# 在view.py中的register函数里面负责开启这个线程
import threading
import os


class D2RQ (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("开启D2RQ:")
        os.system("cd C:\ProgramFiles\d2rq-0.8.1 && d2r-server.bat mapping1.ttl")
