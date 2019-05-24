FROM geographica/gdal2:2.3.1    

# install dependencies    
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends\     
        build-essential \
        software-properties-common \
        python3 \
        python3-dev \
        python3-tk \
        python3-pip \
        build-essential \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        libspatialindex-dev \
        libsm6 \
        vim \
        wget \
        git \
        && \    
    apt-get clean && \    
    rm -rf /var/lib/apt/lists/*


# install python package
RUN pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple setuptools && \
    pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple wheel && \
    pip3 --no-cache-dir install -v fiona==1.8.0 && \
    pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple \
        Pillow \
        numpy \
        gdal \
        ipykernel \
        psycopg2 \
        gunicorn \
        werkzeug \
        gevent \
        shapely \
        rasterio==1.0.8 \
        pyproj \
        geojson \
        geoalchemy2 \
        requests \
        mercantile \
        geopandas \
        argparse \
        torch \
        tifffile \
        torchvision \
        opencv-python \
        scipy 

WORKDIR "/tmp/workdir"

COPY ./ ./

#RUN python3 setup.py install

ENV LANG C.UTF-8


#RUN chmod 777 entrypoint.sh

#CMD ["./entrypoint.sh"]

