# URLShortener
Yet another implementation of the classical URL Shortener.

## How to use it
```
python -m server.rest --configuration-file <path-to-file>
```
`rest` folder contains a `configuration.ini` file with a sample configuration.

`FastAPI` generates a swagger interface that can be accessed in `localhost:port`. 

## Containerization
Run `docker build -t shortener .` in the root of the repository.

Then `docker run -p port:port shortener` should do the trick

If you want to use a custom configuration file you can do it with

```
docker run -v path/to/file/folder/:/config \
-p port:port \
shortener
```

Make sure your configuration file is named `configuration.ini`

It will overwrite the configuration file right before starting the container

## Available storage methods

URL mappings can either be stored in files or in Redis. Both systems have the following common configuration paramters

```
implementation=redis|files
max_generation_retries=10
url_length=3
url_pool=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
```

Names are kind of self-explanatory I think.

### Filesystem
Meant for testing purposes. Stores all entries in a file.

### Redis
Store all short url mappings in a Redis instance, requires the following configuration parameters
```
host=localhost
port=6379
username=root
password=root
bucket_size=16384
```
Redis will convert all the URLs to numbers in base `pool_size`.

A short url with number `N` will belong to bucket `N // num_buckets`.

If `bucket_size = 128` we will only need to check 128 positions to find a suitable candidate for a new, randomly generated short url.



## Local env
You can make the access to your local shortener service more convenient by changing `/etc/hosts` and using a reverse proxy.

For example, you can access to the service via browser as `s.es` by adding this entry to `/etc/hosts`

```
127.0.0.1 s.es
```

And starting an `nginx` instance with this configuration

```
events {
  worker_connections 1024;
}
http {
 server {
   listen 80;

   server_name s.es;
 
   location / {
       proxy_pass http://localhost:8080;
   }
 }
}
```