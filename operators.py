import random

def make_chromosome(n):
    c = list(range(n))
    random.shuffle(c)
    return c

def select(pop, fits, k=5):
    picked = random.sample(range(len(pop)), k)
    winner = min(picked, key=lambda i: fits[i])
    return pop[winner][:]

def crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b+1] = p1[a:b+1]
    seen = set(child[a:b+1])
    fill = (g for g in p2 if g not in seen)
    return [next(fill) if x is None else x for x in child]

def swap_mut(chrom, rate=0.01):
    c = chrom[:]
    if random.random() < rate:
        i, j = random.sample(range(len(c)), 2)
        c[i], c[j] = c[j], c[i]
    return c

def inversion_mut(chrom, rate=0.05):
    c = chrom[:]
    if random.random() < rate:
        i, j = sorted(random.sample(range(len(c)), 2))
        c[i:j+1] = c[i:j+1][::-1]
    return c
