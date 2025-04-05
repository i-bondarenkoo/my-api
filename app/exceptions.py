# файлик для универсальных исключений

from fastapi import HTTPException, status


USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден",
)

LIST_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Список пользователей пуст",
)

NO_DATA_FOR_UPDATES = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Нет данных для обновления",
)
# ---------------------------------------
# Для сущности project
PROJECT_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Проект не найден",
)
LIST_PROJECTS_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Список проектов пуст",
)

ERROR_PAGINATION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Начальный диапазон должен быть меньше чем конечный для списка",
)
