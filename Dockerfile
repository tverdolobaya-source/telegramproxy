FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install buildozer cython==0.29.33

WORKDIR /app

COPY . /app

CMD ["buildozer", "android", "debug"]
