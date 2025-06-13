# Setting up Airflow on Windows with Docker Desktop

---

## Installation

Fetch the `docker-compose.yaml` file.

```bash
Invoke-WebRequest -Uri "https://airflow.apache.org/docs/apache-airflow/2.10.3/docker-compose.yaml" -OutFile "docker-compose.yaml"
```

Make the necessary folders

```bash
mkdir .\dags, .\logs, .\plugins, .\config
```

Initialize the DB

```bash
docker compose up airflow-init
```

Run airflow

```bash
docker compose up -d
```

To run using Dockerfile, use

```bash
docker compose up --build -d
```

Go to localhost:8080, login with user `airflow` and password `airflow`.

To enable flower, do

```bash
docker compose --profile flower up -d
```

To stop all containers, including flower, do

```bash
docker compose --profile flower down
```

## Installing sklearn inside container

```bash
docker exec -it mlops_project-airflow-scheduler-1 bash  
pip install scikit-learn
cd DVC
dvc --version 
pip install dvc # if not installed
dvc remote list # check remote
pip install dvc-gdrive
exit

docker exec -it mlops_project-airflow-worker-1 bash 
pip install scikit-learn
cd DVC
dvc --version 
pip install dvc # if not installed
dvc remote list # check remote
pip install dvc-gdrive
exit

docker-compose restart airflow-scheduler
docker-compose restart airflow-worker
docker-compose restart airflow-webserver
```

## Installing Git

```bash
docker exec -it --user root mlops_project-airflow-worker-1 bash
apt-get update
apt-get -y install git
```

## Remove/Delete all containers

In case if one or more containers status is constanlty `unhealthy`, try removing all containers from the development machine and try creating them again using `docker compose up -d`. To remove all containers, run, 

```bash
docker rm -v $(docker ps --filter status=exited -q)
docker rm -v -f $(docker ps -qa)
```

## Check logs of Docker container

```bash
docker logs mlops_project-airflow-scheduler-1
docker logs mlops_project-airflow-worker-1    
```

## Run DVC without SCM

```bash
dvc config core.no_scm true
```

## Minikube

```bash
kubectl run -i --tty debug --image=busybox --restart=Never -- sh

nslookup mongodb.default.svc.cluster.local
nslookup <service-name>.<namespace>.svc.cluster.local # nslookup mongodb.default.svc.cluster.local
ping mongodb.default.svc.cluster.local

exit
```

To access the app through web browser, run

```bash
minikube service flask-app 
```

To get only the url of the running app, run

```bash
minikube service flask-app --url  
```

## Managing Branches

```bash
git checkout -b feature/feature_name
git add file_name
git commit -m "commit message"
git push -u origin feature/feature_name
```

To delete the local branch, run:
```bash
git branch -d feature/dvc-airflow 
```

To delete the branch from the remote repository (e.g., GitHub), run:
```bash
git push origin --delete feature/dvc-airflow
```

## Medium Blog
https://medium.com/@syeda.areeba.nadeem/from-data-to-deployment-implementing-mlops-with-airflow-dvc-mlflow-and-kubernetes-6b2df084afba
