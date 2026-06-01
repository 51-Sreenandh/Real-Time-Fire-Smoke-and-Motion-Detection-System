import cv2
import time
from datetime import datetime


def send_alert(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("ALERT:", message)

    with open("alerts.txt", "a") as file:
        file.write(current_time + " - " + message + "\n")


def temperature_monitor():
    temperature = float(input("Enter temperature: "))

    if temperature < 10:
        send_alert("Very Cold Temperature!")

    elif temperature <= 40:
        send_alert("Normal Temperature")

    else:
        send_alert("High Temperature Alert!")


def motion_monitor():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Camera not opening!")
        return

    ret, frame1 = camera.read()
    ret, frame2 = camera.read()

    last_alert_time = 0 

    while True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        motion_found = False

        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                motion_found = True

        
        if motion_found:
            current_time = time.time()

            if current_time - last_alert_time > 5:
                send_alert("Motion Detected!")
                last_alert_time = current_time

        cv2.imshow("Smart Monitoring - Motion Detector", frame1)

        frame1 = frame2
        ret, frame2 = camera.read()

        if not ret:
            break

        if cv2.waitKey(10) == 27:   # ESC
            break

    camera.release()
    cv2.destroyAllWindows()

def smoke_monitor():
    smoke = input("Smoke level (Normal/High/Critical): ")

    if smoke.lower() == "critical":
        send_alert("Critical smoke alert")
    else:
        print("Smoke Normal")


def view_alerts():
    try:
        with open("alerts.txt", "r") as file:
            data = file.read()

            if data == "":
                print("No alerts found")
            else:
                print("\n=== ALERT HISTORY ===")
                print(data)

    except FileNotFoundError:
        print("No alert file found")


def clear_alerts():
    with open("alerts.txt", "w") as file:
        file.write("")

    print("Alert history cleared")


print("=== SMART MONITORING SYSTEM STARTED ===")
print("Checking sensors...")


while True:
    print("\n===== SMART MONITORING SYSTEM =====")
    print("1. Motion Monitor")
    print("2. Temperature only")
    print("3. Smoke only")
    print("4. View Alert History")
    print("5. Clear Alert History")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        motion_monitor()

    elif choice == "2":
        temperature_monitor()

    elif choice == "3":
        smoke_monitor()

    elif choice == "4":
        view_alerts()

    elif choice == "5":
        clear_alerts()

    elif choice == "6":
        print("System Closed")
        break

    else:
        print("Invalid choice! Please enter 1, 2, 3, 4, 5 or 6")



try:
    with open("alerts.txt", "r") as file:
        alerts = file.readlines()

    print("\nTotal Alerts Logged:", len(alerts))
    print("\nLast 5 Alerts:")

    for alert in alerts[-5:]:
        print(alert.strip())

    info_count = 0
    warning_count = 0
    critical_count = 0

    for alert in alerts:
        if "[INFO]" in alert:
            info_count += 1
        elif "[WARNING]" in alert:
            warning_count += 1
        elif "[CRITICAL]" in alert:
            critical_count += 1

    print("\nAlert Summary:")
    print("INFO Alerts:", info_count)
    print("WARNING Alerts:", warning_count)
    print("CRITICAL Alerts:", critical_count)

except FileNotFoundError:
    print("No alert history found.")