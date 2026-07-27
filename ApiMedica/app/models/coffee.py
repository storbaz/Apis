from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint, Index, Date
from sqlalchemy.orm import relationship

from app.core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    region = Column(String(50))
    sub_region = Column(String(50))

    productions = relationship("Production", back_populates="country")
    exports_as_origin = relationship(
        "Export", foreign_keys="Export.country_id", back_populates="origin_country"
    )
    exports_as_dest = relationship(
        "Export", foreign_keys="Export.destination_country_id", back_populates="destination_country"
    )
    consumptions = relationship("Consumption", back_populates="country")


class Production(Base):
    __tablename__ = "production"
    __table_args__ = (
        UniqueConstraint("country_id", "year", "variety"),
        Index("idx_production_country_year", "country_id", "year"),
    )

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    year = Column(Integer, nullable=False)
    variety = Column(String(20), default="all")
    bags_60kg = Column(Numeric(12, 2))
    tonnes = Column(Numeric(12, 2))
    source = Column(String(20))

    country = relationship("Country", back_populates="productions")


class Export(Base):
    __tablename__ = "exports"
    __table_args__ = (Index("idx_exports_country_year", "country_id", "year"),)

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer)
    destination_country_id = Column(Integer, ForeignKey("countries.id"))
    hs_code = Column(String(10))
    bags_60kg = Column(Numeric(12, 2))
    tonnes = Column(Numeric(12, 2))
    value_usd = Column(Numeric(14, 2))
    source = Column(String(20))

    origin_country = relationship(
        "Country", foreign_keys=[country_id], back_populates="exports_as_origin"
    )
    destination_country = relationship(
        "Country", foreign_keys=[destination_country_id], back_populates="exports_as_dest"
    )


class Import(Base):
    __tablename__ = "imports"
    __table_args__ = (Index("idx_imports_country_year", "country_id", "year"),)

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer)
    origin_country_id = Column(Integer, ForeignKey("countries.id"))
    hs_code = Column(String(10))
    bags_60kg = Column(Numeric(12, 2))
    tonnes = Column(Numeric(12, 2))
    value_usd = Column(Numeric(14, 2))
    source = Column(String(20))


class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("date", "variety"),
        Index("idx_prices_date", "date"),
    )

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    variety = Column(String(20), nullable=False)
    price_usd_cents_per_lb = Column(Numeric(8, 4))
    source = Column(String(20))


class Consumption(Base):
    __tablename__ = "consumption"
    __table_args__ = (
        UniqueConstraint("country_id", "year"),
        Index("idx_consumption_country_year", "country_id", "year"),
    )

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    year = Column(Integer, nullable=False)
    bags_60kg = Column(Numeric(12, 2))
    tonnes = Column(Numeric(12, 2))
    source = Column(String(20))

    country = relationship("Country", back_populates="consumptions")
