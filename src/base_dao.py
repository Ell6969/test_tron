from fastapi import HTTPException
from sqlalchemy import desc, insert, select
from sqlalchemy.exc import SQLAlchemyError

from src.databases import async_session_maker
from src.dependencies import SFilterPagination
from src.models import HistoryWalletRequest
from src.schemas import SHystoryRequestAll


class BaseDAO:
    model = None
    schema_all_fields = None

    @classmethod
    async def find_all(cls, pagination: SFilterPagination, **filter_by):
        """
        Находит и возвращает все записи. С возможным фильтром и пагинацией.
        :param filter_by: Фильтры для поиска записи.
        :return: Список объектов schema_all_fields.
        """
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .order_by(desc(cls.model.id))
                .limit(pagination.page_size)
                .offset((pagination.page - 1) * pagination.page_size)
            )
            result = await session.execute(query)
            instances = result.scalars().all()
            return [cls.schema_all_fields.model_validate(instance) for instance in instances]

    @classmethod
    async def add(cls, **data):
        """
        Добавляет запись в таблицу.
        :param data: Словарь с данными для добавления.
        :return: Сам объект schema_all_fields
        """
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                instance = result.scalar_one()
                await session.refresh(instance)
                return cls.schema_all_fields.model_validate(instance)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка базы данных при добавлении записи. {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неизвестная ошибка при добавлении записи.{e}")


class HistoryWalletRequestDAO(BaseDAO):
    model = HistoryWalletRequest
    schema_all_fields = SHystoryRequestAll
