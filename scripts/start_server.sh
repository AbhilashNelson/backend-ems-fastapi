#!/bin/bash
cd /home/ec2-user/backend
nohup gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000 > gunicorn.log 2>&1 &