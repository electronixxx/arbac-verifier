class CR:
    def __init__(self, rA, rT):
        self.rA = rA
        self.rT = rT
    
    def getAllMentionedRoles(self):
        return {self.rA} | {self.rT}

    @staticmethod
    def parse(rule):
        R = rule[1:-1].split(',')
        return CR(R[0], R[1])