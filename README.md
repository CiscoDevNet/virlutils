# virl_cli

## Local Development

To easily get started, you can run this inside a docker container like so:

```
docker run --rm -it -v "$(pwd):/home" --workdir /home python:2.7 /bin/bash
root@ab89db25addf:/home# python setup.py install
....
root@ab89db25addf:/home# virl
```
