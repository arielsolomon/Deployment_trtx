#!/usr/bin/env python
import pika
import glob
import os
import time
import random
import sys

sys.path.append('/workspace/Deployment/pre_process/')
from chirp_gen_matlab_to_python import main as chirp_gen

root = '/workspace/Deployment/'
chirp_gen()
file_list = glob.glob(os.path.join(root, '*.png'))
print('File list: ', file_list)
rand_selection = random.choices(file_list, k=1)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()



for file in rand_selection:
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=file)
    time.sleep(2)

connection.close()
