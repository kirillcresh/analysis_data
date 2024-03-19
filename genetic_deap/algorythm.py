import random
from deap import creator, base, tools

min_weight = 1
max_weight = 10
prices = [100, 400, 140]
budget = 3000
tastiness = [10, 100, 80]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, min_weight, max_weight)
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

total_cost = sum([p * w for p, w in zip(prices, toolbox.population)])
if total_cost <= budget and all(min_weight <= w <= max_weight for w in individual):
    summ = sum([t * w for t, w in zip(tastiness, individual)])
else:
    summ = (0.0,)

toolbox.register("evaluate", summ)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selNSGA2)

population = toolbox.population(n=50)
hof = tools.HallOfFame(1)
for ind in population:
    ind.fitness.values = toolbox.evaluate(ind)

print(f"Самое вкусное: {hof}")
print(f"Суммарная вкусность: {hof.fitness.values[0]}")