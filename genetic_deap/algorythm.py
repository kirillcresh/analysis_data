import random

from deap import algorithms, base, creator, tools

min_weight = 1
max_weight = 10
budget = 3000
prices = [100, 400, 140]
tastiness = [10, 100, 80]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, min_weight, max_weight)
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    total_cost = sum([p * w for p, w in zip(prices, individual)])
    if total_cost <= budget and all(min_weight <= w <= max_weight for w in individual):
        return (sum([t * w for t, w in zip(tastiness, individual)]),)
    else:
        return (0,)


toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selNSGA2)

population = toolbox.population(n=50)
hof = tools.HallOfFame(1)
for ind in population:
    ind.fitness.values = toolbox.evaluate(ind)
final_population, logbook = algorithms.eaSimple(
    population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, halloffame=hof, verbose=False
)

print(f"Лучшее решение: {hof[0]}")
result = [round(i) for i in hof[0]]
lost_budget = budget - result[0]*prices[0] - result[1]*prices[1] - result[2]*prices[2]
print("Остаток бюджета: ", lost_budget)
if lost_budget < 0:
    print("В данном решении есть погрешности, запустите генерацию еще раз!!")
print(f"Лучшее решение в целом количестве: {result}")
print(f"Суммарная вкусность: {hof[0].fitness.values[0]}")

