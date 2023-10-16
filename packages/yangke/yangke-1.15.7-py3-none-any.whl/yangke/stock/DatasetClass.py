# 量化分析中使用的数据库对应的类
from sqlalchemy import Column, String, DATETIME, BOOLEAN, DATE, Date

from yangke.dataset.sqlalchemy import Base


class Holiday(Base):
    __tablename__ = "Holiday"
    calendarDate = Column(Date, nullable=False, primary_key=True)
    isOpen = Column(BOOLEAN, nullable=False)

    def __init__(self, date, is_open):
        self.calendarDate = date
        self.isOpen = is_open

    def __repr__(self):
        return f"Holiday({self.calendarDate}: {self.isOpen})"
