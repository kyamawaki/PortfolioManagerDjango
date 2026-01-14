# create docker image from DockerFile
docker build -t django .

# docker run
# docker run -d --name django -v $(pwd):/app django sleep infinity
