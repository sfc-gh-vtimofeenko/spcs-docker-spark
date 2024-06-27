Everything needed to run Spark standalone cluster on Snowpark Container
Services.

This project contains:

- [Spark master dockerfile](./spark-master)
- [Spark worker dockerfile](./spark-worker/)
- [A client container](./sample-client/) with some sample code that exposes shell over a websocket
- [Makefile](./Makefile) to build and push images
- [Instructions](./HOWTO.md) on building and running the service locally and in
  Snowpark Container Services

