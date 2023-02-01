#!/usr/bin/env python
import pika
import glob
import os
import time
import random
import sys
import concurrent.futures

sys.path.append('/workspace/Deployment/pre_process/')
from chirp_gen_matlab_to_python50 import main as chirp_gen

root = '/workspace/Deployment/data/images/'
chirp_gen()
file_list = glob.glob(os.path.join(root, '*.png'))
print('File list loaded fine: ')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
start = time.perf_counter()

def run_quene(file):
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=file)
    time.sleep(2)
with concurrent.futures.ProcessPoolExecutor() as executer:
    executer.map(run_quene, file_list)
finish = time.perf_counter()
print(f'Processing and saving files took {round(finish-start, 2)} second(s)')
connection.close()