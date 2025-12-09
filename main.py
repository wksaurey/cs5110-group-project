from CentralizedModel import Centralized
from StackelbergModel import StackelbergModel
from Cournot import Cournot

def main():
    print("----Centralized Model----")
    centralized = Centralized()
    stats = centralized.summary()
    print_items(stats)
    print("\n")

    print("----Stackelberg Model----")
    stackelbergModel = StackelbergModel()
    stats = stackelbergModel.summary()
    print_items(stats)
    print("\n")

    print("----Cournot Model----")
    cournot = Cournot()
    stats = cournot.summary()
    print_items(stats)

def print_items(stats):
    for item in stats:
        print(f'{item.ljust(8)} {round(stats[item], 2)}')

main()