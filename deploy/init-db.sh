#!/bin/bash
# Se ejecuta una sola vez, en el primer arranque de PostgreSQL.
# Crea las 3 bases de datos que usan los servicios (NocoDB, n8n, Chatwoot).
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE DATABASE nocodb;
	CREATE DATABASE n8n;
	CREATE DATABASE chatwoot;
EOSQL
