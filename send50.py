#!/usr/bin/env python
import glob
import os
import time
import random
import sys
import pika
import time

sys.path.append('/work/Deployment_trtx/pre_process/')
from chirp_gen_matlab_to_python50 import main as chirp_gen

root = '/work/Deployment_trtx/data/images/'
chirp_gen()
file_list = glob.glob(os.path.join(root, '*.png'))
print('\nFile list loaded fine: \n')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

for file in file_list:
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=file)
    time.sleep(5)
print(f'Processing and saving files took {round(time.time()-start, 2)} second(s)')
connection.close()
