from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .extract import Entity


@dataclass(frozen=True)
class Edge:
    snippet_id: int
    entity: str


def build_edges(entities_by_snippet: list[list[Entity]]) -> list[Edge]:
    edges: list[Edge] = []
    for sid, ents in enumerate(entities_by_snippet):
        for e in ents:
            edges.append(Edge(snippet_id=sid, entity=e.key()))
    return edges


def entity_support(edges: Iterable[Edge]) -> dict[str, int]:
    seen: dict[str, set[int]] = {}
    for e in edges:
        seen.setdefault(e.entity, set()).add(e.snippet_id)
    return {k: len(v) for k, v in seen.items()}
