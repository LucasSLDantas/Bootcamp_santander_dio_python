from typing import Annotated
from Workout_api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]