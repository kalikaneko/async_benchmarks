async-benchmarks
================
Some experiments on pythonic async alternatives

tested software
---------------

Server: a simple web service that queries a couchdb database.

* WSGI (stdlib) 
* WSGI (flask)
* WSGI (tornado)

* WSGI (twisted.web)
* twisted (cpython)
* twisted (pypy, 1 core)
* twisted (pypy-stm, multicore)

TLS benchmark
-------------
* twisted tls with openssl
* nginx tls frontend

Datasets
--------
* Dummy payload: same payload is stored n times. measures insertions.
* Dummy payload: homogeneous payload, random queries.
* Prime-numbers (range):
  - calculates primes in range (cpu-bound load, with i/o step)
  - queries primes in range
* Server search: a string is given to be searched on the whole database.
