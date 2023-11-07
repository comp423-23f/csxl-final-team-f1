from fastapi import Request
from fastapi.responses import JSONResponse


# This variable is exposed for consumption in `backend/main.py`. It captures tuples
# of Feature-specific Exception and corresponding Exception Handler for HTTP Error purposes.
