import datetime
import os.path
from enum import unique, Enum
from shutil import copyfile

from yangke.base import get_key_value, yield_every_day
from yangke.common.fileOperate import fill_excel_cell
from yangke.sis.export_history_values import get_history


class Report:
    def __init__(self, template, tags, report_type="year", cache_folder="cache"):
        """
        报表类，用于生成基于Excel的报表

        tags示例：
# ----------------------------------------------------------
from enum import unique, Enum
from yangke.base import get_key_value
@unique
@get_key_value
class TagsRead(Enum):
    发电机功率1 = "DCS1:LOAD"
    总燃料量1 = "DCS1:TFFREAL"
tags = TagsRead
# ----------------------------------------------------------

        :param template: 报表的模板文件，一般为excel文件
        :param tags: 报表用到的数在RDBProxy代理服务器上的测点信息
        :param report_type: 报表类型，可取值'year', 'month'，表示报表需要的数据的范围，year表示需要一年的数据，month表示需要一月的数据
        :param cache_folder: 缓存文件夹
        """
        self.template = template
        self.out_file = None  # 报表的输出文件，由self.generate_report_excel()方法指定
        self.tags = tags
        self.report_type = report_type
        self.cache_folder = os.path.abspath(cache_folder)
        self.year = None
        self.month = None
        self.week = None
        self.day = None
        self.rules = []
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

    def generate_report_excel(self, out_file, year=None, month=None, week=None, day=None):
        """
        生成报表文件

        :param out_file: 报表保存的文件
        :param year: 年份，如果不指定，则默认生成今年
        :param month: 如果是月报，则需要指定月份，如果不指定，则默认当月
        :param week:
        :param day:
        :return:
        """

        now = datetime.datetime.now()
        if self.report_type == "year":
            self.year = year or now.year
        elif self.report_type == "month":
            self.year = year or now.year
            self.month = month or now.month
        elif self.report_type == "week":
            self.year = year or now.year
            _week = int(now.strftime('%W'))  # %W取一年中的星期数（00-53），星期一为星期的开始，%w星期天为星期的开始
            self.week = week or _week
        elif self.report_type == "day":
            self.year = year or now.year
            self.month = month or now.month
            self.day = day or now.day  # 月中的天数{1-31}，不是年中的天数

        start_time, end_time = None, None
        if self.report_type == "year":  # 如果是年报，应该只有year参数是有数的
            start_time = f"{self.year}-1-1 00:00:00"
            end_time = now if self.year >= now.year else f"{self.year}-12-31 23:59:59"
        elif self.report_type == "month":  # 如果是月报
            start_time = f"{self.year}-{self.month}-1 00:00:00"
            if self.year == now.year and self.month == now.month:
                end_time = now
            else:
                end_time = f"{self.year}-{self.month}- 23:59:59"  # 某月的最后一天

        self.download_data(start_time, end_time)

        # 复制模板文件作为报表文件的输出文件
        copyfile(self.template, out_file)
        self.out_file = out_file
        self.exec_rules()  # 执行报表生成规则，填充报表

        return self.out_file

    def add_fill_rules(self, excel_cell=None, content: str | dict = "test hello world"):
        """
        excel文件的填充规则。

        content内容可以是参数组成的公式，参数必须在self.tags中存在。示例如下：
        content = {"expression": "累积值(发电机功率1, 2022-1-1)"}表示填充内容是2022年1月1日发电机功率1的累积值。因为
        数据库中功率单位一般为MW，则累积值单位是MWs，换算成电量kWh应该除以3.6，所以，如果需要填入的是当天的电量，则：
        content = content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}年1月"}

        :param excel_cell: {"sheet": 0, "cell": "A1"}表示第一个sheet的A1单元格
        :param content: 需要填充的内容
        :return:
        """
        if excel_cell is None:
            excel_cell = {"sheet": 0, "cell": "A1"}
        if content is None:
            return
        self.rules.append([excel_cell, content])

    def exec_rules(self):
        for cell, content in self.rules:
            # 计算填充内容
            exp = content.get("expression")

            _ = fill_excel_cell(self.out_file, sheet=cell.get("sheet"), cell=cell.get("cell"), value=val, visible=True,
                                close=False)
            _ = fill_excel_cell(self.out_file, )

    def download_data(self, start_time, end_time):
        """
        下载指定时间段的数据，默认的时间间隔是1分钟，会检测本地缓存数据是否存在，只下载没有缓存的数据

        :param start_time:
        :param end_time:
        :return:
        """
        if isinstance(start_time, str):
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if isinstance(end_time, str):
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # 判断需要下载时间段的数据是否存在
        non_exist_days = []  # 没有缓存数据的日期的列表，每一个元素对应一天
        if self.report_type == "year":
            # 如果是年报，则检查本年度每天的数据是否存在
            year = start_time.year
            for day in yield_every_day(start_time.year):
                if end_time < day:  # 当天的数据也会统计
                    break
                data_file = os.path.join(self.cache_folder, f"{year}_{day.month}_{day.day}.csv")
                if not os.path.exists(data_file):
                    non_exist_days.append(day)
        elif self.report_type == "month":
            # 如果是月报，则检查本月每天的数据是否存在
            year = start_time.year
            month = start_time.month
            for day in yield_every_day(year, month):
                if end_time < day:
                    break
                data_file = os.path.join(self.cache_folder, f"{year}_{day.month}_{day.day}.csv")
                if not os.path.exists(data_file):
                    non_exist_days.append(day)

        for day in non_exist_days:  # 遍历每一天，逐步下载每一天的数据
            _year, _month, _day = day.year, day.month, day.day
            _s = datetime.datetime(year=_year, month=_month, day=_day, hour=0, minute=0, second=0)
            _e = datetime.datetime(year=_year, month=_month, day=_day, hour=23, minute=59, second=59)
            df = get_history(self.tags.get_values(), self.tags.get_keys(), start_time=_s, end_time=_e)
            if df.shape[0]:  # 如果最后一条数据的时间等于23：59分则说明当天的数据是完整的，否则不完整，不予保存
                df.to_csv(os.path.join(self.cache_folder, f"{_year}_{_month}_{_day}.csv"))

    def clear_cache(self, day=None):
        """
        清理缓存数据，已下载的数据会缓存在本地，如果本地数据和服务器不一致，可以通过该方法清理缓存后再次下载，否则，self.download_data()方法只是
        加载本地的缓存数据，而不是真正的下载服务器数据。

        :return:
        """
        if day is None:
            os.removedirs(self.cache_folder)
        else:
            os.remove(os.path.join(self.cache_folder, f"{day.year}_{day.month}_{day.day}.csv"))  # 只删除某一天的文件
