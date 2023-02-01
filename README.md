# Deployment
pip3 install requirements.txt
run MQ server as follow: docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
run your application server, I use ngc torch: docker run --network=host  -it --rm -v /your_local_dir:/workspace nvcr.io/nvidia/pytorch:21.09-py3
run on 2 seperate terminals
on one, run receive, on the other send. In the future, the send should be attach to sensor that sends signal that will be processed into image
Also the output should be directed to the client

For Jetson Orin:
torch docker: nvcr.io/nvidia/l4t-pytorch:r35.1.0-pth1.12-py3
Docker runx2: docker run   -it --rm --runtime nvidia --network host -v /home/nvidia/ariel:/workspace -w '/workspace/Deployment/' nvcr.io/nvidia/l4t-                     pytorch:r35.1.0-pth1.12-py3
pip3 install -r requirments
python3.  send50.py
python3. receive50.py
