from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/run-selenium', methods=['GET'])
def run_selenium():
    options = Options()
    options.headless = True  # Run headless (no window)
    options.add_argument("--no-sandbox")  # Required for App Engine
    options.add_argument("--disable-dev-shm-usage")  # Use /tmp instead of /dev/shm
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging


    # Automatically install and use the appropriate ChromeDriver
    chromedriver_autoinstaller.install()

    # Initialize WebDriver (ensure chromedriver is in your PATH or specify the path here)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Pinterest post URL
    url = "https://es.pinterest.com/pin/2392606047072782/"
    driver.get(url)

    # Give the page time to load and initialize comments section
    time.sleep(5)

    # Extract comments
    comments_elements = driver.find_elements(By.XPATH, "//div[@data-test-id='commentThread-comment']//span[@class='text-container']")
    print(comments_elements)
    comments = [comment.text for comment in comments_elements]

    # Close the driver
    driver.quit()

    # Return the comments as a JSON response
    return jsonify(comments)

if __name__ == '__main__':
    # Use '0.0.0.0' to allow Google App Engine to bind to any network interface
    app.run(host='0.0.0.0')
