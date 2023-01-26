# Scheduling dbt with Airflow

## Getting Started

To set up Airflow:

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```bash
make up
```

To set up a Postgres Connection, use the information below:

- Connection Name: `example_db`
- Connection Type: `Postgres`
- Host: `db`
- Schema: `greenery`
- Login: `postgres`
- Password: `postgres`
- Port: `5432`
