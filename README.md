# Search engine

A search engine project based on Elasticsearch for academic demonstrative use. 



## Use

The only one dependency for this project is to have Docker installed in your machine, so all the processes run into Docker containers. See the official [Docker installation instructions](https://docs.docker.com/engine/install).


### Project server

First, you need to pull the Elasticsearch official dockerization:

```sh
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```

Then, to run a Docker container with an Elasticsearch execution you have to order:

```sh
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```

With this an Elasticsearch engine will be running on your local machine and you will can access it with the port 9200. You can test it using a browser and going to the url `http://localhost:9200`.


### Project client

On the other hand, this project implements a client for the management of the Elasticsearch server.

Firstly you have to build the client dockerization. To do it, run:

```sh
docker build . -f ./client.dockerfile -t elasticsearch-client
```

Now you can start a container with the necessary stuff to work against our Elasticsearch server. Use:

```sh
docker run -ti elasticsearch-client
```


## Uninstall

With these installation steps, you only will have to stop the Docker containers and remove the two images to clean everything of your machine.
