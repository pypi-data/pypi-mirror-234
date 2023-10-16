test_api_doc = {
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": {"Status": "Working"}}},
    }
}

sample_api_doc = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "status": "Success",
                    "status_code": 200,
                    "message": "No Exception",
                    "data": 1,
                }
            }
        },
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {"detail": "Cannot divide by Zero"}
            }
        },
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "status": "Failed",
                    "status_code": 404,
                    "message": "Data Not Available",
                    "data": [],
                }
            }
        },
    },
    401: {
        "description": "HTTP_401_Unauthorized",
        "content": {
            "application/json": {"example": {"detail": "Not authenticated"}}
        },
    },
}
