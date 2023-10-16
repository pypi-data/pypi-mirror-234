import os
import socket

# 读取本机全部ip列表
# return list
def get_ips():
    return socket.gethostbyname_ex(socket.gethostname())[-1]

# 读取本机的ip地址
# return str
def get_ip():
    # 优先读取活跃ip地址
    routes = os.popen('route print').readlines()
    for idx, item in enumerate(routes):
        if ' 0.0.0.0 ' in item and len(item.split()) > 2:
            return item.split()[-2]
    
    # 取第一个地址
    ips = get_ips()
    if len(ips) > 0 :
        return ips[0]

    raise ValueError("Ip address not exists.")
