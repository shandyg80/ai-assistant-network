import pyautogui
import time

def capture_button():
    print("Please position your mouse over the Execute Instructions button...")
    print("Screenshot will be taken in 5 seconds...")
    time.sleep(5)

    # Get mouse position
    x, y = pyautogui.position()

    # Take screenshot of region around button (adjust size if needed)
    button_image = pyautogui.screenshot(region=(x-75, y-15, 150, 30))
    button_image.save('execute_button.png')
    print("Button image saved!")

if __name__ == "__main__":
    capture_button()