from abc import ABC, abstractmethod

# Implementation
# class Cournot(DecisionModel):
#     def classes(self):
#         return "etc"
class DecisionModel(ABC):
    @abstractmethod
    def retailer_profit(self):
        pass

    @abstractmethod
    def supplier_profit(self):
        pass

    @abstractmethod
    def total_profit(self):
        pass
