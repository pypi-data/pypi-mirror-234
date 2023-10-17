import torch
from .custom_list import CustomDataset,CustomFSCopyPasteDataset
from .utils import BalancedBatchSampler

__all__ = ['CustomDataset',
           'CustomFSCopyPasteDataset',
           'create_data_loader',
           'create_fas_data_loader',
           'create_test_data_loader']


def create_data_loader(args):
    kwargs = {'num_workers': args.num_workers, 'pin_memory': True}
    if args.dataset == 'custom':
        train_dataset = CustomDataset(args, is_train=True)
        test_dataset  = CustomDataset(args, is_train=False)
    else:
        raise NotImplementedError('{} is not supported dataset!'.format(args.dataset))
    # dataloader
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True, **kwargs)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False, drop_last=False, **kwargs)

    return train_loader, test_loader


def create_fas_data_loader(args):
    kwargs = {'num_workers': args.num_workers, 'pin_memory': True}
    if args.dataset == 'custom':
        normal_dataset = CustomDataset(args, is_train=True)
        if args.data_strategy == '0':
            # train_dataset = MVTecFSDataset(args, is_train=True)
            pass
        elif args.data_strategy == '0,1':
            train_dataset = CustomFSCopyPasteDataset(args, is_train=True)
        elif args.data_strategy == '0,2':
            # train_dataset = MVTecPseudoDataset(args, is_train=True)
            input("check data_strategy : 0,2")
            pass
        elif args.data_strategy == '0,1,2':
            # train_dataset = MVTecAnomalyDataset(args, is_train=True)
            input("check data_strategy : 0,1,2")
            pass
        if args.not_in_test:
            test_dataset  = CustomDataset(args, is_train=False, excluded_images=train_dataset.a_imgs)
        else:
            test_dataset  = CustomDataset(args, is_train=False)
    else:
        raise NotImplementedError('{} is not supported dataset!'.format(args.dataset))
    # dataloader
    normal_loader = torch.utils.data.DataLoader(normal_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True, **kwargs)
    if args.balanced_data_loader:
        train_loader = torch.utils.data.DataLoader(train_dataset, batch_sampler=BalancedBatchSampler(args, train_dataset), **kwargs)
    else:
        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, drop_last=True, **kwargs)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False, drop_last=False, **kwargs)

    return normal_loader, train_loader, test_loader


def create_test_data_loader(args):
    kwargs = {'num_workers': args.num_workers, 'pin_memory': True}
    if args.dataset == 'custom':
        test_dataset  = CustomDataset(args, is_train=False)
    else:
        raise NotImplementedError('{} is not supported dataset!'.format(args.dataset))
    # dataloader
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False, drop_last=False, **kwargs)

    return test_loader