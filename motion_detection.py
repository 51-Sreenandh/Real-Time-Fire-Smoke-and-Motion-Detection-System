import cv2

def send_alert(message):
    print("ALERT:",message)

    with open("alerts.txt", "a") as file:
        file.write(message + "\n")



                   
camera = cv2.VideoCapture(0)
ret,frame1 = camera.read()
ret,frame2 = camera.read()

while True:
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour)>1000:
            x,y,w,h = cv2.boundingRect(contour)

            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)


            send_alert("Motion Detected - Security Alert")

    cv2.imshow("Motion Detection", frame1)
    frame1 = frame2
    ret,frame2 = camera.read()
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()