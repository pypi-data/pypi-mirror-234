import math

# helper functions

# returns q value as defined in the error analysis section
def get_q(mass_w, mass_w_a, t):
    return ((mass_w - mass_w_a) / t)


def get_area_by_arc(diameter=None, radius=None):
    if radius:
        diameter = radius * 2
    if not diameter:
        return 0
    return (math.pi * (diameter**2) * (1/4))


def get_delta_q_q(delta_m=0, m=0, delta_t=0, t=0):
    return math.sqrt(((delta_m/m) ** 2) + ((delta_t/t) ** 2))


def get_delta_a_a(a, delta_a):
    return math.sqrt(delta_a/a) ** 2


def get_delta_k_k(delta_q_q, delta_a_a):
    return math.sqrt(delta_q_q**2 + delta_a_a**2)

