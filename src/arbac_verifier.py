from models.CA import CA
from models.CR import CR
from timeit import default_timer as timer

class ArbacVerifier:
    def __init__(self, policy_location):
        with open(policy_location) as f: lines = f.readlines()
        self.roles = set(lines[0].split(' ')[1:-1])
        self.users = lines[2].split(' ')[1:-1]
        self.UA = set()
        self.CR = set(CR.parse(cr) for cr in lines[6].split(' ')[1:-1])
        self.CA = set(CA.parse(ca) for ca in lines[8].split(' ')[1:-1])
        self.goal = (lines[10].split(' ')[1:-1])[0]
        for ua in  lines[4].split(' ')[1:-1]:
            p = (ua[1:-1].split(','))
            self.UA.add((p[0], p[1]))
        self.found = False
        self.to_visit_states = [self.UA] # tracks to be visited states
        self.visited_states = set() # tracks already visited states

    def forward_slice(self):
        s_prev = {r for (u, r) in self.UA}
        reached_fixpoint = False
        while not reached_fixpoint:
            s_curr = set()
            CA_match = (ca for ca in self.CA if set({ca.rA} | ca.pos).issubset(s_prev))
            for ca in CA_match:
                s_curr = s_curr | s_prev | {ca.rT}
            if s_curr == s_prev: reached_fixpoint = True
            else: s_prev = s_curr
        rs = self.roles - s_curr # R\S*
        # remove from CA all the rules that mention any role in R\S* , unless this happens just in the negative preconditions
        self.CA -= {ca for ca in self.CA if any(r in rs for r in ca.getAllMentionedRoles() if r in ca.neg and r not in ca.pos)}
        # remove from CR all the rules that mention any role in R\S*
        self.CR -= {cr for cr in self.CR if any(r in rs for r in cr.getAllMentionedRoles())}
        # remove the roles in R\S* from the negative preconditions of all rules
        self.CA = set(CA(ca.rA, ca.pos, ca.neg - rs, ca.rT) for ca in self.CA)
        self.roles -= rs # delete the roles in R\S*

    def backward_slice(self):
        s_prev = {self.goal}
        reached_fixpoint = False
        while not reached_fixpoint:
            s_curr = set()
            CA_match = (ca for ca in self.CA if ca.rT in s_prev)
            for ca in CA_match:
                s_curr = s_curr | s_prev | ca.pos | ca.neg | {ca.rA}
            if s_curr == s_prev: reached_fixpoint = True
            else: s_prev = s_curr
        rs = self.roles - s_curr # R\S*
        self.CA -= {ca for ca in self.CA if ca.rT in rs} # remove from CA all the rules that assign a role in R\S*
        self.CR -= {cr for cr in self.CR if cr.rT in rs} # remove from CR all the rules that revoke a role in R\S*
        self.roles -= rs # delete the roles in R\S*


    def update(self, current_ua, updated_ua): # expand/reduce the to visit states if the updated user-role set is changed
        if current_ua != updated_ua: self.to_visit_states.append(updated_ua)

    def assign(self, uT, ca, ua):
        UR_target = {r for (u, r) in ua if u == uT} # all the current roles of target
        pc1 = ca.rA in {rA for (uA, rA) in ua} # precondition
        c1 = ca.pos <= UR_target # conditions
        c2 = ca.neg & UR_target == set()
        c3 = ca.rT not in UR_target
        if pc1 and c1 and c2 and c3: self.update(ua, ua | {(uT, ca.rT)}) # adds the newly assigned ur only if its not already in the to-visit states

    def revoke(self, uT, cr, ua):
        UR_target = {r for (u, r) in ua if u == uT} # all the current roles of target
        pc1 = cr.rA in {rA for (uA, rA) in ua} # precondition
        c1 = cr.rT in UR_target # condition
        if pc1 and c1: self.update(ua, ua - {(uT, cr.rT)})  # removes the revoked ur only if its already in the to-visit states

    def verifyReachability(self, rule_nr):
        start = timer()
        nr_roles, nr_ca, nr_cr = len(self.roles), len(self.CA), len(self.CR) # previous number of roles, CA and CR rules
        self.forward_slice()
        self.backward_slice()
        print('----------------------------------------------------------------------------------------------------------')
        print(f'Testing reachability of {rule_nr}')
        print(f'Forward and Backward slicing applied. Reductions made: [Nr Roles by {nr_roles - len(self.roles)}] | [CA Rules by {nr_ca - len(self.CA)}] | [CR Rules by {nr_cr - len(self.CR)}]')
        print(f'Number of states reduced from {pow(2, nr_roles * len(self.users))} to {pow(2, len(self.roles) * len(self.users))}')
        while len(self.to_visit_states) > 0 and not self.found: # loop until there are no more states to visit and unless the goal is reachable
            current_state = self.to_visit_states.pop()
            already_explored = hash(frozenset(current_state)) in self.visited_states # checks if state is already visited in past
            if already_explored: continue
            if self.goal in {role for (user, role) in current_state}: self.found = True # check if role is reached in current state
            self.visited_states.add(hash(frozenset(current_state))) # mark current state as visisted
            for ca in self.CA: # for each Can-Assign Rule
                for user in {user for (user, role) in current_state if role == ca.rA}: # for each person who can assign a role for the current state
                    for target in self.users: # for each user
                        self.assign(target, ca, current_state) # try to assign the role to the target
            for cr in self.CR:  # for each Can-Revoke Rule
                for user in {user for (user, role) in current_state if role == cr.rA}: # for each person who can revoke a role for the current state
                    for target in self.users: # for each user
                        self.revoke(target, cr, current_state) # try to revoke the role to the target
        end = timer()
        if self.found: print(f'Role reachable. Found in {end-start} seconds.')
        else: print(f'Role not reachable. Found in {end-start} seconds.')
        print('----------------------------------------------------------------------------------------------------------\n')
        return self.found