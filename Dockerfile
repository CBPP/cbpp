FROM debian:bullseye

ADD live-build_20210216_all.deb /tmp/
RUN apt-get update && apt-get install -y live-build && dpkg -i /tmp/live*.deb
