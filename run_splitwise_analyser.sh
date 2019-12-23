#!/bin/bash

docker build -t splitwise_88_chemin .

docker run -it --rm -v $(pwd):/usr/src/app -p 5000:5000 splitwise_88_chemin
