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
    slope: float = 10.0
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

    # Calculate the Preservation effot, nu (same as paper)
    def calc_nu(self):
        parta = ((4*self.a*self.L2)*(self.a-self.b))/((3*self.a+self.b)*(self.L1*self.L3)**2)
        partb = ((self.a*(2-self.mu)+self.b*self.mu)*self.D)/((3*self.a+self.b)*self.L1*self.L3)
        partc = ((self.a-self.b)*self.C)/(self.L1*self.L3)
        partd = ((self.phi0*self.T**2)-(self.t**2*self.tau))/(self.L1*self.T**2)
        return parta - partb + partc - partd

    # Calculate the ideal Wholesale Price (same as paper)
    def calc_w(self):
        part1 = (2*self.a*self.L2)/((3*self.a+self.b)*self.L1*self.L3)
        part2 = ((2*self.a+self.b)*(1-2*self.mu)*self.D)/(2*(self.a+self.b)*(3*self.a+self.b))
        return part1 - part2 +self.C

    # Calculate ideal quantities for the retailer and supplier
    def get_quantities(self):
        q1, q2 = sp.symbols('q1 q2') # Define symbols

        # Profit functions - Price is linear P = a - bQ
        pr = (self.D - self.slope * (q1 + q2))*q1 - self.W*q1
        ps = (self.D - self.slope * (q1 + q2))*q2 - self.C*q2 + (self.W-self.C)*q1 -self. Cv

        # Take derivative of profit with respect to own quantity and set to zero -> dp/dq = 0
        br1 = sp.diff(pr, q1)
        br2 = sp.diff(ps, q2)

        # Solve the system using fsolve
        br1_func = sp.lambdify((q1, q2), br1)
        br2_func = sp.lambdify((q1, q2), br2)
        def cournot_equilibrium_equations(q):
            return [br1_func(q[0], q[1]), br2_func(q[0], q[1])]
        
        initial_guess = [10, 10]
        equilibrium_quantities = fsolve(cournot_equilibrium_equations, initial_guess)
        qr = equilibrium_quantities[0].item() # extract from numpy
        qs = equilibrium_quantities[1].item() # extract from numpy

        return qr, qs

    # profit = p*qr - W*qr
    def retailer_profit(self):
        return self.p*self.qr - self.W*self.qr

    # profit = p*qs - C*qs + (W-C)*qr
    def supplier_profit(self):
        return self.p*self.qs + (self.W - self.C)*self.qs - self.Cv

    # Total profit will be the sum of the two minus the preservation effort cost
    def total_profit(self):
        return self.retailer_profit() + self.supplier_profit()

    # p = a - b*Q
    def calc_price(self):
        return self.D - self.slope * (self.qr + self.qs)

    # Q = qr + qs
    def output(self):
        return self.Q

    def summary(self):
        return {
            "P1*": self.p,
            "P2*": self.p,
            "W" : self.W,
            "v*": self.nu,
            "s_prof*": self.supplier_profit(),
            "r_prof*": self.retailer_profit(),
            "profit*": self.total_profit(),
            # "Q": self.output()
        }

if __name__ == '__main__':
    cournot = Cournot()
    print(cournot.summary())
    