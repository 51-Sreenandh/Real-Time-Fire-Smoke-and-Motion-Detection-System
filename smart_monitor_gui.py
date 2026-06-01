import tkinter as tk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk
import winsound
import threading
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

class SmartMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Monitoring System")
        self.root.geometry("900x700")

        self.camera = None
        self.running = False
        self.alert_count = 0
        self.email_sent = False
        self.frame1 = None
        self.frame2 = None
        self.last_alert_time = 0

        
        self.title_label = tk.Label(

                        root,

                        text="AI SMART MONITORING SYSTEM",

                        font=("Arial", 24, "bold"),

                        fg="white",

                        bg="#1e1e1e"

        )

        self.title_label.pack(pady=15)

        
        self.video_label = tk.Label(

            root,

            bg="black",

            bd=5,

            relief="ridge"

        )

        self.video_label.pack(pady=10)

         
        self.detect_frame = tk.Frame(
            root,
            bg="#1e1e1e"
        )

        self.detect_frame.pack(pady=10)





        self.motion_status = tk.Label(

            self.detect_frame,

            text="Motion : SAFE",

            font=("Arial", 14, "bold"),

            fg="lime",

            bg="#1e1e1e"

        )

        self.motion_status.grid(
            row=0,
            column=0,
            padx=20
        )





        self.fire_status = tk.Label(

            self.detect_frame,

            text="Fire : SAFE",

            font=("Arial", 14, "bold"),

            fg="lime",

            bg="#1e1e1e"

        )

        self.fire_status.grid(
            row=0,
            column=1,
            padx=20
        )



        self.smoke_status = tk.Label(

            self.detect_frame,

            text="Smoke : SAFE",

            font=("Arial", 14, "bold"),

            fg="lime",

            bg="#1e1e1e"

        )

        self.smoke_status.grid(
            row=0,
            column=2,
            padx=20
        )

        self.alert_count = 0

        self.alert_counter_label = tk.Label(
            root,
            text="Total Alerts : 0",
            font=("Arial", 16, "bold"),
            fg="yellow",
            bg="#1e1e1e"
        )

        self.alert_counter_label.pack(pady=10)



        self.button_frame = tk.Frame(

            root,

            bg="#1e1e1e"
        )

        self.button_frame.pack(pady=15)



        self.start_button = tk.Button(

            self.button_frame,

            text="START CAMERA",

            command=self.start_camera,

            font=("Arial", 14, "bold"),

            bg="#00aa00",

            fg="white",

            width=18,

            height=2

        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=10
        )

        self.stop_button = tk.Button(

            self.button_frame,

            text="STOP CAMERA",

            command=self.stop_camera,

            font=("Arial", 14, "bold"),

            bg="#aa0000",

            fg="white",

            width=18,

            height=2

        )

        self.stop_button.grid(
            row=0,
            column=1,
            padx=10
        )
        
        
        self.exit_button = tk.Button(

            self.button_frame,

            text="EXIT",

            command=root.destroy,

            font=("Arial", 14, "bold"),

            bg="#444444",

            fg="white",

            width=18,

            height=2

        )

        self.exit_button.grid(
            row=0,
            column=2,
            padx=10
        )



        self.status_label = tk.Label(

            root,

            text="SYSTEM STATUS: ACTIVE",

            font=("Arial", 16, "bold"),

            fg="lime",

            bg="#1e1e1e"

        )

        self.status_label.pack(pady=10)


        self.last_snapshot_time = 0




    def start_camera(self):
        self.camera = cv2.VideoCapture(0)

        ret, self.frame1 = self.camera.read()
        ret, self.frame2 = self.camera.read()

        self.running = True
        self.update_frame()

    def update_frame(self):
    
        if self.running:

            ret, frame = self.camera.read()

            if ret:

            
                diff = cv2.absdiff(self.frame1, self.frame2)

                gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

                blur = cv2.GaussianBlur(gray, (5, 5), 0)

                _, thresh = cv2.threshold(
                    blur,
                    20,
                    255,
                    cv2.THRESH_BINARY
                )

                contours, _ = cv2.findContours(
                    thresh,
                    cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE
                )


                motion_found = True


                for contour in contours:
                    

                    if cv2.contourArea(contour) > 1000:

                        x, y, w, h = cv2.boundingRect(contour)

                        cv2.rectangle(
                            self.frame1,
                            (x, y),
                            (x + w, y + h),
                            (0, 255, 0),
                            2
                        )

                        cv2.putText(
                            self.frame1,
                            "MOTION DETECTED",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2
                        )


                        if not motion_found:

                            self.motion_status.config(

                            text="🟢 Motion : SAFE",

                            fg="lime"

                            )

                      
                        if self.can_alert():

                            self.play_alarm()
                            self.log_alert("MOTION DETECTED")
                            self.increase_alert_count()
                            if self.can_save_snapshot():
                            
                                self.save_snapshot(
                                    self.frame1,
                                    "MOTION"
                                )
                                        
                frame_rgb = cv2.cvtColor(
                    self.frame1,
                    cv2.COLOR_BGR2RGB
                )

                frame_rgb = cv2.resize(
                    frame_rgb,
                    (700, 350)
                )

                image = Image.fromarray(frame_rgb)

                photo = ImageTk.PhotoImage(image=image)

                self.video_label.config(image=photo)

                self.video_label.image = photo

            
                self.frame1 = self.frame2

                ret, self.frame2 = self.camera.read()

            self.video_label.after(10, self.update_frame)


            self.motion_status.config(

               text="🔴 Motion : DETECTED",

                fg="red"

            )
                

            hsv = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2HSV)

            lower_fire = (0, 120, 200)
            upper_fire = (35, 255, 255)

            fire_mask = cv2.inRange(
                hsv,
                lower_fire,
                upper_fire
            )

            fire_contours, _ = cv2.findContours(
                fire_mask,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )


            fire_detected = False
           

            for contour in fire_contours:

                if cv2.contourArea(contour) > 3000:

                    fire_detected = True

                    x, y, w, h = cv2.boundingRect(contour)

                    cv2.rectangle(
                        self.frame1,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        self.frame1,
                        "FIRE DETECTED",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )


                if not fire_detected:

                    self.email_sent = False

                    self.fire_status.config(

                        text="🟢 Fire : SAFE",

                        fg="lime"

                    )

            if fire_detected:

                if self.can_alert():

                    self.play_alarm()

                    self.log_alert("FIRE DETECTED")
                    self.increase_alert_count()

                if not self.email_sent:

                    threading.Thread(
                    target=self.send_email_alert,
                    args=(
                        "FIRE DETECTED",
                        "Fire detected by Smart Monitoring System"
                    ),
                    daemon=True
                ).start()

                self.email_sent = True


                if self.can_save_snapshot():

                    self.save_snapshot(
                        self.frame1,
                        "FIRE"
                    )
                                
                self.fire_status.config(

                    text="🔴 Fire : DETECTED",

                    fg="red"

                )


                # SMOKE DETECTION

                gray = cv2.cvtColor(
                    self.frame1,
                    cv2.COLOR_BGR2GRAY
                )

                blur = cv2.GaussianBlur(
                    gray,
                    (21, 21),
                    0
                )

                _, smoke_mask = cv2.threshold(
                    blur,
                    180,
                    255,
                    cv2.THRESH_BINARY
                )

                smoke_contours, _ = cv2.findContours(
                    smoke_mask,
                    cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE
                )

                smoke_detected = False

                for contour in smoke_contours:

                    if cv2.contourArea(contour) > 5000:

                        smoke_detected = True

                        x, y, w, h = cv2.boundingRect(contour)

                        cv2.rectangle(
                            self.frame1,
                            (x, y),
                            (x + w, y + h),
                            (255, 255, 255),
                            3
                        )

                        cv2.putText(
                            self.frame1,
                            "SMOKE DETECTED",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 255, 255),
                            3
                        )
                if not smoke_detected:

                    self.smoke_status.config(
                       text="🟢 Smoke : SAFE",
                        fg="lime"
                    )
                if smoke_detected:

                    if self.can_alert():

                        self.play_alarm()

                        self.log_alert("SMOKE DETECTED")
                        self.increase_alert_count()

                        threading.Thread(

                            target=self.send_email_alert,

                            args=(
                                "SMOKE DETECTED",
                                "Smoke detected by Smart Monitoring System"
                            ),

                            daemon=True

                        ).start()

                    if self.can_save_snapshot():

                        self.save_snapshot(
                            self.frame1,
                            "SMOKE"
                        )
                 

                        self.smoke_status.config(
                           text="🔴 Smoke : DETECTED",
                            fg="red"
                        )
                     
                     




    def stop_camera(self):

            self.running = False

            if self.camera is not None:
                self.camera.release()

            self.video_label.config(image="")

    def play_alarm(self):

        threading.Thread(
            target=self.beep_sound,
            daemon=True
       ).start()  
    def beep_sound(self):

       duration = 500
       frequency = 1000

       winsound.Beep(frequency, duration)

    def can_alert(self):

        current_time = time.time()

        if current_time - self.last_alert_time > 3:

            self.last_alert_time = current_time

            return True

        return False
    

    def can_save_snapshot(self):

        current_time = time.time()

        if current_time - self.last_snapshot_time > 5:

            self.last_snapshot_time = current_time

            return True

        return False




    def log_alert(self, message):

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        with open("alerts.txt", "a") as file:

            file.write(
                current_time +
                " - " +
                message +
                "\n"
            )
   

    def increase_alert_count(self):

        self.alert_count += 1

        self.alert_counter_label.config(
            text=f"Total Alerts : {self.alert_count}"
        )


    def save_snapshot(self, frame, alert_type):

            now = datetime.now()

            filename = now.strftime(
                "%Y%m%d_%H%M%S"
            )

            path = (
                "snapshots/" +
                alert_type +
                "_" +
                filename +
                ".jpg"
            )

            threading.Thread(
                        target=cv2.imwrite,
                        args=(path, frame.copy()),
                        daemon=True
            ).start()
            print("Snapshot Saved:", path)


    

    def send_email_alert(self, subject, message):
            print("EMAIL FUNCTION CALLED")

            sender_email = "sreenandhpreneeshtp@gmail.com"

            app_password = "oity fict acnt qwwb"

            receiver_email = "sreenandhpreneesh19@gmail.com"

            msg = MIMEText(message)

            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            try:

                print("Connecting...")
                server = smtplib.SMTP("smtp.gmail.com", 587)

                print("TLS...")
                server.starttls()

                print("Login...")
                server.login(sender_email, app_password)

                print("Sending...")
                server.sendmail(
                    sender_email,
                    receiver_email,
                    msg.as_string()
                )

                print("Email Alert Sent")

            except Exception as e:
                print("Email Error:", e)



root = tk.Tk()
root.title("AI Smart Monitoring System")

root.geometry("1300x900")

root.configure(bg="#1e1e1e")


app = SmartMonitorApp(root)
root.mainloop()