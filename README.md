# URLShortener
Yet another implementation of the classical URL Shortener.

## How to use it
```
python server/rest.py --configuration-file <path-to-file>
```
`rest` folder contains a `configuration.ini` file with a sample configuration.

`FastAPI` generates a swagger interface that can be accessed in `localhost:port`. 

## Containerization
Run `docker build -t shortener .` in the root of the repository.

Then `docker run shortener p port:port` should do the trick

## Available storage methods

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
Redis will convert all the URLs to numbers in base `pool_size`. Each number will belong to a bucket `num // bucket_size`. This will allow the shortener to easily find available short URLs.


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