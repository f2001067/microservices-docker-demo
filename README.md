# microservices-docker-demo
DigitalOcean Hyderabad Second meetup, July 2016

On a command line session, we must export our DigitalOcean API Token
export DO_TOKEN=<API-TOKEN>

Token can be generated from
https://cloud.digitalocean.com/settings/api/tokens

Once we do this, we can use 'docker-machine' to create a Droplet from
command line. Setting up docker / docker-machine / docker-compose is
beyond the scope of this tutorial

docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=512mb --digitalocean-region=tor1 --digitalocean-private-networking=true --digitalocean-image=ubuntu-14-04-x64 microservices-host

1) For running all microservices on a common docker network, we must create one
docker network create routing-net

From within nginx-routing-demo folder, run
docker-compose run -d

This will start dev, test & nginx Docker containers.
We can check the status of running containers by
docker-compose ps

Also, we can check running statistics using
docker stats

2) For running microservices on different droplets, but with same docker network

Create a Droplet that runs 'consul' service discovery soctware;
docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=512mb --digitalocean-region=tor1 --digitalocean-private-networking=true --digitalocean-image=ubuntu-14-04-x64 consul-host

Select that Droplet as the current 'docker machine'
eval $(docker-machine env consul-host)

Run a 'consul' Docker container
docker run -d --net=host progrium/consul --server -bootstrap-expect 1

Then run individual Droplets for Nginx / dev / test components

Create 'dev' Droplet
docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=512mb --digitalocean-region=tor1 --digitalocean-private-networking=true --digitalocean-image=ubuntu-14-04-x64 --engine-opt="cluster-store=consul://$(docker-machine ip consul-host):8500" --engine-opt "cluster-advertise eth1:2376" dev

Select 'dev' machine
eval $(docker-machine env dev)

Create a Docker 'overlay' network which spans across machines. Before doing this step, we just need to make sure that
the 'consul-host' machine is created and a 'consul' Docker container is running within it
docker network create -d overlay routing-net

It is enough to create 'routing-net' Docker 'overlay' network once on a particular Droplet.
After that whichever Droplet links to the 'consul-host', automatically will be able to see 'routing-net' network

Launch 'dev' Docker container (all dependencies shall be downloaded automatically if this is the first time that we are doing this)
cd nginx-routing-demo && docker-compose -d dev

Create 'test' Droplet
docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=512mb --digitalocean-region=tor1 --digitalocean-private-networking=true --digitalocean-image=ubuntu-14-04-x64 --engine-opt="cluster-store=consul://$(docker-machine ip consul-host):8500" --engine-opt "cluster-advertise eth1:2376" test

Select 'test' machine
eval $(docker-machine env test)
cd nginx-routing-demo && docker-compose -d test

Create 'nginx' Droplet
docker-machine create --driver=digitalocean --digitalocean-access-token=$DO_TOKEN --digitalocean-size=512mb --digitalocean-region=tor1 --digitalocean-private-networking=true --digitalocean-image=ubuntu-14-04-x64 --engine-opt="cluster-store=consul://$(docker-machine ip consul-host):8500" --engine-opt "cluster-advertise eth1:2376" nginx

Select 'nginx' machine
eval $(docker-machine env nginx)
cd nginx-routing-demo && docker-compose -d nginx

Now, just use the Public IP of 'nginx' Droplet and open in browser
http://<nginx-public-ip>/test
http://<nginx-public-ip>/test/colors
http://<nginx-public-ip>/dev
http://<nginx-public-ip>/dev/cities
