import os
import numpy as np
import torch
import warnings
from config import parse_args
from utils.utils import init_seeds


def main_single(args):
    # model path
    args.model_path = "{}_{}_{}_{}".format(
        args.dataset, args.backbone_arch, args.flow_arch, args.class_name)
    
    # image
    args.img_size = (args.inp_size, args.inp_size)  
    args.crop_size = (args.inp_size, args.inp_size)  
    args.norm_mean, args.norm_std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    
    args.img_dims = [3] + list(args.img_size)

    # output settings
    args.save_results = True
    ############################################################################################################################################################
    # set data
    train_list = []
    val_list = []
    ng_list = []

    train_normal_list = os.listdir("./Data_toptec_center_png300/bottle/train/good")
    for t in train_normal_list:
        train_list.append(["./Data_toptec_center_png300/bottle/train/good/"+t,0,None,'good'])
    val_normal_list = os.listdir("./Data_toptec_center_png300/bottle/test/good")
    for v in val_normal_list:
        val_list.append(["./Data_toptec_center_png300/bottle/test/good/"+v,0,None,'good'])

    total_ng_list = os.listdir("./Data_toptec_center_png300/bottle/test/NG")
    for n in total_ng_list:
        ng_list.append(["./Data_toptec_center_png300/bottle/test/NG/"+n,1,"./Data_toptec_center_png300/bottle/ground_truth/NG/"+n.split(".")[0]+"_mask.png",'NG'])
    train_list = train_list + ng_list[:30]
    val_list = val_list + ng_list[30:]
    args.train_list = train_list
    args.val_list = val_list
    ############################################################################################################################################################

    from engines.bgad_test_engine import test
    img_auc, pix_auc, pro_auc = test(args)

    return img_auc, pix_auc, pro_auc


def main():
    init_seeds()
    args = parse_args()

    # setting cuda 
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    args.device = torch.device("cuda")


    img_auc, pix_auc, pro_auc = main_single(args)
    print(f'Image-AUC: {img_auc}, Pixel-AUC: {pix_auc}, Pro-AUC: {pro_auc}')


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    main()

