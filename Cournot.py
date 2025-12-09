from DecisionModel import DecisionModel

from scipy.optimize._lsq.trf_linear import qr
import sympy as sp
from scipy.optimize import fsolve

class Cournot(DecisionModel):
    phi0: float = 1     # φ0
    L1: float = 0.3     # λ1
    L2: float = 55      # λ2
    L3: float = 16      # λ3
    tau: float = 2      # τ
    T: float = 10       # T
    t: float = 5        # current time
    mu: float = 0.46    # μ
    a: float = 0.95     # price elasticity
    b: float = 0.1      # cross-price elasticity
    D: float = 100      # base market demand
    C: float = 60       # unit cost
    slope: float = 1.0
    nu = None
    Cv = None
    W = None
    qs = None
    qr = None
    p = None
    Q = None

    def __init__(self):
        self.nu = self.calc_nu()
        self.Cv = self.nu*self.L2
        self.W = self.calc_w()
        self.qr, self.qs = self.get_quantities()
        self.p = self.calc_price()
        self.Q = self.qr + self.qs

    def calc_nu(self):
        parta = ((4*self.a*self.L2)*(self.a-self.b))/((3*self.a+self.b)*(self.L1*self.L3)**2)
        partb = ((self.a*(2-self.mu)+self.b*self.mu)*self.D)/((3*self.a+self.b)*self.L1*self.L3)
        partc = ((self.a-self.b)*self.C)/(self.L1*self.L3)
        partd = ((self.phi0*self.T**2)-(self.t**2*self.tau))/(self.L1*self.T**2)
        return parta - partb + partc - partd

    def calc_w(self):
        part1 = (2*self.a*self.L2)/((3*self.a+self.b)*self.L1*self.L3)
        part2 = ((2*self.a+self.b)*(1-2*self.mu)*self.D)/(2*(self.a+self.b)*(3*self.a+self.b))
        return part1 - part2 +self.C

    def total_profit(self, P,q1):
        return (P-self.W)*q1 + (P-self.c)*(self.D-q1) + (self.W-self.C)*q-self.Cv

    def get_quantities(self):
        # Define symbols
        q1, q2 = sp.symbols('q1 q2')

        # Market demand function (example: linear demand P = a - bQ)
        # P = D - (q1 + q2)

        # Profit functions
        # Profit = (Price * Quantity) - (Cost * Quantity)
        pr = (self.D - self.slope * (q1 + q2)) * q1 - self.C * q1
        ps = (self.D - self.slope * (q1 + q2)) * q2 - self.W * q2

        # Derive best response functions by taking the first derivative of profit
        # with respect to own quantity and setting it to zero.
        # d(profit1)/dq1 = 0
        # d(profit2)/dq2 = 0
        br1 = sp.diff(pr, q1)
        br2 = sp.diff(ps, q2)

        # Convert best response functions to numerical functions for fsolve
        br1_func = sp.lambdify((q1, q2), br1)
        br2_func = sp.lambdify((q1, q2), br2)

        # Define a system of equations to solve for the Cournot equilibrium
        def cournot_equilibrium_equations(q):
            return [br1_func(q[0], q[1]), br2_func(q[0], q[1])]

        # Solve the system using fsolve
        initial_guess = [10, 10]  # Initial guess for quantities
        equilibrium_quantities = fsolve(cournot_equilibrium_equations, initial_guess)
        qr = equilibrium_quantities[0].item()
        qs = equilibrium_quantities[1].item()

        return qr, qs

    # profit = p*qr - C*qr
    def retailer_profit(self):
        return self.p*self.qr - self.W*self.qr

    # profit = p*qs - C*qs
    def supplier_profit(self):
        return self.p*self.qs + (self.W - self.C)*self.qs - self.Cv

    # Total profit = Q*p = Pi1+ Pi2
    def total_profit(self):
        return self.supplier_profit() + self.retailer_profit()

    # p = a - b*Q
    def calc_price(self):
        return self.D - self.slope * (self.qr + self.qs)

    # Q = qr + qs
    def output(self):
        return self.Q

    def summary(self):
        return {
            "P1*": self.retailer_profit(),
            "P2*": self.supplier_profit(),
            "v*": self.calc_nu(),
            "W" : self.calc_w(),
            "profit*": self.total_profit()
        }

if __name__ == '__main__':
    cournot = Cournot()
    print(cournot.summary())
