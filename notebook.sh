#!/bin/bash
docker run \
	--rm \
	--env-file "./env.sh" \
	-p 8888:8888 \
	-v "$PWD":"/home/jovyan/work" -w "/home/jovyan/work" \
	jupyter/scipy-notebook
