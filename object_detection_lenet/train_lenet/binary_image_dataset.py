import torch.utils.data as data
import os
from cv2 import imread


def image_loader(path):
    return imread(path), int(path.split("_")[-1].split(".")[0])


def dataset_loader(path):
    return os.listdir(path)


class BinaryImageDataset(data.Dataset):
    """
    A custom dataset to handle binary images
    """
    def __init__(self,
                 root,
                 dataset_path,
                 transform=None,
                 target_transform=None,
                 dataset_loader=dataset_loader,
                 image_loader=image_loader):

        self.root = root
        self.im_list = dataset_loader(dataset_path)
        self.transform = transform
        self.target_transform = target_transform
        self.image_loader = image_loader

    def __getitem__(self, index):
        im_path, target = self.im_list[index]
        img = self.image_loader(os.path.join(self.root,im_path))
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return img, target

    def __len__(self):
        return len(self.im_list)