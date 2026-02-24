from fastapi import Request

def log_request(request: Request) -> None:
    print(f"[LOOOOOGIIIINN] {request.method}{request.url}")