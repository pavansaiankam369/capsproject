from app.db.session import Base  # This imports the Base from session.tion

# Now Base.metadata.create_all(bind=engine) in main.py will create all tables
# Import all models here to register them with Base
from app.models.user import User, UserLogins, Movies, Reviews, Watchlist, Platforms, Regions, MovieAvailability, UserActivityLogs, Recommendation
