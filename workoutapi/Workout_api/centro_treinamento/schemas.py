from typing import Annotated
from Workout_api.contrib.schemas import BaseSchema
from pydantic import Field, UUID4


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT jubarte", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua X Q02", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="Lucas Dantas", max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT jubarte", max_length=20)]

class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="ID do centro de treinamento")]