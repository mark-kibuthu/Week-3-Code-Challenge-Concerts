from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='band')

    def venues(self):
        return [concert.venue for concert in self.concerts]

    def play_in_venue(self, venue, date):
        return Concert(band=self, venue=venue, date=date)

    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        return session.query(cls).join(Concert).group_by(cls.id).order_by(sa.func.count(Concert.id).desc()).first()

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='venue')

    def bands(self):
        return [concert.band for concert in self.concerts]

    def concert_on(self, date):
        return next((concert for concert in self.concerts if concert.date == date), None)

    def most_frequent_band(self):
        band_count = {}
        for concert in self.concerts:
            band = concert.band
            band_count[band] = band_count.get(band, 0) + 1
        return max(band_count, key=band_count.get) if band_count else None

class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def hometown_show(self):
        return self.venue.city == self.band.hometown

    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
