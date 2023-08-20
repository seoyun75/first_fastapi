from fastapi.responses import PlainTextResponse


def integrity_excption_handler(request, exc):
    return PlainTextResponse(str("UNIQUE constraint failed"), status_code=400)
