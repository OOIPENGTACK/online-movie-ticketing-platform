# Online Movie Ticketing Platform
## Description:
This program simulates an online movie ticketing platform of a cinema in real life, operating within the cinema's own website or mobile application, where the audiences can buy movie tickets and book their desired theatre's seats from.
## How does it work?
This program first displays a list of movies currently showing on screen, followed by prompting the user for their choice of movie. After the user inputs a valid movie choice, the program then displays a list of time slots available corresponding to that selected movie, followed by prompting the user for their choice of time slot.

After the user inputs a valid time slot, a seating map of the theatre, designed with seats (depicted as "□") from Rows A to E and column 1 to 10, is displayed to the user for selection. After the user enters both a valid row and column (e.g. A5), the selected seat is then marked as reserved (depicted as "■"), and then the user gets to choose whether to further book multiple seats or not. If the user repeatedly selects an already taken seat, the program will then display an error message and prompts the user to select another seat instead. Once the seat selection phase is completed, the program will then move forward to the payment processing stage.

The program will indicate to the user the total costs of booked seats, and then prompts the user for their input of a preferred payment methods out of the three available, namely credit card, PayPal and bank transfer. Under the credit card payment method, the user must provide a valid format of credit card details, such as card number (16 digits), name on card, expiry date (MM/YY), CVV (3 digits) as well as user's email address in order to proceed further, just like most of the online credit card payment methods in real life are where there is usually not much flexibility given. As for PayPal and bank transfer, the program has no validation measure implemented in place and will simply approve the payment instead, as it assumes the user to be redirected to an external site of either PayPal or bank transfer gateway for processing the payment.

Once the payment step is completed, the program will generate a booking confirmation containing the information of Order No, Movie, Timeslot, Seat, Total, Transaction Date and Transaction Time. Finally, the program will also generate a movie ticket to the user, in the form of PDF file and with a QR code embedded in it for the user to show it at the theatre's entry point when attending the movie.
## Libraries
**fpdf2**: `fpdf2` is a PDF creation library for Python.. [**READMORE**](https://pypi.org/project/fpdf2/)

**qrcode**: Pure python QR Code generator.. [**READMORE**](https://pypi.org/project/qrcode/)

**tabulate**: Pretty-print tabular data in Python, a library and a command-line utility. [**READMORE**](https://pypi.org/project/tabulate/)

**validator-collection**: The Validator Collection is a Python library that provides more than 60 functions that can be used to validate the type and contents of an input value. [**READMORE**](https://pypi.org/project/validator-collection/)
## Installing Libraries
To install the required libraries, run:

``pip install -r requirements.txt``
## Important Functions
### display_movies() function:
This function prints out a list of movies currently showing on screen in sorted order, prompts the user for their choice of movie and then returns the `selected_movie`. Unless a valid input of movie selection is provided, the infinite loop `while True` within the function will continue to re-prompt the user until they oblige.
### select_time_slot(selected_movie) function:
This function prints out a list of time slots corresponding to the `selected_movie`, prompts the user for their choice of time slot and then returns the `selected_time`. Unless a valid input of time slot is provided, the infinite loop `while True` within the function will continue to re-prompt the user until they oblige.
### seat_selection():
This function initializes `ticket_price = 18` (i.e. $18.00), `total = 0`, and `seat_no = []`, and then prompts the user to input their desired `row` and `column`, followed by calling the `validate_seat(row, column)` function to validate if both inputs are valid. Next, it further calls the `booking_seat(row, column, ticket_price, total, seat_no, seats)` function to verify if the seat is already taken, and if not, to reserve that seat, updates the total costs `total` and appends the selected seat to the empty list `seat_no`. Finally, the program asks if the user would like to select multiple seats, which will then repeat the entire booking process, if the user selects "Y" as Yes. This function returns `seat_no` and `total` in the end.
### validate_seat(row, column):
This function returns `True` if:
* the user's input of `row` is between A to E; and
* `column` is a digit between 1 to 10.
### booking_seat(row, column, ticket_price, total, seat_no, seats):
```
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
```
This function verifies if the user's input of a seat is already taken. If the seat is still available, the function will "mark" the selected seat as booked (depicted as "■"), updates the total costs with `total += ticket_price` and append the booked seat to `seat_no = []`. It returns `True` (`False` for taken seat), `total` and `seat_no`.

Since the user is required to select an alphabet between `A` to `E` for the seat row, and with the seat row `A` begins at the 4th (i.e. index `3`) element of the `seats` list (see above), [**ord(c)**](https://docs.python.org/3/library/functions.html#ord) function is being used here to convert the row letters (`A`, `B`, `C`, `D` & `E`) to the Unicode integer value as index numbers. Therefore, with the seat row index formula as `row_index = ord(row) - ord("A") + 3`, of which `ord("A")` is returning the Unicode interger value of `65`, the function is able to index into the correct rows in the `seats` list, say index `5` (i.e. 6th element) of the `seats` list, if the user chooses row `C`.
### process_payment(total):
This function prompts the user to select a preferred payment method for the payment of total costs out of the three available options, namely `Credit Card`, `PayPal` and `Bank Transfer`. If the user chooses `Credit Card`, the function will call the `credit_card_payment()` function to further validate the user's input of personal and card details etc. If the user chooses `Paypal` or `Bank Transfer` instead, the function will simply print out the selected method is successful without any validation process, based on the assumption that both `PayPal` or `Bank Transfer` are to be redirected to external site of payment gateway for payment processing.
### credit_card_payment():
This function uses infinite loops `while True` to force the user into providing:
* a valid card number `card_number` (16 digits).
* a valid name on card `name_on_card`.
* a valid expiry date `expiry` (MM/YY).
* a valid `CVV` (3 digits).
* a valid email address by calling `validate_email(email)` function to validate.
### validate_email(email):
This function uses the [**validator-collection**](https://pypi.org/project/validator-collection/) from PyPI together with `try` and `except` block to validate and returns the user's email address if found valid, or, if found invalid, to raise (i.e. propagate) any `errors.InvalidEmailError` and `errors.EmptyValueError` found back to the `credit_card_payment()` function for handling.
### create_confirmation(selected_movie, selected_time, seat_no, total):
This function generates a movie booking confirmation pretty-printed in table formatted as ASCII art using `tabulate`, a package on PyPI at [pypi.org/project/tabulate](https://pypi.org/project/tabulate/). The confirmation is formatted using the library's `fancy_grid` format. It contains the information of `Order No`, `Movie`, `Timeslot`, `Seat`, `Total`, `Transaction Date` and `Transaction Time`. The `Order No` is generated using the `random.randint(a, b)` function from the `random` module, whereas the `date.today()` and `datetime.now().strftime("%H:%M:%S")` functions from the `datetime` module are used to obtain `Transaction Date` and `Transaction Time` respectively. This function returns `order_no` and `formatted_time` in the end.
### create_ticket(order_no, selected_movie, selected_time, seat_no, total, formatted_time):
This function generates a movie ticket in a PDF file using [**fpdf2**](https://pypi.org/project/fpdf2/), with also an image of a QR code, generated using the  [**qrcode**](https://pypi.org/project/qrcode/) library, to be added / embedded into the PDF file itself. The ticket contains all the booking informations and details the same as provided in the booking confirmation above. The ticket PDF is named in the format of `ticket_order_no.pdf`, where `order_no` is based on the random order number generated in the `create_confirmation(selected_movie, selected_time, seat_no, total)` function above. The ticket also has a reminder of "SHOW YOUR CODE AT ENTRY POINT" located at the bottom of the qr code image within the movie ticket PDF itself.
