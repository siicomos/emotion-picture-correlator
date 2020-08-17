FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# install python
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

# install openface dependencies
RUN apt-get install -y build-essential \
    && apt-get install -y g++-8 \
    && apt-get install -y cmake \
    && apt-get install -y libopenblas-dev \
    && apt-get install -y git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev \
    && apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev

RUN apt-get install wget \
    && apt-get install zip unzip \
    && wget https://github.com/opencv/opencv/archive/4.1.0.zip
RUN unzip 4.1.0.zip

WORKDIR /opencv-4.1.0/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_TIFF=ON -D WITH_TBB=ON .. \
    && make -j2 \
    && make install

WORKDIR /
RUN wget http://dlib.net/files/dlib-19.13.tar.bz2 \
    && tar xf dlib-19.13.tar.bz2
WORKDIR /dlib-19.13/build
RUN cmake .. \
    && cmake --build . --config Release \
    && make install \
    && ldconfig

# optional install boost
RUN apt-get install -y libboost-all-dev

## OpenFace install
ENV OPENFACE_ROOT=/OpenFace
ENV OPENFACE_BUILD=/OpenFace/build
ENV OPENFACE_BIN=/OpenFace/build/bin

# install OpenFace
WORKDIR /
RUN git clone https://github.com/TadasBaltrusaitis/OpenFace.git

# download models
WORKDIR /OpenFace
COPY scripts/download_models.sh /opencv-4.1.0/download_models.sh
RUN chmod +x /opencv-4.1.0/download_models.sh \
    && /opencv-4.1.0/download_models.sh
    
WORKDIR ${OPENFACE_BUILD}
RUN cmake -D CMAKE_CXX_COMPILER=g++-8 -D CMAKE_C_COMPILER=gcc-8 -D CMAKE_BUILD_TYPE=RELEASE .. \
    && make

# clean up
WORKDIR /
RUN rm 4.1.0.zip \
    && rm dlib-19.13.tar.bz2

# install API dependencies
WORKDIR /model_1
COPY requirements.txt /model_1/requirements.txt
RUN pip install -r requirements.txt

# copy API code
COPY . /model_1

# API log level
ENV LOG_LEVEL=DEBUG
# model 1 classifier
ENV MODEL_1_PCA=pca_faces_aur.pkl
ENV MODEL_1_CLF=svm_faces_aur_clf.joblib

ENTRYPOINT [ ]
CMD uvicorn src.app:app --host 0.0.0.0 --port 8080