from DecisionModel import DecisionModel

class Cournot(DecisionModel):
    Q = None    # Total Output
    p = None    # Price
    qp = None   # q* = qr = qs
    a = None    # 
    b = None    # 
    C = None    # Marginal Cost

    def __init__(self, a=0.95, b=0.1, C=60):
        self.qp = (a-C)/3*b
        self.Q = self.qp + self.qp
        self.p = a - b*self.Q
        self.a = a
        self.b = b 
        self.C = C

    # profit = p*qr - C*qr
    def retailer_profit(self):
        return self.p*self.qp - self.C*self.qp

    # profit = p*qs - C*qs
    def supplier_profit(self):
        return self.p*self.qp - self.C*self.qp

    # Total profit = Q*p = Pi1+ Pi2
    def total_profit(self):
        return self.supplier_profit() + self.retailer_profit()

    # p = a - b*Q
    def price(self):
        return self.p

    # Q = qr + qs
    def output(self):
        return self.Q

    def summary(self):
        return {
            "P1*": self.retailer_profit(),
            "P2*": self.supplier_profit(),
            #"v*": self.optimal_v(),
            "profit*": self.total_profit()
        }

if __name__ == '__main__':
    cournot = Cournot()
    print(cournot.summary())