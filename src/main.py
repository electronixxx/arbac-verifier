from arbac_verifier import ArbacVerifier
from timeit import default_timer as timer

flag = []
policies = [
    "policy1.arbac",
    "policy2.arbac",
    "policy3.arbac",
    "policy4.arbac",
    "policy5.arbac",
    "policy6.arbac",
    "policy7.arbac",
    "policy8.arbac"
]

start = timer()
for policy in policies:
    verifier = ArbacVerifier(f'../policies/{policy}')
    reachable = verifier.verifyReachability(policy)
    if reachable: flag.append(1)
    else: flag.append(0)
end = timer()

print('\n\nFlag: ', end='')
for c in flag: print(c, end='')
print(f' found in {end-start} seconds.')