FROM jjanzic/docker-python3-opencv

WORKDIR /
ENV CV2_CASCADE_FILE_PATH="/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
RUN apt-get update
RUN apt-get install git
RUN git clone https://github.com/marutaku/BadManChecker.git
WORKDIR /BadManChecker
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
RUN pip install Pillow h5py
RUN mkdir img

CMD python server.py $PORT



