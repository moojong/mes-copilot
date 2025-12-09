from fastapi import FastAPI

app = FastAPI(title="MES Copilot API")


@app.get("/", response_model=str)
def read_root() -> str:
    """루트 엔드포인트

    MES Copilot 서비스의 루트 엔드포인트입니다. GET 요청 시
    "MES Copilot" 문자열을 반환합니다.

    Returns:
        str: 항상 "MES Copilot" 문자열을 반환합니다.

    Raises:
        없음
    """
    return "MES Copilot"
