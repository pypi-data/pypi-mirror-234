import setuptools
import os
from gettext import gettext as _

# 国际化：生成语言目录，需要确保相应目录已经创建
# python setup.py extract_messages -k _ --output-file locale/main.pot   # 生成模板，会覆盖已经存在的模板
# python setup.py init_catalog --domain main -l zh_CN -i locale/main.pot -d locale  # 生成po文件
# python setup.py compile_catalog --domain main -l zh_CN -d locale  # 等同上一句

# 发布wheel安装文件
# python setup.py sdist bdist_wheel

# ----------------------- 离线安装1 ------------------------------
# 首先，离线安装最好保证离线计算机和在线计算机架构及软件版本尽量一致。
# 1.安装anaconda,
# 2.复制在线安装生成的conda环境至离线计算机
# 3.win32api库需要运行Scripts\pywin32_postinstall.py，运行方式为：
#   a) 切换到指定env环境，conda activate <python38>
#   b) 运行脚本： python .\Scripts\pywin32_postinstall.py -install
# 如果以上方法迁移后，运行python时出现错误：无法启动此程序，因为计算机中丢失api-ms-win-core-path-l1-1-0.dll尝试重新安装该程序以解决此问题。
# 该错误可能是低版本的anaconda安装高版本的python导致的，如离线机器Anaconda3-2021.05上安装python3.9会出现该问题。
# 解决方法：
# 1.在联网计算机上安装python 3.8，命令如下：
#   a) conda create --name=python38 python=3.8
# 2.将安装的python3.8的虚拟环境复制到离线电脑上
# 3.离线电脑试运行python3.8，如果不再报错，则继续安装以下额外第三方库
# 4.pip download yangke[All] torch torchvision torchaudio tensorflow -d D:/whl
# 5.将D:/whl文件夹复制到离线机器上。
# 6.pip install --no-index --find-links=D:/whl yangke[All] torch torchvision torchaudio tensorflow
# ----------------------- 离线安装1 ------------------------------

# ----------------------- 离线安装2 ------------------------------
# 1.在离线计算机中安装python3.9.12
# 2.在联网机器上安装好所有包，开始在联网计算机上进行以下操作
# 3.执行命令：pip freeze > require.txt，将安装包的信息保存到txt文件
# 4.执行命令: pip wheel -w DIR -r require.txt
# 5.执行命令: pip download -d DIR -r require.txt，如果生成的require.txt中yangke库是本地路径，则删除后面的路径
# 6.将require.txt和dir目录拷贝到离线计算机中，以下为在离线计算机中的操作
# 7.执行命令pip install --no-index --find-links=DIR -r require.txt
# ----------------------- 离线安装2 ------------------------------

# ----------------------- 上传pypi -----------------------------
# twine upload dist/*
# 输入账号密码即可
# yangke08
# YangKe.12
# ----------------------- 上传pypi -----------------------------

from yangke import __version__, extras_require

yangke_version = __version__
with open(os.path.join(os.path.dirname(__file__), 'README.md'), "r", encoding="utf8") as fh:
    long_description = fh.read()

install_requires = [  # 申明依赖包，安装包时pip会自动安装
    'pandas>=1.3.0',
    'pyyaml>=5.2',
    'json5>=0.8.5',
    'dill>=0.3.3',  # 储存函数对象
    'babel>=2.9',
    'pathlib2',
    'pillow>=7.0.0',
    # 'pywin32',  # 如果添加了pywin32依赖，则无法在linux系统上安装，因为依赖无法满足
    'cmake',
    'loguru',
    'apscheduler',
    'matplotlib>=3.5.0',
    'openpyxl>3',
    'pyKriging',
    'opencv-python',
    'psutil',
    'markupsafe>=2.1.1',  # scrapy框架需要
    'pyecharts',
    'iapws>=1.5',
    'qt_material',

],

all_lib = []
for v in extras_require.values():
    all_lib.extend(v)
all_lib = list(set(all_lib))
extras_require['All'] = all_lib
extras_require['ugly'] = [  # 容易出错的包
    'dlib>=19.17.0',  # dlib需要单独安装，涉及到cmake和boost
    'torch>=1.4.0',  # pytorch需要单独安装，pypi里版本太老
    'scikit_learn',  # 32位python中该库无法从源代码编译安装，需要下载whl文件安装
    'scipy',  # 32位无法从源代码编译安装，需要下载whl文件安装
    'PyQt6-WebEngine',  # 32位python无法安装该库
    'pyWinhook>=1.6.2',  # 32位python无法编译安装，需要下载whl文件安装
    'scikit-image>=0.19.3',  # paddleocr依赖
    'lmdb>=1.3.0',  # paddleocr依赖
    'orjson>3.7.3',  # paddleocr依赖
]

setuptools.setup(
    name="yangke",  # 模块名
    version=yangke_version,
    packages=setuptools.find_packages(
        exclude=['StockData', 'yangke..idea', 'yangke..git']),  # 这里输入Mod包文件目录
    # scripts=["sis_io.py"],
    py_modules=["main",
                # "yangke/spider/stock10jqka/start_stock10jqka",
                # "yangke\spider\stock10jqka\stock10jqka\spiders\jqka_spider",
                ],  # 打包的*.py文件

    package_data={
        "": ["*.py", "*.cfg", "*.js", "*.html", "*.ico"],
    },
    include_package_data=True,  # 将MANIFEST.in中的文件也打包进wheel文件中

    python_requires=">=3.6",

    # metadata to display on PyPI
    author="杨可",
    author_email="yangyangyangkekeke@qq.com",
    description=_("个人工具综合平台，包含常用工具，网络爬虫，知识图谱，神经网络预测等工具"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="yangke",
    url="https://gitee.com/yangke02/lib4python",
    project_urls={
        "Bug Tracter": "https://gitee.com/yangke02/lib4python",
        "Documentation": "https://gitee.com/yangke02/lib4python",
        "Source Code": "https://gitee.com/yangke02/lib4python",
        "Funding": "https://gitee.com/yangke02/lib4python",
    },
    classifiers=[  # 给pip工具一些额外的元数据信息，只是用来给pypi提供搜索依据的，对实际项目不做任何限制
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: Freely Distributable",
        "Natural Language :: Chinese (Simplified)",

        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=install_requires,
    extras_require=extras_require,
    message_extractors={
        'yangke': [
            ('**.py', 'python', None),
            # ('**/templates/**.html', 'genshi', None),
            # ('**/templates/**.txt', 'genshi', {'template_class': 'genshi.template:TextTemplate'})
        ],
    },
)
