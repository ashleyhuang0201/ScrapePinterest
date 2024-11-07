import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time

app = Flask(__name__)

# Configure the Firefox options
options = webdriver.firefox.options.Options()
options.add_argument('-headless')  # Run headless
options.set_capability('marionette', True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"})

@app.route('/run-selenium', methods=['GET'])
def run_selenium():
    # Set path for Geckodriver if not already in PATH
    os.environ['PATH'] += ':' + os.path.dirname(os.path.realpath(__file__)) + "/web_driver"
    
    # Initialize WebDriver
    driver = webdriver.Firefox(options = options) 
    
    try:
        # Set a maximum page load time of 2 minutes
        driver.set_page_load_timeout(120)
        
        # Load the Pinterest URL
        url = "https://es.pinterest.com/pin/2392606047072782/"
        driver.get(url)
        
        # Give the page time to load
        time.sleep(10)
        
        # Extract comments (customize the XPath as needed)
        comments_elements = driver.find_elements(By.XPATH, "//div[@data-test-id='commentThread-comment']//span[@class='text-container']")
        comments = [comment.text for comment in comments_elements]
    
    except TimeoutException as ex:
        print(f"Exception has been thrown: {ex}")
        return jsonify({"error": str(ex)}), 500
    finally:
        driver.quit()
    
    # Return the comments as JSON response
    return jsonify(comments)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
