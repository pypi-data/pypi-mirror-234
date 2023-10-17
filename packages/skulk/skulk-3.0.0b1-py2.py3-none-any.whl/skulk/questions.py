
import sys
from bullet import Bullet, Check, YesNo, Input, colors
from skulk import util




def choose(prompt, choice_map, echo=True):
    
    labels = [x["label" ] for x in choice_map]
    labels.append("Exit")

    cli = Bullet(
        util.yellow(prompt), 
        choices = labels,
        bullet = " >",
        margin = 2,
        pad_right   = 5,
        bullet_color = colors.bright(colors.foreground["cyan"]),
        background_color = colors.background["black"],
        word_color = colors.foreground["blue"],
        background_on_switch = colors.background["black"],
        word_on_switch = colors.bright(colors.foreground["green"])
        )

    answer = cli.launch()
    if answer.lower() == "exit":
        sys.stdout.write("Exiting.\n")
        sys.exit(0)

    result = next((x for x in choice_map if x["label"] == answer), None)
    if echo:
        print( f'You chose: {result["label"]} ({result["value"]})' )
    print("\n")
    return next((x["value"] for x in choice_map if x["label"] == answer), None)


def wait(prompt):
    
    choose(
         util.yellow(f"{prompt}\nChoose 'Continue' when you are ready"), 
           [{"label": "Continue", "value":"continue"}],
           echo=False)
    
def input_string(prompt, validator=None, echo=True):
    
    prompt = util.yellow(f"{prompt} Type 'exit' to quit: ")
    valid = False
    while not valid:
        cli = Input(
            prompt,
            word_color = colors.bright(colors.foreground["green"])
        )
        
        answer = cli.launch()
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
    
    cli = YesNo(prompt , word_color = colors.foreground["green"])
    answer = cli.launch()
    if echo:
        print(f"Your answer was: {answer}")
    print("\n")
    return answer