import os.path

from yangke.performance.tools.natural_gas import NaturalGas, logger


def gas_properties(compositions=None, visible=False):
    """
    计算天然气物性。


    :param compositions:
    :param visible: 本函数使用excel计算天然气物性，该参数表示计算过程是否显示Excel界面，默认不显示
    :return:
    """
    if compositions is None:
        compositions = {"CH4": 0.9, "N2": 0.1}
    k_idx = {
        "CH4": 1,
        "N2": 52,
        "CO2": 54,
        "C2H6": 2,
        "C3H8": 3,
        "H2O": 42,
        "H2S": 43,
        "H2": 41,
        "CO": 46,
        "O2": 53,
        "C4H10": 4,
        "C4H10-1": 5,
        "C5H12": 6,
        "C5H12-1": 7,
        "C6H14": 9,
        "C7H16": 14,
        "C8H18": 15,
        "C9H20": 16,
        "C10H22": 17,
        "He": 49,
        "Ar": 51,
        "C2H4": 18,
        "C3H6": 19,
        "C4H8": 20,
    }

    app = xw.App(visible=visible, add_book=False)
    app.display_alerts = False
    app.screen_updating = visible
    wb = app.books.open(os.path.join(os.path.dirname(__file__), "resource/ISO6976.xlsx"))
    sht = wb.sheets['Summary']
    for i in range(9, 69, 1):
        sht.range(f"C{i}").value = 0

    for k, v in compositions.items():
        idx = k_idx.get(k)
        row = idx + 8
        sht.range(f"C")

    app.quit()


if __name__ == "__main__":
    comp = {
        "CH4": 95,
        "N2": 1,
        "CO2": 1,
        "C2H6": 3
    }
    gas_properties(comp)
