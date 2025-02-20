import pandas
from tabulate import tabulate
from datetime import date


# functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def yes_no(question):
    """Checks that users enter yes / y  or no/ n to a question"""

    while True:
        response = input(question).lower()

        if response == "yes" or response == "y":
            return "yes"
        elif response == "no" or response == "n":
            return "no"
        else:
            print("Please enter yes (y) or no (n).\n")


def instructions():
    print(make_statement("Instructions", "ℹ️"))


def not_blank(question):
    """check user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("sorry, this can't be blank.")


def num_check(question, num_type="float", exit_code=None):
    """checks that response is a float / integer more than zero"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        response = input(question)

        # check for the exit code
        if response == exit_code:
            return response

        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def get_expenses(exp_type, how_many=1):
    """gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # list for pandas
    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    # expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Item": all_dollar_per_item
    }

    # defaults for fixed expenses
    amount = how_many  # how_many defaults into 1
    how_much_question = "How much? $"

    # loop to get expenses
    while True:

        # get item name and check it's not blank
        item_name = not_blank("Item Name: ")

        # check users enter at least one variable expense
        # NOTE: if you type the conditions without the brackets,
        # all on one line and then add in enters,
        # pycharm will add in the brackets automatically.
        if ((exp_type == "variable" and item_name == "xxx")
                and len(all_items) == 0):
            print("Oops - you have not entered anything. "
                  "You need at least one item.")
            continue

        elif item_name == "xxx":
            break

        # get variable expenses item amount enter defaults to number of products being made
        if exp_type == "variable":
            amount = num_check(f"How many <enter for {how_many}>: ",
                               "integer", "")

            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"

        price_for_one = num_check(how_much_question, "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)

    # make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # calculate cost column
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    # calculate subtotal
    sub_total = expense_frame['Cost'].sum()

    # apply currency formatting to currency columns.
    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # make expense frame into a string with desired columns
    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return all items
    return expense_string, sub_total


# currency formatting
def currency(x):
    return "${:.2f}".format(x)


# main routine goes here

# assume we have no fixed expenses
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Fund Raising Calculator", "💰"))

print()
want_instructions = yes_no("Do you want to see instructions? ")

if want_instructions == "yes":
    instructions()

print()

product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ",
                          "integer")


print("Lets get variable expenses...")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print()
has_fixed = yes_no("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"


# get profit goal here

# string / output area

# *** get current date for heading and filename***
today = date.today()

# get day month and year
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%y")

# headings / strings..
main_heading_string = make_statement(f"Fund Raising Calculator "
                                     f"({product_name}, {day}/{month}/{year})", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement("Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: {fixed_subtotal:.2f}"

# set fixed cost string to blank if we don't have fixed cost
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal : $0.00"

# list of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string]

# print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)
file_name = f"{product_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")
