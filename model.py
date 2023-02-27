import torch
from torch import nn
import random

class NeuralNet(nn.Module):
    def __init__(self,mutation_power=0,mutate=False,l1=nn.Linear(8,32),l2=nn.Linear(32,32),l3=nn.Linear(32,4)):
        super(NeuralNet, self).__init__()
        self.mutation_power = mutation_power
        self.l2 = l2
        self.l1 = l1
        self.l3 = l3
        self.position = [random.randint(10,1200),random.randint(10,600)]
        self.idlestate = 300
        self.score = 0
        if mutate:
            with torch.no_grad():
                self.l1.weight += self.mutation_power * torch.randn_like(self.l1.weight)
                self.l1.bias += self.mutation_power * torch.randn_like(self.l1.bias)
                self.l2.weight += self.mutation_power * torch.randn_like(self.l2.weight)
                self.l2.bias += self.mutation_power * torch.randn_like(self.l2.bias)
                self.l3.weight += self.mutation_power * torch.randn_like(self.l3.weight)
                self.l3.bias += self.mutation_power * torch.randn_like(self.l3.bias)
        self.relu = nn.ReLU()

    
    def forward(self, x):
        x = torch.Tensor(x)
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out
    
    def mutate(self,n,mutation_power):
        children = []
        for i in range(int(n)):
            children.append(NeuralNet(mutation_power=mutation_power,mutate=True))
        return children