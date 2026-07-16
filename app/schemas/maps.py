from pydantic import BaseModel
from typing import Optional


class Coordinates(BaseModel):
    lat: float
    lng: float


class Hours(BaseModel):
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None


class EmailInfo(BaseModel):
    email: str
    status: str
    type: str


class SocialLinks(BaseModel):
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    youtube: Optional[str] = None


class Enrichment(BaseModel):
    emails: list[EmailInfo] = []
    social: SocialLinks = SocialLinks()


class BusinessResult(BaseModel):
    place_id: str
    name: str
    category: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    coordinates: Optional[Coordinates] = None
    hours: Optional[Hours] = None
    is_claimed: Optional[bool] = None
    enrichment: Optional[Enrichment] = None
    service_options: Optional[dict] = None
    price_level: Optional[str] = None
    thumbnail_url: Optional[str] = None
    google_maps_url: Optional[str] = None


class Pagination(BaseModel):
    current_page: int
    total_results: int
    has_next: bool


class SearchResponse(BaseModel):
    results: list[BusinessResult]
    pagination: Pagination


class SearchRequest(BaseModel):
    query: str
    location: str = ""
    limit: int = 20


class Review(BaseModel):
    author: str
    rating: Optional[int] = None
    text: Optional[str] = None
    time: Optional[str] = None
    profile_image: Optional[str] = None


class ReviewsResponse(BaseModel):
    place_id: str
    reviews: list[Review]
    total: int


class PlaceRequest(BaseModel):
    place_id: str
    enrich: bool = False
