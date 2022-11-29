class Node:
    def __init__(self, weights, afunct):
        # the weights for each of the nodes this node points to
        self.weights = weights
        self.afunct = afunct
        self.input = 0

    def set_input(self, input):
        self.input = input
    
    def get_output(self, index):
        return self.input * self.weights[index]

    def get_weights(self):
        return self.weights

    def adjust_weights(self, error, lr):
        for weight in range(len(self.weights)):
            self.weights[weight] += error * self.input * lr
        # print(*self.weights)
