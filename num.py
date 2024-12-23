import os
import time
import re

# Function to check if the login page is visible


def is_login_page():
    output = os.popen(
        "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.safeum.android:id/et_login" in xml_content and "com.safeum.android:id/et_password" in xml_content and "com.safeum.android:id/login_button" in xml_content

# Function to check if the progress bar is visible


def is_progress_bar_visible():
    output = os.popen(
        "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/progress" in xml_content

# Function to check if "Invite" or "Settings" button is visible


def check_for_buttons():
    output = os.popen(
        "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
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
    print(f"Logging in with username: {username}")
    # Coordinates of the username field
    os.system("adb shell input tap 539 822")
    os.system(f"adb shell input text {username}")
    # Coordinates of the password field
    os.system("adb shell input tap 539 989")
    os.system(f"adb shell input text {password}")
    # Coordinates of the login button
    os.system("adb shell input tap 539 1220")

# Launch SafeUM app


def launch_safeum():
    print("Launching SafeUM app...")
    os.system("adb shell monkey -p com.safeum.android 1")

# Wait for progress bar to disappear


def wait_for_progress_bar_to_disappear():
    print("Waiting for the progress bar to disappear...")
    while True:
        if not is_progress_bar_visible():
            print("Progress bar disappeared!")
            break
        time.sleep(1)

# Click on the appropriate button


def click_button(button):
    if button == "settings":
        print("Clicking the Settings button...")
        os.system("adb shell input tap 767 323")

# Function to extract phone number from the screen XML


def extract_phone_number():
    print("Extracting phone number...")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    phone_number_pattern = r'\b9944[\d\s]{10}\b'
    phone_numbers = re.findall(phone_number_pattern, xml_content)
    if phone_numbers:
        for number in phone_numbers:
            print("Found phone number:", number)
    else:
        print("No phone number found.")

# Function to log out from SafeUM


def logout(username):
    while True:
        output = os.popen(
            "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account control" in xml_content:
            print("Found Account control, clicking coordinates...")
            os.system("adb shell input tap 599 2106")
            os.system("adb shell input tap 599 2006")
            break
        time.sleep(1)

    while True:
        output = os.popen(
            "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if username in xml_content:
            print("Username found, clicking logout...")
            os.system("adb shell input tap 1003 443")
            break
        time.sleep(1)

    while True:
        output = os.popen(
            "adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml .").read()
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account exit" in xml_content:
            print("Found Account exit, clicking Keep on device...")
            os.system("adb shell input tap 622 1441")
            break
        time.sleep(1)

# Main function to login and logout multiple accounts


def main():
    usernames = input("Enter usernames separated by commas: ").split(',')
    usernames = [username.strip()
                 for username in usernames if username.strip()]
    password = input("Enter password for all accounts: ")
    # Launch SafeUM app
    launch_safeum()
    time.sleep(3)  # Wait for the app to load
    for username in usernames:
        print(f"\nProcessing account: {username}")

        # Login
        for attempt in range(10):
            print(f"Checking for login page... Attempt {attempt + 1}")
            if is_login_page():
                print("Login page found!")
                automate_login(username, password)
                break
            time.sleep(2)
        else:
            print(f"Login page not found for {username}, skipping...")
            continue

        # Wait for progress bar
        wait_for_progress_bar_to_disappear()
        while True:
            print("Checking for Invite or Settings button...")
            button = check_for_buttons()

            if button == "invite":
                click_button("settings")
                break  # Exit after clicking invite
            elif button == "settings":
                click_button("settings")
                break  # Exit after clicking settings
        # Extract phone number
        extract_phone_number()

        # Logout
        logout(username)
        print(f"Logged out from account: {username}\n")


if __name__ == "__main__":
    main()
