# Elasticsearch Snack

A search engine project based on Elasticsearch, Python and Docker, for academic demonstrative use, to scrap, index and search on a collection of snack cooking recipes. 



## Description

The practical objective of this project is to access online to cooking recipes and store them in Elasticsearch for searching purpose.

So firstly we scrap data from the web [Allrecipes](https://www.allrecipes.com), limiting our scope to the snacks category. To index them, we create a strict schema; or mapping, in Elasticsearch argot; so that we can make sure that data is being indexed in correct format and type. For the above steps we are going to use our `scrapper.py` module, which correctly prepare the information into JSON format to easily manage it with Elasticsearch. We also need to use the `elasticsearch_manager.py` module, which contains functionalities to use our Elasticsearch "local" server.

Then we can play searching things in our search engine. To do it (and all of the above steps) easily you can use a TUI (terminal user interface), that will guide you in the process. It is written in the `tui.py` module.

We can search:

- By the title of the recipe.
- By the used ingredients.

With the above options, Elasticsearch is going to match and order the potential recipes that is going to show to us.

Bu we also can use a filter, in this case with the number of calories of the recipe. With this, Elasticsearch strictly filters recipes that exceeds this calories limit and won't show it to us.

All the modules are stored into the Python package `elasticsearch_snack`.



## Set up the project environment

The only one dependency for this project is to have Docker installed in your machine, so all the processes run into Docker containers. See the official [Docker installation instructions](https://docs.docker.com/engine/install).


### Project server

First, you need to pull the Elasticsearch official dockerization:

```sh
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```

The second step is to create a Docker network to connect our two containers. You can do ir as:

```sh
docker network create elasticsearch-snack
```

Then, to run a Docker container with an Elasticsearch execution you have to order:

```sh
docker run --rm -d --net elasticsearch-snack -p 9200:9200 -e "discovery.type=single-node" --name elasticsearch-snack-server docker.elastic.co/elasticsearch/elasticsearch:7.7.0
```

With this an Elasticsearch engine will be running on your local machine and you will can access it with the port 9200. Warning: the host of this server will be `elasticsearch-snack-server` (on the net `elasticsearch-snack`) and not the `localhost` one.


### Project client

On the other hand, this project implements a client for the management and use of the Elasticsearch server.

Firstly you have to build the client dockerization, customized for this project. To do it, run:

```sh
docker build . -f ./client.dockerfile -t elasticsearch-snack-client
```

Now you can start a container with the necessary stuff to work against our Elasticsearch server. Use:

```sh
docker run --rm -it --net elasticsearch-snack --name elasticsearch-snack-client elasticsearch-snack-client
```

### All the above in one command

```sh
# "Install docker" && \ 
# cd <project-directory> && \
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.7.0 && \
	docker network create elasticsearch-snack && \
	docker run --rm -d --net elasticsearch-snack -p 9200:9200 -e "discovery.type=single-node" --name elasticsearch-snack-server docker.elastic.co/elasticsearch/elasticsearch:7.7.0 && \
	docker build . -f ./client.dockerfile -t elasticsearch-snack-client && \
	docker run --rm -it --net elasticsearch-snack --name elasticsearch-snack-client elasticsearch-snack-client
```



## Use

When you run the last command of the set up instructions, to run the client container (i.e.: `docker run --rm -it --net elasticsearch-snack --name elasticsearch-snack-client elasticsearch-snack-client`) a prompt of the virtual machine appears in your terminal. You simply need to start the application as Python default way. I.e.:

```sh
python -m elasticsearch_snack
```

The TUI starts and helps you to go on.



## Uninstall

With these installation steps, you only will have to stop the Docker containers and remove the two images to clean everything of your machine.
