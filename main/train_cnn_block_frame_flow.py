import argparse
import os

from dataset import *
from models.cnn_block_frame_flow import CNNBlockFrameFlow
from train_helper import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block Frame&Flow ConvNet")
    parser.add_argument("--dataset_dir", type=str, default="data",
                        help="directory to dataset")
    parser.add_argument("--batch_size", type=int, default=64,
                        help="batch size for training (default: 64)")
    parser.add_argument("--num_epochs", type=int, default=3,
                        help="number of epochs to train (default: 3)")
    parser.add_argument("--start_epoch", type=int, default=1,
                        help="start index of epoch (default: 1)")
    parser.add_argument("--lr", type=float, default=0.001,
                        help="learning rate for training (default: 0.001)")
    parser.add_argument("--log", type=int, default=10,
                        help="log frequency (default: 10 iterations)")
    parser.add_argument("--cuda", type=int, default=0,
                        help="whether to use cuda (default: 0)")
    args = parser.parse_args()

    dataset_dir = args.dataset_dir
    batch_size = args.batch_size
    num_epochs = args.num_epochs
    start_epoch = args.start_epoch
    lr = args.lr
    log_interval = args.log

    if args.cuda == 1:
        cuda = True
    else:
        cuda = False

    print("Loading dataset")
    train_set = BlockFrameFlowDataset(dataset_dir, "train")
    dev_set = BlockFrameFlowDataset(dataset_dir, "dev")
    train_set.zero_center(train_set.mean)
    dev_set.zero_center(train_set.mean)

    # Create model and optimizer.
    model = CNNBlockFrameFlow()

    if start_epoch > 1:
        resume = True
    else:
        resume = False

    # Create directory for storing checkpoints.
    os.makedirs(os.path.join(dataset_dir, "cnn_block_frame_flow"),
                exist_ok=True)

    print("Start training")
    train(model, num_epochs, train_set, dev_set, lr=lr, batch_size=batch_size,
          start_epoch=start_epoch, log=log_interval, 
          checkpoint_path=os.path.join(dataset_dir, "cnn_block_frame_flow"),
          validate=True, resume=resume, flow=True, use_cuda=cuda)

