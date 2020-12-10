
from selenium import webdriver
#from bs4 import BeautifulSoup
from pdb import set_trace as bp ##for testing
import re
import time
import csv
outputFileName='result'
link = "https://play.google.com/store/apps/details?id=io.fusetech.stackademia&hl=ru&showAllReviews=true"
driver = webdriver.Chrome("./chromedriver")
driver.get(link)

title = driver.find_element_by_xpath('//h1/span').text

print(title)

time.sleep(2)
flag=0
while 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        loadMore=driver.find_element_by_xpath("//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click()
    except:
        time.sleep(1)
        flag=flag+1
        if flag >= 2:
            break
    else:
        flag=0




reviews=driver.find_elements_by_css_selector('h3 + div > div')

print("There are "+str(len(reviews))+" reviews avaliable")
#print("Writing the data...")

with open(outputFileName+'.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["name","rating","comment"])
    for review in reviews:
        try:
            r = review.find_element_by_css_selector('div:first-of-type > div:nth-child(2)')
            
            my_file = open("dump.html", "w")
            my_file.write(review.get_attribute("innerHTML").encode('utf-8'))
            my_file.close()

            rating = review.find_element_by_css_selector('div:first-of-type > div:nth-child(2) > div:nth-child(1) > div > div > span > div > div').get_attribute('aria-label')
            rating = rating.split(':')[1].split(' ')[1]
            name = review.find_element_by_css_selector('div:first-of-type > div:nth-child(2) > div:nth-child(1) > div > span').text
            comment = review.find_element_by_css_selector('div:first-of-type > div:nth-child(2) > div:nth-child(2) > span').text

            print name + ' ('+rating+'): ' + comment
            writer.writerow([name.encode('utf-8'),rating.encode('utf-8'),comment.encode('utf-8')])
        except:
            print("error")
            
driver.quit()
exit()
