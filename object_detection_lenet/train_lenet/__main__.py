import torch.utils.data as data
from binary_image_dataset import BinaryImageDataset
from binary_image_lenet import BinaryImageLeNet
import torch
from torch.autograd import Variable
import torchvision.transforms as transforms
import torch.optim as optim


root = "."
trans = transforms.Compose([transforms.ToTensor()])

train_set = BinaryImageDataset(root=root, dataset_path="dataset", transform=trans)
test_set = BinaryImageDataset(root=root, dataset_path="test_dataset", transform=trans)

batch_size = 128
kwargs = {'num_workers': 1, 'pin_memory': True}
train_loader = torch.utils.data.DataLoader(
                 dataset=train_set,
                 batch_size=batch_size,
                 shuffle=True, **kwargs)
test_loader = torch.utils.data.DataLoader(
                dataset=test_set,
                batch_size=batch_size,
                shuffle=False, **kwargs)

print '==>>> total trainning batch number: {}'.format(len(train_loader))
print '==>>> total testing batch number: {}'.format(len(test_loader))


def train():

    model = BinaryImageLeNet().cuda()

    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    for epoch in xrange(10):

        # training
        for batch_idx, (x, target) in enumerate(train_loader):
            optimizer.zero_grad()
            x, target = Variable(x.cuda()), Variable(target.cuda())
            _, loss = model(x, target)
            loss.backward()
            optimizer.step()
            if batch_idx % 100 == 0:
                print '==>>> epoch: {}, batch index: {}, train loss: {:.6f}'.format(epoch, batch_idx, loss.data[0])

        # testing
        correct_cnt, ave_loss = 0, 0
        for batch_idx, (x, target) in enumerate(test_loader):
            x, target = Variable(x.cuda(), volatile=True), Variable(target.cuda(), volatile=True)
            score, loss = model(x, target)
            _, pred_label = torch.max(score.data, 1)
            correct_cnt += (pred_label == target.data).sum()
            ave_loss += loss.data[0]
        accuracy = correct_cnt*1.0/len(test_loader)/batch_size
        ave_loss /= len(test_loader)
        print '==>>> epoch: {}, test loss: {:.6f}, accuracy: {:.4f}'.format(epoch, ave_loss, accuracy)

    model.save_state_dict('trained_lenet.pt')