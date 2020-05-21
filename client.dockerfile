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

# Install Python Elasticsearch 7.7.0 manager
RUN pip install elasticsearch==7.7.0

# Copy necessary stuff from local
ADD . $WORKDIR

CMD ["/bin/bash"]
