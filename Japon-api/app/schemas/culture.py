from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Language(str, Enum):
    SPANISH = "es"
    ENGLISH = "en"
    FRENCH = "fr"
    PORTUGUESE = "pt"


class PhraseCategory(str, Enum):
    BASIC = "basico"
    RESTAURANT = "restaurante"
    SHOPPING = "compras"
    TRANSPORT = "transporte"
    HOTEL = "hotel"
    EMERGENCY = "emergencia"
    SOCIAL = "social"


class Phrase(BaseModel):
    japanese: str
    romaji: str
    translation: str
    context: str
    pronunciation_tip: Optional[str] = None


class EtiquetteRule(BaseModel):
    category: str
    title: str
    description: str
    importance: str  # "alta", "media", "baja"
    tip: Optional[str] = None


class DoAndDont(BaseModel):
    category: str
    do: list[str]
    dont: list[str]


class Scenario(BaseModel):
    id: str
    title: str
    description: str
    phrases: list[Phrase]
    etiquette_rules: list[EtiquetteRule]
