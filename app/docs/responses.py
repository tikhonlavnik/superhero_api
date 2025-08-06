from fastapi import status


COMMON_HERO_RESPONSES = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Hero is not found",
        "content": {"application/json": {"example": {"detail": "Hero is not found"}}},
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["query", "power_ge"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ]
                }
            }
        },
    },
}


CREATE_HERO_RESPONSES = {
    **COMMON_HERO_RESPONSES,
    status.HTTP_409_CONFLICT: {
        "description": "This hero is already added",
        "content": {
            "application/json": {"example": {"detail": "This hero is already added"}}
        },
    },
}


GET_HEROES_RESPONSES = {
    **COMMON_HERO_RESPONSES,
    status.HTTP_200_OK: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "name": "Batman",
                        "intelligence": 81,
                        "strength": 40,
                        "speed": 29,
                        "power": 63,
                    }
                ]
            }
        },
    },
}
