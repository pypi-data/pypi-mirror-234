from unidecode import unidecode
import re
import os
import csv
from typing import List
from abc import abstractmethod
from datetime import datetime
from langchain.schema import BaseOutputParser


def limpiar_texto(texto, **kwargs):

    texto_limpio = texto
    if "quitar_acentos" in kwargs and kwargs["quitar_acentos"] is True:
        texto_limpio = unidecode(texto_limpio)

    if "quitar_caracteres_especiales" in kwargs and kwargs["quitar_caracteres_especiales"] is True: # noqa
        texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)
        texto_limpio = texto_limpio.replace(",", "")

    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
    texto_limpio = texto_limpio.strip('\'\n".,[]*- ')
    texto_limpio = texto_limpio.replace(" - ", " -")

    if "minusculas" in kwargs and kwargs["minusculas"] is True:
        texto_limpio = texto_limpio.lower()

    return texto_limpio


def get_llm_cost(directory, func_nombre, modelo, tokens_totales, costo_total, execution_time): # noqa

    file_path_costos = os.path.join(directory, "costos")

    if not os.path.exists(file_path_costos):
        os.mkdir(file_path_costos)

        with open(f'{file_path_costos}/costos_llm.csv', "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["fecha", "función", "modelo", "tokens utilizados", "costo total", "duración"]) # noqa

    with open(f'{file_path_costos}/costos_llm.csv', "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            func_nombre,
            modelo,
            tokens_totales,
            f'{costo_total: .5f}',
            f'{execution_time: .2f}'
        ])


class ListOutputParser(BaseOutputParser[List[str]]):
    """Parse the output of an LLM call to a list."""

    @property
    def _type(self) -> str:
        return "list"

    @abstractmethod
    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""


class TripleHyphenSeparatedListOutputParser(ListOutputParser):
    """Parse the output of an LLM call to a triple hyphen separated list."""

    @property
    def lc_serializable(self) -> bool:
        return True

    def get_format_instructions(self) -> str:
        return (
            "Your response should be a list of triple hyphen separated values,"
            "eg: `foo --- bar --- baz`"
        )

    def parse(self, text: str) -> List[str]:
        """Parse the output of an LLM call."""
        return text.strip().split(" --- ")
