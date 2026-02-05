# option description
# -d : run in the background
# --name X : set the container name to X
# --mount : bind the host's $(PWD)/web directory to /app in the container
# -p : forward host port 3000 to container port 8000
# start the container sleep infinity
 
# run docker container
docker run -d --name django \
  --env-file .env \
  --mount type=bind,source=$(pwd)/web,target=/app/ \
  -p 3000:8000 \
  django sleep infinity
#  django python manage.py runserver 0.0.0.0:8000

