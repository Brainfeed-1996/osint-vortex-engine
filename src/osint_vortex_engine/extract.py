from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


RE_EMAIL = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
RE_URL = re.compile(r"https?://[^\s]+")
RE_IP = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
RE_HANDLE = re.compile(r"(?<!\w)@[a-zA-Z0-9_]{3,20}")
RE_DOMAIN = re.compile(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")


def normalize_domain(d: str) -> str:
    return d.lower().strip(".")


@dataclass(frozen=True)
class Entity:
    kind: str
    value: str

    def key(self) -> str:
        return f"{self.kind}:{self.value}"


def extract_entities(text: str) -> list[Entity]:
    emails = [m.group(0).lower() for m in RE_EMAIL.finditer(text)]
    urls = [m.group(0) for m in RE_URL.finditer(text)]
    ips = [m.group(0) for m in RE_IP.finditer(text)]
    handles = [m.group(0).lower() for m in RE_HANDLE.finditer(text)]

    domains: list[str] = []
    for u in urls:
        dom = re.sub(r"^https?://", "", u).split("/")[0]
        domains.append(normalize_domain(dom))
    for e in emails:
        domains.append(normalize_domain(e.split("@")[-1]))
    for m in RE_DOMAIN.finditer(text):
        domains.append(normalize_domain(m.group(0)))

    ents = []
    ents += [Entity("email", v) for v in set(emails)]
    ents += [Entity("url", v) for v in set(urls)]
    ents += [Entity("ip", v) for v in set(ips)]
    ents += [Entity("handle", v) for v in set(handles)]
    ents += [Entity("domain", v) for v in set(domains)]
    # stable ordering
    ents = sorted(ents, key=lambda e: (e.kind, e.value))
    return ents


def extract_from_snippets(snippets: Iterable[str]) -> list[list[Entity]]:
    return [extract_entities(s) for s in snippets]
