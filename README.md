# URLShortener
Yet another implementation of the classical URL Shortener.

## How to use it
```
python server/rest.py --configuration-file <path-to-file>
```
`rest` folder contains a `configuration.ini` file with a sample configuration.

`FastAPI` generates a swagger interface that can be accessed in `localhost:port`. 

## Containerization
TODO

## Available storage methods

### Filesystem
Meant for testing purposes. Stores all entries in a file.

### Redis
TODO


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