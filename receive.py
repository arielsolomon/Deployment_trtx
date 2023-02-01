#!/usr/bin/env python
import pika, sys, os

sys.path.append('/workspace/Deployment/inference/')
from local_inference import main as lc  # model loading script
from PIL import Image
import time

sys.path.append('/workspace/Deployment/post_process_data_extraction/')
from extract_time_frequency import main as et
import pandas as pd



# from Signal_stft import calc_stft as st
# from read_bin import read_file as rf

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    model_path = '/workspace/Deployment/inference/models/epoch2500_SGD_BIG_dataset_best_model.pt'
    model = lc(model_path)

    def callback(ch, method, properties, body, model=model):
        start = time.time()
        body = body.decode('UTF-8')
        print('Body: ', body)
        img = Image.open(body)
        print('\nImage loaded')
        inference = model(img)
        print('\nSucess inference', inference)
        data = inference.xywhn[0][:, :6].tolist()
        print('\nData: ', data)
        output = et(data)
        pd.set_option('display.max_columns', None)
        print('\nOutput for this pipeline: \n', output, 'output type: ', type(output))
        print('\nSingle inference: \n', "%.2f" % (time.time() - start), 'Seconds')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    # print('\nWaiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
