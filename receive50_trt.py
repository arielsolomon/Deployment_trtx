#!/usr/bin/env python
import pika, sys, os
import torch
import shutil

sys.path.append('/work/Deployment_trtx/tensorrtx/yolov5/')
from yolov5_trt_accuracy import run1 as lc  # model loading script
from PIL import Image
import time
import pandas as pd
import ctypes

sys.path.append('/work/Deployment_trtx/post_process_data_extraction/')
from extract_time_frequency import main as et

sys.path.append('/work/Deployment_trtx/')
from yolov5_trt_accuracy import inferThread as it


# from Signal_stft import calc_stft as st
# from read_bin import read_file as rf
def avr_time(time_list):
    return sum(time_list) / len(time_list)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model.to(device)

    def callback(ch, method, properties, body, inf_net_time_all=[]):
        inf_net_time_all = []
        after_load_time = []
        start = time.time()
        body = body.decode('UTF-8')
        print('Output (only body in image open) is: ', body)
        net_img_load_inference = time.time()
        lc(body)
        after_load_time.append(inf_time)
        #data = inference.xywhn[0][:, :6].tolist()
        # output = et(data)
        # print('\nOutput: ', output, '\n')
        # pd.set_option('display.max_columns', None)
        # print('\nSingle inference: \n', '%.2f'%(1000*(time.time()) - 1000*(start)), 'ms')
        # if inf_net_time_all[1:] == []:
        #     pass
        # else:
        #      print('image #: ', len(inf_net_time_all[1:]))
        #      print('\nAvr net time for 50 images: ', avr_time(inf_net_time_all[1:]))
        #      print('\nAvr net time for 50 images after loading model: ', avr_time(after_load_time[1:]))
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # print('\nWaiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    print('\n 50 images past: \n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
