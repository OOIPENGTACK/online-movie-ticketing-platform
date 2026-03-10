import pytest
from validator_collection import errors
from project import validate_seat, validate_email, booking_seat, create_confirmation


def test_validate_seat():
    assert validate_seat("A", "1") == True
    assert validate_seat("0", "2") == False
    assert validate_seat("F", "4") == False


def test_validate_email():
    assert validate_email("example@gmail.com") == "example@gmail.com"
    with pytest.raises(errors.InvalidEmailError):
        validate_email("example@@@gmail.com")
    with pytest.raises(errors.EmptyValueError):
        validate_email("")


def test_booking_seat():
    seats = [
        ("+----------+"),
        ("|  Screen  |"),
        ("+----------+"),
        ["A", "□", "□", "□", "□", "□", "□", "□", "□", "□", "□", "A"],
        ["B", "□", "□", "□", "□", "□", "□", "□", "□", "□", "□", "B"],
        ["C", "□", "□", "□", "□", "□", "□", "□", "□", "□", "□", "C"],
        ["D", "□", "□", "□", "□", "□", "□", "□", "□", "□", "□", "D"],
        ["E", "□", "□", "□", "□", "□", "□", "□", "□", "□", "□", "E"]
    ]

    total = 0
    seat_no = []
    booking_result, total, seat_no = booking_seat("B", 3, 18, total, seat_no, seats)
    assert booking_result == True
    assert total == 18
    assert seat_no == ["B3"]
    assert seats[4][3] == "■"

    # Booking second seat
    booking_result, total, seat_no = booking_seat("A", 5, 18, total, seat_no, seats)
    assert booking_result == True
    assert total == 36
    assert seat_no == ["B3", "A5"]
    assert seats[3][5] == "■"

    booking_result, total, seat_no = booking_seat("B", 3, 36, total, seat_no, seats)
    assert booking_result == False # Assume re-booking the already taken seat B3
    assert total == 36
    assert seat_no == ["B3", "A5"]
    assert seats[4][3] == "■"


def test_create_confirmation():
    order_no, _ = create_confirmation("John Wick", "12:15 PM", ["A2"], 18)
    assert 100000 <= order_no <= 999999 # Intentionally asserting order_no < 100000 or > 999999 will fail the test
    assert len(str(order_no)) == 6
