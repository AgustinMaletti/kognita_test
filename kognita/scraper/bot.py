import sys, os, pathlib
from selenium import webdriver
from time import sleep
# from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_profile import  FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException
import parsel

PATH = pathlib.Path(__file__).parent
path_to_driver = PATH.joinpath('geckodriver').resolve().__str__()
FILES_TYPES = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/xlsx,text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml"


class Selenium_bot():
    
    def __init__(self, javascript=True, headless=False):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 0)
        profile.set_preference('general.useragent.vendor', 'Linux Mint')
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.panel.shown', False)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', os.getcwd() + '/')
        # profile.set_preference("browser.helperApps.neverAsk.openFile",FILES_TYPES)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', FILES_TYPES)

        profile.DEFAULT_PREFERENCES['frozen']['dom.webnotifications.serviceworker.enabled'] = False
        profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = javascript
        opts = Options()
        opts.profile = profile
        opts.headless = headless
        caps = DesiredCapabilities.FIREFOX
        caps['marionette'] = True
        caps['firefox_profile'] = profile.encoded
        # path_to_driver = 'static/geckodriver'
        # bin = FirefoxBinary(path_to_driver)
        self.driver = webdriver.Firefox(executable_path=path_to_driver,
                                        options=opts,
                                        capabilities=caps,)
        self.driver.maximize_window()                                        
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        self.proxy = []
        self.page = None
    
    def scroll_to_botton(self):
        high_viewport = self.driver.execute_script("return window.innerHeight;")
        self.driver.execute_script(f"window.scrollBy(0, {high_viewport};")
        
    def scrap_proxy(self, ):
        destinys = [('pagina_para_sacar_proxys1','ip_dir')]
        scrap = [('pagina_para_sacar_proxys1', ('pagination_xpath'))]
        proxy = []
        for d, s in zip(destiny, scrap):
            page = self.driver.get(d)
            sel = parsel.Selector(page.source)
            proxy.append(tuple(sel.xpath(s)))
        
        self.proxy = proxy
        
    def start_proxy(self, how_many=10):
        if len(proxy) == 0:
            self.scrap_proxy()
        # put the proxy in front

    def get_element(xpath):
        element = self.driver.find_element_by_xpath(xpath, self.page)
   
    def go_to(self, url):
        self.driver.get(url)
        self.page = self.driver.page_source
       
    def wait_element(element):
        # block until element is there
        self.wait.until(EC.element_to_be_clickable, element)

    # def wait_precense():

    #    put the proxy in front of selenium



    # def how_much_elements(self, element):
    #     return len(self.driver.find_elements_by_xpath(element))
    
    # def check_click_check(self, label, button, i):
    #     # check the valua of the label
    #     check = self.driver.find_elements_by_xpath(label)[i].text
    #     # check if the button is there
    #     button_display = self.driver.find_elements_by_xpath(button)[i].is_displayed()
    #     # click in the button
    #     self.driver.find_elements_by_xpath(button)[i].click()
    #     # check the value of the label before click in button
    #     check2 = self.driver.find_elements_by_xpath(label)[i].text

    #     return [check, check2, button_display]

    # def measure_scroll_check():
    #     pass
    
    # def click_check(self):
    #     pass


    
    # def write_check(self, xpath, text):
    #     # get element
    #     element_text = self.driver.find_element_by_xpath(xpath)
    #     # click and send text
    #     # self.action.click(element_text)
    #     # self.action.send_keys(text) 
    #     self.action.send_keys_to_element(element_text, text)
    #     self.action.perform()
    #     # self.action.perform()
    #     # get text element
    #     text_in_field =  self.driver.find_element_by_xpath(xpath).get_attribute('value')
    #     # print(text_in_field)
    #     return text_in_field.strip()
    
    # def write(self, xpath, text):
    #     element = self.driver.find_element_by_xpath(xpath)
    #     self.action.double_click(element)
    #     self.action.send_keys_to_element(element, text)
        
       



    # def get_text(self, selector):
    #     pass



if __name__== '__main__' :
#    bot = Selenium_bot()
#    bot.go_to('https://www.lopes.com.br/busca/comprar-prontos/todos-florianopolis-sc/todos?ordernar=Relevancia&pagina=1')

    print(os.getcwd())
