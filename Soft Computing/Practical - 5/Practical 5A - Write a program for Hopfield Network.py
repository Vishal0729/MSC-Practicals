class Neuron:
    def __init__(self,weights): 
        self.weights=weights
    def activate(self,inputs):
        return sum(x * w for x,w in zip(inputs,self.weights))
class Network:
    def __init__(self, *weight_vectors):
        self.neurons = [Neuron(w) for w in weight_vectors]
    def threshold(self, x):
        return 1 if x >= 0 else 0
    def test_pattern(self, pattern):
        print(f"\nInput Pattern: {pattern}")
        outputs = [self.threshold(n.activate(pattern)) for n in self.neurons]
        print(f"Outputs: {outputs}")
        for p, o in zip(pattern, outputs):
            print(f"pattern={p} output={o} → {'match' if p==o else 'discrepancy'}")

#-------------MAIN-----------
print("\nHopfield Network (4 neurons) recalling 1010 and 0101\n")
pattern1, pattern2 = [1,0,1,0], [0,1,0,1]
weights = [
    [0, -3, 3, -3],
    [-3, 0, -3, 3],
    [3, -3, 0, -3],
    [-3, 3, -3, 0]
]
net = Network(*weights)
net.test_pattern(pattern1)
net.test_pattern(pattern2)

