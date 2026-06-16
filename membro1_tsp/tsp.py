"""Membro 1 — Algoritmo TSP por força bruta.

Como o MVP tem poucos locais, testar permutações é suficiente e deixa a
explicação acadêmica mais direta: o TSP exato possui crescimento fatorial.
"""
from itertools import permutations
from math import inf


def distancia_rota(rota: list[str], mapa: dict[str, dict[str, int]]) -> int | float:
    """Calcula a distância total de uma rota."""
    total = 0
    for atual, proximo in zip(rota, rota[1:]):
        distancia = mapa.get(atual, {}).get(proximo)
        if distancia is None:
            return inf
        total += distancia
    return total


def calcular_melhor_rota(
    local_inicial: str,
    locais_obrigatorios: list[str],
    mapa: dict[str, dict[str, int]],
) -> tuple[list[str], int | float]:
    """Calcula a menor rota que sai do local inicial, visita todos e retorna.

    Exemplo:
        Vila -> Bosque -> Lago -> Ruínas -> Vila
    """
    melhor_rota = []
    menor_distancia = inf

    for ordem in permutations(locais_obrigatorios):
        rota = [local_inicial, *ordem, local_inicial]
        total = distancia_rota(rota, mapa)
        if total < menor_distancia:
            melhor_rota = rota
            menor_distancia = total

    return melhor_rota, menor_distancia
