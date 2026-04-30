'''
Movie Ticket Booking System - Low Level Design Problem

## Problem Statement

Design and implement a **Movie Ticket Booking System** that allows users to search for movies, view available shows, book tickets for specific seats, and cancel bookings. The system should handle seat availability, prevent double-booking, and manage show timings.

---

## Functional Requirements

### 1. Core Entities

- **Movie**: Represents a movie
  - Movie ID, Title, Duration, Genre
- **Theater**: Represents a theater/cinema
  - Theater ID, Name, Location
- **Show**: Represents a movie show at a theater
  - Show ID, Movie, Theater, Show Time, Date
  - Seat Layout (rows and columns)
- **Seat**: Represents a seat in a show
  - Seat ID (e.g., "A1", "B5"), Row, Column, Status (Available/Booked)
- **Booking**: Represents a ticket booking
  - Booking ID, Show, List of Seats, User ID, Booking Time

### 2. Core Operations

- **Search Movies**: Search movies by title or genre
- **Get Shows**: Get all shows for a movie at a theater (or all theaters)
- **View Available Seats**: View seat layout with availability for a show
- **Book Tickets**: Book specific seats for a show
  - Check seat availability
  - Reserve seats (prevent double-booking)
  - Create booking record
- **Cancel Booking**: Cancel a booking and release seats
- **View Booking**: View details of a booking

### 3. Constraints & Rules

- **Seat Availability**: Cannot book already booked seats
- **Concurrent Bookings**: Prevent multiple users from booking the same seat simultaneously
- **Booking Validation**: Can only cancel own bookings
- **Seat Selection**: Must book at least 1 seat
- **Show Time**: Cannot book seats for past shows (optional)

---

## Example

```python
# Initialize system
booking_system = MovieTicketBookingSystem()

# Add movies
movie1 = booking_system.add_movie("Inception", 148, "Sci-Fi")
movie2 = booking_system.add_movie("The Matrix", 136, "Action")

# Add theaters
theater1 = booking_system.add_theater("Cineplex", "Downtown")
theater2 = booking_system.add_theater("AMC", "Uptown")

# Add shows
show1 = booking_system.add_show(movie1.id, theater1.id, "2024-01-15", "14:00")
show2 = booking_system.add_show(movie1.id, theater1.id, "2024-01-15", "18:00")

# View available seats
seats = booking_system.get_available_seats(show1.id)
# Returns: [{"seat_id": "A1", "row": "A", "col": 1, "status": "available"}, ...]

# Book tickets
booking = booking_system.book_tickets(show1.id, ["A1", "A2", "A3"], "user123")
# Returns: Booking object with booking_id, seats, total_price

# View booking
booking_details = booking_system.get_booking(booking.booking_id)
# Returns: Booking details

# Cancel booking
booking_system.cancel_booking(booking.booking_id, "user123")
# Releases seats A1, A2, A3
```

---

## Design Constraints

1. **Object-Oriented Design**: Use classes for Movie, Theater, Show, Seat, Booking
2. **Data Structures**: Use appropriate data structures (dictionaries, lists, sets)
3. **Seat Management**: Use 2D array or dictionary for seat layout (e.g., 5 rows A-E, 10 seats per row)
4. **Thread Safety**: Consider basic thread safety for seat booking (locks or atomic operations)
5. **Exception Handling**: Use custom exceptions with descriptive messages
6. **Simple Implementation**: Focus on core functionality, not payment processing

---

## Expected Classes

1. **Movie**: 
   - Attributes: movie_id, title, duration, genre
   - Methods: (optional getters)

2. **Theater**:
   - Attributes: theater_id, name, location
   - Methods: (optional getters)

3. **Show**:
   - Attributes: show_id, movie, theater, date, time, seats (2D array or dict)
   - Methods: get_seat_status(), is_seat_available()

4. **Seat**:
   - Attributes: seat_id, row, column, status (enum: AVAILABLE, BOOKED)
   - Methods: (optional getters)

5. **Booking**:
   - Attributes: booking_id, show, seats, user_id, booking_time
   - Methods: (optional getters)

6. **MovieTicketBookingSystem** (Main class):
   - Methods: add_movie(), add_theater(), add_show(), search_movies(), 
             get_shows(), get_available_seats(), book_tickets(), 
             cancel_booking(), get_booking()

7. **Custom Exceptions**:
   - `SeatAlreadyBookedException`
   - `InvalidSeatException`
   - `BookingNotFoundException`
   - `InvalidBookingException`

---

## Edge Cases to Handle

1. **Double Booking**: Two users try to book the same seat simultaneously
2. **Invalid Seat**: Trying to book non-existent seat (e.g., "Z99")
3. **Already Booked Seat**: Trying to book an already booked seat
4. **Cancel Non-existent Booking**: Canceling a booking that doesn't exist
5. **Cancel Others' Booking**: User trying to cancel someone else's booking
6. **Empty Seat List**: Trying to book with no seats selected
7. **Past Show**: (Optional) Booking for a show that already happened
8. **Full Show**: All seats are booked

'''
import uuid
from enum import Enum
from threading import Lock
from datetime import datetime

class MovieTicketBookingSystem:
    def __init__(self):
        self.movies = {}
        self.theaters = {}
        self.shows = {}
        self.bookings = {}
        self.lock = Lock() # global lock for collections
        self.show_locks = {} # {show_id: Lock()}
    
    def add_movie(self, title, duration, genre):
        new_movie = Movie(title, duration, genre)
        self.movies[new_movie.movie_id] = new_movie
        return new_movie

    def add_theater(self, name, location):
        new_theater = Theater(name, location)
        self.theaters[new_theater.theater_id] = new_theater
        return new_theater
   
    def add_show(self, movie_id, theater_id, date, time):
        new_show = Show(movie_id, theater_id, date, time)
        self.shows[new_show.show_id] = new_show
        return new_show

    def _validate_seats(self, show_id, seat_list):
        show = self.shows[show_id]
        seat_layout = show.seats
        seats = []
        for seat in seat_list:
            row, column = seat[0], int(seat[1:])
            if row not in seat_layout.row_map or column > seat_layout.columns or column < 1:
                raise InvalidSeatException()
            valid_row = seat_layout.row_map[row]
            valid_col = column - 1
            if seat_layout.seats[valid_row][valid_col].status == Status.BOOKED:
                raise SeatAlreadyBookedException()
            seats.append(seat_layout.seats[valid_row][valid_col])
        return seats

    def book_tickets(self, show_id, seats, user_id):
        with self.lock:
            try:
                seats_to_book = self._validate_seats(show_id, seats)
            except InvalidSeatException:
                raise InvalidSeatException()
            except SeatAlreadyBookedException:
                raise SeatAlreadyBookedException()
            for seat in seats_to_book:
                seat.status = Status.BOOKED
            new_booking = Booking(show_id, seats_to_book, user_id)
            self.bookings[new_booking.booking_id] = new_booking
            return new_booking

    def cancel_booking(self, booking_id, user_id):
        with self.lock:
            booking = self.bookings.get(booking_id)
            if booking is None:
                raise BookingNotFoundException()
            if booking.user_id != user_id:
                raise InvalidBookingException()
            for seat in booking.seats:
                seat.status = Status.AVAILABLE
            del self.bookings[booking_id]

class Theater:
    def __init__(self, name, location):
        self.theater_id = uuid.uuid4()
        self.name = name
        self.location = location

class Movie:
    def __init__(self, title, duration, genre):
        self.movie_id = uuid.uuid4()
        self.title = title
        self.duration = duration
        self.genre = genre

class Show:
    def __init__(self, movie_id, theater_id, date, time):
        self.show_id = uuid.uuid4()
        self.movie_id = movie_id
        self.theater_id = theater_id
        self.date = date
        self.time = time
        self.seats = SeatLayout(5, 10)

class SeatLayout:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        start_row = ord('A')
        self.row_map = dict(zip([chr(c) for c in range(start_row, start_row+rows+1)],range(1, rows+1)))
        self.seats = [[None] * columns for _ in range(rows)]
        for row in range(rows):
            for column in range(columns):
                self.seats[row][column] = Seat(row, column)

class Status(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"

class Seat:
    def __init__(self, row, column):
        self.seat_id = uuid.uuid4()
        self.row = row
        self.column = column
        self.status = Status.AVAILABLE

class Booking:
    def __init__(self, show_id, seats, user_id):
        self.booking_id = uuid.uuid4()
        self.show_id = show_id
        self.seats = seats
        self.user_id = user_id
        self.booking_time = datetime.now()


class SeatAlreadyBookedException(Exception):
    def __init__(self):
        super().__init__('This seat is already booked')

class InvalidSeatException(Exception):
    def __init__(self):
        super().__init__('Invalid seat')

class BookingNotFoundException(Exception):
    def __init__(self):
        super().init('Booking not found')

class InvalidBookingException(Exception):
    def __init__(self):
        super().init('Invalid booking')


# Test Case 1: Basic booking flow
system = MovieTicketBookingSystem()
movie = system.add_movie("Avengers", 180, "Action")
theater = system.add_theater("Cineplex", "Downtown")
show = system.add_show(movie.movie_id, theater.theater_id, "2024-01-15", "14:00")

# Book seats
booking = system.book_tickets(show.show_id, ["A1", "A2"], "user1")
assert booking is not None
assert len(booking.seats) == 2

# Try to book same seats again (should fail)
try:
    system.book_tickets(show.show_id, ["A1"], "user2")
    assert False, "Should raise SeatAlreadyBookedException"
except SeatAlreadyBookedException:
    pass

# Test Case 2: Cancel booking
system.cancel_booking(booking.booking_id, "user1")
# Now A1, A2 should be available again
booking2 = system.book_tickets(show.show_id, ["A1"], "user3")
assert booking2 is not None

# Test Case 3: Invalid seat
try:
    system.book_tickets(show.show_id, ["Z99"], "user1")
    assert False, "Should raise InvalidSeatException"
except InvalidSeatException:
    pass