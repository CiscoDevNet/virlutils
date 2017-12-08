import random
import string

def generate_sim_id():
    return ''.join(random.choice(string.letters + string.digits) for _ in range(6))
