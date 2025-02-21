import pandas
import random


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    print(f"{decoration * 3} {statement} {decoration * 3}")


# functions go here
def string_check(question, valid_answers=('yes', 'no'),
                 num_letters=1):
    """checks that users enter the full word or the
    'n' letter/s of a word from a list of valid responses"""

    while True:

        response = input(question).lower()

        for item in valid_answers:

            # check if the response is the entire word
            if response == item:
                return item

            # check if it's the 'n' letter
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from {valid_answers}")


def instructions():
    make_statement("Instructions", "ℹ️")

    print('''
    
For each ticket holder enter...
- Their name
- Their age
- The payment method (cash / credit)

The program will record the ticker sale
 and calculate the ticket cost (and the profit).
 
 Once you have either sold all of the tickets or 
 entered the exit coe ('xxx'), the program will display
 the ticket sales information and write the data to a text file.
 
 It will also choose one lucky ticket holder who wins the
 draw (their ticket is free).
 
''')


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again.\n")


def int_check(question):
    """checks user enter an integer"""

    error = "Oops - please enter an integer"

    while True:
        response = input(question).lower()

        # check for the exit code
        if response == "xxx":
            return response

        try:
            # change the response to an integer and check that it's more than zero
            response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


# currency formatting
def currency(x):
    return "${:.2f}".format(x)


# main routine goes here

# initialise ticket numbers
MAX_TICKETS = 5
tickets_sold = 0

# initialise variables / non-default options for string checker
payment_ans = ('cash', 'credit')

# TICKET PRICE LIST
CHILD_PRICE = 7.50
ADULT_PRICE = 10.50
SENIOR_PRICE = 6.50

# credit card surcharge (5%)
CREDIT_SURCHARGE = 0.05

# lists to hold ticket details
all_names = []
all_ticket_costs = []
all_surcharges = []

mini_movie_diet = {
    'Name': all_names,
    'Ticket Price': all_ticket_costs,
    'Surcharge': all_surcharges
}

# program main heading
make_statement("Mini-Movie Fundraiser Program", "🍿")

# ask user if they want to see instructions
print()
want_instructions = string_check("Do you want to see instructions? ")

if want_instructions == "yes":
    instructions()

print()

# loop to get name, age and payment details
while tickets_sold < MAX_TICKETS:
    # as user for their name ( and check it's not blank)
    print()
    name = not_blank("Name: ")

    # if name is exit code, break out of loop
    if name == "xxx":
        break

    # asks for their age and check it's between 12 and 120
    age = int_check("Age: ")

    # Output error message / success message
    if age < 12:
        print(f"{name} is too young")
        continue

    # child price is $7.50
    elif age < 16:
        ticket_price = CHILD_PRICE

    # adult price is $10.50
    elif age < 65:
        ticket_price = ADULT_PRICE

    # senior price is $6.50
    elif age < 121:
        ticket_price = SENIOR_PRICE

    else:
        print(f"{name} is too old")
        continue

    # ask user for payment method (credit/cash/cr/ca)
    pay_method = string_check("Payment Method: ", payment_ans, 2)

    # paying by cash no surcharge
    if pay_method == "cash":
        surcharge = 0

    # if paying credit, calculate surcharge
    else:
        surcharge = ticket_price * CREDIT_SURCHARGE

    # add name ticket cost and surcharge
    all_names.append(name)
    all_ticket_costs.append(ticket_price)
    all_surcharges.append(surcharge)

    tickets_sold += 1

# end of ticket loop

# create dataframe / table from dictionary
mini_movie_frame = pandas.DataFrame(mini_movie_diet)

# calculate the total payable for each ticket
mini_movie_frame['Total'] = mini_movie_frame['Ticket Price'] + mini_movie_frame['Surcharge']
mini_movie_frame['Profit'] = mini_movie_frame['Ticket Price'] - 5

# work out total paid and total paid...
total_paid = mini_movie_frame['Total'].sum()
total_profit = mini_movie_frame['Profit'].sum()

# currency formatting
add_dollars = ['Ticket Price', 'Surcharge', 'Total', 'Profit']
for var_item in add_dollars:
    mini_movie_frame[var_item] = mini_movie_frame[var_item].apply(currency)

print(mini_movie_frame.to_string(index=False))

print()
print(f"Total Paid: ${total_paid:.2f}")
print(f"Total Profit: ${total_profit:.2f}")


# choose random winner...
winner = random.choice(all_names)

# find index of winner ( ie: position in list)
winner_index = all_names.index(winner)
print("winner", winner, "list position", winner_index)

# find total won
total_won = mini_movie_frame.at[winner_index, 'Total']

# winner announcement
print(f"The lucky winner is {winner}. Their ticket is worth ${total_won} is free!!")


if tickets_sold == MAX_TICKETS:
    print(f"You have sold all the tickets (ie: {MAX_TICKETS} tickets")
else:
    print(f"You have sold {tickets_sold} / {MAX_TICKETS} tickets.")
