import os
from flask import Flask, request, redirect, render_template, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from db_operations import *



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_string = "https://www.flipkart.com/search?q=" + request.form['product_name'].replace(' ','%20')
        review_limit = int(request.form['review_limit'])
        # print(review_limit)
        if review_limit < 0 or review_limit > 100:
            err_message = "Enter a valid input between 1 and 100"
            print(err_message)
            return render_template('index.html', err_message=err_message)
        
        count = 0

        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')

        mongo_db = MongoDBManagement(username, password)

        mongo_db.delete_records('Collection1', 'Database1')


        # code for running selenium chrome web driver in heroku

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        # options.add_argument("--window-size=1920,1080")
        
        # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--allow-running-insecure-content')
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        # service = Service("./chromedriver_win32/chromedriver.exe")
        service = Service(os.environ.get("CHROMEDRIVER_PATH"))
        driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(1)

        driver.get(search_string)

        try:
            products_on_page = driver.find_elements(By.XPATH, "//div[@class='_2kHMtA']/a")
        
            for product in products_on_page:
                
                if (review_limit-count) > 0:
                
                    product.click()

                    driver.switch_to.window(driver.window_handles[1])

                    product_name = driver.find_element(By.XPATH, "//*[@class='B_NuCI']").text

                    review_link = driver.find_element(By.XPATH, "//*[@class='_1AtVbE col-12-12']/div/a/div/span")
                    review_link.click()

                    reviews = driver.find_elements(By.XPATH, "//div[@class='col _2wzgFH K0kLPL']")


                    for review in reviews:
                        customer_name = review.find_element(By.XPATH, ".//p[@class='_2sc7ZR _2V5EHH']").text

                        rating = review.find_element(By.XPATH, ".//div[1]/div").text

                        review_title = review.find_element(By.XPATH, ".//div[1]/p").text

                        review_comments = review.find_element(By.XPATH, ".//div[2]/div/div/div").text

                        # print(product_name, customer_name, rating, review_title, review_comments)

                        record = {
                            "product_name": product_name,
                            "customer_name": customer_name,
                            "rating": rating,
                            "review_title": review_title,
                            "review_comments": review_comments
                        }

                        # print(record)
                        mongo_db.insert_record('Collection1', 'Database1', record=record)
                        count+= 1

                        if (review_limit-count) > 0:
                            continue
                        else:
                            break
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            data = mongo_db.find_records('Collection1', 'Database1')
            return render_template('results.html', data=data)

        except:
            err_message = "Oops! Something went wrong. Try again or search a different item."
            return render_template('index.html', err_message=err_message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


