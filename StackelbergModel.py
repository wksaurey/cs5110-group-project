from abc import ABC, abstractmethod
from DecisionModel import DecisionModel


class StackelbergModel(DecisionModel):
    def retailer_profit(self, supplier_price, retailer_price, online_demand):
        return (supplier_price - retailer_price) * online_demand

    def supplier_profit(self, supplier_price, unit_cost, in_store_demand, wholesale_price, online_demand, preservation_cost):
        in_store_profit = (supplier_price - unit_cost) * in_store_demand
        online_demand = (wholesale_price - unit_cost) * online_demand 
        return in_store_demand + online_demand - preservation_cost

    def total_profit(self):
        pass

    def set_supplier_price():
        pass

"""
Player Choices:
    supplier_price
    retailer_price 
    preservation_efforts
    wholesale_price 

Set Data
    unit_cost 
    in_store_demand 
    online_demand 
    preservation_cost
"""