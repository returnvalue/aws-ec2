#!/bin/bash
echo "Hello from LocalStack Web Server!" > index.html
python3 -m http.server 80 &
