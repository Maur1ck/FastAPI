from app.models.bookings import BookingsORM
from app.repositories.base import BaseRepository
from app.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking
