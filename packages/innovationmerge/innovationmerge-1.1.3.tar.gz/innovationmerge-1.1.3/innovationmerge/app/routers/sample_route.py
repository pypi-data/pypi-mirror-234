from fastapi import HTTPException, APIRouter, status, Response, Depends
from innovationmerge.app.schemas.sample_schema import SampleItem
from innovationmerge.docs.api_doc import sample_api_doc
from innovationmerge.app.sample import sample_division
from innovationmerge.app.schemas.user_schema import User
from innovationmerge.app.security import get_current_active_user

router = APIRouter()


@router.post("/sample_api", responses=sample_api_doc)
async def sample_api_function(
    response: Response,
    sample_item: SampleItem,
    current_user: User = Depends(get_current_active_user)
):
    try:
        result = sample_division(sample_item.val1, sample_item.val2)
        status_data = {
            "status": "Success",
            "status_code": status.HTTP_200_OK,
            "message": "No Exception",
            "data": result,
        }
        response.status_code = status.HTTP_200_OK
    except Exception as e:
        if type(e).__name__ == "ZeroDivisionError":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot divide by Zero"
            )
        else:
            status_data = {
                "status": "Failed",
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "Data Not Available",
                "data": [],
            }
            print(type(e).__name__)
            response.status_code = status.HTTP_404_NOT_FOUND
    return status_data
