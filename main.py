import os
import time
import re

# Function to check if the login page is visible
def is_login_page():
    output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    # Check if login-related resource IDs are present
    return "com.safeum.android:id/et_login" in xml_content and "com.safeum.android:id/et_password" in xml_content and "com.safeum.android:id/login_button" in xml_content

# Function to check if the progress bar is visible
def is_progress_bar_visible():
    output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    # Check if the progress bar is present in the UI
    return "android:id/progress" in xml_content

# Function to check if "Invite" or "Settings" button is visible
def check_for_buttons():
    output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    
    if "Invite" in xml_content:
        return "invite"
    elif "Settings" in xml_content:
        return "settings"
    else:
        return None

# Function to automate login
def automate_login(username, password):
    # Input username
    print("Entering username...")
    os.system("adb shell input tap 539 822")  # Coordinates of the username field
    os.system(f"adb shell input text {username}")

    # Input password
    print("Entering password...")
    os.system("adb shell input tap 539 989")  # Coordinates of the password field
    os.system(f"adb shell input text {password}")

    # Tap the login button
    print("Clicking the login button...")
    os.system("adb shell input tap 539 1220")  # Coordinates of the login button

# Launch SafeUM app
def launch_safeum():
    print("Launching SafeUM app...")
    os.system("adb shell monkey -p com.safeum.android 1")  # Launch SafeUM app by package name

# Wait for progress bar to disappear
def wait_for_progress_bar_to_disappear():
    print("Waiting for the progress bar to disappear...")
    while True:
        if not is_progress_bar_visible():
            print("Progress bar disappeared!")
            break
        time.sleep(1)  # Check every second

# Click on the appropriate button
def click_button(button):
    if button == "settings":
        print("Clicking the Settings button...")
        # Coordinates of the Settings button
        os.system("adb shell input tap 767 323")  # Replace with actual Invite button coordinates

# Function to extract phone number from the screen XML
def extract_phone_number():
    print("Extracting phone number...")
    # Read the XML file
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Regular expression to match a phone number starting with 9944 and 14 digits, including spaces
    phone_number_pattern = r'\b9944[\d\s]{10}\b'
    phone_numbers = re.findall(phone_number_pattern, xml_content)

    # Display the phone numbers found
    if phone_numbers:
        for number in phone_numbers:
            print("Found phone number:", number)
    else:
        print("No phone number found.")

# Function to log out from SafeUM
def logout(username):
    # Continuously check for "Account control" text
    while True:
        output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()

        # Look for "Account control" text in the XML
        if "Account control" in xml_content:
            print("Found Account control, clicking coordinates...")
            # Click both coordinates for Account control button
            os.system("adb shell input tap 599 2106")
            os.system("adb shell input tap 599 2006")
            break
        time.sleep(1)  # Check every second

    # Look for the username in the XML and click logout if found
    while True:
        output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()

        if username in xml_content:
            print("Username found in Account control page, clicking logout...")
            os.system("adb shell input tap 1003 443")  # Click logout button
            break
        time.sleep(1)  # Check every second

    # Wait for the "Keep on device" prompt and click "Keep on device"
    while True:
        output = os.popen("adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()

        if "Account exit" in xml_content:
            print("Found Account exit, clicking Keep on device...")
            os.system("adb shell input tap 622 1441")  # Click "Keep on device" button
            break
        time.sleep(1)  # Check every second

# Main logic
username = "sofa100"  # Replace with actual username
password = "2244"     # Replace with actual password

# Step 1: Launch SafeUM app
launch_safeum()

# Step 2: Wait for the app to load
time.sleep(5)  # Wait for 5 seconds (adjust if needed)

# Step 3: Check for the login page and automate login
login_found = False
for attempt in range(10):  # Check 10 times
    print(f"Checking for login page... Attempt {attempt + 1}")
    if is_login_page():
        print("Login page found!")
        automate_login(username, password)
        login_found = True
        break
    time.sleep(2)  # Wait for 2 seconds before checking again

if not login_found:
    print("Login page not found after 10 attempts.")
else:
    # Step 4: Wait for the progress bar to disappear
    wait_for_progress_bar_to_disappear()

    # Step 5: Continuously check for "Invite" or "Settings" button
    while True:
        print("Checking for Invite or Settings button...")
        button = check_for_buttons()

        if button == "invite":
            click_button("settings")
            break  # Exit after clicking invite
        elif button == "settings":
            click_button("settings")
            break  # Exit after clicking settings
        
        time.sleep(1)  # Check every second for the button

    # Step 6: Extract the phone number after settings page is loaded
    extract_phone_number()

    # Step 7: Logout after handling account and exiting
    logout(username)
