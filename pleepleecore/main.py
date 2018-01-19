import client
import get_plant
import time
import RPi.GPIO as GPIO
import picamera
import math
import numpy as np
import argparse
import cv2
import json
import MPU9250

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
servo=GPIO.PWM(17, 100)

c = client.create_client("test")
c.conn()
import time
time.sleep(1)
c.send("take/9999999/motor1:1\n")
time.sleep(1)
c.send("take/9999999/odometry:1\n")

i = [0, 0, 0, 0]
last_time = time.time()

def p():
    global i
    while True:
        msg = c.recv(10000)
        try:
            i = list(map(int, msg.rsplit(":", 1)[1].split(" ")))
        except:
            continue
        time.sleep(0.25)


#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
pos = [10, 10]

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

import threading
a = threading.Thread(target=p)
a.start()

def get_angle():
    angles = []
    xs = []
    ys = []
    data = mpu.readMagnet()
    for i in range(400):
        data = mpu.readMagnet()
        while (data["x"] == 0 and data["y"] == 0):
            time.sleep(0.01)
            data = mpu.readMagnet()
        data["x"] -= 39.66
        data["x"] /= 24.47
        data["y"] -= 2.8675
        data["y"] /= 23.84
        xs.append(data["x"])
        ys.append(data["y"])
        a = math.atan2(data["y"], data["x"])
        angles.append(a)
        time.sleep(0.015)
    avg = sum(angles) / len(angles)
    avg = math.atan2(sum(ys), sum(xs))
    return avg


def get_pos(vals):
    return (vals[1] + vals[2]) / 2, (vals[0] + vals[3]) / 2

def move(dist, to_left=1, to_right=1):
    dist /= 0.90
    vals = list(i)
    left, right = get_pos(vals)
    left_init = left
    right_init = right
    end_left = left + dist
    end_right = right + dist
    last_left, last_right = left, right
    sl = 120
    sr = 120
    cu_l = 0
    cu_r = 0
    distance_obj_cm = 3000
    while distance_obj_cm > 55 and (left < end_left or right < end_right):
        old_sl = sl
        old_sr = sr
        cur_left, cur_right = get_pos(i)
        dl = cur_left - last_left
        dr = cur_right - last_right
        cu_l += dl
        cu_r += dr
        ratio = (cu_l + 0.1) / (cu_r + 0.1)
        ratio2 = (cu_r + 0.1) / (cu_l + 0.1)
        cur_ratio = (dl + 0.1) / (dr + 0.1)
        cur_ratio2 = (dr + 0.1) / (dl + 0.1)
        if cu_l < cu_r:
            if sl < 125 or sr < 125:
                sl *= ratio2
            else:
                sr /= ratio2
        elif cu_l > cu_r:
            if sr < 125 or sl < 125:
                sr *= ratio
            else:
                sl /= ratio
        if sl < 100:
            sl = 100
        if sr < 100:
            sr = 100
        if sl > 170:
            sl = 170
        if sr > 170:
            sr = 170
        c.sendtoserial("motor1", int(sr) * to_left)
        c.sendtoserial("motor2", int(sl) * to_right)
        c.sendtoserial("motor3", int(sl) * to_right)
        c.sendtoserial("motor4", int(sr) * to_left)
        left, right = cur_left, cur_right
        last_left, last_right = cur_left, cur_right
        distance_obj_cm = distance()
        print("DIST: ", distance_obj_cm)
        time.sleep(0.25)
    c.sendtoserial("motor1", "0")
    c.sendtoserial("motor2", "0")
    c.sendtoserial("motor3", "0")
    c.sendtoserial("motor4", "0")
    time.sleep(0.5)
    if distance_obj_cm < 60:
        return (1, left - left_init)
    return (0, left - left_init)


def move_centimeter(cm):
    global init_angle, pos, tunny_right
    unit_per_cm = 290 / 71 / 2 / 1.44
    ret = []
    while cm > 0.1:
        cur = min(cm, 100)
        cm -= cur
        ret = move(unit_per_cm * cur)
        if ret[0] == 1:
            break
        angle = get_angle()
        old_angle = init_angle
        init_angle = angle
        turn(get_angle_diff(angle, old_angle)[1])
        time.sleep(1)

    if tunny_right == 1:
        pos[1] += ret[1] / unit_per_cm
    else:
        pos[0] += ret[1] / unit_per_cm
    if ret[0] == 1 and tunny_right:
        found_obstacle(pos[0], pos[1] + 50)
    else:
        found_obstacle(pos[0] + 50, pos[1])

    print(ret[1] / unit_per_cm)

def iset_servo_angle(angle_idx):
    vals = [5, 9, 13, 17, 21]
    servo.start(vals[angle_idx])
    time.sleep(1.5)
    servo.start(0)


mpu=MPU9250.MPU9250()

def get_angle_diff(angle1, angle2):
    diff = angle2 - angle1
    while diff < -3.1415:
        diff += 3.1415*2
    while diff > 3.1415:
        diff -= 3.1415*2
    return abs(diff), diff

def turn(rad, first=True):
    global init_angle
    target_angle = init_angle + rad
    while target_angle > 3.1415:
        target_angle -= 3.1415 * 2
    while target_angle < -3.1415:
        target_angle += 3.1415 * 2
    rad *= -1
    left_val = -1 if rad > 0 else 1
    right_val = -left_val
    c.sendtoserial("motor1", str(160 * left_val))
    c.sendtoserial("motor2", str(160 * right_val))
    c.sendtoserial("motor3", str(160 * right_val))
    c.sendtoserial("motor4", str(160 * left_val))
    time.sleep(abs(rad) / 2 + 0.1)
    c.sendtoserial("motor1", "0")
    c.sendtoserial("motor2", "0")
    c.sendtoserial("motor3", "0")
    c.sendtoserial("motor4", "0")
    time.sleep(0.2)
    angle = get_angle()
    diff, dir = get_angle_diff(angle, target_angle)
    if diff > 0.05:
        time.sleep(0.1)
        init_angle = angle
        turn(dir, False)
    if first:
        init_angle=target_angle
        time.sleep(0.5)


def overwrite_mapinit(x, y):
    map_data = []
    f_size = 4.5

    print("x: " + str(x))
    print("y: " + str(y))

    with open('fetch/map.capture_init', 'r+') as map_file:
        f_size = float(map_file.readline())
        print(str(f_size))

        map_data = list(map_file.read().replace('\n', ''))

        n = y * f_size * 900 + x * f_size
        for j in range(0, 60):
            for i in range(0, 60):
                map_data[int(900 * j  + i + n)] = 'P'
                map_file.close()

    with open('fetch/map.capture_init', 'w+') as f:
        f.write(str(f_size) + "\n")
        map_str = ''.join(map_data)
        f.write(map_str)
        f.close()

def process_image(image_path):
    name = image_path
    source_image = cv2.imread(name)
    average_color_per_row = np.average(source_image, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = np.uint8(average_color)
    print(average_color)
    average_color_img = np.array([[average_color]*100]*100, np.uint8)
    return average_color

nb_photo = 0
camera = picamera.PiCamera()
camera.rotation = 90
camera.contrast = 60
def found_obstacle(x,  y):
    global nb_photo
    camera.capture("fetch/pics/photo_" + str(nb_photo) + ".jpg");
    is_plant = get_plant.get_plant("fetch/pics/photo_" + str(nb_photo) + ".jpg");
    if is_plant:

        # Water the plant
        GPIO.output(25, True)
        time.sleep(2)
        GPIO.output(25, False)
        print("True")

        # Write data in data_json
        try:
            with open("fetch/data_json", "rt") as file:
                data = json.load(file)
        except IOError:
            data = {}

        if 'plants' not in data:
            data['plants'] = []

        str_pos = str(str(int(x)) + ',' + str(int(y)))
        data['plants'].append({
            'position' : str_pos,
            'to_water' : '0',
            'picture_path': "../fetch/pics/photo_" + str(nb_photo) + ".jpg"
        })

        with open("fetch/data_json", "wt") as outfile:
            json.dump(data, outfile)

        # Write data in map.capture_init
        overwrite_mapinit(int(x), int(y))
    else:
        print("FALSE")
    nb_photo += 1

init_angle = get_angle()
tunny_right = 0
move_centimeter(100)
time.sleep(2)
turn(-3.14/2)
tunny_right = 1
move_centimeter(100)

