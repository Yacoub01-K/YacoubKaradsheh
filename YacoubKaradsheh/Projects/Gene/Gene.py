
import random
import turtle
from deap import base, creator, tools
CANVAS_SIZE = 500
DENSITY = 12
POPULATION_SIZE = 3
NUM_GENERATIONS = 3
CXPB = 0.2
MUTPB = 0.4

t = turtle.Turtle()
s = turtle.Screen()
s.bgcolor("black")
s.setup(CANVAS_SIZE, CANVAS_SIZE)

t.penup()
def draw_line(row, col, color):
    x1 = row - CANVAS_SIZE / 2
    y1 = col - CANVAS_SIZE / 2
    x2 = x1 + CANVAS_SIZE / DENSITY
    y2 = y1 + CANVAS_SIZE / DENSITY
    res = random.randint(0, 1)

    if sum(color) > 1.5:
        t.color(color)
        res = random.randint(0, 1)

        if res == 0:
            t.penup()
            t.goto(x1, y1)
            t.pendown()
            t.goto(x2, y2)
            t.penup()
        else:
            t.penup()
            t.goto(x1, y2)
            t.pendown()
            t.goto(x2, y1)
            t.penup()


def evaluate(individual):
    score = 0
    drawn_lines = []
    for i in range(len(individual)):
        if individual[i] == 0:
            row = i // DENSITY
            col = i % DENSITY
            x = col * CANVAS_SIZE / DENSITY + CANVAS_SIZE / (2 * DENSITY)
            y = row * CANVAS_SIZE / DENSITY + CANVAS_SIZE / (2 * DENSITY)
            color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)) 
            line = (x, y, color) # new line to be drawn
            if line not in drawn_lines: # check if line hasn't been drawn before
                draw_line(x, y, color)
                drawn_lines.append(line) # add new line to list of drawn lines
                score += 1
    return score,

creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

def create_individual():
    return creator.Individual([random.randint(0, 1) for _ in range(DENSITY**2)])

toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("evaluate", evaluate)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# Create the initial population
pop = toolbox.population(n=POPULATION_SIZE)

# Evaluate the fitness of each individual in the initial population
fitnesses = [toolbox.evaluate(ind) for ind in pop]
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit

# Evolve the population over NUM_GENERATIONS
for gen in range(NUM_GENERATIONS):
    # Select the next generation of parents
    offspring = toolbox.select(pop, len(pop))
    
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    
    # Evaluate the fitness of the offspring
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = [toolbox.evaluate(ind) for ind in invalid_ind]
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    # Replace the parents with the offspring
    pop[:] = offspring
    
    # Print the best individual of the current generation
    best_ind = tools.selBest(pop, k=1)[0]

for i in range(len(best_ind)):
    if best_ind[i] == 0:
        row = i // DENSITY
        col = i % DENSITY
        color = (random.random(), random.random(), random.random()) # randomly generated RGB color tuple
        draw_line(row, col, color)

turtle.mainloop()







