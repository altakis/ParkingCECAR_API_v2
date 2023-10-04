CORS_ALLOW_ALL_ORIGINS = (
    True  # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]  # If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`
CORS_ALLOWED_ORIGIN_REGEXES = [
    "http://localhost:8000",
]