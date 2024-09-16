from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert

# Set up database connection and session
engine = create_engine('sqlite:///concerts.db')
Base.metadata.create_all(engine)  # Ensure tables are created
Session = sessionmaker(bind=engine)
session = Session()

# Create a band and a venue
band = Band(name="The Rolling Stones", hometown="London")
venue = Venue(title="Wembley Stadium", city="London")

# Play a concert
concert = band.play_in_venue(venue, "2024-12-31")
session.add_all([band, venue, concert])
session.commit()

# Test methods
print("Introduction:", concert.introduction())  
# Expected output: "Hello London!!!!! We are The Rolling Stones and we're from London"

# Test Band's venues method
print("Band's venues:", band.venues())  
# Expected output: [<Venue(title='Wembley Stadium', city='London')>]

# Test Venue's bands method
print("Venue's bands:", venue.bands())  
# Expected output: [<Band(name='The Rolling Stones', hometown='London')>]

# Test Venue's concert_on method
print("Concert on '2024-12-31':", venue.concert_on("2024-12-31"))  
# Expected output: <Concert(date='2024-12-31', band_id=..., venue_id=...)>

# Test Band's most_performances method
print("Band with most performances:", Band.most_performances(session))  
# Expected output: <Band(name='The Rolling Stones', hometown='London')> or None if no band

# Test Venue's most_frequent_band method
print("Most frequent band at venue:", venue.most_frequent_band())  
# Expected output: <Band(name='The Rolling Stones', hometown='London')>

# Cleanup
session.close()
