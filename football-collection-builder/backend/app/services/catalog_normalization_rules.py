from __future__ import annotations
import hashlib, html, re, unicodedata
from dataclasses import dataclass

RULES_VERSION = "1.0.1"
PRESERVED_TOKENS = frozenset({"FC","AC","EC","SC","AFC","CF","CD","CA","AS","SS","US","FK","SK","SV","TSV","VFB","PSV","AZ","MG","RJ","RN","SP","PR","RS"})
UNKNOWN_NAMES = frozenset({"unknown", "unknown country", "unknown team", "desconhecido", "outros"})

@dataclass(frozen=True)
class Rule:
    code: str
    entity_type: str
    description: str
    version: str = RULES_VERSION
    deterministic: bool = True

RULE_REGISTRY = (
    Rule("CN001","country","Normalização técnica conservadora de Country/Region."),
    Rule("TM001","team","Normalização técnica conservadora de Team."),
    Rule("CL001","collection","Normalização técnica e período de inclusão."),
    Rule("IT001","item","Normalização técnica conservadora de título."),
    Rule("SL001","all","Slug URL-safe determinístico."),
    Rule("SL002","all","Desambiguação de slug por stableKey."),
    Rule("MR001","all","Overlay manual ativo, resolvido e reconciliado."),
)

def technical_text(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", html.unescape(value or ""))).strip()

def safe_uppercase_display(value: str) -> str:
    value = technical_text(value)
    letters = [c for c in value if c.isalpha()]
    if not letters or not all(c.isupper() for c in letters):
        return value
    words = re.split(r"(\s+|-)", value)
    converted=[]
    for word in words:
        upper=word.upper()
        if upper in PRESERVED_TOKENS:
            converted.append("VfB" if upper == "VFB" else upper)
        elif word.isalpha() and len(word) > 1:
            converted.append(word[0].upper()+word[1:].lower())
        else:
            converted.append(word)
    return "".join(converted)

def normalize_value(value: str) -> tuple[str,list[str]]:
    technical=technical_text(value); rules=[]
    if technical != value: rules.append("technical")
    cased=safe_uppercase_display(technical)
    if cased != technical: rules.append("case")
    return cased,rules

def slugify(value: str) -> str:
    ascii_value=unicodedata.normalize("NFKD",value).encode("ascii","ignore").decode("ascii").lower()
    return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",ascii_value)).strip("-") or "entity"

def unique_slug(base: str, stable_key: str, used: set[str]) -> tuple[str,bool]:
    if base not in used: used.add(base); return base,False
    suffix=hashlib.sha256(stable_key.encode("utf-8")).hexdigest()[:6]
    candidate=f"{base}-{suffix}"
    used.add(candidate)
    return candidate,True

def inclusion_period(month: int|None, year: int|None, batch: int|None) -> str|None:
    if month is None or year is None:return None
    return f"{month:02d}/{year}" + (f" — lote {batch}" if batch is not None else "")

def is_unknown(name: str, confidence: str) -> bool:
    return confidence == "unknown" or technical_text(name).casefold() in UNKNOWN_NAMES
