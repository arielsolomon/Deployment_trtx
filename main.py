import sys
sys.path.append('/workspace/Sat_proj/deployment_pipeline_2__11_07_2022/inference/')
from local_inference import main as lc # model loading script
from PIL import Image
import time
sys.path.append('/workspace/Sat_proj/deployment_pipeline_2__11_07_2022/post_process_data_extraction/')
from extract_time_frequency import main as et
import pandas as pd
sys.path.append('/workspace/Sat_proj/deployment_pipeline_2__11_07_2022/pre_process/')
from Signal_stft import calc_stft as st
from read_bin import read_file as rf

def main():

    start = time.time()
    """ this should be replaced by 2 stages
        1. Receiving the raw signal
        2. calculating STFT
        3. producing image from STFT
        Two stages because section 2 and 3 are in the same block"""
    img_path = '/workspace/Sat_proj/deployment_pipeline_2__11_07_2022/inference/models/spectrogram_42.png'
    # bin_file = '/workspace/Sat_proj/deployment_pipeline/bin_example_files/12_complex.bin'
    img = Image.open(img_path) # at this stage this is the input,
    # file_name = 'bin file path'                                         # will change into loading signal--> stft-->image
    # z = rf(bin_file)
    # img = st(z)
    model = lc()
    inference = model(img)
    data = inference.xywhn[0][:,:6].tolist()
    # Todo: seperate the chirps if more than single cluster
    output = et(data)
    pd.set_option('display.max_columns', None)
    print('\nOutput for this pipeline: \n', output, 'output type: ', type(output))
    print('\nSingle inference: \n', "%.2f" %(time.time()-start), 'Seconds')


if __name__ == '__main__':

    main()


