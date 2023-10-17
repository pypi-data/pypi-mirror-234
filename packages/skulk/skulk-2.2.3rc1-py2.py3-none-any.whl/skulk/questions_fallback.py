import sys
from skulk import util


def choose(prompt, choice_map, echo=True):
    """Present a list of choices to the user.
    
    The user makes a choice by entering a number.
    """
    labels = [x["label"] for x in choice_map]
    labels.append("Exit")

    num_options = len(labels)
    choice = 0
    while choice not in range(1, num_options + 1):
        print(prompt)
        for i, label in enumerate(labels):
            n = i + 1
            print(f"{n}: {label}")
        choice = input(util.green("Enter a number: "))
        if not choice.isdigit():
            choice = 0
        choice = int(choice)
        prompt = f"Please choose a number between 1 and {num_options}."

    answer = labels[choice - 1]
    if answer.lower() == "exit":
        sys.stdout.write("Exiting.\n")
        sys.exit(0)

    result = next((x for x in choice_map if x["label"] == answer), None)
    if echo:
        print(f'You chose: {result["label"]} ({result["value"]})')
    print("\n")
    return next((x["value"] for x in choice_map if x["label"] == answer), None)


def wait(prompt):
    """Wait for input from the user.
    """
    choose(
        util.yellow(f"{prompt}\nChoose 'Continue' when you are ready"),
        [{"label": "Continue", "value": "continue"}],
        echo=False,
    )


def input_string(prompt, validator=None, echo=True):
    """Prompt the user for a string."""
    prompt = util.green(f"{prompt} Type 'exit' to quit: ")
    valid = False
    while not valid:
        answer = input(prompt)

        if not answer:
            print("\n")
            continue
        if answer.lower() == "exit":
            sys.stdout.write("Exiting.\n")
            sys.exit(0)
        if not validator:
            valid = True
        else:
            problem = validator(answer)
            if problem:
                print(util.red(problem))
                valid = False
            else:
                valid = True
        if echo:
            print(f"You entered: {answer}")
        print("\n")

    return answer


def yes_no(prompt, echo=False):
    """Prompt the user for a yes/no answer."""
    answer = None
    while True:
        inp = input(f"[y/n] {util.green(prompt)}[y]: ")
        inp = inp.strip().lower()
        if not inp or inp.startswith("y"):
            answer = "y"
        elif inp.lower().startswith("n"):
            answer = "n"
        else:
            print(util.yellow("You must choose 'y' or 'n'"))

        if answer:
            if echo:
                print(f"Your answer was: ({answer})")
            return True if answer == "y" else False
