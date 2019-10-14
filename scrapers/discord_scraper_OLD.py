### main scraper for discord. Gets links from a channel
# works as long as the channel does not get deleted

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options           # for chrome
# from selenium.webdriver.firefox.options import Options        # for firefox


import time
import datetime
import decode
import os.path

if not os.path.isfile("decode.py"):
    print('Please change your current working directory to scrapers, then run "python discord_scraper.py" in that directory')
    quit(1)

start = datetime.datetime.now()

# setup
print("setting up web drivers")
options = Options()
options.add_argument("--headless")               # for chrome
# options.headless = True                         # for firefox

# use these if your drivers are in your PATH directory
browser = webdriver.Chrome(options=options)      # for chrome
# browser = webdriver.Firefox(options=options)               # for firefox

# use these if you have your drivers in this git repo "playlist-creator/drivers" or anywhere else other than path (type it manually)
# browser = webdriver.Chrome(r"../drivers", options=options)    
# browser = webdriver.Firefox(executable_path=r"../drivers/geckodriver.exe", options=options)

#######################################################
# Change channel url to the channel of your choice    #
#######################################################
url = "https://discordapp.com/channels/453373412707008522/626072947580469258"

browser.get(url) # navigate to the page

# login
print("********************************")
print("logging into discord")
print("********************************")
email = browser.find_element_by_xpath("//input[@type='email']")
email.send_keys(decode.data[0])
password = browser.find_element_by_xpath("//input[@type='password']")
password.send_keys(decode.data[1])
button = browser.find_element_by_xpath("//button[@type='submit']")
button.click()
print("login successful")

time.sleep(10)

# do stuff on the main discord page
print("performing actions in discord")

# filter used when looking only for links
def my_filter(x):
    return "https://" in x

action = ActionChains(browser)
# scroll up loop.  
links = []
j = 0 
error_amount = 0 # shouldn't surpass 3
freq = 30        # the frequency of link scraping
call_amount = 7  # amount of times you call the link scraper
for i in range(freq * call_amount + 1):
    try:
        action.send_keys(Keys.PAGE_UP).perform()
        if j % freq == 0:
            # scrape links
            sub_links = browser.find_elements_by_xpath("//a")
            sub_links = [x.text for x in sub_links]    # convert to array
            # print(str(links) + "\n\n\n" + str(sub_links))
            links.extend(sub_links)
            links = list(set(links))
            print(len(links))
        j += 1
        time.sleep(0.1 / i)
    except Exception as e:
        print("Error: trying again...")
        error_amount += 1
        if error_amount >= 3: 
            print("too many errors. Exiting...")
            print(e)
            quit(2)
    
print(len(links))
links = list(filter(None, links))      # filter empty
links = list(filter(my_filter, links)) # filter only containing https://

end = datetime.datetime.now()
delta = end - start

# save to file
filename = "songs.dat"
if os.path.isfile(filename):
    file_in = open(filename, "r")
    old_data = file_in.read()
    old_size = str(old_data.count('\n'))
    new_size = str(len(links))
    print("old file size: " + old_size)
    print("new file size: " + new_size)
    file_in.close()
    if new_size < old_size:
        print("Warning: new size is less than the old size.")
        print("Either someone deleted a song or the program messed up")


def save(filename):
    file_out = open(filename, "w")
    for x in links:
        file_out.write(x + "\n")
    file_out.close()

print("Please enter the song filename. (Type in 'a' to abort) (Press enter for default: songs.dat): ")
new_filename = input()
if new_filename == "a": 
    print("aborting...")
    browser.quit()
    quit(3)
if not new_filename: new_filename = filename
save(new_filename)


print("********************************")
print("Done reading songs")
print("********************************")
print("total time: " + str(delta.total_seconds()))
print("press enter to exit: ")
exit = input()
browser.quit()