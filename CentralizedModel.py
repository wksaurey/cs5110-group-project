import DecisionModel

class Centralized(DecisionModel):
    phi0: float = 1        # φ0
    lambda1: float = 0.3   # λ1
    lambda2: float = 55   # λ2
    lambda3: float = 16   # λ3
    tau: float = 2        # τ
    T: float = 10         # T
    t: float = 5         # current time
    mu: float = 0.46     # μ
    a: float = 0.95      # price elasticity
    b: float = 0.1       # cross-price elasticity
    D: float = 100       # base market demand
    C: float = 60        # unit cost
    
    def retailer_profit(self, P1, P2, v):
        #pi₁ = (P1 − C) D1
        return (P1 - self.C) * self.D1(P1, P2, v)

    
    def supplier_profit(self, P1, P2, v):
        #pi2 = (P2 − C) D2
        return (P2 - self.C) * self.D2(P1, P2, v)

    
    def total_profit(self, P1, P2, v):
        return (
            (P1 - self.C) * self.D1(P1, P2, v)
            + (P2 - self.C) * self.D2(P1, P2, v)
            - self.cost_preservation(v)
        )