import torch
import torch.nn as nn
import torch.nn.functional as F


class MyModel(nn.Module):
	def __init__(self, layer, size):
		super(MyModel, self).__init__()
		#no hidden layer
		if layer == 0:
			self.fc = nn.Linear(1*64*32, 100)
		#1 hidden layer
		if layer == 1:
			self.fc1 = nn.Linear(1*64*32, size) #256 512 1024 hidden layer size
			self.fc2 = nn.Linear(size, 100)
		#2 hidden layer
		if layer == 2:
			self.fc1 = nn.Linear(1*64*32, size) #256 512 1024 hidden layer size
			self.fc2 = nn.Linear(size, size)	#256 512 1024 hidden layer size
			self.fc3 = nn.Linear(size, 100)

	def forward(self, x, layer, func):
		x = x.view(x.size(0), -1) # size = (64,1,32,64)
		if func == "relu":
			f = F.relu
		if func == "sig":
			f = torch.sigmoid
		if func == "tanh":
			f = torch.tanh
		
		#no hidden layer
		if layer == 0:
			x = self.fc(x)
		#1 hidden layer
		if layer == 1:
			x = self.fc1(x)
			x = f(x)
			x = self.fc2(x)
		#2 hidden layer
		if layer == 2:
			x = self.fc1(x)
			x = f(x)
			x = self.fc2(x)
			x = f(x)
			x = self.fc3(x)
		return x
