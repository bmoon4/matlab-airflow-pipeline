FROM apache/airflow:2.2.4

ARG VERSION="2.2.4"

ARG SUBMODULES="kubernetes"

ARG AIRFLOW_MODULE="apache-airflow[${SUBMODULES}]==${VERSION}"

RUN pip install --no-cache-dir "${AIRFLOW_MODULE}"

USER airflow
