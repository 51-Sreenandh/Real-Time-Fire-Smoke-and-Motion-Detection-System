alerts_history = []

def save_log(message):
    file = open("alerts.txt","a")
    file.write(message + "\n")
    file.close

def show_old_logs():
    file = open("alerts.txt", "r")
    logs = file.readlines()
    file.close()

    print("\n Previous logs")
    for log in logs:
        print(log.strip())



def send_alert(level):
    print("ALERT:", level)
    alerts_history.append(level)
    save_log(level)

def check_temperature(temperature):
 if temperature < 10:
     send_alert("very cold environment")
 elif temperature <35 :
     send_alert("normal temperature")
 elif temperature < 50 :
     send_alert("warning: High temperature")
 elif temperature <= 80:
     send_alert("Critical alert!")
 else:
     send_alert("extreme fire risk")

try:
    temp = int(input("enter temp:"))
    check_temperature(temp)

except:
    print("Invalid input! Enter number only")

print("\n ALERT HISTORY")
for alert in alerts_history:
    print(alert)

show_old_logs()


