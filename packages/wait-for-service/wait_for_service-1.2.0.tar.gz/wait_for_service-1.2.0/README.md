# wait-for-service

Waits for a dependency before continuing. It's meant to be used in startup scripts like Docker's entrypoint.
This project is forked from <http://github.com/wlatanowicz/wait-for-service>

## Installing

```
pip install wait-for-service
```

## Usage

```
wait-for-service dependency-url-1 dependency-url-2 ... dependency-url-n
```

ie:

```
wait-for-service https://my-server/healthz/ psql://user@db-host/db-name
```

# Available checks

## HTTP(s)

HTTP and HTTPS are available by default. Follows redirects; only response with HTTP code 2XX is accepted as valid.

### Accepted URL schemas

* http://
* https://

### Example

```
wait-for-service https://my-server/healthz/ http://my-server/healthz/
```

## PostgreSQL

RDBMS has to accept connection and allow to perform simple SELECT query.

### Installation

```
pip install wait-for-service[postgres]
```

### Accepted URL schemas

* postgres://
* postgresql://
* psql://

### Example

```
wait-for-service psql://admin:password@db-host/db_name
```

## MySQL

RDBMS has to accept connection and allow to perform simple SELECT query.

### Installation

```
pip install wait-for-service[mysql]
```

### Accepted URL schemas

* mysql://

### Example

```
wait-for-service mysql://admin:password@db-host/db_name
```

## Redis

Rdis has to accept connection to selected database (defaults to 0).

### Installation

```
pip install wait-for-service[redis]
```

### Accepted URL schemas

* redis://

### Example

```
wait-for-service redis://redis-host/5
```

## Memcached

Memcached has to accept connection.

### Installation

```
pip install wait-for-service[memcached]
```

### Accepted URL schemas

* memcached://

### Example

```
wait-for-service memcached://memcached-host/
```

## MongoDB

MongoDB has to accept connection.

### Installation

```
pip install wait-for-service[mongodb]
```

### Accepted URL schemas

* mongodb://

### Example

```
wait-for-service mongodb://admin:password@db-host/db_name
```

## RabbitMQ

RabbitMQ has to accept connection to given vhost. You can use optional querystring params `require_queue` and `require_exchange` to additionaly check if particular queue or exchange exists (check will fail otherwise).

### Installation

```
pip install wait-for-service[amqp]
```

### Accepted URL schemas

* amqp://

### Example

```
wait-for-service amqp://admin:password@rabbit-host/vhost
wait-for-service amqp://admin:password@rabbit-host/vhost?require_queue=myqueue
wait-for-service amqp://admin:password@rabbit-host/vhost?require_exchange=myexchange
wait-for-service amqp://admin:password@rabbit-host/vhost?require_exchange=myexchange&require_exchange=mysecondexchange&require_queue=myqueue&require_queue=mysecondqueue
```

## Apache Kafka

Kafka has to accept connection. In HA mode (node count > 1) only one node is required to accept the connection.

### Installation

```
pip install wait-for-service[kafka]
```

### Accepted URL schemas

* kafka://

### Example

```
wait-for-service kafka://kafka-host/
wait-for-service kafka://kafka-first-host/,kafka://kafka-second-host/
```

## TCP

Plain TCP is available by default. Service port is required.

### Accepted URL schemas

* tcp://

### Example

```
wait-for-service tcp://my-server:7624
```

## Unix

Unix sockets are available by default.

### Accepted URL schemas

* unix://

### Example

```
wait-for-service unix:///var/run/docker.sock
```
