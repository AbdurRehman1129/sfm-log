import os
import time
import re
import json

# Helper function to run ADB commands and suppress standard output while preserving errors
def run_adb_command(command):
    return os.system(f"{command} >nul 2>&1")  # Redirect stdout to null, keep stderr

# Function to check if the login page is visible
def is_login_page():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.safeum.android:id/et_login" in xml_content and "com.safeum.android:id/et_password" in xml_content and "com.safeum.android:id/login_button" in xml_content

# Function to check if the GO TO AUTH button is visible
def is_go_to_auth_button():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "GO TO AUTH" in xml_content

# Function to check if the progress bar is visible
def is_progress_bar_visible():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/progress" in xml_content

# Function to check if "Invite" or "Settings" button is visible
def check_for_buttons():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
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
    run_adb_command("adb shell input tap 539 822")
    run_adb_command(f"adb shell input text {username}")
    run_adb_command("adb shell input tap 539 989")
    run_adb_command(f"adb shell input text {password}")
    run_adb_command("adb shell input tap 539 1220")

# Launch SafeUM app
def launch_safeum():
    print("Launching SafeUM app...")
    run_adb_command("adb shell monkey -p com.safeum.android 1")

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
        run_adb_command("adb shell input tap 767 323")

# Function to extract phone number from the screen XML
def extract_phone_number():
    print("Extracting phone number...")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    phone_number_pattern = r'\b9944[\d\s]{10}\b'
    phone_numbers = re.findall(phone_number_pattern, xml_content)
    time.sleep(0.012)
    if phone_numbers:
        for number in phone_numbers:
            print("Found phone number:", number)
        return phone_numbers
    else:
        return []

# Function to log out from SafeUM
def logout(username):
    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account control" in xml_content:
            print("Found Account control, clicking button...")
            run_adb_command("adb shell input tap 599 2106")
            run_adb_command("adb shell input tap 599 2006")
            break
        time.sleep(1)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if username in xml_content:
            print("Username found, clicking logout...")
            run_adb_command("adb shell input tap 1003 443")
            break
        time.sleep(1)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account exit" in xml_content:
            print("Found Account exit Page, clicking Keep on device...")
            run_adb_command("adb shell input tap 622 1441")
            break
        time.sleep(1)

# Main function to login and logout multiple accounts
def main():
    usernames = input("Enter usernames separated by commas: ").split(',')
    usernames = [username.strip() for username in usernames if username.strip()]
    password = input("Enter password for all accounts: ")

    # Load existing data from extracted_phone_numbers.json if it exists
    extracted_data = {}
    if os.path.exists("extracted_phone_numbers.json"):
        with open("extracted_phone_numbers.json", "r", encoding="utf-8") as json_file:
            extracted_data = json.load(json_file)

    # Launch SafeUM app
    launch_safeum()
    time.sleep(3)  # Wait for the app to load

    for username in usernames:
        # Skip the username if it already has a phone number in the extracted data
        if username in extracted_data:
            print(f"Skipping {username} as it already has extracted phone numbers.")
            continue

        print(f"\nProcessing account: {username}")

        # Login or handle GO TO AUTH
        for attempt in range(10):
            print(f"Checking for login page or GO TO AUTH button... Attempt {attempt + 1}")
            if is_go_to_auth_button():
                print("GO TO AUTH button found! Clicking it...")
                run_adb_command("adb shell input tap 560 2340")  # Coordinates for the GO TO AUTH button
                time.sleep(1)  # Wait for the transition
            if is_login_page():
                print("Login page found!")
                automate_login(username, password)
                break
            else:
                print("Neither GO TO AUTH nor Login page found.")
            time.sleep(2)
        else:
            print(f"Login page not found for {username}, skipping...")
            continue

        # Wait for progress bar
        wait_for_progress_bar_to_disappear()
        while True:
            print("Checking for Settings button...")
            button = check_for_buttons()

            if button == "invite":
                click_button("settings")
                break
            elif button == "settings":
                click_button("settings")
                break

        # Extract phone number
        phone_numbers = extract_phone_number()
        if phone_numbers:
            extracted_data[username] = phone_numbers
            # Append new data to the JSON file without overwriting
            with open("extracted_phone_numbers.json", "w", encoding="utf-8") as json_file:
                json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)
            print(f"Phone number for {username} has been saved to 'extracted_phone_numbers.json'.")

        # Logout
        logout(username)
        print(f"Logged out from account: {username}\n")
import json

def display_accounts(file_path):
    # Open and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Display the accounts in a readable format
    for username, numbers in data.items():
        for number in numbers:
            print(f"{username} : {number}")


def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux/Unix/MacOS
    else:
        os.system('clear')


if __name__ == "__main__":
    clear_screen()
    print("MENU:")
    print("1. Extract phone numbers from safeum.")
    print("2. Display Extracted accounts.")
    print("3. Exit")
    while(True):
        choice =int(input("\nEnter Your choice: "))
        if choice == 1:
            main()
        elif choice == 2:
            display_accounts('extracted_phone_numbers.json')
        elif choice == 3:
            exit("Exiting...")
