# Mini FastApi Gateway

FastAPI Gateway is a user-friendly microservices gateway built on the FastAPI framework, employing the same syntax for endpoint definitions. Its primary objective is to streamline the process of defining endpoints for microservices within a database and subsequently utilizing them within a gateway.

At present, the gateway exclusively supports the definition of endpoints within a database and their utilization within the gateway. However, future enhancements are planned to enable the extraction of endpoints from files for use within the gateway.

## Installation

```bash
pip install mini-fastapi-gateway
```

## Usage

### Set environment variables

```TEXT
GATEWAY_DB_URL=postgresql://user:password@localhost:5432/db_name
```

### Use GatewayRouter instead of FastApi in your main file

```python
from gateway import GatewayRouter, gateway_crud_router

app = GatewayRouter()

app.include_router(gateway_crud_router)

```

### Make migrations

```bash
gateway-migrate
```

### Now you can use your dynamic gateway
