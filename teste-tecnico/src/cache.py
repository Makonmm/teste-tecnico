from collections import OrderedDict
from typing import Optional


class LRUCache:
    """Cache LRU, melhora  tempo de respostas armazenando o par 'pergunta:resposta'"""

    def __init__(self, capacity: int = 20):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str) -> Optional[str]:
        """Retorna o valor, caso exista, e remove o mais antigo (caso capacity > 20)"""

        if key not in self.cache:
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, key: str, value: str) -> None:
        """Salva um valor e remove o mais antigo caso atinja a máxima capacity"""
        self.cache[key] = value
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


cache_em_memoria = LRUCache(capacity=20)
