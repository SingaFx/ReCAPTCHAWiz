import requests
import io
import random
import time
import os
import sys
import urllib
import numpy as np

# Image
from PIL import Image


# Selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


# Keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from traceback import print_exception
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras import applications

# Randomization Related
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.5
LONG_MAX_RAND   = 6.5

RECAPTCHA_PAGE_URL = "https://www.google.com/recaptcha/api2/demo"



# CNN Setup
img_width, img_height = 100, 100

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


# build the VGG16 network
model_VGG = applications.VGG16(include_top=False, weights='imagenet', input_shape=input_shape)

# VGG output shape to be fed in to FC layer
VGG_output_shape = (3, 3, 512)

# FC layer
model = Sequential()
model.add(Flatten(input_shape=VGG_output_shape))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy', metrics=['accuracy'])

model.load_weights('model_weights/bottleneck_fc_model.h5')


def get_mountain_challenge():

    # identify the type of challenge
    challenge_type = driver.find_element_by_xpath('//div[@class="rc-imageselect-desc-no-canonical"]/strong').text

    while challenge_type != 'mountains':
        # click refresh button
        refresh_button = driver.find_element_by_xpath('//button[@id="recaptcha-reload-button"]')
        ActionChains(driver).move_to_element_with_offset(refresh_button, -0.35, 0.37).click().perform()
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))
        challenge_type = driver.find_element_by_xpath('//div[@class="rc-imageselect-desc-no-canonical"]/strong').text


def classify(f):
    img = load_img(f, grayscale=False, target_size=(img_width, img_height))
    img = img_to_array(img)/255
    img = np.expand_dims(img, axis=0)
    bottleneck_features = model_VGG.predict(img, batch_size=1)
    prediction = model.predict(bottleneck_features, batch_size=1)
    return prediction


def crop(filename, height, width):
    im = Image.open(filename)
    imgwidth, imgheight = im.size
    im_list = []
    k = 0
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            a.save('recaptchapics/cropped/out%s.jpg' % k)
            im_list.append(a)
            k += 1
    return im_list


def checkbox_status():
    driver.switch_to.default_content()
    # get iframes (embedded html doc within parent html)
    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to_frame(iframes[0])
    checkbox_status = driver.find_elements_by_xpath('//span')[2].get_attribute('aria-checked')
    if checkbox_status == 'true':
        return True
    else:
        driver.switch_to.default_content()
        # reload iframes
        iframes = driver.find_elements_by_tag_name("iframe")
        # get second (last) iframe once picture challenge is loaded
        driver.switch_to_frame(iframes[-1])
        return False

# ORIGINAL WORKING LOOP
def straightpass_loop():

    status = checkbox_status()

    while status == False:

        driver.switch_to.default_content()

        # reload iframes
        iframes = driver.find_elements_by_tag_name("iframe")

        # get second (last) iframe once picture challenge is loaded
        driver.switch_to_frame(iframes[-1])

        get_mountain_challenge()

        # save original picture
        original_path = 'recaptchapics/original/payload.jpg'
        picture_url = driver.find_elements_by_xpath('//img[contains(@class, "rc-image-tile-")\
                                                            and contains(@src, "https://")]')[0].get_attribute('src')
        urllib.request.urlretrieve(picture_url, original_path)

        # crop and save individual pics and make sure no files exist in cropped directory
        cropped_path = 'recaptchapics/cropped/'
        for f in os.listdir(cropped_path):
            file_path = os.path.join(cropped_path, f)
            if not f.startswith('.'):
                os.remove(file_path)

        crop(original_path, 100, 100)

        predictions = []

        # feed pics to CNN

        for n, f in enumerate(os.listdir(cropped_path)):
            if not f.startswith('.'):
                file_path = os.path.join(cropped_path, f)
                prediction = classify(file_path)     # use int to make probabilities into binary
                print(n, prediction)

        #       keep clicking on successive pictures until not mountain
                while prediction < 0.1:
                    table = driver.find_elements_by_xpath('//tbody/tr/td')
                    table[n].click()
                    time.sleep(6)

                    picture = driver.find_elements_by_xpath('//td//img')[n]
                    picture_url = picture.get_attribute('src')
                    f = 'out%s.jpg' % n
                    file_path = os.path.join(cropped_path, f)
                    urllib.request.urlretrieve(picture_url, file_path)
                    prediction = classify(file_path)   # break out of while loop when image no longer a mountain
                    print('while', n, prediction)

        # click verify button
        driver.find_element_by_xpath('//button[@id="recaptcha-verify-button"]').click()

        # check checkbox_status
        status = checkbox_status()
        print(status)
        time.sleep(3)

def main():
    # selenium setup
    chromedriver = "/Applications/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver

    PROXY = 'http://us-fl.proxymesh.com:31280'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)

    global driver
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)

    AC = ActionChains(driver) # create Action Chain to simulate mouse movement

    # check IP
    driver.get('https://www.google.com/search?q=ip+address&oq=ip+address&aqs=chrome..69i57j0l5.2406j0j7\
    &sourceid=chrome&ie\=UTF-8')
    time.sleep(10)

    # open recaptcha demo page
    driver.get(RECAPTCHA_PAGE_URL)

    # get iframes (embedded html doc within parent html)
    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to_frame(iframes[0])

    # click I'm not a robot checkbox
    AC = ActionChains(driver) # create Action Chain to simulate mouse movement
    checkbox_button = driver.find_element_by_xpath('//div[@class="recaptcha-checkbox-checkmark" and @role="presentation"]')
    AC.move_to_element(checkbox_button).click().perform()
    driver.switch_to.default_content()
    # reload iframes
    iframes = driver.find_elements_by_tag_name("iframe")
    # get second (last) iframe once picture challenge is loaded
    driver.switch_to_frame(iframes[-1])
    time.sleep(3)

    # run straightpass_loop
    straightpass_loop()

if __name__ == "__main__":
    main()
