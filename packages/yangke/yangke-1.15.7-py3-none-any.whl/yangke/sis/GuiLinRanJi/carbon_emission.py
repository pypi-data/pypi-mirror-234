import datetime
import os.path
from enum import unique, Enum
from shutil import copyfile

from yangke.base import get_key_value, yield_every_day
from yangke.common.fileOperate import fill_excel_cell
from yangke.sis.Report import Report
from yangke.sis.export_history_values import get_history


@unique
@get_key_value
class TagsRead(Enum):
    发电机功率1 = "DCS1:LOAD"
    发电机功率2 = "DCS1:LOAD"
    发电机功率3 = "DCS1:LOAD"
    供电功率1 = ""
    供电功率2 = ""
    供电功率3 = ""
    燃料消耗量1 = ""  # Nm3/h
    燃料消耗量2 = ""
    燃料消耗量3 = ""
    供热负荷1 = ""  # GW
    供热负荷2 = ""  # GW
    供热负荷3 = ""  # GW
    运行小时数1 = ""
    运行小时数2 = ""
    运行小时数3 = ""


report: Report | None = None


def init_carbon():
    global report
    template_file = os.path.join(os.path.dirname(__file__), "../../web/static/碳排放量计算.xlsx")
    report = Report(template=template_file, tags=TagsRead)
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "E3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}年1月"}  #
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "F3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-2"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "G3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-3"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "I3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-4"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "J3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-5"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "K3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-6"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "M3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-7"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "N3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-8"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "O3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-9"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "Q3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-10"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "R3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-11"}  # 填入d
    )
    report.add_fill_rules(
        excel_cell={"sheet": "附表 C.3 化石燃料燃烧排放表", "cell": "S3", },
        content={"expression": "累积值(燃料消耗量)/3600", "date_range": "{year}-12"}  # 填入d
    )


def generate_report(year):
    global report
    out_file = os.path.join(os.path.dirname(__file__), "碳排放量计算1.xlsx")
    report.generate_report_excel(out_file=out_file, year=year)
    return out_file


if __name__ == "__main__":
    ...
