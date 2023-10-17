from train import main_single


# # setting cuda 
# device = "GPU"   # CPU or GPU
# gpu = "0"        # set gpu numer
# seed = 0         # fix seed
# input_size = 300 # set image size e.g.) 300 -> (300x300)    
# batch_size = 4   # set batch size
# lr = 2e-4        # set learning-rate

# # total train epoch = meta_epoch * sub_epoch
# # start validation when end of sub_epochs
# meta_epochs = 25 # set total_epoch
# sub_epochs = 8   # set sub_epoch

# output_dir = "./"

img_auc, pix_auc, pix_pro = main_single()
print(f'Image-AUC: {img_auc}, Pixel-AUC: {pix_auc}, Pixel-PRO: {pix_pro}')
