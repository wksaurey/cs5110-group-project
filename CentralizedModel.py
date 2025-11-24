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
    
    #helper functions
    def phi1(self, v):
        #φ₁(t) = φ₀ + λ₁ v
        return self.phi0 + self.lambda1 * v

    def phi(self, v):
        #φ(t) = φ₁(t) − τ t² / T²
        return self.phi1(v) - self.tau * (self.t**2) / (self.T**2)

    def cost_preservation(self, v):
        #Cᵥ = λ₂ v
        return self.lambda2 * v

    def D1(self, P1, P2, v):
        #Demand for retailer
        return (
            self.mu * self.D
            - self.a * P1
            + self.b * P2
            + self.lambda3 * self.phi(v)
        )

    def D2(self, P1, P2, v):
        #Demand for supplier
        return (
            (1 - self.mu) * self.D
            - self.a * P2
            + self.b * P1
            + self.lambda3 * self.phi(v)
        )


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