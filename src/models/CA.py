class CA:
    def __init__(self, rA, pos, neg, rT):
        self.rA = rA
        self.pos = pos
        self.neg = neg
        self.rT = rT

    def getAllMentionedRoles(self):
        res = set()
        res |= {self.rA}
        res |= self.pos
        res |= self.neg
        res |= {self.rT}
        return res

    @staticmethod
    def parse(rule):
        R = rule[1:-1].split(',')
        if R[1] == 'TRUE':
            return CA(R[0], set(), set(), R[2])
        pos = set()
        neg = set()
        conditions = R[1].split('&')
        for c in set(conditions):
            if c[0] == '-': neg = neg | {c[1:]}
            else: pos = pos | {c}
        return CA(R[0], pos, neg, R[2])