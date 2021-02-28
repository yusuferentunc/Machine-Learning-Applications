import os
from torch.utils.data import Dataset, DataLoader
from PIL import Image 

class MnistDataset(Dataset):
	def __init__(self, dataset_path, split, transforms):
		images_path = os.path.join(dataset_path, split)
		self.data = []
		with open(os.path.join(images_path, 'labels.txt'), 'r') as f:
			for line in f:
				image_name, label = line.split()
				image_path = os.path.join(images_path, image_name)
				label = int(label)
				self.data.append((image_path, label))
		self.transforms = transforms
	
	def __len__(self):
		return len(self.data)

	def __getitem__(self, index):
		image_path = self.data[index][0]
		label = self.data[index][1]
		image = Image.open(image_path)
		image = self.transforms(image)
		return image, label


class MnistDatasetTest(Dataset):
	def __init__(self, dataset_path, split, transforms):
		images_path = os.path.join(dataset_path, split)
		self.data = []
		with open(os.path.join(images_path, 'labels.txt'), 'r') as f:
			for line in f:
				image_name = line.split()[0]
				image_path = os.path.join(images_path, image_name)
				self.data.append((image_path, image_name))
		self.transforms = transforms

	def __len__(self):
		return len(self.data)

	def __getitem__(self, index):
		image_path = self.data[index][0]
		image_name = self.data[index][1]
		image = Image.open(image_path)
		image = self.transforms(image)
		return image, image_name