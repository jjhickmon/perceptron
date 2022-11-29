import pygame
import random
from node import Node

pygame.init()

WIDTH = 600
HEIGHT = 600
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("perceptron")
clock = pygame.time.Clock()

# Constants
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont("Segoe UI", 15)

NEURON_VISUAL = False
MAP_SCALE = .5
# the top-left of the screen for the scaled visual
MAP_L = 0
MAP_T = 0
MAP_W = WIDTH * MAP_SCALE
MAP_H = HEIGHT * MAP_SCALE
VISUAL_L = WIDTH * MAP_SCALE
VISUAL_T = HEIGHT / 2 - (HEIGHT * MAP_SCALE / 2)
VISUAL_W = WIDTH * MAP_SCALE
VISUAL_H = HEIGHT * MAP_SCALE

NEURONS = [3, 1]

def sign(num):
    if num >= 0:
        return 1
    else:
        return -1

def f(x):
    y = x
    return y

# this class is simpler because a perceptron only has one lyaer of inputs and one layer of output
class Perceptron:
    def __init__(self, neurons, learning_rate):
        self.layers = []
        self.learning_rate = learning_rate
        for layer, nodes in enumerate(neurons):
            self.layers.append([])
            for node in range(nodes):
                self.layers[layer].append(None)
        
        for i, layer in enumerate(self.layers):
            # input & hidden layers
            if i < len(neurons) - 1:
                next = i + 1
                # set weights for all connections to the next layer
                for node in range(len(layer)):
                    weights = []
                    for _ in range(len(self.layers[next])):
                        if _ == len(self.layers[next]) - 1:
                            weights.append(1)
                        else:
                            weights.append(random.randint(-1, 1))
                        # weights.append(random.uniform(-1, 1))
                    layer[node] = Node(weights, None)
            # output layers
            else:
                for node in range(len(layer)):
                    # there should be no weight to the output and the activation function is sign()
                    layer[node] = Node([1], sign)

    # there must be one input for every input neuron
    def get_output(self, input):
        # set the input layer
        for i in range(len(input)):
            self.layers[0][i].set_input(input[i])
        # get the outputs for each successive layer
        for layer in range(1, len(self.layers)):
            for node in range(len(self.layers[layer])):
                sum = 0
                for prev_node in self.layers[layer - 1]:
                    sum += prev_node.get_output(node)
                self.layers[layer][node].set_input(sum)

        out_neuron = self.layers[len(self.layers) - 1][0]
        return out_neuron.afunct(out_neuron.get_output(0))
    
    def get_y(self, x):
        y = -(self.layers[0][0].get_weights()[0]/self.layers[0][1].get_weights()[0])*x - (self.layers[0][2].get_weights()[0]/self.layers[0][1].get_weights()[0])
        return y

    # trains this perceptron based on its error
    def train(self, inputs, answer):
        guess = self.get_output(inputs)
        error = answer - guess
        for layer in range(len(self.layers) - 1):
            for node in self.layers[layer]:
                node.adjust_weights(error, self.learning_rate)
                
    def draw(self):
        pygame.draw.line(screen, RED, (VISUAL_L, 0), (VISUAL_L, HEIGHT))
        pygame.draw.line(screen, BLACK, [0, MAP_T], [MAP_W, MAP_T])
        pygame.draw.line(screen, BLACK, [0, MAP_T + MAP_H], [MAP_W, MAP_T + MAP_H])
        for layer in range(len(self.layers)):
            x = (MAP_W / 2 / len(self.layers)) + (MAP_W * (layer / len(self.layers)))
            for node in range(len(self.layers[layer])):
                y = MAP_T + (MAP_H / 2 / len(self.layers[layer])) + (MAP_H * (node / len(self.layers[layer])))
                # draw weights
                if layer < len(self.layers) - 1:
                    for weight in range(len(self.layers[layer][node].get_weights())):
                        color = None
                        if self.layers[layer][node].get_weights()[weight] >= 0:
                            color = GREEN
                        else:
                            color = RED
                        new_x = (MAP_W / 2 / len(self.layers)) + (MAP_W * (layer + 1 / len(self.layers)))
                        new_y = MAP_T + (MAP_H / 2 / len(self.layers[layer+1])) + (MAP_H * (weight / len(self.layers[layer+1])))
                        pygame.draw.line(screen, color, (x, y), (new_x, new_y))

                        text = FONT.render(str(self.layers[layer][node].get_weights()[weight]), True, BLACK)
                        textRect = text.get_rect()
                        textRect.center = ((x + new_x) / 2, (y + new_y) / 2)
                        screen.blit(text, textRect)   

                # draw nodes
                pygame.draw.circle(screen, WHITE, (x, y), 20)
                pygame.draw.circle(screen, RED, (x, y), 20, 2)
                text = FONT.render(str(self.layers[layer][node].input), True, BLACK)
                textRect = text.get_rect()
                textRect.center = (x, y)
                screen.blit(text, textRect)

perceptron = Perceptron(NEURONS, 0.1)

training_data = []
def make_training_data():
    training_data.clear()
    for i in range(2000):
        point = [random.randrange(-WIDTH/2, WIDTH/2), random.randrange(-HEIGHT/2, HEIGHT/2), 1]
        training_data.append(point)

def draw():
    for point in training_data:
        # flip y axis for cartesian coordinates
        offset_point = (point[0] * VISUAL_SCALE + VISUAL_L + WIDTH/2, -(point[1] * VISUAL_SCALE + VISUAL_T) + HEIGHT/2)
        correct_sign = sign(point[1] - f(point[0]))
        if correct_sign >= 0:
            pygame.draw.circle(screen, BLACK, offset_point, 4, 1)
        else:
            pygame.draw.circle(screen, BLACK, offset_point, 4)

def update(count):
    pygame.draw.line(screen, GREEN, [VISUAL_L, HEIGHT - f(0)], [VISUAL_L + VISUAL_W, f(WIDTH) - VISUAL_H])
    pygame.draw.line(screen, RED, [0, HEIGHT + perceptron.get_y(0)], [WIDTH, HEIGHT -perceptron.get_y(WIDTH)])
    for point in range(count):
        point = training_data[point]
        offset_point = (point[0] * VISUAL_SCALE + VISUAL_L + WIDTH/2, -(point[1] * VISUAL_SCALE + VISUAL_T) + HEIGHT/2)
        correct_sign = sign(point[1] - f(point[0]))
        guess = perceptron.get_output(point)
        if guess == correct_sign:
            pygame.draw.circle(screen, GREEN, offset_point, 4)
        else:
            pygame.draw.circle(screen, RED, offset_point, 4)

make_training_data()
running = True
count = 0
while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            make_training_data()
            # perceptron.train(error)

    if NEURON_VISUAL:
        MAP_SCALE = 0.5
    else:
        MAP_SCALE = 0
        MAP_L = 0
        MAP_T = 0
        MAP_W = WIDTH * MAP_SCALE
        MAP_H = HEIGHT * MAP_SCALE
        VISUAL_SCALE = 1 - MAP_SCALE
        VISUAL_L = WIDTH * MAP_SCALE
        VISUAL_T = 0
        VISUAL_W = WIDTH * VISUAL_SCALE
        VISUAL_H = HEIGHT * VISUAL_SCALE
    
    screen.fill(WHITE)
    perceptron.train(training_data[count], sign(training_data[count][1] - f(training_data[count][0])))
    count = (count + 1) % len(training_data)
    draw()
    update(count)
    perceptron.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()