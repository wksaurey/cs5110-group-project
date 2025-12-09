from CentralizedModel import Centralized
from StackelbergModel import StackelbergModel

print("----Centralized Model----")
centralized = Centralized()
stats = centralized.summary()
for item in stats:
    print(item, stats[item])
print("\n")

print("----Stackelberg Model----")
stackelbergModel = StackelbergModel()
stats = stackelbergModel.summary()
for item in stats:
    print(item, stats[item])
print("\n")


print("\n")
print("----Cournot Model----")