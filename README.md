## build cmd

```
docker run --privileged --cap-add=ALL -v /proc:/proc -v /sys:/sys -v $PWD:/build -w /build -it --rm debian:bookworm /bin/sh -c 'apt-get update && apt-get install -y live-build && mkdir .build && touch .build/config && lb build'
```
