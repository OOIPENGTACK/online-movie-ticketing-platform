from fpdf import FPDF
import qrcode
from tabulate import tabulate
import random
from datetime import date, datetime
from validator_collection import validators, errors

# List of movies
movies = ["Avengers: End Game", "Spider-Man: No Way Home", "Top Gun: Maverick",
"Dune: Part One", "Avatar", "Godzilla vs. Kong", "John Wick",
"The Conjuring", "Titanic", "Fantastic Beasts and Where to Find Them"]

# Time slots
time_slots = {
    "Avengers: End Game": ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM"],
    "Spider-Man: No Way Home": ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM"],
    "Top Gun: Maverick": ["11:00 AM", "2:00 PM", "5:00 PM", "8:00 PM"],
    "Dune: Part One": ["10:30 AM", "1:30 PM", "4:30 PM", "7:30 PM"],
    "Avatar": ["9:30 AM", "12:30 PM", "3:30 PM", "6:30 PM"],
    "Godzilla vs. Kong": ["8:00 AM", "11:00 AM", "2:00 PM", "5:00 PM"],
    "John Wick": ["9:15 AM", "12:15 PM", "3:15 PM", "6:15 PM"],
    "The Conjuring": ["10:45 AM", "1:45 PM", "4:45 PM", "7:45 PM"],
    "Titanic": ["8:30 AM", "11:30 AM", "2:30 PM", "5:30 PM"],
    "Fantastic Beasts and Where to Find Them": ["9:45 AM", "12:45 PM", "3:45 PM", "6:45 PM"]
}

# Seating Map
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

def main():
    selected_movie = display_movies()
    selected_time = select_time_slot(selected_movie)
    seat_no, total = seat_selection()
    process_payment(total)
    order_no, formatted_time = create_confirmation(selected_movie, selected_time, seat_no, total)
    create_ticket(order_no, selected_movie, selected_time, seat_no, total, formatted_time)


def display_movies():
    """Prompt user to select a movie from a list of movies on screen."""
    while True:
        print("\033[1mNow Showing: \033[0m" + "\n")
        for index, movie in enumerate(sorted(movies)):
            print(index + 1, movie)
        print()
        try:
            movie_choice = int(input("Select a movie (1-10): ").strip())
            if 1 <= movie_choice <= len(movies):
                selected_movie = sorted(movies)[movie_choice - 1]
                return selected_movie
            else:
                print("Invalid movie selection. Please try again.")
        except ValueError:
            print("Invalid input! Please select a number between 1 and 10.")


def select_time_slot(selected_movie):
    """Prompt user to select a time slot for their selected movie."""
    while True:
        print("\033[1mAvailable time slots:\033[0m" + "\n")
        print(selected_movie)
        for index, time in enumerate(time_slots[selected_movie]):
            print(f"{index + 1}. {time}")

        time_choice = input("Please select a time slot (1-4): ")

        if time_choice.isdigit() and 1 <= int(time_choice) <= len(time_slots[selected_movie]):
            selected_time = time_slots[selected_movie][int(time_choice) - 1]
            print(f"Successfully booked {selected_movie} at {selected_time}.")
            return selected_time
        else:
            print("Invalid time slot selection! Please try again.")


def display_seats(seats):
    """Display seating map."""
    for seat in seats:
        print(*seat)
    print("Rows: A-E, Column: 1-10")


def seat_selection():
    """Prompt user to input seating row and column and to repeat the process for multiple seats booking (if any)."""
    ticket_price = 18
    total = 0
    seat_no = []

    while True:
        display_seats(seats)
        row = input("Enter row (A-E): ").upper().strip()
        column = input("Enter column (1-10): ").strip()

        if not validate_seat(row, column):
            continue

        booking_result, total, seat_no = booking_seat(row, column, ticket_price, total, seat_no, seats)
        if not booking_result:
            continue

        display_seats(seats)

        while True:
            multiple_seats = input("Choose another seat? (Y/N): ").upper().strip()
            if multiple_seats in ("Y", "N"):
                break
            print("Please select Y or N.")

        if multiple_seats == "N":
            break

    return seat_no, total


def validate_seat(row, column):
    """Validate user's input of seating row and column."""
    if not row in ("A", "B", "C", "D", "E"):
        print("Invalid row. Please try again.")
        return False
    if not column.isdigit() or not (1 <= int(column) <= 10):
        print("Invalid column. Please try again.")
        return False
    return True


def booking_seat(row, column, ticket_price, total, seat_no, seats):
    """Book a seat if available as well as updating the seating map and total price."""
    # Seat rows start from 4th (i.e. index 3) element of the seats list
    row_index = ord(row) - ord("A") + 3
    column_index = int(column)

    if seats[row_index][column_index] == "□":
        seats[row_index][column_index] = "■"
        total += ticket_price
        seat_no.append(f"{row}{column}")
        print(f"Successfully booked seat {row}{column}.")
        return True, total, seat_no
    else:
        print(f"Seat {row}{column} is taken. Please choose another seat.")
        return False, total, seat_no


def process_payment(total):
    """Prompt user to select a payment option to proceed payment for their booked seats."""
    print()
    print(f"Total costs for booked seats ${total:.2f}")
    print("Proceed to payment...")

    # Payment options
    print("Payment methods:")
    print("1. Credit Card")
    print("2. PayPal")
    print("3. Bank Transfer")

    while True:
        try:
            payment = int(input("Select payment method (1-3): "))
            # if the payment method is Credit Card
            if payment == 1:
                credit_card_payment()
                break
            # if the payment method is PayPal
            # assumed to be redirected to external site
            elif payment == 2:
                print("Payment via PayPal successful!")
                break
            # if the payment method is Bank Transfer
            # assumed to be redirected to external site
            elif payment == 3:
                print("Payment via Bank Transfer successful!")
                break
            else:
                print("Invalid payment method. Please select a valid method.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")


def credit_card_payment():
    """Validate user's input of card details in credit card payment stage."""
    while True:
        # Assuming "-" are provided or "embedded" in the credit card gateway
        card_number = input("Card number (16 digits): ")
        if card_number.isdigit() and len(card_number) == 16:
            break
        print("Invalid card number. Please try again.")

    while True:
        name_on_card = input("Name on card: ")
        if not name_on_card:
            print("Missing name. Please enter your name.")
            continue
        if not name_on_card.isalpha():
            print("Invalid name. Please try again.")
            continue
        break

    while True:
        expiry = input("Expiry (MM/YY): ")
        if expiry[:2].isdigit() and expiry[3:].isdigit() and len(expiry) == 5 and expiry[2] == "/" and (1 <= int(expiry[:2]) <= 12):
            break
        print("Invalid expiry date. Please try again.")

    while True:
        cvv = input("CVV (3 digits): ")
        if cvv.isdigit() and len(cvv) == 3:
            break
        print("Invalid CVV. Please try again.")

    while True:
        """Validate user's email address."""
        email = input("Email address: ")
        try:
            if validate_email(email):
                break
        except(errors.InvalidEmailError, errors.EmptyValueError):
            continue

    print("Payment via Credit Card successful!")


def validate_email(email):
    try:
        return validators.email(email.strip())
    except (errors.InvalidEmailError, errors.EmptyValueError):
        print("Invalid email. Please try again")
        raise


def create_confirmation(selected_movie, selected_time, seat_no, total):
    """Create booking confirmation."""
    order_no = random.randint(100000, 999999)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%I:%M %p")

    confirmation = [
        ["Order No", order_no],
        ["Movie", selected_movie],
        ["Timeslot", selected_time],
        ["Seat", ", ".join(seat_no)],
        ["Total", f"${total:.2f}"],
        ["Transaction Date", date.today()],
        ["Transaction Time", formatted_time]
    ]

    print()
    print("Generating confirmation...")
    print(f"Booking confirmation for order {order_no} successfully generated.")
    print(tabulate(confirmation, tablefmt="fancy_grid"))
    return order_no, formatted_time


def create_ticket(order_no, selected_movie, selected_time, seat_no, total, formatted_time):
    """Create movie ticket with QR code in PDF."""
    ticket_qrcode = qrcode.make(
        f"Order No: {order_no}\n"
        f"Movie: {selected_movie}\n"
        f"Timeslot: {selected_time}\n"
        f"Seat: {', '.join(seat_no)}\n"
        f"Total ${total:.2f}\n"
        f"Transaction Date: {date.today()}\n"
        f"Transaction Time: {formatted_time}"
    )

    type(ticket_qrcode)  # qrcode.image.pil.PilImage
    ticket_qrcode.save("ticket.png")

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("helvetica", "", 50)
    # Moving cursor downwards
    pdf.set_y(20)

    # Calculating center x position
    cell_width = 150
    pdf.center_x = (pdf.w - cell_width) / 2

    # Moving cursor to the page center
    pdf.set_x(pdf.center_x)

    # Printing title:
    pdf.cell(cell_width, 15, "CS50 Cinemas", new_x="LMARGIN", new_y="NEXT", align="C")

    # Printing ticket details
    pdf.ln(20)
    pdf.set_font("helvetica", "", 30)
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Order No: {order_no}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Movie: {selected_movie}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Timeslot: {selected_time}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Seat: {', '.join(seat_no)}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Total: ${total:.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Transaction Date: {date.today()}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, f"Transaction Time: {formatted_time}", new_x="LMARGIN", new_y="NEXT")

    # Adding QR code
    pdf.ln(10)
    pdf.set_x(pdf.center_x)
    pdf.image("ticket.png", w=cell_width, h=130)
    pdf.set_font("helvetica", "", 25)
    pdf.set_x(pdf.center_x)
    pdf.cell(cell_width, 10, "SHOW YOUR CODE AT ENTRY POINT", new_x="LMARGIN", new_y="NEXT")

    pdf.output(f"ticket_{order_no}.pdf")

    print()
    print("Generating ticket...")
    print(f"ticket_{order_no}.pdf successfully generated.")


if __name__ == "__main__":
    main()
