import requests as rq
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import io
from PIL import Image


def get_status_code(url):
    r = rq.get(url)
    r_status = r.status_code
    if r_status == 200:
        return True
    else:
        return False

def get_images(driver, paintings):
    image = paintings[0]
    image_src_list = [image.find_element(By.XPATH, './/img[@class = "img-fluid"]').get_attribute('src') for image in paintings]
    return image_src_list

def get_names(driver, paintings):
    image = paintings[0]
    names_list = [image.find_element(By.XPATH, './/div[@class = "product-name"]').text for image in paintings]
    return names_list

def download_image(image_source_list,names_source_list):
    counter = 0
    for i in image_source_list:
        try:
            print('Descargando imagen #: {}'.format(counter))
            image_content = rq.get(i).content
            image_file = io.BytesIO(image_content)
            picture = Image.open(image_file)
            file_path = r"C:\Users\jeanf\OneDrive\Desktop\Trabajo\Freelancer\Upwork\Web Scraper\annuairesanteamelie\images\'" + str(names_source_list[(counter)]) + ".jpg"

            with open(file_path, "wb") as f:
                picture.save(f, "JPEG")

        except OSError:
            image_content = rq.get(i).content
            image_file = io.BytesIO(image_content)
            picture = Image.open(image_file)
            file_path = r"C:\Users\jeanf\OneDrive\Desktop\Trabajo\Freelancer\Upwork\Web Scraper\annuairesanteamelie\images\'" + str(names_source_list[(counter)]) + ".png"
            picture.save(file_path)

        counter += 1

def run():
    print('Checking the status code')
    url = r"http://slarts.com/c/products.html"
    # Checking status code
    get_status_code(url)

    if get_status_code(url) is True:
        print('Status OK --> Starting the driver')
        options = webdriver.ChromeOptions()
        options.add_argument('--incognit')
        driver = webdriver.Chrome(executable_path = r"C:\Users\jeanf\OneDrive\Desktop\Trabajo\Freelancer\Upwork\Web Scraper\annuairesanteamelie\chromedriver_win32\chromedriver.exe")
        # Opening URL
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)
        paintings = driver.find_elements(By.XPATH, './/div[@class = "col-6 col-md-3 col-lg-5ths  product-item-wrap"]')

        # Getting info
        for i in range(0,5):
            paintings = driver.find_elements(By.XPATH, './/div[@class = "col-6 col-md-3 col-lg-5ths  product-item-wrap"]')
            image_source_list = get_images(driver, paintings)
            print('Lista de imágenes obtenidas con un total de: {}'.format(len(image_source_list)))
            names_source_list = get_names(driver, paintings)
            print('Lista de nombres obtenidas con un total de: {}'.format(len(names_source_list)))

            download_image(image_source_list,names_source_list)

            # Clicking the next button
            button = driver.find_element(By.XPATH, '//*[contains(text(), "Next")]')
            button.click()
            time.sleep(5)

    else:
        print('Status code -ERROR-')


if __name__ == '__main__':
    run()