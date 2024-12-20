import subprocess
import time

# Replace these with your SafeUM credentials
USERNAME = "sofa100"
PASSWORD = "2244"


def run_adb_command(command):
    """Runs an ADB shell command."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def open_safeum():
    """Opens the SafeUM app."""
    print("Opening SafeUM app...")
    run_adb_command(
        "adb shell monkey -p com.safeum.android -c android.intent.category.LAUNCHER 1")
    time.sleep(5)


def tap_coordinates(x, y):
    """Taps on the screen at specified coordinates."""
    run_adb_command(f"adb shell input tap {x} {y}")
    time.sleep(1)


def input_text(text):
    """Inputs text into the focused field."""
    run_adb_command(f"adb shell input text \"{text}\"")
    time.sleep(1)


def login_to_safeum():
    """Automates the SafeUM login process."""
    print("Starting login process...")

    # Open the app
    open_safeum()

    # Tap on the username field and input the username
    print("Entering username...")
    tap_coordinates(540, 740)  # Adjust coordinates based on your screen
    input_text(USERNAME)

    # Tap on the password field and input the password
    print("Entering password...")
    tap_coordinates(540, 900)  # Adjust coordinates based on your screen
    input_text(PASSWORD)
    # Tap the login button
    print("Clicking login button...")
    tap_coordinates(540, 1281)  # Adjust coordinates based on your screen

    print("Login process completed!")


if __name__ == "__main__":
    login_to_safeum()
