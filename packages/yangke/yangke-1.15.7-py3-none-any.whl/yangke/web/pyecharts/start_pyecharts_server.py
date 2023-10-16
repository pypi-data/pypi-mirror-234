import os
import sys
import traceback

from yangke.web.pyecharts.app import start_ws_serve
from jinja2 import Environment, select_autoescape, FileSystemLoader
from yangke.common.fileOperate import write_line


def start_pyecharts_server(port=5000, callback=None):
    """
    渲染jinja2模板后，在计算机指定端口上建立长连接监听，用于监听网页端发送给python端的数据，只要接受到数据，就会触发callback方法。本长连接
    相当于是pyecharts的后台服务。python也会通过该端口发送数据以更新html网页端的图表画面。

    开启pyecharts后台服务，如果需要调试前端js代码或html模板，在该方法执行后打开des_file文件即可。des_file文件见本方法第二行定义。

    :param port:
    :param callback: 服务端接收到前端画面返回的信息后，调用的函数
    :return:
    """
    os.chdir(os.path.dirname(__file__))  # 改变当前工作路径
    des_file = os.path.join(os.path.dirname(__file__), "templates", "temp_index.html")  # 渲染后的静态html文件路径

    # ---------------------------- 根据端口渲染目标html文件 -----------------------------------
    template_folder = os.path.join(os.path.dirname(__file__), "templates")  # html模板文件所在的目录
    env = Environment(  # 构建jinja2环境
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape()
    )
    template = env.get_template('index.html')  # jinja2获取模板文件
    write_line(file=des_file, line=template.render(port=port))  # jinja2渲染端口至目标文件中
    # ---------------------------- 根据端口渲染目标html文件 -----------------------------------

    try:
        # 在计算机某个端口上建立长连接，作为python端的接口，监听html网页发送的数据
        start_ws_serve(port=port, callback=callback)
    except:
        traceback.print_exc()


if __name__ == "__main__":
    start_pyecharts_server(5000)
