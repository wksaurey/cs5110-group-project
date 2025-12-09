from DecisionModel import DecisionModel

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
    
    # made these and realized I didn't need them for optimized
    # keeping them for now just in case
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
    
# optized equations
    def optimal_retailer(self):
        return (self.lambda2 / (2 * self.lambda1 * self.lambda3)
                - (1 - 2 * self.mu) * self.D / (4 * (self.a + self.b))
                + self.C)

    def optimal_supplier(self):
        return (self.lambda2 / (2 * self.lambda1 * self.lambda3)
                + (1 - 2 * self.mu) * self.D / (4 * (self.a + self.b))
                + self.C)

    def optimal_v(self):
        # optimal preservation
        P1 = self.optimal_retailer()
        P2 = self.optimal_supplier()

        numerator = (
            self.lambda3 * self.tau * self.t**2 / self.T**2
            + 2*self.a*P1
            - 2*self.b*P2
            - self.mu*self.D
            - (self.a - self.b)*self.C
            - self.lambda3*self.phi0
        )
        return numerator / (self.lambda1 * self.lambda3)

    def optimal_D1(self):
        # demand for supplier
        return ((self.a - self.b)*self.lambda2
                / (2*self.lambda1*self.lambda3)
                - (1 - 2*self.mu)*self.D / 4)

    def optimal_D2(self):
        return ((self.a - self.b)*self.lambda2
                / (2*self.lambda1*self.lambda3)
                + (1 - 2*self.mu)*self.D / 4)

    def optimal_profit(self):
        term1 = ((1 - 2*self.mu)*self.D)**2 / (8*(self.a + self.b))

        term2 = -(self.a - self.b)*(self.lambda2**2) / (2*(self.lambda1*self.lambda3)**2)

        term3 = (
            self.lambda2 * (
                self.D*self.T**2
                - 2*(self.a - self.b)*self.C*self.T**2
                + 2*self.lambda3*(self.phi0*self.T**2 - self.t**2*self.tau)
            )
        ) / (2*self.lambda1*self.lambda3*self.T**2)

        return term1 + term2 + term3
    
    def summary(self):
        return {
            "P1*": self.optimal_retailer(),
            "P2*": self.optimal_supplier(),
            "v*": self.optimal_v(),
            "profit*": self.optimal_profit()
        }

# model = Centralized()
# print(model.summary())