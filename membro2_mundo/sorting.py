"""Membro 2 — MergeSort para ordenar o inventário.

Este é o segundo problema computacional do projeto.
Complexidade: O(n log n).
"""

ORDEM_RARIDADE = {
    "comum": 1,
    "incomum": 2,
    "rara": 3,
    "epica": 4,
    "lendaria": 5,
}

def valor_chave(item: dict, chave: str):
    if chave == "raridade":
        return ORDEM_RARIDADE.get(item.get("raridade", "comum"), 0)
    return item.get(chave, 0)


def merge_sort_itens(itens: list[dict], chave: str) -> list[dict]:
    """Ordena itens por uma chave usando MergeSort."""
    if len(itens) <= 1:
        return itens[:]

    meio = len(itens) // 2
    esquerda = merge_sort_itens(itens[:meio], chave)
    direita = merge_sort_itens(itens[meio:], chave)
    return _merge(esquerda, direita, chave)


def _merge(esquerda: list[dict], direita: list[dict], chave: str) -> list[dict]:
    resultado = []
    i = j = 0

    while i < len(esquerda) and j < len(direita):
        if valor_chave(esquerda[i], chave) <= valor_chave(direita[j], chave):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado
