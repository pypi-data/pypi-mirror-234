from selenium import webdriver

# Get the username and password
username = "your_username"
password = "your_password"

# Create a web driver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get("https://www.example.com/login")

# Find the username and password input fields
username_input = driver.find_element_by_id("username")
password_input = driver.find_element_by_id("password")

# Enter the username and password
username_input.send_keys(username)
password_input.send_keys(password)

# Click the login button
login_button = driver.find_element_by_id("login-button")
login_button.click()

# Check if the login was successful
if driver.current_url == "https://www.example.com/home":
    print("Login successful")
else:
    print("Login failed")

# If the login was successful, you can now access the website's content. For example, you can use Selenium to click on links, fill out forms, and submit requests.

# If the login failed, you can try again with different credentials. You can also try to debug the code to see where the problem is.

# Finally, when you are done using Selenium, you should close the web driver.
driver.quit()
