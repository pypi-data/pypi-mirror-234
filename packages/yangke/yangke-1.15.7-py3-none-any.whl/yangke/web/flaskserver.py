from flask import Flask, request, jsonify, make_response, send_from_directory, Response
from yangke.base import name_transfer
from flask_cors import *
from yangke.common.config import logger
import traceback
import os

example = None


def start_server_app(deal=None, app_name='yangke.web.flaskserver', instance_path=__file__,
                     instance_relative_config=True, host="0.0.0.0", port="5000", allow_action=None, use_action=True,
                     example_url=None, content="json", template_folder="templates", static_folder="static",
                     run_immediate=True):
    """
    启动Flask Server服务，服务启动后将调用用户传入的deal函数来对url请求进行处理，deal函数通过args参数拿到请求的参数字典。
    如果用户需要自定义deal函数处理http://127.0.0.1:5000这类没有参数的url，则应设置useAction为False，并在deal函数中对空字典进行判断处理。
    如果用户需要过滤允许的Action类型，则需要设置允许的操作类型列表allow_action。

    当use_action为True时，如果请求url不带Action参数，则该方法会自动返回提示信息。因此，传递给用户函数deal的参数字典中确保含有Action参数。
    当use_action为False时，即使请求url不带任何参数，也会调用deal函数，且将对应的参数字典或空字典传递给deal函数，deal函数需要判空。

    使用示例1：
    #==============================================================================================
    def deal(args):
        action = args.get('Action')  # 因为下方use_action=True，所以这里的action必然有值，避免eval函数出错
        result = eval("{}(args)".format(action))
        return result

    start_server_app(deal, use_action=True)  # 启动服务器.
    #==============================================================================================

    使用示例2：创建app后，可以通过@app.route('/')设置路由，主要是deal=None和run_immediate=False两个参数设置,通过run()方法启动服务
    #==============================================================================================
    app = start_server_app(deal=None, use_action=False, template_folder=os.path.abspath("templates"), content="html",
                       run_immediate=False)
    @app.route("/add")
    def add(args):
        var1 = args.get("var1")
        var2 = args.get("var2")
        return str(var1+var2)
    run(app)
    #==============================================================================================

    :param use_action: 是否使用Action参数指定操作类型，不使用则完全由用户定义所有url响应
    :param deal: 用户指定的url处理方法
    :param app_name: Flask app名，一般不需要也不能更改，Flask根据该参数查找模板和静态文件等东西
    :param instance_path:
    :param instance_relative_config:
    :param host:
    :param port:
    :param allow_action:  允许用户调用的方法
    :param example_url: 示例http访问请求，当用户访问出错时提示用户
    :param content: 如果content="json"，则会将json字符串包装一下返回，如果为"html"，则直接返回deal的执行结果
    :param template_folder: 静态资源路径
    :param static_folder: 除了原Flask的路径功能外，下载文件时默认的检索路径也是该目录
    :param run_immediate: 是否立即运行，默认为True,否则返回app对象，可以由用户进一步处理后，调用run(app)运行
    :return:
    """
    app = Flask(app_name, instance_path=instance_path, instance_relative_config=instance_relative_config,
                template_folder=template_folder, static_folder=static_folder)
    app.logger = logger
    app.config['JSON_AS_ASCII'] = False  # 让Flask返回的字符串可以正确显示中文，默认显示的是utf-8编码
    CORS(app)
    global example
    example = example_url

    # 当用户自定义'/'路由时，此处不能添加，因此，后面判断deal不为None时，则手动添加app.route，否则说明用户自定义了'/'路由
    # @app.route('/', methods=['GET', 'POST'])
    def start_service():
        if deal is None:
            return {}
        t = request.get_data(as_text=True).split('=')
        t_dict = {}
        if len(t) > 1:
            for ix in range(0, len(t), 2):  # start=0, stop=len(t), step=2
                t_dict[str(t[ix])] = t[ix + 1]
        args = dict(request.args)
        args.update(t_dict)
        args.update(request.form)
        action = request.args.get('Action')
        # allow_action为空，表示没有设置允许的操作，则放行所有Action
        if allow_action is None or action in allow_action:
            if use_action:
                if len(args) == 0:
                    global example
                    if example is None:
                        example = [f"http://{host}:{port}/?Action=CreatePerson&GroupName=test&PersonName=yk",
                                   f"http://{host}:{port}/download/test.xlsx"
                                   ]
                    return jsonify({"Success": True,
                                    "Info": "服务正常，请使用Action传入指定的操作！",
                                    "Example": example})
                else:
                    logger.debug("执行操作{}".format(action))
                    logger.debug(args)
            else:  # 没有使用Action，则直接放行，将所有请求转发至deal函数
                pass
            try:
                # result = eval("{}(args)".format(action))
                result = deal(args) or {}  # 需要确保result不为空
            except:
                traceback.print_exc()
                if use_action:
                    logger.debug(f"远程调用了{action}方法，但该方法在服务端没有定义！")
                    return jsonify({"Success": False, "Info": "未知命令：{}".format(action)})
                else:
                    return jsonify({"Success": False})
            if content == "html":
                return result
            elif content == "rawJson":
                return jsonify(result)
            else:
                result = name_transfer(result, 'CamelCase')  # 将字典中key的命名方式修改为驼峰命名方式
                result1 = jsonify(result)
                return result1

        else:
            logger.debug("操作{}不允许".format(action))
            return jsonify({"Success": False, "Info": "操作不允许，操作类型：{}".format(action)})

    def start_service_null():
        global example
        if example is None:
            example = [
                f"http://localhost:{port}/download/test.xlsx"
            ]
        return jsonify({"Success": True, "Info": f"通过 http://localhost:{port}/download/baidu.py 下载文件",
                        "Example": example})

    @app.route('/download/<file_name>', methods=['GET', 'POST'])
    @cross_origin(origins="*", methods=['GET', 'POST'])
    def download_file(file_name):
        """
        下载文件功能，该功能默认启动。通过 ip:port/download/<file_name> 下载文件
        如果初始化时，传入的static_folder为绝对路径，则可以直接下载到绝对路径下的文件。
        否则下载到的是工作目录下的"static"下的文件，如果上述两个目录下未找到文件，则在../yangke/web/static/下查找

        前段通过 ip/download/<下载参数>进行下载，这里的下载参数一般是文件名。
        @download
        def deal(args_str):
            return os.path.join("C:/users", args_str)

        :param file_name: 前段传入的下载参数，一般为文件名，如果是中文文件名，只接受使用utf8编码为base64的字符串
        :return:
        """
        logger.debug(f"下载文件{file_name}")
        if os.path.isabs(app.static_folder):  # 优先使用app.static_folder作为被下载文件的检索路径
            directory = app.static_folder
        else:
            directory = os.path.join(os.getcwd(), app.static_folder)

        from yangke.base import is_base64_code
        import base64
        if is_base64_code(file_name):
            file_name = base64.b64decode(file_name).decode("utf8")
        # 如果app.static_folder下不存在被下载文件，则在yangke.web.static下查找
        if not os.path.exists(os.path.join(directory, file_name)):
            directory = os.path.join(os.path.dirname(__file__), "static")
        if not os.path.exists(os.path.join(directory, file_name)):  # 如果文件没找到，则返回错误
            return jsonify({"Info": f"文件下载失败，服务器端文件不存在，{os.path.abspath(file_name)}",
                            "Success": False})
        response = make_response(send_from_directory(directory, file_name, as_attachment=True))
        return response

    @app.route('/preview/<file_name>', methods=['GET', 'POST'])
    @cross_origin(origins="*", methods=['GET', 'POST'])
    def preview_file(file_name):
        """
        在线预览文件，暂不支持
        """
        url = f"http://localhost:8012/onlinePreview?url=aHR0cDovL2xvY2FsaG9zdDo1MDAwL2Rvd25sb2FkL3Rlc3QueGxzeA%3D%3D"

    options = {'methods': ['GET', 'POST']}
    endpoint = options.pop("endpoint", None)
    if deal is not None:  # 当deal不为None时，则"/"的路由有deal处理
        options = {'methods': ['GET', 'POST']}
        endpoint = options.pop("endpoint", None)
        app.add_url_rule("/", endpoint, start_service, **options)  # 相当于使用@app.route('/')，将start_service服务添加到/路由上
    else:
        app.add_url_rule("/", endpoint, start_service_null, **options)
    if run_immediate:  # 如果需要立即运行
        logger.info(f"服务已启动，通过 http://localhost:{port}/ 访问")
        from waitress import serve
        serve(app, host=host, port=port)
    return app


def run(app, host="0.0.0.0", port="5000"):
    logger.info(f"服务已启动，通过 http://localhost:{port}/ 访问")
    from waitress import serve
    serve(app, host=host, port=port)
    return app


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port='5678', use_reloader=False)
    app = start_server_app()
