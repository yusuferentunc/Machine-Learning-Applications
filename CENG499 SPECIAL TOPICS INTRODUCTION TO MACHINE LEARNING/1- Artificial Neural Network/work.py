import torch
import torchvision.transforms as T
# import torch.nn.functional as F
from torch.utils.data import DataLoader
from test import MnistDataset, MnistDatasetTest
from model import MyModel


def main():
	device = torch.device('cpu')
	torch.manual_seed(1234)
	layer = 2
	size = 1024
	func = "relu"
	model = MyModel(layer, size)
	model.load_state_dict(torch.load('model_state_dict_final'))
	model.eval()
	transforms = T.Compose([
		T.ToTensor(),
		T.Normalize((0.5,), (0.5,))
	])
	test_dataset = MnistDatasetTest('data', 'test', transforms)
	test_dataloader = DataLoader(test_dataset, batch_size=64, shuffle=False, num_workers=4)
	result = open("result.txt", "w") # to create a result
	with torch.no_grad():
		for images, image_name in test_dataloader:
			images = images.to(device)
			prediction = model(images, layer, func)
			for i in range(images.size()[0]):
				x = image_name[i]+' '+str(int(torch.argmax(prediction[i])))
				result.write(x)
				result.write("\n")
	result.close()


if __name__ == '__main__':
	main()
