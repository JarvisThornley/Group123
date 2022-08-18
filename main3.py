# general libraries
from this import d
import time
import random
import math
import datetime

# camera libraries
from picamera import PiCamera, Color

# servo libraries
import RPi.GPIO as GPIO
from gpiozero import Servo

# load cell libraries
from hx711 import HX711
import sys

# imu libraries
from mpu6050 import mpu6050



# setup:
#now = datetime.time.now()

# camera:
camera = PiCamera()
camera.rotation = 270
camera.resolution = (1080, 1080)

def take_photo(name, preview_time):
    camera.start_preview()
    time.sleep(3+preview_time)
    camera.capture('/home/pi/Desktop/%s.jpg' % name)   #'/home/pi/Desktop/image.jpg'
    camera.stop_preview()
	
def take_video(name, length):
	camera.start_preview()
	camera.start_recording('/home/pi/Desktop/%s.h264' % name)
	time.sleep(3+length)
	camera.stop_recording()
	camera.stop_preview()
	
	
# servo:
GPIO.setmode(GPIO.BCM)

GPIO.setup(11,GPIO.OUT)  #set pin 11 as output

'''
servo = Servo(11)

servo_pos = 0   # global variable to keep track of servo position

def rotate_servo(final_pos, current_pos):   # direction in 1 for cw, -1 for ccw
    if abs(final_pos)>1:
        print("please enter a valid position between -1 and 1")
    else:
        current_pos = round(current_pos, 2)
        final_pos = round(final_pos,2)
        if current_pos<final_pos:
            while current_pos!=final_pos:
                current_pos+=0.01
                servo.value = current_pos
                time.sleep(0.05)
        else:
            while current_pos!=final_pos:
                current_pos-=0.01
                servo.value = current_pos
                time.sleep(0.05)

'''

# servo alt

servo = GPIO.PWM(11, 50)

servo_angle = 0 # global variable to keep track of servo angle

def start_servo():
    servo.start(0)  

def stop_servo():
    servo.stop()

def rotate_servo(final_angle, current_angle):   # positive for cw, negative for ccw
    if abs(final_angle - 90)>90:
        print("please enter a valid integer angle between 0 and 180 degrees")
    else:
        target_pos = round((1/18)*final_angle + 2.5, 1)
        current_pos = round((1/18)*current_angle + 2.5, 1)
        if current_pos<target_pos:
            while current_pos<target_pos:
                current_pos+=0.1
                servo.ChangeDutyCycle(current_pos)
                time.sleep(0.1)
        else:
            while current_pos>target_pos:
                current_pos-=0.1
                servo.ChangeDutyCycle(current_pos)
                time.sleep(0.1)
        servo.ChangeDutyCycle(0)
        return final_angle

# load cell:
EMULATE_HX711=False

hx = HX711(5, 6) # GPIO PINS OF RPI
referenceUnit = 1
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()
hx.tare()

def load_tare():
    hx.tare
    print("tare complete")

    
def get_weight(print_bool=True):
    weight = hx.get_weight(5)
    if print_bool:
        print(weight)
    return weight
    
def calibrate_ref_unit():
    print("beginning calibration...")
    time.sleep(1)
    print("please place an object of known weight on platform")
    
    cont = input("ready? (y/n)")
    while cont != 'y':
        time.sleep(1)
        
    knownWeight = float(input("please enter precise weight of object"))
    time.sleep(1)
    
    val = get_weight(False)
    referenceUnit = val/knownWeight
    
    hx.set_reference_unit(referenceUnit)
    
    print("calibration complete :)")

# imu:
mpu = mpu6050(0x68)

def get_accel(print_bool=True, store_bool=False, store_name=""):
    accel_data = mpu.get_accel_data()
    if print_bool:
        print("Acc X : "+str(accel_data['x']))
        print("Acc Y : "+str(accel_data['y']))
        print("Acc Z : "+str(accel_data['z']))
        print()
    if store_bool:
        with open(f"{store_name}.txt", 'w') as f:
            f.write(now + "\n")
            f.write(str(accel_data['x']) + "\n")
            f.write(str(accel_data['y']) + "\n")
            f.write(str(accel_data['z']) + "\n")
    
    return accel_data

def get_gyro(print_bool=True, store_bool=False, store_name=""):
    gyro_data = mpu.get_gyro_data()
    if print_bool:
        print("Gyro X : "+str(gyro_data['x']))
        print("Gyro Y : "+str(gyro_data['y']))
        print("Gyro Z : "+str(gyro_data['z']))
        print()
    if store_bool:
        with open(f"{store_name}.txt", 'w') as f:
            f.write(now + "\n")
            f.write(str(gyro_data['x']) + "\n")
            f.write(str(gyro_data['y']) + "\n")
            f.write(str(gyro_data['z']) + "\n")
    
    return gyro_data

# general:
def cleanAndExit():
    print("Cleaning...")
    servo.stop()
    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()



# main code:
print('starting up..')
time.sleep(2)
servo.start(0)

print('calibrating load cell')
calibrate_ref_unit()

print('commence operation:')
i = 1
while i<18:
    try:
        servo_angle = rotate_servo(10*i, servo_angle)
        
        print('current acceleration:\n')
        get_accel()
        time.sleep(1)
    
        print('current weight:\n')
        get_weight()
        time.sleep(1)
        
        if i%6 == 0:
            take_photo(f'{i}',  1)
            
        i+=1
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
while i>0:
    try:
        servo_angle = rotate_servo(10*i, servo_angle)
        
        print('current acceleration:\n')
        get_accel()
        time.sleep(1)
        
        print('current weight:\n')
        get_weight()
        time.sleep(1)
    
        if i%6 == 0:
            take_photo(f'{i}',  1)
            
        i-=1
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
         

    
    
    

'''
get_gyro()

start_servo()
servo_angle = rotate_servo(90, servo_angle)
time.sleep(2)
servo_angle = rotate_servo(0, servo_angle)


while True:
    get_accel()
    time.sleep(3)
take_photo('hype', 5)
calibrate_ref_unit()

while True:
    try:
        get_weight()
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
'''

    
'''
calibrate_ref_unit()

try:
    get_weight(True)    
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])



- calibrate scale
- add weight
- spin
- print imu data
- stop spin
- show video 


'''
