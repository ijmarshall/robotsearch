#!/bin/bash
MODEL_PATH="$(pwd)/robotsearch/data"
docker run --name "robotsearch" --volume ${MODEL_PATH}:/var/lib/deploy/robotsearch/data  -d --restart="on-failure" -p 127.0.0.1:5050:5000 -e LANG=C.UTF-8 robotsearch
