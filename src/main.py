from selenium import webdriver
from selenium.webdriver.common.by import By
import os
# import chromedriver_binary
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.ch .options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Replace with the website URL you want to crawl (start with a small number of links)
website_url = "https://www.diepxuan.com"

# Create a new Chrome session using WebDriver Manager
chromepath=os.environ.get('chromepath')
# driver = webdriver.Chrome()
driver = webdriver.Chrome(service=ChromeDriverManager().install())

# Open the website
driver.get(website_url)

# This example retrieves only the first 5 links
for i in range(5):
    # Find all links using the anchor tag (a)
    links = driver.find_elements(By.TAG_NAME, "a")

    # Check if links exist before accessing them
    if links:
        # Get the first link and its href attribute (URL)
        link = links[i]
        link_url = link.get_attribute("href")

        # Open the link in the same tab (avoid overwhelming the server)
        driver.get(link_url)

        # You can add a short pause here to simulate human-like behavior (optional)
        # time.sleep(1)

        # Print the current URL for reference
        print(f"Visited: {link_url}")
    else:
        print("No more links found on this page.")
        break  # Exit the loop if no links are found

# Close the browser window
driver.quit()
