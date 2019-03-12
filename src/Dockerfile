FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get upgrade -y

ENV TZ=Europe/Amsterdam

RUN apt-get install -y python-dev software-properties-common wget vim
RUN apt-get install -y build-essential cmake gfortran git pkg-config
RUN apt-get autoremove -y

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libopencv-dev
RUN apt-get install -y --no-install-recommends libboost-all-dev doxygen
RUN apt-get install -y libatlas-base-dev libopenblas-dev libgphoto2-dev libeigen3-dev libhdf5-dev
RUN apt-get install -y python3-dev python3-pip python3-nose python3-numpy python3-scipy
RUN apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev libblas-dev

RUN pip3 install pandas scikit-image imutils six numpy
RUN pip3 install tensorflow==1.5.0
RUN pip3 install opencv-python==3.4.0.12
RUN pip3 install dlib==19.16.0
RUN pip3 install scipy==1.2.1

RUN mkdir /application
RUN mkdir /base_requerements
COPY ./REQUIREMENTS.txt /base_requerements/
WORKDIR /application
RUN pip3 install --upgrade pip
RUN pip3 install -r /base_requerements/REQUIREMENTS.txt
COPY . /application

WORKDIR /application