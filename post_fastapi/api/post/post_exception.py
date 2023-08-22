from fastapi.responses import JSONResponse


def integrity_exception_handler(request, exc):
    message = "UNIQUE constraint failed"
    return JSONResponse(content={"message": message}, status_code=409)
