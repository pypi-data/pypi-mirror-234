# Stage 1: Builder/Compiler
FROM python:3.8-slim as builder
ARG GH_ACCESS_TOKEN
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc git

COPY src/requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

RUN pip install --no-cache-dir --user -e "git+https://$GH_ACCESS_TOKEN@github.com/aixplain/aixplain-models-internal.git@master#egg=model_interfaces"

# Stage 2: Runtime
FROM nvidia/cuda:11.3.0-cudnn8-runtime-ubuntu20.04
ARG ASSET_URI

RUN DEBIAN_FRONTEND=noninteractive apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
    apt install --no-install-recommends -y build-essential software-properties-common git && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.8 python3-distutils && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local/lib/python3.8/site-packages /usr/local/lib/python3.8/dist-packages
COPY --from=builder /src/aixplain-models /src/aixplain-models

RUN mkdir /code
RUN mkdir /$ASSET_URI

WORKDIR /code
COPY src /code
COPY $ASSET_URI/. /$ASSET_URI/

RUN chmod +x /code/bash.sh
RUN ./bash.sh

CMD python3.8 -m model
EXPOSE 8080