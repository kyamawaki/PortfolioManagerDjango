# option description
# -d : run in the background
# --name X : set the container name to X
# --mount : bind the host's $(PWD)/web directory to /app in the container
# -p : forward host port 3000 to container port 8000
# start the container sleep infinity

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
#echo $SCRIPT_DIR
#exit 0

# run docker container
docker run -d --name django \
  --env-file $SCRIPT_DIR/.env \
  --mount type=bind,source=$SCRIPT_DIR/web,target=/app/ \
  --dns=8.8.8.8 \
  --dns=8.8.4.4 \
  -p 3000:8000 \
  django sleep infinity
#  django python manage.py runserver 0.0.0.0:8000

