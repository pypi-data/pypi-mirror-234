import time
import traceback

import selenium.common.exceptions as exceptions
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.service import Service

from yangke.common.config import logger
from selenium import webdriver
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from yangke.common.fileOperate import write_as_pickle, read_from_pickle
from yangke.base import sound_beep

i = 1  # 开始下载的文件的编号
num_of_reports_in_single_page = 20  # 每一页的报告数量


def double_click_element(ele):
    action.double_click(ele).perform()


def switch_to_window_by_title(driver, title):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if title in driver.title:
            break
    return


def 打开技术报告页面(driver):
    driver.get("http://10.219.2.75/seeyon/main.do?method=main")  # 打开系统主页
    # driver.get("http://10.219.2.67/WebCenter/Open/00000000-0000-0000-0000-00000000000a")
    logger.debug(f"登录协同并打开技术报告页面...")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginBtn"]/div/span'))
    )
    time.sleep(1)
    element.click()
    driver.switch_to.frame("loginPreBtnIframeId")  # 切换到iframe中，iframe中的元素无法直接定位
    # 逆操作为：driver.switch_to.default_content()
    driver.find_element(by=By.XPATH, value='//*[@id="login_username"]').send_keys("luoliujuan")  # 输入账号名
    driver.find_element(by=By.XPATH, value='//*[@id="login_password"]').send_keys("Luo012210!")  # 输入密码
    driver.find_element(by=By.XPATH, value='//*[@id="login_button"]').click()  # 点击登录按钮
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//ul[@id="showedNav"]'))
    )  # 登录后等待界面加载
    element = element.find_element(By.XPATH, value='//li[contains(@title, "项目管理")]')  # 获取title中包含"项目管理"的元素
    main_window_handle = driver.current_window_handle  # 协同主页窗口
    element.click()  # 点击项目管理
    driver.implicitly_wait(10)  # 最长等待10s等待加载完成
    driver.switch_to.window(driver.window_handles[-1])  # 切换到最新打开的窗口
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "科技成果")]'))
    )
    element.click()  # 点击科技成果
    if driver.find_element(By.XPATH, '//span[contains(text(), "技术报告")]').text == "":  # 如果页面中没有技术报告标签
        element = driver.find_element(By.XPATH, '//span[text()="报告"]')  # 则点击报告，展开报告项
        element.click()  # 展开报告
    element = driver.find_element(By.XPATH, '//span[contains(text(), "技术报告")]')
    element.click()
    time.sleep(10)
    # ------------------------------ 切换到技术报告页面中的子iframe中 -----------------------------------
    # 技术报告显示在新的iframe中
    driver.switch_to.frame(0)  # 页面中只有一个frame
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "技术报告名称")]'))
    )
    # ------------------------------ 切换到技术报告页面中的子iframe中 -----------------------------------
    return driver, main_window_handle


def download_one_page_file(driver, start_file_id=1):
    """
    下载主页->科技成果->技术报告中主界面的iframe中一页的所有附件，调用该方法时，driver必须已经指向页面的iframe中

    :param driver:
    :return:
    """
    global i
    for j in range(1, num_of_reports_in_single_page + 1):  # 一页下载15个
        if i < start_file_id:
            i += 1
            continue
        try:
            ele = driver.find_element(By.XPATH, f'//div[text()="{i}"]')  # 文件编号是总的编号
            double_click_element(ele)  # 双击技术报告列表中的行，弹出技术报告框
        except NoSuchElementException:
            break
        time.sleep(4)
        driver.switch_to.default_content()
        ele_附件 = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[contains(@name, "mini-iframe-")]'))
        )
        logger.debug(f"正在下载第{i}个文件")
        driver.switch_to.frame(ele_附件)  # 切换到弹出的技术报告对话框
        ele_附件 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "附件")]'))
        )
        ele_附件.click()
        time.sleep(4)

        # 找到下一层iframe，这一层frame的name可能是"mini-iframe-120"或"mini-iframe-119"
        ele_frame = driver.find_elements(By.XPATH, '//iframe[contains(@name, "mini-iframe-")]')
        if len(ele_frame) == 1:
            ele_frame = ele_frame[0]
        else:
            logger.error(f"当前iframe下发现多个iframe，请处理！")
        driver.switch_to.frame(ele_frame)  # 切换到技术报告对话框右侧的表格中
        time.sleep(1)
        存在附件 = True
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[@id="1$cell$4"]'))
            )
            time.sleep(1)
        except exceptions.TimeoutException:
            存在附件 = False
            logger.debug(f"第{i}个项目没有附件")
        if 存在附件:
            # ---------------------------- 选中需要下载的文件 ------------------------------
            ele_pdf = driver.find_element(By.XPATH, "//span[@id='mini-5checkall']")  # 应该点击选择所有的按钮
            ele_pdf.click()
            time.sleep(1)
            # # ---------------------------- 选中需要下载的文件 ------------------------------
            # # ---------------------------- 点击下载按钮 ------------------------------
            ele_下载按钮 = driver.find_element(By.XPATH, '//button[@id="btnDownLoad"]')
            ele_下载按钮.click()
            # ---------------------------- 点击下载按钮 ------------------------------
        # ---------------------------- 点击关闭按钮 ------------------------------
        # 无论是否存在附件，都需要点击关闭按钮
        driver.switch_to.default_content()  # 切换到最外层的主页面所在的内容
        time.sleep(1)
        driver.switch_to.frame(
            driver.find_element(By.XPATH, '//iframe[contains(@name, "mini-iframe-")]'))  # 切换到中间层的iframe
        time.sleep(1)
        ele_close = driver.find_element(By.XPATH, '//a[@id="RGY_MOST_TechReport.CloseForm"]')
        ele_close.click()
        time.sleep(2)
        # ---------------------------- 点击关闭按钮 ------------------------------
        # ---------------------------- 解析页面切换回主界面中的项目列表中 ----------------------------------
        driver.switch_to.frame(0)
        # ---------------------------- 解析页面切换回主界面中的项目列表中 ----------------------------------
        i = i + 1


def next_page(driver: WebDriver):
    logger.info("点击下一页按钮")
    ele_next_page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//span[@class="mini-button-icon mini-icon mini-iconfont mini-pager-next"]'))
    )
    ele_next_page.click()
    time.sleep(4)


def goto_page(driver: WebDriver, page):
    """
    翻到第page页

    :param driver:
    :param page:
    :return:
    """
    logger.debug(f"翻到第{page}页")
    ele = driver.find_element(By.XPATH, '//input[@type="text" and @class="mini-pager-num"]')
    double_click_element(ele)
    ele.send_keys(str(page))
    ele.send_keys(Keys.ENTER)


def download_file(driver):
    global i
    i = read_from_pickle("default.pkl") or i
    page = int((i - 0.5) // num_of_reports_in_single_page) + 1
    if page > 2:
        goto_page(driver, page)
    while True:  # 当有下一页内容时，则一直下载，直到找不到下一页按钮
        download_one_page_file(driver, i)
        next_page(driver)
        logger.debug("翻到下一页")


action = None


def run():
    global action, i
    driver: WebDriver = webdriver.Edge(service=Service(r"D:\msedgedriver.exe"))
    action = ActionChains(driver)  # 初始化一个动作对象
    try:
        driver, main_window = 打开技术报告页面(driver)
        download_file(driver)
        msg = "下载结束"
    except exceptions.TimeoutException or exceptions.ElementClickInterceptedException or exceptions.StaleElementReferenceException:
        msg = "下载超时"
    except exceptions.NoSuchElementException:
        i = 2  # 当前层级下载结束，重置索引序号
        sound_beep(500, 1000)
        msg = "下载结束"
    except:
        sound_beep(5000, 1000, 1000, 3)  # 下载出错提示音
        msg = "未知错误"
    finally:
        write_as_pickle(file="default.pkl", obj=i - 1)
        traceback.print_exc()
        driver.close()
        return msg


if __name__ == "__main__":
    # 重新下载需要删除掉运行目录下的default.pkl文件，否则会跳过default.pkl文件中记录的已经下载的文件编号
    res = run()
    while res == "下载超时" or res == "未知错误":  # 如果是下载超时，则重新尝试
        res = run()
        traceback.print_exc()
        logger.debug(f"下载过程中发生错误:{res}，尝试重新下载...")
