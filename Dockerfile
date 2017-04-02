FROM python:3.6-slim
MAINTAINER Harvard Unviersity Faculty of Arts and Sciences Research Computing

# Install requirements
ADD requirements.txt /tmp/requirements.txt
RUN BUILDDEPS="gcc libc6-dev libssl-dev" \
    && set -x \
    && apt-get update && apt-get install -y $BUILDDEPS --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r /tmp/requirements.txt \
    && apt-get purge -y --auto-remove $BUILDDEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Developement
RUN pip install ipython

# Copy code base
RUN mkdir /source
ADD . /source
WORKDIR /source

# Command
ENTRYPOINT ["scrapy"]
CMD ["crwal", "public-wpdocs"]
