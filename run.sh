docker compose up | tee "logs/log_`date +"%m-%d-%Y_%H-%M-%S"`.log"
docker compose down
