###########################################################
##
## Search engine client dockerization
##
## Copyright 2020 Borja González Seoane
##
## This dockerfile builds an image with Python 3.7 and
## the project stuff necessary to work against an
## Elasticsearch server.
##
###########################################################

FROM python:3.7

MAINTAINER Borja González Seoane <borja.gseoane@udc.es>

WORKDIR $HOME/work/

# Copy necessary stuff from local
ADD . $WORKDIR

# Install all the neccesary Python libraries. One is Elasticsearch 7.7.0
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
