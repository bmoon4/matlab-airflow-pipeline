# Dockerfile

```
FROM apache/airflow:2.2.4

ARG VERSION="2.2.4"

ARG SUBMODULES="kubernetes"

ARG AIRFLOW_MODULE="apache-airflow[${SUBMODULES}]==${VERSION}"

RUN pip install --no-cache-dir "${AIRFLOW_MODULE}"

USER airflow
```
# Docker build

```
# docker build -t myImageName:TagName dir
docker build -t bmoon0702/airflow-custom:2.2.4-k8s .
[+] Building 556.2s (8/8) FINISHED
...
...
```

# Docker push

```
matlab-airflow-pipeline on  main [+]
❯ docker push bmoon0702/airflow-custom:2.2.4-k8s
The push refers to repository [docker.io/bmoon0702/airflow-custom]
1157a5eabb8b: Pushed
5f70bf18a086: Layer already exists
98ec9ef0a571: Layer already exists
0aa8958ab0d3: Layer already exists
f219fa6fb690: Layer already exists
ec35a78b3acf: Layer already exists
9d6d109d9533: Layer already exists
8c71c0b029ba: Layer already exists
25b0f678602e: Layer already exists
5d6562ea07fb: Layer already exists
6722e74c53d1: Layer already exists
0e1f1c8f01cf: Layer already exists
65a900eeb209: Layer already exists
8cc37281088b: Layer already exists
f18b02b14138: Layer already exists
2.2.4-k8s: digest: sha256:12a36f78cc1e379ca1b0308d5e85f8f2405ffc94cbd1b05a7c5781ce278527e0 size: 3462
```

# Spin up your airflow with your new docker image

```
helm upgrade --install airflow apache-airflow/airflow --values=values.yaml --namespace airflow --create-namespace
```

```
❯ k get po -n airflow
NAME                                   READY   STATUS              RESTARTS   AGE
airflow-flower-7686758645-lw46n        0/1     ContainerCreating   0          10s
airflow-postgresql-0                   0/1     ContainerCreating   0          10s
airflow-redis-0                        0/1     ContainerCreating   0          10s
airflow-run-airflow-migrations-9vbfw   0/1     ContainerCreating   0          9s
airflow-scheduler-5cb497f658-f5h62     0/2     Init:0/1            0          10s
airflow-statsd-75f567fd86-fxq9c        0/1     ContainerCreating   0          10s
airflow-triggerer-55987478bd-jvnkw     0/1     Init:0/1            0          10s
airflow-webserver-7fddd96fcc-r4rt5     0/1     Init:0/1            0          10s
airflow-worker-0                       0/2     Init:0/1            0          10s
```

# Port-forwarding
```
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```

# check kubernetes installed

```
❯ k -n airflow exec -it airflow-worker-0 -- /bin/bash
Defaulted container "worker" out of: worker, worker-log-groomer, wait-for-airflow-migrations (init)
airflow@airflow-worker-0:/opt/airflow$ pip list | grep kubernetes
apache-airflow-providers-cncf-kubernetes 3.0.2
kubernetes                               11.0.0
```

# Login GUI
url: `localhost:8080`
username: `admin`
password: `admin`


![Screenshot](images/../../images/airflow(1).png)

# Copy dags into scheduler and worker
```
matlab-airflow-pipeline/dags on  main [!+] via 🐍 v3.9.12
❯ k -n airflow cp test.py airflow-scheduler-5cb497f658-f5h62:/opt/airflow/dags/test.py
Defaulted container "scheduler" out of: scheduler, scheduler-log-groomer, wait-for-airflow-migrations (init)

matlab-airflow-pipeline/dags on  main [!+] via 🐍 v3.9.12
❯ k -n airflow cp test.py airflow-worker-0:/opt/airflow/dags/test.py
Defaulted container "worker" out of: worker, worker-log-groomer, wait-for-airflow-migrations (init)
```

```
❯ k -n airflow exec -it airflow-worker-0 -- /bin/bash
Defaulted container "worker" out of: worker, worker-log-groomer, wait-for-airflow-migrations (init)
airflow@airflow-worker-0:/opt/airflow$ ls
airflow-worker.pid  airflow.cfg  config  dags  logs  webserver_config.py
airflow@airflow-worker-0:/opt/airflow$ cd dags
airflow@airflow-worker-0:/opt/airflow/dags$ ls
test.py
```

![Screenshot](images/../../images/airflow(2).png)
