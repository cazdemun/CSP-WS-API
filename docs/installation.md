# Package list & commands

# Anaconda

  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  sudo bash Miniconda3-latest-Linux-x86_64

  sudo chown -R charles /home/charles/miniconda3/
  sudo chmod -R +x /home/charles/miniconda3/

## Flask

    conda install -c anaconda flask

## Flask-SocketIO********

    conda install -c conda-forge flask-socketio
    conda install -c anaconda gevent-websocket 
    conda install -c conda-forge eventlet

## Pymongo

    conda install -c anaconda pymongo
    pip/pip3 install pymongo[srv]

## Pymonad

    # conda install -c yikelu pymonad
    pip/pip3 install pymonad
    conda install -c anaconda toolz

# AsyncIO

    pip install asyncio

# Websockets

    pip install websockets

# Quart

    pip install quart

set FLASK_APP=server.py && python -m flask run
python server.py