# functions go here...

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


def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


def instructions():
    print(make_statement("Instructions", "ℹ️"))


# Main routine goes here
# ask user if they want to see instructions
print()
want_instructions = yes_no("Do you want to see instructions? ")

if want_instructions == "yes":
    instructions()

print()
