FROM pypy:latest
WORKDIR /usr/src/app
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install firefox
RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

# Download and geckodriver
RUN wget -qO- https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /bin
CMD [ "pypy3", "-u", "./main.py", "|", "tee", "logs/log_$(date +\"%m-%d-%Y_%H-%M-%S\").log" ]
