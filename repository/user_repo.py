import logging
from typing import Literal, Union, Optional

from fastapi import Depends
from pymongo import ReturnDocument, database

from config.mongodb import getMongoDB
from core.logging import logger
from domain.dto import user_dto
from domain.model import user_model


class UserRepo:
    def __init__(
        self,
        mongodb: database.Database = Depends(getMongoDB),
    ):
        self.users_coll = mongodb[user_model.UserModel()._coll_name]

    def create(self, data: user_model.UserModel):
        self.users_coll.insert_one(data.model_dump())

    def update(
        self, id: str, data: user_model.UserModel
    ) -> Union[user_model.UserModel, None]:
        res = self.users_coll.find_one_and_update(
            {"id": id},
            {"$set": data.model_dump(exclude=["id", "created_at"])},
            return_document=ReturnDocument.AFTER,
        )

        return user_model.UserModel(**res) if res else None

    def patch(
        self, id: str, data: user_model.UserModel
    ) -> Union[user_model.UserModel, None]:
        res = self.users_coll.find_one_and_update(
            {"id": id},
            {"$set": data.model_dump(exclude=["id", "created_at"], exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )

        return user_model.UserModel(**res) if res else None

    def delete(self, id: str) -> Union[user_model.UserModel, None]:
        res = self.users_coll.find_one_and_delete({"id": id})
        return user_model.UserModel(**res) if res else None

    def get(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Union[user_model.UserModel, None]:
        if not id and not username:
            raise ValueError("id or username must be provided")

        filter = {}
        if id != None:
            filter = {"id": id}
        if username != None:
            filter = {"username": username}
        res = self.users_coll.find_one(filter=filter)
        return user_model.UserModel(**res) if res else None

    def getList(
        self,
        query: str = None,
        query_by: Literal["username", "fullname"] = "username",
        sort_by: Literal[
            "username", "fullname", "created_at", "updated_at"
        ] = "created_at",
        sort_order: Literal[1, -1] = -1,
        skip: int = 1,
        limit: int = 10,
        get_total: bool = False,
    ) -> tuple[list[user_dto.GetListResItem], int]:
        pipeline = []

        match1_filter = {}
        if query != None:
            match1_filter[query_by] = {"$regex": query, "$options": "i"}

        if match1_filter:
            pipeline.append({"$match": match1_filter})

        pipeline.extend(
            [
                {"$sort": {sort_by: sort_order}},
                {
                    "$facet": {
                        **({"total": [{"$count": "total"}]} if get_total else {}),
                        "paginated_results": [
                            {"$skip": skip},
                            {"$limit": limit},
                        ],
                    }
                },
                {"$unwind": "$total"},
                {
                    "$project": {
                        "total": "$total.count",
                        "paginated_results": "$paginated_results",
                    }
                },
            ]
        )

        cursor = list(self.users_coll.aggregate(pipeline))

        try:
            data = [
                user_dto.GetListResItem(**item)
                for item in cursor[0].get("paginated_results", [])
            ]
            count = cursor[0].get("total", 0)
            return data, count
        except Exception as e:
            logger.warning(e)
            return [], 0
