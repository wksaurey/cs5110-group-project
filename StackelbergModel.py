from DecisionModel import DecisionModel

class StackelbergModel(DecisionModel):
    phi0: float = 1       # φ0 - freshness
    lambda1: float = 0.3  # λ1 - preservation effectiveness
    lambda2: float = 55   # λ2 - 
    lambda3: float = 16   # λ3 - 
    tau: float = 2        # τ  - freshness decay
    T: float = 10         # T  - time
    t: float = 5          # t  - current time
    mu: float = 0.46      # μ  - online/offline ratio 
    a: float = 0.95       # price elasticity
    b: float = 0.1        # cross-price elasticity
    D: float = 100        # base market demand
    C: float = 60         # unit cost
    
    # made these and realized I didn't need them for optimized
    # keeping them for now just in case
    def phi1(self, v):
        #φ₁(t) = φ₀ + λ₁ v
        # v - preservation efforts
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

    # -- Model Specific --

    def retailer_profit(self, P1, P2, v, W):
        #pi₁ = (P1 − W) D1
        return (P1 - W) * self.D1(P1, P2, v)

    
    def supplier_profit(self, P1, P2, v, W):
        #pi2 = (P2 − C) D2
        return (P2 - self.C) * self.D2(P1, P2, v) + (W - self.C) * self.D1(P1, P2, v) - self.cost_preservation(v)

    
    def total_profit(self, P1, P2, v):
        return self.retailer_profit(P2, P2, v) + self.supplier_profit(P1, P2, v)
    
# optized equations
    def optimal_retailer(self):
        return (
            ((3 * self.a - self.b) * self.lambda2) 
            / ((3 * self.a + self.b) * self.lambda1 * self.lambda3) 
            - ((3 * self.a + 2 * self.b) * (1 - 2 * self.mu) * self.D) 
            / (2 * (self.a + self.b) * (3 * self.a + self.b)) 
            + self.C
        ) 

    def optimal_supplier(self):
        return (
            (2 * self.a * self.lambda2) 
            / ((3 * self.a + self.b) * self.lambda1 * self.lambda3) 
            + (self.a * (1 - 2 * self.mu) * self.D) 
            / (2 * (self.a + self.b) * (3 * self.a + self.b)) 
            + self.C
        ) 

    def optimal_W(self):
        return (
            (2 * self.a * self.lambda2) 
            / ((3 * self.a + self.b) * self.lambda1 * self.lambda3) 

            - ((2 * self.a + self.b) * (1 - 2 * self.mu) * self.D) 
            / (2 * (self.a + self.b) * (3 * self.a + self.b)) 

            + self.C
        ) 

    def optimal_v(self):
        return (
            (4 * self.a * self.lambda2 * (self.a - self.b))
            / ((3 * self.a + self.b) * (self.lambda1 * self.lambda3)**2)

            - ((self.a * (2 - self.mu) + self.b * self.mu) * self.D)
            / ((3 * self.a + self.b) * self.lambda1 * self.lambda3)

            + ((self.a - self.b) * self.C)
            / (self.lambda1 * self.lambda3)

            - ((self.phi0 * self.T**2) - (self.t**2 * self.tau))
            / (self.lambda1 * self.T**2)
        )

    def optimal_D1(self):
        # demand for supplier
        return ((self.a * (self.a - self.b) * self.lambda2)
                / ((3 * self.a + self.b) * self.lambda1 * self.lambda3)
                - (self.a * (1 - 2*self.mu) * self.D) / (2 * (3 * self.a + self.b)))

    def optimal_D2(self):
        return (((2 * self.a + self.b) * (self.a - self.b) * self.lambda2)
                / ((3 * self.a + self.b) * self.lambda1 * self.lambda3)
                - (self.a * (1 - 2*self.mu) * self.D) / (2 * (3 * self.a + self.b)))

    def optimal_retailer_profit(self):
        P1_opt = self.optimal_retailer()
        P2_opt = self.optimal_supplier()
        v_opt = self.optimal_v()
        W_opt = self.optimal_W()
        return self.retailer_profit(P1_opt, P2_opt, v_opt, W_opt)

    def optimal_supplier_profit(self):
        P1_opt = self.optimal_retailer()
        P2_opt = self.optimal_supplier()
        v_opt = self.optimal_v()
        W_opt = self.optimal_W()
        return self.supplier_profit(P1_opt, P2_opt, v_opt, W_opt)

    def optimal_profit(self):
        return self.optimal_retailer_profit() + self.optimal_supplier_profit()
    
    def summary(self):
        return {
            "P1*": self.optimal_retailer(),
            "P2*": self.optimal_supplier(),
            "W*": self.optimal_W(),
            "v*": self.optimal_v(),
            "s_prof*": self.optimal_supplier_profit(),
            "r_prof*": self.optimal_retailer_profit(),
            "profit*": self.optimal_profit()
        }


def print_items(stats):
    for item in stats:
        print(f'{item.ljust(8)} {round(stats[item], 2)}')


if __name__ == '__main__':
    stackelberg = StackelbergModel()
    print_items(stackelberg.summary())