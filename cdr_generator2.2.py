import boto3
import logging
from logging.handlers import WatchedFileHandler
import datetime
from datetime import tzinfo
from pytz import timezone
import pytz
import random
import string
import time
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler
import os
from threading import Thread
import shutil


logger = logging.getLogger()
log_level = logging.DEBUG

logFormatter = logging.Formatter("%(message)s")

handler = WatchedFileHandler("/home/mike/My_projects/Master.csv")
handler.setFormatter(logFormatter)
handler.setLevel(log_level)
logger.addHandler(handler)
logger.setLevel(log_level)

s3client = boto3.resource("s3")

s3_bucket = 'h2o-hydrant-test'

count = 0

def rotate_and_upload():
    try:
        #print("Try block...")
        if os.stat("/home/mike/My_projects/Master.csv").st_size > 0:
            print("In with ")
            time = str(datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d_%H-%M-%S"))
            shutil.move("/home/mike/My_projects/Master.csv", "/home/mike/My_projects/Master.csv"+time)
            print("shutil.move: " + str(shutil.move))
            s3client.meta.client.upload_file("/home/mike/My_projects/Master.csv"+time, s3_bucket, "Master.csv"+time)
            #print("This is rotate and upload logs")
    except Exception as e:
        print(e)


def generate_one_call(duration=1):
    end_time = datetime.datetime.now(pytz.utc)
    start_time = end_time - datetime.timedelta(seconds=duration)
    track_id = ''.join(random.choices(string.ascii_letters + string.digits, k=36))
    b_leg_uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=35))
    #print("This is One Call function...")
    # Ext 1026 call Ext 402
    # write B leg
    logger.debug('"10","","call-devint","i-0a299ec207ef9bbfa","10.203.135.91","' + str(
        track_id) + '","400045","BS00=502648|UX40=503189","Lun Li","1026","VH2848","account-400045","' + str(
        start_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(start_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(
        end_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(duration) + '","' + str(
        duration) + '","NORMAL_CLEARING","' + str(b_leg_uuid) + '","","400045","","","","' + str(
        track_id) + '","1026","VH2848","' + str(duration * 1000) + '","' + str(
        duration * 1000) + '","85d00112-1297-1236-9480-06f01c62b29c","","","","device","device","","","VH2845","1026","VH2848","402","402"')
    #print("One call logger.debug: " + str(logger.debug))
    # write A leg
    logger.debug(
        '"10","","call-devint","i-0a299ec207ef9bbfa","10.203.135.91","' + str(track_id) + '","400045","BS00=502648|UX40=503189","Lun Li","1026","402","account-400045","' + start_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + start_time.strftime("%Y-%m-%d %H:%M:%S") + '","' + end_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + str(duration) + '","' + str(
            duration) + '","NORMAL_CLEARING","' + str(track_id) + '","'+ str(b_leg_uuid)+'","400045","","","","","VH2845","402","' + str(
            duration * 1000) + '","' + str(
            duration * 1000) + '","85d00112-1297-1236-9480-06f01c62b29c","","","","device","device","","","VH2845","1026","","402","402"')


def generate_one_VR_to_VM_call(duration=1):
    end_time = datetime.datetime.now(pytz.utc)
    start_time = end_time - datetime.timedelta(seconds=duration)
    track_id = ''.join(random.choices(string.ascii_letters + string.digits, k=36))
    b_leg_uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=35))
    #print("This is VR function...")
    
    # Ext 1026 call Ext 402
    # write B leg
    logger.debug('"10","","call1","-0d3534c8ec06ae108","10.202.136.57","' + str(
        track_id) + '","730378","BS00=1274074|AA00=1274076|CCR-D50=1664871","VONAGE","18482197282","14245329556","account-730378","' + str(
        start_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(start_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(
        end_time.strftime("%Y-%m-%d %H:%M:%S")) + '","' + str(duration) + '","' + str(
        duration) + '","NORMAL_CLEARING","' + str(b_leg_uuid) + '","","730378","VH2848","","","' + str(
        track_id) + '","","","' + str(duration * 1000) + '","' + str(
        duration * 1000) + '","85d00112-1297-1236-9480-06f01c62b29c","vr|ccr|vm","","","device","device","","","18482197282","14245329556","18482197282","14245329556","402"')
    #print("One VR call logger.debug: " + str(logger.debug))
        # write A leg
    logger.debug(
        '"10","","call1","i-0d3534c8ec06ae108","10.202.136.57","' + str(track_id) + '","730378","BS00=1274074|AA00=1274076|CCR-D50=1664871","VONAGE","18482197282","VH886441","account-730378","' + start_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + start_time.strftime("%Y-%m-%d %H:%M:%S") + '","' + end_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + str(duration) + '","' + str(
            duration) + '","UNALLOCATED_NUMBER","' + str(track_id) + '","'+ str(b_leg_uuid)+'","730378","","","","","","","' + str(
            duration * 1000) + '","' + str(
            duration * 1000) + '","85d00112-1297-1236-9480-06f01c62b29c","vr|ccr","","","carrier","device","","","","VH886441","","410","18482197282"')

        # write F leg
    logger.debug(
        '"10","","call1","i-0d3534c8ec06ae108","10.202.136.57","' + str(track_id) + '","730378","BS00=1274074|AA00=1274076|CCR-D50=1664871","VONAGE","18482197282","feature-voicemail-put","account-730378","' + start_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + start_time.strftime("%Y-%m-%d %H:%M:%S") + '","' + end_time.strftime(
            "%Y-%m-%d %H:%M:%S") + '","' + str(duration) + '","' + str(
            duration) + '","NORMAL_CLEARING","' + str(track_id) + '","'+ str(b_leg_uuid)+'","730378","feature-voicemail-put","","","","","","' + str(
            duration * 1000) + '","' + str(
            duration * 1000) + '","85d00112-1297-1236-9480-06f01c62b29c","vr|ccr|vm","","","carrier","feature","","","","VH886441","","410","18482197282"')


sched = BackgroundScheduler()
sched.add_job(rotate_and_upload, 'cron', second=0)
sched.start()

start_time = time.time()
for timer in range(600):
    print("This is timer: " + str(timer))
    end_time = time.time()
    print("Loop time was: " + str(end_time - start_time) )
    
    for i in range(400):
        
        print("This is i: " + str(i))
        generate_one_call(duration=2)
        #print("This is is one call fuction.."  + str(generate_one_call(duration=2)))
        generate_one_VR_to_VM_call(duration=2)
        #print("This is calling the generate_one_VR_to_VM_call..: " + str(generate_one_VR_to_VM_call(duration=2)))
        count = count + 1
        
    time.sleep(0.9)

time.sleep(60)

print("Total calls = " + str(count))


