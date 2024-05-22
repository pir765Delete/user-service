DATABASE_CONFIG = {
    "connections": {"default": "postgres://postgres:8s8wxa@localhost:5433/user_service_db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
