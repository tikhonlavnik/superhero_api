from abc import ABC, abstractmethod
from typing import Sequence


class IHeroRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> "Superhero":
        pass

    @abstractmethod
    def get_list(self, params: dict) -> Sequence["Superhero"]:
        pass
