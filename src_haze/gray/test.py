import os
import sys
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



import tensorflow as tf
import numpy as np
from skimage.measure import compare_psnr as psnr
from skimage.measure import compare_ssim as ssim
from morph_layers import *
from generator_gray import *
from  models_gray import *




def get_model_list(input_shape=(512, 512, 1)):
    model_cnn=create_CNN_model(input_shape=input_shape)
    model_path1=path1_old(input_shape=input_shape)
    model_path2=path2_old(input_shape=input_shape)
    model_path12=path12_old(input_shape=input_shape)
    model_path12_new=create_morph_path12_model(input_shape=input_shape)
    model_morph_type2=create_morph_model_type2(input_shape=input_shape)

    model_list=[model_path1,model_path2,model_path12,model_cnn,model_path12_new,model_morph_type2]
    return model_list






def get_trained_models(path="./models/",input_shape=(512, 512, 1)):
    model_list=get_model_list(input_shape=input_shape)
    model_name=["1model_path1.h5","1model_path2.h5","1model_path12.h5","1model_cnn.h5","1model12_new.h5","1model_morph_type2.h5"]

    for i in range(len(model_list)):
        print i
        model_list[i].load_weights(path+model_name[i])

    return model_list




def read_resize_image(file_path,size=(640,480,3)):
    Img = misc.imread(file_path)
    print Img.shape
    #Img = rgb2gray(Img)/255.0
    Img = resize(Img, size)

    return Img




def read_files(file_in,file_out):

    images_in=[]
    images_out=[]
    print"getting all the images..."
    for f1,f2 in zip(file_in,file_out):
        img1=read_resize_image(f1)
        img2=read_resize_image(f2)
        img1=rgb2gray(img1)
        img2=rgb2gray(img2)

        images_in.append(img1) 
        images_out.append(img2) 

    images_in=np.array(images_in,dtype="float32")
    images_out=np.array(images_out,dtype="float32")


    images_in=images_in[:,:,:,np.newaxis]
    images_out=images_out[:,:,:,np.newaxis]
    return images_in,images_out



def calculate_score(Y_out,Y_gt):

    Score=[]
    print("computing  Score")
    for i in range(Y_out.shape[0]):
        t1=psnr(Y_out[i],Y_gt[i])
        t2=ssim(Y_out[i],Y_gt[i],multichannel=True)
        Score.append([t1,t2])

    Score=np.array(Score)
    Score=np.mean(Score,axis=0)
    return  Score   





###########MAIN TEST CODE###########################################################################
model_list=get_trained_models(input_shape=(None,None,1))


file_in,file_out=get_in_out_file_test_nyu()
X,Y_gt=read_files(file_in,file_out)

S=[]


for model in model_list:
    Y_out=model.predict(X,batch_size=32)
    Y_out=np.clip(Y_out,0,1)
    score=calculate_score(Y_out,Y_gt)
    S.append(score)






def save_images():
    


