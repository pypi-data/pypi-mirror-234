import os
import socket
import base64
import hashlib
import json
import traceback
from pyecharts import options
from pyecharts.charts import Bar
from yangke.base import start_threads
from yangke.common.config import logger
from yangke.common.fileOperate import read_lines, write_lines

connections_available = []
stop_serve = False
ready = False


class DataPackage:
    def __init__(self, cmd: str, option=None, series=None, args: dict | None = None):
        """
        发送给html网页端的数据包结构，pyecharts使用，用于其他数据包发送时，需要通过args传递参数。

        :param cmd: 命令，js端根据该命令执行相应的处理。
        :param option: echarts的option对象
        :param series: echarts的series对象
        :param args: 发送给前端的数据对象，是一个字典。如果命令不需要参数，可以不指定该参数。
        """
        self.cmd = cmd
        self.option = option
        self.series = series
        self.args = args

    def to_msg(self):
        """
        将当前数据包转换为json字符串
        """
        if self.args is None:
            self.args = {"cmd": self.cmd, "option": self.option, "series": self.series}
        else:
            self.args.update({"cmd": self.cmd, "option": self.option, "series": self.series})
        return self.args

    def send(self):
        send_msg(self.to_msg())


def get_headers(data):
    """
    解析浏览器端发送到websocket的数据头
    """
    header_dict = {}
    data = data.decode(encoding='utf-8')

    header, body = data.split("\r\n\r\n", 1)
    header_list = header.split("\r\n")
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(":", 1)
            header_dict[k] = v.strip()
    return header_dict


def send_msg(msg):
    """
    WebSocket服务端向客户端发送消息。即python端向html网页发送数据。
    示例1：
    send_msg("你好")
    示例2：
    from pyecharts.charts import Bar
    c = (
    Bar()
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
    .set_global_opts(title_opts=options.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    message = c.dump_options_with_quotes()
    send_msg(message)

    :param msg: 向客户端发送的数据，可以是字符串或字典
    :return:
    """
    import struct
    if isinstance(msg, str):
        print(f"发送消息：{msg}")
        msg = msg.encode('utf8')
    elif isinstance(msg, dict) or isinstance(msg, list):
        print(f"发送消息：dict object")
        msg = json.dumps(msg)
        msg = msg.encode('utf8')
    # 不知道以下编码规则是啥，尝试删除看还能不能正常发送数据
    token = b"\x81"

    length = len(msg)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg
    for conn in connections_available:
        try:
            conn.send(msg)
        except ConnectionAbortedError:  # 强行关闭前端网页时，可能出现连接实际已经不存在，但后台还有记录
            pass
    return True


def start_ws_serve(port=8017, ip='127.0.0.1', callback=None):
    """
    在计算机某个端口上建立长连接监听

    :param port:
    :param ip:
    :param callback: 服务端接收到前端画面返回的信息后，调用的函数
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(5)  # 允许的连接数量
    global connections_available
    print(f"服务建立：{ip}:{port}")
    global stop_serve, ready
    stop_serve = False
    ready = True
    while True:
        conn, address = sock.accept()
        data = conn.recv(1024)  # 阻塞式监听
        headers = get_headers(data)  # 网页端打开并初次建立ws连接时，会发送header数据
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection:Upgrade\r\n" \
                       "Sec-WebSocket-Accept:%s\r\n" \
                       "WebSocket-Location:ws://%s%s\r\n\r\n"

        value = headers['Sec-WebSocket-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
        conn.send(bytes(response_str, encoding='utf-8'))
        start_threads(on_message, (conn, callback))  # 启动新线程处理该连接，相当于调用on_message(conn, callback)
        print(f"接收到新的连接：{response_str=}, {conn=}")
        connections_available.append(conn)  # 记录已建立的连接，以方便在退出时关闭这些连接
        if stop_serve:  # 当外界将stop_serve设置为True时，则长连接退出
            break
    for conn in connections_available:
        conn.close()
    sock.close()


def decode_bytes(ws_bytes):
    """
    解码前端长连接返回的数据，解码原理未知，反正不是UTF8

    :param ws_bytes:
    :return:
    """
    if len(ws_bytes) == 0:
        return ""
    payload_len = ws_bytes[1] & 127
    if payload_len == 126:
        extend_payload_len = ws_bytes[2:4]
        mask = ws_bytes[4:8]
        decoded = ws_bytes[8:]
    elif payload_len == 127:
        extend_payload_len = ws_bytes[2:10]
        mask = ws_bytes[10:14]
        decoded = ws_bytes[14:]
    else:
        extend_payload_len = None
        mask = ws_bytes[2:6]
        decoded = ws_bytes[6:]

    bytes_list = bytearray()
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    try:
        message = bytes_list.decode("utf8")
        return message
    except UnicodeDecodeError:
        if bytes_list == b"\x03\xe9":
            return "close"
        else:
            logger.warning(f"解码字节流{bytes_list}时出错！")


def on_message(conn: socket.socket, callback=None):
    """
    该线程一直监听端口，接收前端发回的信息，并处理

    :param conn:
    :param callback: 后台接收到消息后，执行的回调函数
    :return:
    """
    while True:
        try:
            info = conn.recv(8096)
        except Exception as e:
            logger.warning("发生异常，但服务仍继续")
            break
        info = decode_bytes(info)
        if info == "close":
            print(f"conn-{conn.getpeername()[1]}连接已关闭！")
            if conn in connections_available:
                connections_available.remove(conn)
            conn.close()
            break
        elif info != "":
            print(f"服务器接收到conn-{conn.getpeername()[1]}的消息：{info}")
            if info == "test":
                c = (
                    Bar()
                    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
                    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
                    .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
                    .set_global_opts(title_opts=options.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
                )
                echarts_option = c.dump_options_with_quotes()  # pyecharts将图表设置转换为网页端可以理解的字符串，类似于字典
                data_package = DataPackage(cmd="initChart", option=echarts_option)
                data_package.send()  # 发送数据包
            if type(callback).__name__ == "method" or type(callback).__name__ == "function":
                callback(info)


def stop_ws_serve():
    global ready
    global stop_serve
    stop_serve = True
    ready = False


def is_ready():
    return ready


if __name__ == "__main__":
    start_ws_serve()
