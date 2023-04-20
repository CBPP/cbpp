## cbpp
# #!++, A CrunchBang revival project.

In 2015, Philip Newborough -- Corenominal -- had officially discontinued his efforts with the fast and light distro. While Philip believes that the project no longer serves the Linux space in the way he had originally intended, we believe that #! still has great potential and serves the Linux community as the perfect combination of elegance and efficiency.

While we intend to keep the distro very much the same as it has been over the years, some changes must be made to adapt to newer dependencies. Most notably, #!++ will have a new gtk3 theme and a new default iconset using the faenza-crunchbang-icon-theme package.

A few more changes have been made under the hood over the years with the advent of systemd, the deprecation of slim and some userspace utilities, the changes to gtk-3.0 and soon gtk-4.0, but the original experience is largely unchanged.

Lastly, we'd like to thank Philip for all his hard work through the years, the legacy he's created, and the bar he's set for sleek high-performance distros.

### The ISO

In this repository, you'll find the sources used to generate the actual system image, with installer, along with some configurations.

### Building

While you can certainly build the iso natively, it's easiest and very tidy to use docker, as below.

```
$ docker run --privileged --cap-add=ALL -v /proc:/proc -v /sys:/sys -v $PWD/amd64:/build -w /build -it --rm debian:bookworm /bin/sh -c 'apt-get update && apt-get install -y live-build && mkdir .build && touch .build/config && lb build'
```

If you don't want to run docker, you can run the same commands that get passed to the shell (as root, or with sudo):

```
# apt-get update && apt-get install -y live-build && cd amd64 && mkdir .build && touch .build/config && lb build
```

### Packages

For the most part, CBPP is just a thin layer of configuration files added on top of Debian Stable. However, we do package those files for distribution. While the packages have been made available at several URLs over the years, you can currently find them at:

- Committed in binary form at [CBPP/crunchbangplusplus.org/packages](https://github.com/CBPP/packages.crunchbangplusplus.org)
- Hosted for consumption via apt at [crunchbangplusplus.org/packages](crunchbangplusplus.org/packages) though not browseable in the web browser(yet)

### Package Sources

All of the sources for CBPP's custom packages are available here on Github

- todo

