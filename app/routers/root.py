from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping() -> dict:
    """간단한 헬스체크 엔드포인트

    Returns:
        dict: {"message": "pong"}
    """
    return {"message": "pong"}
