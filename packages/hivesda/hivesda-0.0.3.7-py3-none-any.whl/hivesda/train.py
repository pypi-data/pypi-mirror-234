import os
import numpy as np
import torch
from .config import parse_args
from .utils.utils import init_seeds, setting_lr_parameters


def main_single():
    
    init_seeds(0)
    args = parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    args.device = torch.device("cuda")
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

    # unsup-train lr settings
    setting_lr_parameters(args)
    
    ############################################################################################################################################################
    # set data
    train_list = []
    val_list = []
    ng_list = []

    train_normal_list = os.listdir("../Data_toptec_center_png300/bottle/train/good")
    for t in train_normal_list:
        train_list.append(["../Data_toptec_center_png300/bottle/train/good/"+t,0,None,'good'])
    val_normal_list = os.listdir("../Data_toptec_center_png300/bottle/test/good")
    for v in val_normal_list:
        val_list.append(["../Data_toptec_center_png300/bottle/test/good/"+v,0,None,'good'])

    total_ng_list = os.listdir("../Data_toptec_center_png300/bottle/test/NG")
    for n in total_ng_list:
        ng_list.append(["../Data_toptec_center_png300/bottle/test/NG/"+n,1,"../Data_toptec_center_png300/bottle/ground_truth/NG/"+n.split(".")[0]+"_mask.png",'NG'])
    train_list = train_list + ng_list[:30]
    val_list = val_list + ng_list[30:]
    args.train_list = train_list
    args.val_list = val_list
    ############################################################################################################################################################

    # selecting train functions
    if args.with_fas:
        from .engines.bgad_fas_train_engine import train
        img_auc, pix_auc, pix_pro = train(args)
    else:
        from .engines.bgad_train_engine import train
        img_auc, pix_auc, pix_pro = train(args)

    return img_auc, pix_auc, pix_pro


