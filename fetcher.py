from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from PIL import Image
import requests
import csv

driver = webdriver.Chrome("C:\\Users\\Rajdeep\\Desktop\\chromedriver.exe")

months = []

textfilepath = "./textinfo.txt"
csvfilepath = "./data.csv"

with open('C:\\Users\Rajdeep\Documents\Python Code\selenium\hubbleimages\months.txt', 'r') as f:
    for item in f:
        months.append(item.upper().strip())

with open(csvfilepath, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['month', 'date', 'year', 'title', 'description', 'imageurl', 'moreinfourl'])

open(textfilepath, 'w')

m30 = [months[i] for i in (0, 2)]
driver.get("https://imagine.gsfc.nasa.gov/hst_bday/")

sleep(7)
#driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

for month in months:
    # select month field and place input
    elem = driver.find_element_by_xpath('//input[@placeholder="Select Month"]')
    elem.clear()
    elem.send_keys(month)

    # select date field
    elem = driver.find_element_by_xpath('//input[@placeholder="Select Date"]')

    # iterate through dates
    for date in range(1,32):
        # conditions for months
        if month == "FEBRUARY" and date == 30:
            break
        elif month in m30 and date == 31:
            break

        # place input on date field
        elem.clear()
        elem.send_keys(date)

        # click submit button
        driver.find_element_by_xpath('//button[@class="submit-btn"]').send_keys(Keys.RETURN)
        #driver.find_element_by_xpath('//button[@class="submit-btn"]').click()
        sleep(1)

        # fetch image and moreinfo
        imgurl = driver.find_element_by_xpath('//a[@class="view-full-image"]').get_attribute('href')
        moreinfourl = driver.find_element_by_xpath('//a[@class="more-info"]').get_attribute('href')

        # prepare filepath for image and textfile
        imagefilepath = "./fullimages/" + str(month) + str(date) + ".png"
        ssfilepath = "./screencaps/" + str(month) + str(date) + "-ss.png"

        # prepare text info
        resultdate = driver.find_element_by_xpath('//div[@class="result-date"]').text
        resulttitle = driver.find_element_by_xpath('//div[@class="result-title"]').text
        resultdesc = driver.find_element_by_xpath('//div[@class="result-description"]').text
        text = resultdate + ": " + resulttitle + " | " + resultdesc + "\n\n"
        year = resultdate[-4:]        

        # request and download image and save the text
        print("fetching image, ", end="")

        while True:
            try:
                r = requests.get(imgurl, timeout=1)
                break
            except requests.exceptions.Timeout:
                print("timed out, retrying")
            except requests.exceptions.ConnectionError:
                print("connection error, retrying")

        print("fetched image, ", end="")
        open(imagefilepath, 'wb').write(r.content)
        open(textfilepath, 'a+').write(text)

        # checking pixel values for ensuring browser image load
        while True:
            driver.save_screenshot("./checkss.png")
            im = Image.open(r"./checkss.png")
            px = im.load()
            if(px[7, 767] == (95, 53, 50) and px[733, 764] == (156, 73, 60) and px[1359, 766] == (194, 75, 63)):
                sleep(3)
                continue
            else:
                break

        # taking the screenshot
        driver.save_screenshot(ssfilepath)

        # write into csv file
        with open(csvfilepath, 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([str(month), str(date), str(year), str(resulttitle), str(resultdesc), str(imgurl), str(moreinfourl)])
        
        # click close button for next set of inputs
        driver.find_element_by_xpath('//button[@class="result-close-btn"]').click()

        # just to keep track
        print(resultdate)

