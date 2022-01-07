from os import getenv


POSTGRES_HOST=getenv("POSTGRES_HOST", "postgres")
POSTGRES_USER=getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD=getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB=getenv("POSTGRES_DB", "shipments")
