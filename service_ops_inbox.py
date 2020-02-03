import datetime
import os
import time
import unittest
from calendar import week

import moment
from dateutil.relativedelta import relativedelta, MO
from dateutil.rrule import rrule
from selenium.webdriver.support.select import Select

import config
import logging
from selenium import webdriver

import prism_test.auth as auth
from prism_test.argument_parser import ArgumentParser

logger = logging.getLogger(config.LOG_ALIAS)


class ServiceOpsInbox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.debug("service ops inbox test cases")
        web_driver_dir, prism_url, login_email, login_pwd = ArgumentParser().start()

        cls.web_driver_dir = web_driver_dir if web_driver_dir is not None else config.web_driver_dir
        cls.prism_url = prism_url if prism_url is not None else config.PRISM_URL
        cls.login_email = login_email if login_email is not None else config.login_email
        cls.login_pwd = login_pwd if login_pwd is not None else config.login_pwd
        cls.chrome_driver = os.path.join(cls.web_driver_dir, "chromedriver")
        cls.driver = webdriver.Chrome(cls.chrome_driver)


        # login prism application
        auth.app_login(cls.driver, cls.prism_url, cls.login_email, cls.login_pwd)
        time.sleep(20)


    def test_case_001_create_new_request(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        time.sleep(5)
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[2]').click()
        time.sleep(5)
        # for contract resource - worker rate
        #driver.find_element_by_id("workerRate").send_keys('100')
        #time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()
        # For On-site Task
        # driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        # driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')

        # start_date and end_date
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hour
        driver.find_element_by_id("estimatedHours").click()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=3)
        gap = (end - start).days
        gap1 = gap+1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(100)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)
        
        # Request revise
        # click on hide/show filter
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/span[3]/i[2]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//a[contains(text(),"Show")]').click()
        time.sleep(5)

        # search by last modified name in filter
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").click()
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").send_keys("Valtanix Team")
        time.sleep(5)

        # selecting first row in staffing queue
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(5)

        # To set start date for current week
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        startdate = moment.now().add(days=2).format('DD-MMM-YYYY')
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)

        # To set end date in future
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=4).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Start date time and end date time
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        # Selecting "PM" in end date time
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=2)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # Click on request revised
        driver.find_element_by_xpath("//span[contains(text(),'Request Revised')]").click()
        time.sleep(5)
        # click on first row and request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(160)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # for automate cancel request
        driver.find_element_by_xpath("//span[contains(text(),'Request Cancel')]").click()
        time.sleep(5)
        # driver.find_element_by_model("comments.dropDown").click()
        driver.find_element_by_xpath("//option[contains(text(),'Customer had an urgent internal change')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn-danger text-uppercase ng-binding']").click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(20)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for cancelled
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("CANCELLED", status)
        time.sleep(5)


    def test_case_002_Daily_request(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[1]').click()
        time.sleep(5)
        # for contract resource - worker rate
        # driver.find_element_by_id("workerRate").send_keys('100')
        # time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[15]').click()
        time.sleep(10)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()
        # For On-site Task
        # driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        # driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')

        # start_date and end_date
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hour
        driver.find_element_by_id("estimatedHours").click()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=3)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

    def test_case_003_weekly_request(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)
        # for contract resource - worker rate
        # driver.find_element_by_id("workerRate").send_keys('100')
        # time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()
        # For On-site Task
        # driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        # driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')

        # start_date and end_date
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for Weekly - repeats
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[2]').click()
        time.sleep(5)
        driver.find_element_by_id("checkbox1").click()
        driver.find_element_by_id("checkbox3").click()
        driver.find_element_by_id("checkbox5").click()
        time.sleep(5)

        # estimate hour
        driver.find_element_by_id("estimatedHours").click()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=1)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

    def test_case_04_cancel_request_for_past_week_monday_and_current_week_friday(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[11]').click()
        time.sleep(5)
        # for contract resource - worker rate
        # driver.find_element_by_id("workerRate").send_keys('100')
        # time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()
        # For On-site Task
        # driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        # driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')

        # for past week monday and current week friday
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start date
        week = moment.now().replace(weekday=1).subtract(days=7).format("DD-MMM-YYYY")
        print(week)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(week)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # for end date current friday date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        week = moment.now().replace(weekday=5).format("DD-MMM-YYYY")
        print(week)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(week)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(10)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=11)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # cancel request
        driver.find_element_by_xpath("//span[contains(text(),'Request Cancel')]").click()
        time.sleep(5)
        # driver.find_element_by_model("comments.dropDown").click()
        driver.find_element_by_xpath("//option[contains(text(),'Customer had an urgent internal change')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn-danger text-uppercase ng-binding']").click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(20)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for cancelled
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("CANCELLED", status)
        time.sleep(5)

    def test_case_05_cancel_request_for_future_date(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[13]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()
        # For On-site Task
        # driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        # driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')

        # for future week schedule
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=7).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=6)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # cancel request
        driver.find_element_by_xpath("//span[contains(text(),'Request Cancel')]").click()
        time.sleep(5)
        # driver.find_element_by_model("comments.dropDown").click()
        driver.find_element_by_xpath("//option[contains(text(),'Customer had an urgent internal change')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn-danger text-uppercase ng-binding']").click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(20)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for cancelled
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("CANCELLED", status)
        time.sleep(5)

    def test_case_06_cancel_request_for_past_date(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[2]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        # For On-site Task
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')
        time.sleep(5)

        # for past week monday to current date schedule
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        week = moment.now().replace(weekday=1).subtract(days=7).format("DD-MMM-YYYY")
        print(week)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(week)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=10)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # cancel request
        driver.find_element_by_xpath("//span[contains(text(),'Request Cancel')]").click()
        time.sleep(5)
        # driver.find_element_by_model("comments.dropDown").click()
        driver.find_element_by_xpath("//option[contains(text(),'Customer had an urgent internal change')]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//button[@class='btn btn-danger text-uppercase ng-binding']").click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(20)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for cancelled
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("CANCELLED", status)
        time.sleep(5)

    def test_case_007_request_revise_end_date_to_future_date(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()

        # for future week schedule
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=2)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # Request revise
        # click on hide/show filter
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/span[3]/i[2]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//a[contains(text(),"Show")]').click()
        time.sleep(5)

        # search by last modified name in filter
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").click()
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").send_keys("Valtanix Team")
        time.sleep(5)

        # selecting first row in staffing queue
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(5)

        # To set end date in future
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=5).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Start date time and end date time
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        # Selecting "PM" in end date time
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=3)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # Click on request revised
        driver.find_element_by_xpath("//span[contains(text(),'Request Revised')]").click()
        time.sleep(5)
        # click on first row and request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

    def test_case_008_request_revise_start_date_and_end_date_to_future_date(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[2]').click()

        # for future week schedule
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=2)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # Request revise
        # click on hide/show filter
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/span[3]/i[2]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//a[contains(text(),"Show")]').click()
        time.sleep(5)

        # search by last modified name in filter
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").click()
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").send_keys("Valtanix Team")
        time.sleep(5)

        # selecting first row in staffing queue
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(5)

        # revise start date in future
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().add(days=1).format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)

        # revise end date in future
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=3).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Start date time and end date time
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        # Selecting "PM" in end date time
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=1)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # Click on request revised
        driver.find_element_by_xpath("//span[contains(text(),'Request Revised')]").click()
        time.sleep(5)
        # click on first row and request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(150)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

    def test_case_009_request_revise_past_date(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # select task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        # For On-site Task
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')
        time.sleep(5)

        # start date as past week monday and end date as one day past
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        week = moment.now().replace(weekday=1).subtract(days=7).format("DD-MMM-YYYY")
        print(week)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(week)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().subtract(days=1).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # for daily
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[4]/div[1]/div[1]/span/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskFrequency_listbox"]/li[1]').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=9)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # Request revise
        # click on hide/show filter
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/span[3]/i[2]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//a[contains(text(),"Show")]').click()
        time.sleep(5)

        # search by last modified name in filter
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").click()
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").send_keys("Valtanix Team")
        time.sleep(5)

        # selecting first row in staffing queue
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(5)

        # revise end date in future
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=1).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Start date time and end date time
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        # Selecting "PM" in end date time
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(5)

        # estimate hours
        driver.find_element_by_id("estimatedHours").clear()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=11)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # Click on request revised
        driver.find_element_by_xpath("//span[contains(text(),'Request Revised')]").click()
        time.sleep(5)
        # click on first row and request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)


    def test_case_010_request_revise_for_resource(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        # for contract resource - worker rate
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[4]').click()
        time.sleep(5)
        driver.find_element_by_id("workerRate").send_keys('100')
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # For On-site Task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')
        time.sleep(5)

        # start_date and end_date
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        # start_date
        startdate = moment.now().format("DD-MMM-YYYY")
        print(startdate)
        driver.find_element_by_xpath('//datetimepicker[@id="startDate"]//input[@name="datepicker"]').send_keys(startdate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[2]').click()
        time.sleep(5)
        # end_date
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').clear()
        time.sleep(5)
        enddate = moment.now().add(days=2).format("DD-MMM-YYYY")
        print(enddate)
        driver.find_element_by_xpath('//datetimepicker[@id="endDate"]//input[@name="datepicker"]').send_keys(enddate)
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[11]/div/div[3]').click()
        time.sleep(5)

        # Time/hours
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="startDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('09')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').clear()
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[1]/input').send_keys('05')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="endDate"]/ng-form/div[2]/div/table/tbody/tr[2]/td[6]/button').click()
        time.sleep(10)

        # estimate hour
        driver.find_element_by_id("estimatedHours").click()
        time.sleep(5)
        start = moment.now()
        end = moment.now().add(days=1)
        gap = (end - start).days
        gap1 = gap + 1
        print("Days gap:")
        estimated = gap1 * 8
        print(estimated)
        driver.find_element_by_id("estimatedHours").send_keys(estimated)
        time.sleep(5)

        # RM instruction service ops team
        driver.find_element_by_id("instructionEsm").send_keys("Training")
        time.sleep(5)
        # Instruction to solution architects
        driver.find_element_by_id('instructionSpecial').send_keys("Test")
        time.sleep(5)

        # submit the request
        driver.find_element_by_xpath("//span[contains(text(),'Submit')]").click()
        time.sleep(10)
        # waiting/verifying the status to complete and clicking on request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(130)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)

        # Request revise
        # click on hide/show filter
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[1]/div/div[4]/div[2]/div[2]/div/span[3]/i[2]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//a[contains(text(),"Show")]').click()
        time.sleep(5)

        # search by last modified name in filter
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").click()
        driver.find_element_by_xpath("//input[@name='assigned_to_name']").send_keys("Valtanix Team")
        time.sleep(5)

        # selecting first row in staffing queue
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        # click on request id in first row
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[3]').click()
        time.sleep(5)

        # Click on request revised
        driver.find_element_by_xpath("//span[contains(text(),'Request Revised')]").click()
        time.sleep(5)
        # click on first row and request id
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]').click()
        time.sleep(150)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="wrapper"]/div/div/div[2]/div/div/table/tbody/tr[1]/td[1]/span/a').click()
        time.sleep(10)
        # assert for complete status
        status = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/ng-view[1]/div[1]/div[1]/div[1]/fieldset[1]/div[1]/div[1]/div[3]/div[1]/footer[1]/span[1]').text
        print(status)
        self.assertEqual("COMPLETED", status)
        time.sleep(5)


    def test_case_011_draft(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # click on draft
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[15]/div/div[2]/div/button[3]').click()
        time.sleep(10)

    def test_case_012_zeroHour(self):
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # Select Project
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[2]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="project_listbox"]/li[12]').click()
        time.sleep(5)

        # click on automate Fill contacts,timezone
        driver.find_element_by_xpath('.//*[.="Fill Contact"]').click()
        time.sleep(5)

        # select phase
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[1]/div/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskPhase_listbox"]/li[1]').click()
        time.sleep(5)
        # For On-site Task
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[12]/div/div[1]/div[2]/div/span[2]/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskType_listbox"]/li[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="taskLocation"]').send_keys('India')
        time.sleep(5)

        # click on zeroHour
        driver.find_element_by_id('zeroHourBooking').click()
        time.sleep(10)

    def test_case_013_soft_book(self):
        driver = self.driver
        driver = self.driver
        driver.find_element_by_xpath('.//*[@href="#/service_ops_inbox"]').click()
        time.sleep(10)
        driver.maximize_window()
        driver.find_element_by_id('createnew').click()
        time.sleep(5)

        # Select resource
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[3]/div/div[1]/span/span/span[2]/span').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="resource_listbox"]/li[10]').click()
        time.sleep(5)

        # click on soft book which is tentative booking
        driver.find_element_by_xpath('//*[@id="content"]/ng-view/div/div[1]/div/fieldset/div[15]/div/div[2]/div/button[2]').click()
        time.sleep(10)




        print("clear")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
