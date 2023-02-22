from sqlite3 import Cursor
from unittest import result
import RPi.GPIO as GPIO
import time
import pymysql
import datetime

db=pymysql.connect(host="192.168.0.11",user="proyecto1",passwd="1234",db="tasksdb")
db.autocommit(True)
cur=db.cursor()

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER=23
GPIO_ECHO=24
pin_led=17
Buzzer=18
umbral=10

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.setup(pin_led,GPIO.OUT)
GPIO.setup(Buzzer,GPIO.OUT)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime=time.time()
    StopTime=time.time()
    while GPIO.input(GPIO_ECHO)==0:
        StartTime=time.time()
    while GPIO.input(GPIO_ECHO)==1:
        StopTime=time.time()
    TimeElapsed=StopTime-StartTime
    distance=(TimeElapsed*34300)/2
    return distance

if  __name__=='__main__':
    try:
        while True:            
            sql2="select Estado from estado"
            cur.execute(sql2)
            result=cur.fetchone()
            print(result)
            if bool(result):
                GPIO.output(pin_led, GPIO.LOW)
                GPIO.output(Buzzer, GPIO.LOW)
                time.sleep(1)
                dist=distance()
                print("Measured Distance=%.1f cm"%dist)
                if dist<=umbral:
                    print("Detected")
                    GPIO.output(pin_led, GPIO.HIGH)
                    GPIO.output(Buzzer, GPIO.HIGH)
                    today=datetime.datetime.now()
                    date_time=today.strftime("%Y-%m-%d %H:%M:%S")
                    print("date and time:", date_time)
                    time.sleep(5)
                    sql=("""INSERT INTO tasks (title) VALUES (%s)""", (date_time))
                    try:
                        print("Writing to database...")
                        cur.execute(*sql)
                        db.commit()
                        print("Write complete")
                    except:
                        db.rollback()
                        print("Failed writing to database")
                    time.sleep(3)
                else:
                    print("Nothing detected")
                    time.sleep(1)
            else:
                print("Circuit off")
                time.sleep(5)
    except KeyboardInterrupt:
        cur.close()
        db.close()
        print("Measurement stopped by User")
        GPIO.cleanup()