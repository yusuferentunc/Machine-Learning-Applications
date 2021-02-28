import torch
import torchvision.transforms as T
import torch.nn as N
from torch.utils.data import DataLoader
from test import MnistDataset
from model import MyModel
import matplotlib.pyplot as plt

def train(model, optimizer, train_dataloader, validation_dataloader, epochs, device, layer, func, flag):
	model.train()
	model.eval() # TODO
	l_hist = []
	c_hist = []
	v_l_hist = []
	v_c_hist = []
	for epoch_idx in range(epochs):
		l = 0.0 # loss value
		c = 0.0 # correct prediction value
		v_l = 0.0 # validation loss value
		v_c = 0.0 # validation correct prediction value
		for images, labels in train_dataloader:
			# implement device to images and labels (outputs and targets)
			images = images.to(device)
			labels = labels.to(device)
			optimizer.zero_grad() # clear gradient descents that calculated before loop
			pred = model(images, layer, func)
			crit = N.CrossEntropyLoss() # loss function
			loss = crit(pred, labels)
			loss.backward() # calculates gradient of loss wrt input
			optimizer.step() # stochastic gradient descent // multiply gradient descent with learning rate then subtract from parameters // adam optimizer		
			#train graph preperation
			preds = torch.max(pred,1)
			l = l + loss.item()
			c = c + torch.sum(preds[1]==labels)		

		with torch.no_grad():
		 	for images, labels in validation_dataloader:
		 		optimizer.zero_grad()# ihtiyac olmayabilir
		 		pred = model(images, layer, func)
		 		crit = N.CrossEntropyLoss()
		 		loss = crit(pred, labels)
		 		# no backward due to not training model
		 		# validaton graph preperation
		 		preds = torch.max(pred,1)
		 		v_l = v_l + loss.item()
		 		v_c = v_c + torch.sum(preds[1]==labels)

		#train graph last preperations before graph
		e_loss = l/len(train_dataloader)
		e_acc = c.float()/len(train_dataloader)
		l_hist.append(e_loss) # train loss history
		c_hist.append(e_acc.item()) # train correct history
		#validation graph last preperations before graph
		v_e_loss = v_l/len(validation_dataloader)
		v_e_acc = v_c.float()/len(validation_dataloader)
		v_l_hist.append(v_e_loss) # validation loss history
		v_c_hist.append(v_e_acc.item()) # validation correct history
	#Calculation of success of model
	print("result= ", max(v_c_hist)/max(v_l_hist))
	# If flag is true, that means model that we train is final selected model. System gives 2 graph and a model saving to file
	if flag == True:
		torch.save(model.state_dict(), 'model_state_dict_final') 
		plt.plot(l_hist,label='Training Loss')
		plt.plot(v_l_hist,label='Validation Loss')
		plt.legend()
		plt.show()
		plt.plot(c_hist,label='Training Accuracy') 
		plt.plot(v_c_hist,label='Validation Accuracy')
		plt.legend()
		plt.show()

def main():
	device = torch.device('cpu') # I didn't select gpu due to prevent possible failures
	torch.manual_seed(1234)
	transforms = T.Compose([
		T.ToTensor(),
		T.Normalize((0.5, ),(0.5, ))
	])
	dataset = MnistDataset('data', 'train', transforms)
	train_dataset, validation_dataset = torch.utils.data.random_split(dataset, [8000, 2000])
	train_dataloader = DataLoader(train_dataset, batch_size = 64, shuffle = True, num_workers = 4)
	validation_dataloader = DataLoader(validation_dataset, batch_size = 64, shuffle = False, num_workers = 4)
	lr_list = [0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003]
	layer_list = [256, 512, 1024]
	func_list = ["relu", "sig", "tanh"]
	hidden_layer = [0, 1, 2]
	epochs = 12
	
	for hl in hidden_layer:
		for lal in layer_list:
			for lrl in lr_list:
				if hl != 0:
					for fl in func_list:
						layer = hl
						size = lal
						func = fl
						model = MyModel(layer, size)
						model = model.to(device)
						optimizer = torch.optim.Adam(model.parameters(), lr=lrl)
						print("hidden layer",layer,"layer size",size,"learning rate",lrl,"function",func)
						train(model, optimizer, train_dataloader, validation_dataloader, epochs, device, layer, func, False)
				if hl == 0:
					layer = hl
					size = lal
					func = "relu" # to prevent possible failuers, I give a function that is never used
					model = MyModel(layer, size)
					model = model.to(device)
					optimizer = torch.optim.Adam(model.parameters(), lr = lrl)
					print("hidden layer",layer,"layer size",size,"learning rate",lrl)
					train(model, optimizer, train_dataloader, validation_dataloader, epochs, device, layer, func, False)
	
	#Selected final model with saving option
	model = MyModel(2, 1024)
	model = model.to(device)
	optimizer = torch.optim.Adam(model.parameters(), lr=0.0003)
	print("Last training before test")
	train(model, optimizer, train_dataloader, validation_dataloader, 24, device, 2, "relu", True)

if __name__ == '__main__':
	main()
