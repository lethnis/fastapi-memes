# fastapi-memes

s3 команды
создаю сервер
9000 для апи
9001 для веб клиента
docker run -p 9000:9000 -p 9001:9001 -it --rm quay.io/minio/minio server /data --console-address ":9001"

docker exec -it container_name bash
mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc mb myminio/fromcon
mc admin policy create
