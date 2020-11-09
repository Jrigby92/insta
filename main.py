from selenium import webdriver
import os
import time
from time import sleep
import random
from random import choice
from random import randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
from random import uniform
import urllib3



 # Username:str: the instagram username
    # Password:str:  instagram password

    # login function is included in the class body

class InstagramBot:
   
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com"
        self.driver = webdriver.Chrome(r'./chromedriver')
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        sleep(2)
        self.driver.find_element_by_name("username")\
            .send_keys(self.username)
        self.driver.find_element_by_css_selector("input[name='password']")\
            .send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type='submit']")\
            .click()

# sleep while logging in
        sleep(uniform(3,6))

# PRIMARY BUILDING BLOCK FUNCTIONS I.E. BASE FUNCTIONS


 # navigate to the user / needs work 
    def nav_user(self, user):

        self.driver.get('{}/{}/'.format(self.base_url, user))
        # sleep whilst user page loads
        sleep(uniform(3,5))
        

    def opening_followers_box(self):
        followers_link = self.driver.find_element_by_xpath("//a[contains(@href, 'followers')]")
        followers_link.click()

        sleep(uniform(2,4))



    def scrolling_followers(self):
        driver = self.driver

        fBody  = driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll < randint(12,16): # scroll 12, 16 times
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
            time.sleep(uniform(1,2))
            scroll += 1

        print("ended")



    def storing_followers_in_json(self):
        
        dialog = self.driver.find_element_by_xpath("//div[contains(@role, 'dialog')]")
        # identifying user accounts from followers box
        names = dialog.find_elements_by_tag_name('a')
        # compiling accounts into a list
        to_follow = [name.text for name in names if name != ''][2:]
        
        # filtering list from empty values
        to_follow = list(filter(None, to_follow))

        print(to_follow)

        sleep(uniform(2,4))

        # exporting list to json 
        with open(f'to_follow_{self.username}.json', 'w') as f:
             json.dump(to_follow, f)



    def like(self):
        
        # PUTTING POST LINKS IN LIST
        # Finding post elements by href into a list / using list to navigate to specificposts in clicking_and_liking function    
        post = self.driver.find_elements_by_xpath('//a[contains(@href,"/p/C")]')
        # extracting the full href from each element in the 'post' list
        links = [elem.get_attribute('href') for elem in post]


        def navigating_to_post_and_liking(first_post, last_post):
        # Navigating and liking one of the first 3 values in the links list (userspost) at random
            try:
                self.driver.get(links[randint(first_post,last_post)].format(self.base_url))
                like_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                like_button.click()
            except IndexError as exception:
                pass

        sleep(uniform(1,3))
 
        #  first like
        navigating_to_post_and_liking(1,4)
        # sleep before next like
        sleep(uniform(1,3))


        # Second like/ 50% chance of happening
        a = randint(1,3)
        if a == 2:
            navigating_to_post_and_liking(4,8)
        # sleep before next like
        sleep(uniform(2,4))

        # Third like/ 40% chance of happening
        b = randint(1,6)
        if b >= 4:
            navigating_to_post_and_liking(8,12)
        


    def follow_and_like(self):
        
        # opening users from to_follow.json and followed.json lists
        # storing users in python lists
        with open(f"to_follow_{self.username}.json","r") as f:
            to_follow = json.load(f)
        with open(f"followed_{self.username}.json","r") as f:
            followed = json.load(f)
        
        #  backing up followed list
        with open(f"followed_backup_{self.username}.json","w") as f:
            json.dump(followed,f)


        # if user not already followed 
        # follwing the top user in to_follow list,
        # then deleting the followed user from follow_list
        # adding to followed and to_unfollow lists
        # rerunning program until follow_list empty
        while len(to_follow) > 0:
            
            user1 = [to_follow[0]]

            if [to_follow[0]] not in followed:
                   self.nav_user(to_follow[0])
                   sleep(uniform(3,5))
                   # locating and clicking follow buton
                   self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]").click()
                   # appending followed user to followed list
                   followed.extend(user1)
 
                   sleep(uniform(1,2))
                   
                   self.like()
                   

                   # saving the new followed list
                   with open(f"followed_{self.username}.json","w") as f:
                      json.dump(followed, f, indent=1)
                
                   # deleting followed user from to_follow list
                   del to_follow[0]
                   with open(f"to_follow_{self.username}.json","w") as f:
                      json.dump(to_follow, f, indent=1)

                   with open(f"to_unfollow_{self.username}.json","w") as f:
                       json.dump(followed, f, indent=1)

                   # self.driver.find_element_by_class_name("//div[@class='eLAPa']").click
                   # print("yep")

                
                   a = randint(1,10)

                   # 1/10 times program will wait 7-11(ish) minutes before finding a new user
                   # 1/10 times program will wait 30-90 seconds before finding a new user
                   # 8/10 times it will wait 1.5-5(ish) minutes
                   if a > 9:
                       sleep(uniform(420,686))
                   elif a < 2:
                       sleep(uniform(30,90))
                   else:
                       sleep(uniform(123,264))
                
            
            else:
                 del to_follow[0]



    def unfollow(self):
        # opening users from to_unfollow.jsonlist
        # storing users in python list variable
        with open(f"to_unfollow_{self.username}.json","r") as f:
            to_unfollow = json.load(f)
        
        # backing up to_unfollow list in json
        with open(f"to_unfollow_backup_{self.username}.json","w") as f:
            json.dump(to_unfollow,f)
         
        while len(to_unfollow) > 0:
            # navigating to top user in unfollow list
            self.nav_user(to_unfollow[1])

            # 1/10 times program will wait 11-26 secs before clicking unfollow
            # 9/10 times it will wait 3-8
            a = randint(1,11)
            if a > 9:
                sleep(uniform(11,26))
            else:
                sleep(uniform(3,8))

            # Finding and lciking unfollow button
            self.driver.find_element_by_class_name('vBF20 _1OSdk').click
            del to_unfollow[0]
            with open(f"to_unfollow_{self.username}.json","w") as f:
                   json.dump(to_unfollow, f, indent=1)

            sleep(uniform(2,5))




# SECONDARY BUILDING BLOCKS // COMPILATIONS OF PRIMARY FUNCTIONS*

    def follow_cycle(self):

        # random selection from pool of users to target
        # (the followers of these users will be targetted for following and unfollowing)
        scrape_accounts = ['amore.aesthetics','klccosmetics', 'kiss_aesthetics', 'goddessaestheticsmcr', 'm.i.a_aestheticsmcr', 'demijeanaesthetics', 'medical.aestheticsmcr', 'misshudsonaesthetics_', 'c.caesthetics', 'nicolelucia_aesthetics', 'lauren.cosmetic.aesthetics', 'nassifmedspauk', 'amicaaesthetics', 'luxe.aesthetics', 'facesbyakj',]
        user_to_scrape = choice(scrape_accounts)

        self.nav_user(user_to_scrape)
        self.opening_followers_box()
        self.scrolling_followers()
        self.storing_followers_in_json()
        self.follow_and_like()



# ACTIVE FUCTIONS
    
    def follow_unfollow(self):

        # to ensure the program runs continuously 
        while True:
            
            # Follow cycle 1
            self.follow_cycle()
            

            # follow cycle 2
            self.follow_cycle()
            

            # RANDOM BREAK between 43 minutes and 64 minutes (ish)
            sleep(uniform(2556,3850))

            # follow cycle 3
            self.follow_cycle()
            

            # unfollow cycle
            self.unfollow()

            #RANDOM BREAK between 8 and 22 minutes
            sleep(uniform(496,1388))
        



if __name__ == '__main__':
    
    scrape_accounts = ['natgeo','portraitamazing', 'portraitvision_', 'expofilm', 'theportraitpr0ject', 'fantasticportrait', 'manchestereveningnews']
    
    user_to_scrape = choice(scrape_accounts)

    ig_bot = InstagramBot('Francessolutions', 'Skorpor1942')

    ig_bot.follow_cycle()