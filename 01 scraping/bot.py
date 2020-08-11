"""
A simple selenium test example written by python
"""
from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import random
import time
import re
import collections
import sys

class Bot:
    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--lang=en")
        self.times_restarted = 0  # keep track of how many times profile page has to be refreshed
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(20)

    def tear_down(self):
        """Stop web driver"""
        self.driver.quit()

    def go_to_page(self, url):
        """Find and click top-right button"""
        try:
            self.driver.get(url)
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def login(self, username, password):
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
        notNow = self.driver.find_element_by_class_name("HoLwm")
        time.sleep(3)
        notNow.click()
        time.sleep(5)

    def get_my_followers(self, username):
        self.go_to_page("https://instagram.com/" + username + "/")
        time.sleep(5)
        my_followers_set = set()
        followers = self.driver.find_elements_by_class_name("-nal3")
        followers[1].click()
        time.sleep(2)
        initialise_vars = 'elem = document.getElementsByClassName("isgrP")[0]; followers = parseInt(document.getElementsByClassName("g47SY")[1].innerText); times = parseInt(followers * 0.14); followersInView1 = document.getElementsByClassName("FPmhX").length'
        initial_scroll = 'elem.scrollTop += 500'
        next_scroll = 'elem.scrollTop += 1500'

        with open('./jquery-3.3.1.min.js', 'r') as jquery_js:
            # 3) Read the jquery from a file
            jquery = jquery_js.read()
            # 4) Load jquery lib
            self.driver.execute_script(jquery)
            # scroll down the page
            self.driver.execute_script(initialise_vars)
            #self.driver.execute_script(scroll_followers)
            self.driver.execute_script(initial_scroll)
            time.sleep(3)

            next = True
            while(next):
                n_li_1 = len(self.driver.find_elements_by_class_name("FPmhX"))
                self.driver.execute_script(next_scroll)
                time.sleep(1.5)
                n_li_2 = len(self.driver.find_elements_by_class_name("FPmhX"))
                if(n_li_1 != n_li_2):
                    following = self.driver.find_elements_by_xpath("//*[contains(text(), 'Following')]")
                    for follow in following:
                        el = follow.find_element_by_xpath('../..')
                        el = el.find_element_by_tag_name('a')
                        profile = el.get_attribute('href')
                        my_followers_set.add(profile)
                else:
                    next = False

            return list(my_followers_set)

    def get_followers(self, my_followers_arr, start_profile, relations_file):
        n_my_followers = len(my_followers_arr)
        count_my_followers = start_profile - 1

        for current_profile in my_followers_arr[start_profile - 1 : -1] + [my_followers_arr[-1]]:
            print("Start scraping " + current_profile)
            self.go_to_page(current_profile)
            time.sleep(random.randint(5, 20))
            last_5_following = collections.deque([1, 2, 3, 4, 5])  # queue to keep track of Instagram blocking scroll requests
            count_my_followers += 1

            with open('start_profile.txt', 'w+') as outfile: # keep track of last profile checked
                outfile.write(str(count_my_followers))

            followers = self.driver.find_elements_by_class_name("-nal3")
            followers[2].click()
            time.sleep(2)
            initialise_vars = 'elem = document.getElementsByClassName("isgrP")[0]; followers = parseInt(document.getElementsByClassName("g47SY")[1].innerText); times = parseInt(followers * 0.14); followersInView1 = document.getElementsByClassName("FPmhX").length'
            initial_scroll = 'elem.scrollTop += 500'
            next_scroll = 'elem.scrollTop += 2000'

            with open('./jquery-3.3.1.min.js', 'r') as jquery_js:
                # 3) Read the jquery from a file
                jquery = jquery_js.read()
                # 4) Load jquery lib
                self.driver.execute_script(jquery)
                # scroll down the page
                self.driver.execute_script(initialise_vars)
                # self.driver.execute_script(scroll_followers)
                self.driver.execute_script(initial_scroll)
                time.sleep(random.randint(2, 5))

                next = True
                follow_set = set()
                # check how many people this person follows
                nr_following = int(re.sub(",","",self.driver.find_elements_by_class_name("g47SY")[2].text))

                n_li = 1
                while next:
                    print(str(count_my_followers) + "/" + str(n_my_followers) + " " + str(n_li) + "/" + str(nr_following))
                    time.sleep(random.randint(7, 12) / 10.0)
                    self.driver.execute_script(next_scroll)
                    time.sleep(random.randint(7, 12) / 10.0)
                    if not (n_li < nr_following - 11):
                        next = False

                    n_li = len(self.driver.find_elements_by_class_name("FPmhX"))
                    last_5_following.appendleft(n_li)
                    last_5_following.pop()
                    # if instagram starts blocking requests, reload page and start again
                    if len(set(last_5_following)) == 1:
                        print("Instagram seems to keep on loading. Refreshing page in 7 seconds")
                        self.times_restarted += 1
                        if self.times_restarted == 4:
                            print("Instagram keeps on blocking your request. Terminating program. Start it again later.")
                            sys.exit()
                        time.sleep(7)
                        self.get_followers(my_followers_arr, count_my_followers, relations_file)

                self.times_restarted = 0

                following = self.driver.find_elements_by_class_name("FPmhX")
                for follow in following:
                    profile = follow.get_attribute('href')
                    if profile in my_followers_arr:
                        follow_set.add((current_profile, profile))

                with open(relations_file, "a") as outfile:
                    for relation in follow_set:
                        outfile.write(relation[0] + " " + relation[1] + "\n")

                print("This person follows " + str(len(follow_set)) + " of your connections. \n")

        sys.exit()

