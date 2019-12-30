#!/bin/bash
docker run \
	--rm \
	--env-file "./env.sh" \
	-v "$PWD":"/home/jovyan/work" -w "/home/jovyan/work" \
	--entrypoint "./_entrypoint.sh" \
	-it \
	jupyter/scipy-notebook
