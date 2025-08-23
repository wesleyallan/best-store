# Comando para suber o banco de dados

```
docker compose -p beststore-database -f infra/database/compose.yaml up -d
```

# Comando para parar o serviço do banco de dados

```
docker compose -p beststore-database -f infra/database/compose.yaml stop
```

# Comando para destruir serviço do banco de dados

```
docker compose -p beststore-database -f infra/database/compose.yaml down
```
