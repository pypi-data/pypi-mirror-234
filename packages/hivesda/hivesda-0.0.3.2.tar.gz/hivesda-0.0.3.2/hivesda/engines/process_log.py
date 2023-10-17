is_brain = False

if is_brain:
    import Brain


def sub_train_statues(epoch,sub_epoch,batch,loader):
    if is_brain:
        Brain(epoch,sub_epoch,batch,loader)
    else:
        print("Sub epoch statues : " , epoch,sub_epoch,batch,loader)

def sub_train_end(epoch,sub_epoch,mean_loss):
    if is_brain:
        Brain(epoch,sub_epoch,mean_loss)
    else:
        print("Sub epoch end : ",epoch,sub_epoch,mean_loss)

def validate_statues(batch,loader):
    if is_brain:
        Brain(batch,loader)
    else:
        print("Validation statues : ",batch,loader)


def validate_end(epoch,mean_loss,img_auc,pix_auc):
    if is_brain:
        Brain()
    else:
        print("Validation End : ",epoch,mean_loss,img_auc,pix_auc)
