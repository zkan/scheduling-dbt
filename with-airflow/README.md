# Scheduling dbt with Airflow

```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```bash
make up
```

### Postgres Connection

```
Connection Name: `example_db`
Connection Type: `Postgres`
Host: `db`
Schema: `greenery`
Login: `postgres`
Password: `postgres`
Port: `5432`
```