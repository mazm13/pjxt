# coding=utf-8
import codecs
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import numpy as np
import re
import datetime


def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result


def parse_qn(driver, qn):
    qn.click()

    been_parsed = driver.find_elements_by_xpath('//a[@class="btn btn-warning"]')

    if len(been_parsed) == 1:
        driver.back()
        return

    star = driver.find_element_by_xpath('//div[@class="jStar"]')
    score = np.random.randint(80, 90)
    score = score / 100.0
    offset = star.size['width'] * score
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(star, xoffset=offset, yoffset=0).click().perform()

    ctrls = driver.find_elements_by_xpath('//input[starts-with(@id, "pjnr_")]')
    # print(len(ctrls))
    for ctrl in ctrls:
        ctl_id = ctrl.get_attribute('id')
        if re.match(r'pjnr_\d_2', ctl_id) is None:
            continue
        ctrl.click()

    textarea = driver.find_element_by_xpath('//*[@id="pjjy"]')
    textarea.send_keys('Wu')

    submit_btn = been_parsed[0]
    submit_btn.click()

    # c = input()

    driver.back()
    pass


def course_pj(driver, course):
    course.click()
    cnt = len(driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr/td/div/a'))
    for i in range(cnt):
        qns = driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr/td/div/a')
        parse_qn(driver, qns[i])
    driver.back()


if __name__ == "__main__":
    driver = webdriver.Firefox(executable_path='./third_party/geckodriver')
    url = 'http://222.28.190.163/pjxt2.0/main/index'
    driver.get(url)
    try:
        nav = driver.find_element_by_xpath('//ul[@class="nav nav-list"]')

    except Exception, e:
        sure = input("Input...\n")
        nav = driver.find_element_by_xpath('//ul[@class="nav nav-list"]')

    menuItem = driver.find_element_by_xpath('//ul[@class="nav nav-list"]'
                                            '/li[@id="lm126"]/ul[@class="submenu"]/li[@id="z127"]')

    actions = ActionChains(driver)
    actions.move_to_element(nav).click(menuItem).move_by_offset(xoffset=200, yoffset=200).perform()

    dates = datelist((2017, 12, 1), (2018, 1, 26))

    for date in dates:

        driver.get('http://222.28.190.163/pjxt2.0/stpj/queryListStpj')
        WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "Wdate")))
        wdate = driver.find_element_by_class_name("Wdate")
        wdate.clear()
        wdate.send_keys(date)

        search = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div/form[1]/table[1]/tbody/tr/td[2]/button')
        search.click()

        courses = driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr/td/div/a')
        cnt = len(courses)
        for i in range(cnt):
            courses = driver.find_elements_by_xpath('//table[@id="table_report"]/tbody/tr/td/div/a')
            course_pj(driver, courses[i])

