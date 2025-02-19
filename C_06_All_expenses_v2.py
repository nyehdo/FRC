import pandas
from tabulate import tabulate


# functions go here


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

quantity_made = num_check("Quantity being made: ",
                          "integer")

print()

print("Getting variables costs...")
variable_expenses = get_expenses("variable", quantity_made)
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print("Getting Fixed Cost...")
fixed_expenses = get_expenses("fixed")
print()
fixed_panda = fixed_expenses[0]
fixed_subtotal = fixed_expenses[1]

# temporary output area

print("=== Variable Expenses ===")
print(variable_panda)
print(f"Variable subtotal: ${variable_subtotal:.2f}")
print()

print("=== Fixed Expenses ===")
print(fixed_panda)
print(f"Fixed subtotal: ${fixed_subtotal:.2f}")

print()
total_expenses = variable_subtotal + fixed_subtotal
print(f"Total Expenses: ${total_expenses:.2f}")
