# -*- coding: utf-8 -*-
""" utils for model merge


https://pypi.org/project/torchmerge/


Quick Prototype

Pre-Trained model should have this method get_embedding(x)
    emb = model.get_embedding(x)

class MySmallClass()     
      pretrained
      
   def get_embedding(x):
       my custom code 

#### Inspect the layer: 
   extract_embedding_custom(emb)          
 
   depends on pytorch version ? 
      huggingFace already they wrap: Maybe consistent.
      
      SafeTensors as storage     
      hugging face timm (pretrained computer vision models)
      
      
torch.view(-1)  --> reshape stuff.  (embedding is 1D)
toch.mean(-1)  --> average of all channels.      

####
headless pre-trained output is 1D vector :  768, 512, 256

#######
torchinfo() summary : trainable  --->   dictionary



########################################################
ptyorch 2.0 and pytorch 1.0
compiler for pytorch
  ONNX   model.compile() 


  

ModelA: [embA]   

               --> Merged [ embA, embB ] --> MiddleMLP   [NewEmbedding] --> HeadMLP Task (classifier for image) 

ModelB : [embB]


 Use case 1: 
     2 same images but Model are different


           
 Use case 2:
     1 image + 1 Long label Text

          ---> Price of the image ?
          ---> Category, sub-category

      Fine tuning : 100 images.
            
      
########################################################################
      
Pros / Cons:  Pytorch  architecture

     nn : forward        





Doc::
        import utilmy.deeplearning.ttorch.model_ensemble as me
        me.test1()
        me.help()
        https://discuss.pytorch.org/t/combining-trained-models-in-pytorch/28383/45
        https://discuss.pytorch.org/t/merging-3-models/66230/3
        Issue wthen reloading jupyte
                import library.Child
                reload(library)
                import library.Child
Code::
        if ARG.MODE == 'mode1':
            ARG.MODEL_INFO.TYPE = 'dataonly'
            train_config                     = Box({})
            train_config.LR                  = 0.001
            train_config.DEVICE              = 'cpu'
            train_config.BATCH_SIZE          = 32
            train_config.EPOCHS              = 1
            train_config.EARLY_STOPPING_THLD = 10
            train_config.VALID_FREQ          = 1
            train_config.SAVE_FILENAME       = './model.pt'
            train_config.TRAIN_RATIO         = 0.7
        #### SEPARATE the models completetly, and create duplicate
        ### modelA  ########################################################
        model_ft = models.resnet18(pretrained=True)
        embA_dim = int(model_ft.fc.in_features)  ###
        ARG.modelA               = Box()   #MODEL_TASK
        ARG.modelA.name          = 'resnet18'
        ARG.modelA.nn_model      = model_ft
        ARG.modelA.layer_emb_id          = 'fc'
        ARG.modelA.architect     = [ embA_dim]  ### head s
        ARG.modelA.dataset       = Box()
        ARG.modelA.dataset.dirin = "/"
        ARG.modelA.dataset.coly  = 'ytarget'
        modelA = modelA_create(ARG.modelA)
        ### modelB  ########################################################
        model_ft = models.resnet50(pretrained=True)
        embB_dim = int(model_ft.fc.in_features)
        ARG.modelB               = Box()
        ARG.modelB.name          = 'resnet50'
        ARG.modelB.nn_model      = model_ft
        ARG.modelB.layer_emb_id          = 'fc'
        ARG.modelB.architect     = [embB_dim ]   ### head size
        ARG.modelB.dataset       = Box()
        ARG.modelB.dataset.dirin = "/"
        ARG.modelB.dataset.coly  = 'ytarget'
        modelB = modelB_create(ARG.modelB )
        ### merge_model  ###################################################
        ARG.merge_model           = Box()
        ARG.merge_model.name      = 'modelmerge1'
        ARG.merge_model.architect = { 'layers_dim': [ 200, 32, 1 ] }
        ARG.merge_model.architect.merge_type= 'cat'
        ARG.merge_model.dataset       = Box()
        ARG.merge_model.dataset.dirin = "/"
        ARG.merge_model.dataset.coly = 'ytarget'
        ARG.merge_model.train_config  = train_config
        model = MergeModel_create(ARG, modelB=modelB, modelA=modelA)
        #### Run Model   ###################################################
        # load_DataFrame = modelB_create.load_DataFrame
        # prepro_dataset = modelB_create.prepro_dataset
        model.build()
        model.training(load_DataFrame, prepro_dataset)
        inputs = torch.randn((1,5)).to(model.device)
        outputs = model.predict(inputs)
TODO :
    make get_embedding works
"""
import os, random,glob, numpy as np, pandas as pd ;from box import Box
from copy import deepcopy
import copy, collections
from abc import abstractmethod

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset, Dataset
import torchvision
from torchvision import transforms, datasets, models
from pandas.core.frame import DataFrame
from utilmy.deeplearning.ttorch import  util_torch as ut
#############################################################################################
from utilmy import log
from utilmy.deeplearning import  util_embedding as ue
##############################################################################################
def help():
    """function help
    """
    from utilmy import help_create
    ss =  help_create(__file__)
    log(ss)



##############################################################################################
def test_all():
    test1()
    test2a()
    test2b()
    test2c()
    test2d()
    test3()
    test4()
    test5()
    test6()
    test2_lstm()


def init_ARG():
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = Box()

    ARG.MODEL_INFO.TYPE = 'dataonly'
    #train_config
    train_config                     = Box({})
    train_config.LR                  = 0.001
    train_config.SEED                = 42
    train_config.DEVICE              = 'cpu'
    train_config.BATCH_SIZE          = 4
    train_config.EPOCHS              = 1
    train_config.EARLY_STOPPING_THLD = 10
    train_config.VALID_FREQ          = 1
    train_config.SAVE_FILENAME       = './model.pt'
    train_config.TRAIN_RATIO         = 0.7
    train_config.VAL_RATIO           = 0.2
    train_config.TEST_RATIO          = 0.1   

    #ARG.merge_model= {}
    #ARG.merge_model.train_config  = train_config
    return ARG, train_config


def test1():
    """
    """
    from box import Box ; from copy import deepcopy
    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df

    prepro_dataset = None


    ##################################################################
    ARG, train_config = init_ARG()

    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    ARG.modelA                            = Box()   #MODEL_TASK
    ARG.modelA.name                       = 'modelA1'
    ARG.modelA.nn_model                   = None
    ARG.modelA.architect                  = [ 5, 100, 16 ]
    ARG.modelA.architect.input_dim        = [train_config.BATCH_SIZE,5]
    ARG.modelA.dataset                    = Box()
    ARG.modelA.nn_model                   = None
    ARG.modelA.layer_emb_id               = ""
    ARG.modelA.dataset.dirin              = "/"
    ARG.modelA.dataset.coly               = 'ytarget'
    modelA = zzmodelA_create(ARG.modelA)


    ### modelB  ########################################################
    ARG.modelB               = Box()
    ARG.modelB.name          = 'modelB1'
    ARG.modelB.nn_model      = None
    ARG.modelB.architect     = [5,100,16]
    ARG.modelB.architect.input_dim = [train_config.BATCH_SIZE,5]
    ARG.modelB.dataset       = Box()
    ARG.modelB.nn_model      = None
    ARG.modelB.layer_emb_id  = ""
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = zzmodelB_create(ARG.modelB)


    ### merge_model  ###################################################
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    #ARG.merge_model.architect = { 'layers_dim': [ 200, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'

    ARG.merge_model.architect = {}
    ARG.merge_model.architect.input_dim        =  200
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [100, 32]
    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]

    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)

    #### Run Model   ###################################################
    model.build()
    model.training(load_DataFrame, prepro_dataset)
    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,5)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)


def test2a():
    """
    """
    log('### test Merging list of Custom models provided')
    from box import Box ; from copy import deepcopy

    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df

    prepro_dataset = None

    ##################################################################
    ARG, train_config = init_ARG()


    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    ARG.modelA                     = Box()   #MODEL_TASK
    ARG.modelA.name                = 'modelA1'
    ARG.modelA.architect           = [ 5, 100, 16 ]
    ARG.modelA.architect.input_dim = [train_config.BATCH_SIZE,5]
    ARG.modelA.dataset             = Box()
    ARG.modelA.nn_model            = None
    ARG.modelA.layer_emb_id        = ""
    ARG.modelA.dataset.dirin       = "/"
    ARG.modelA.dataset.coly        = 'ytarget'
    ARG.modelA.seed                = 42
    modelA = zzmodelA_create(ARG.modelA)


    ### modelB  ########################################################
    ARG.modelB                     = Box()
    ARG.modelB.name                = 'modelB1'
    ARG.modelB.architect           = [5,100,16]
    ARG.modelB.architect.input_dim = [train_config.BATCH_SIZE,5]
    ARG.modelB.dataset             = Box()
    ARG.modelB.nn_model            = None
    ARG.modelB.layer_emb_id        = ""
    ARG.modelB.dataset.dirin       = "/"
    ARG.modelB.dataset.coly        = 'ytarget'
    ARG.modelB.seed                = 42
    modelB = zzmodelB_create(ARG.modelB)

    ### merge_model  ###################################################
    ARG.merge_model                            = Box()
    ARG.merge_model.name                       = 'modelmerge1'
    ARG.merge_model.seed                       = 42
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  200
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [100, 32]
    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]


    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)


    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()
    model.training(load_DataFrame, prepro_dataset)

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,5)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)


def test2b():
    """
    """
    log('### test Merging pretrained CNN models provided with fake data')
    from box import Box ; from copy import deepcopy

    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    ###########################

    def load_DataFrame():
        return df

    ##################################################################
    ARG, train_config = init_ARG()

    def prepro_dataset(self,df:pd.DataFrame=None):
        """
        Docs:
            
            Dataset : Preparing random Image dataset for torchvision models

        """       
        trainx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        trainy = torch.rand(train_config.BATCH_SIZE)
        validx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        validy = torch.rand(train_config.BATCH_SIZE)
        testx = torch.rand(train_config.BATCH_SIZE,3,224,224)
        testy = torch.rand(train_config.BATCH_SIZE)
        return (trainx, trainy,validx,validy,testx,testy)

    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ########################################################
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA                     = Box()   #MODEL_TASK
    ARG.modelA.name                = 'resnet18'
    ARG.modelA.nn_model            = model_ft
    ARG.modelA.layer_emb_id        = 'fc'
    ARG.modelA.architect           = [ embA_dim]  ### head s
    ARG.modelA.architect.input_dim = [train_config.BATCH_SIZE,3,224,224]
    ARG.modelA.dataset             = Box()
    ARG.modelA.dataset.dirin       = "/"
    ARG.modelA.dataset.coly        = 'ytarget'
    modelA = zzmodelA_create(ARG.modelA)

    #model_ft.fc = modelA
    ### modelB  ########################################################
    model_ft = models.resnet50(pretrained=True)
    embB_dim = model_ft.fc.in_features

    ARG.modelB                     = Box()
    ARG.modelB.name                = 'resnet50'
    ARG.modelB.nn_model            = model_ft
    ARG.modelB.layer_emb_id        = 'fc'
    ARG.modelB.architect           = [embB_dim ]   ### head size
    ARG.modelB.architect.input_dim = [train_config.BATCH_SIZE,3,224,224]
    ARG.modelB.dataset             = Box()
    ARG.modelB.dataset.dirin       = "/"
    ARG.modelB.dataset.coly        = 'ytarget'
    modelB = zzmodelB_create(ARG.modelB)


    ### merge_model  ###################################################
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'
    #ARG.merge_model.architect = { 'layers_dim': [ embA_dim + embB_dim, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [512, 32]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]
    ARG.merge_model.architect.head_custom      = None

    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly  = 'ytarget'
    ARG.merge_model.train_config  = train_config
    modelC = None
    model_create_list = [modelA, modelB, modelC]
    model = MergeModel_create(ARG, model_create_list)

    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()
    model.training(load_DataFrame, prepro_dataset)

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,224,224)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)


def test2c():
    """
    """
    log('### test Merging pretrained CNN model(Resnet & EfficientNet) provided')
    from box import Box ; from copy import deepcopy

    ####################################################################
    from utilmy.adatasets import test_dataset_classifier_fake
    df, cols_dict = test_dataset_classifier_fake(100, normalized=True)

    def load_DataFrame():
        return df

    def prepro_dataset(self,df:pd.DataFrame=None):
        """
        Docs:
            
            Dataset : Preparing random Image dataset for torchvision models
            
        """  
        trainx = torch.rand(train_config.BATCH_SIZE,3,28,28)
        trainy = torch.rand(train_config.BATCH_SIZE)
        validx = torch.rand(train_config.BATCH_SIZE,3,28,28)
        validy = torch.rand(train_config.BATCH_SIZE)
        testx = torch.rand(train_config.BATCH_SIZE,3,28,28)
        testy = torch.rand(train_config.BATCH_SIZE)
        return (trainx, trainy,validx,validy,testx,testy)


    ##################################################################
    ARG, train_config = init_ARG()


    #### SEPARATE the models completetly, and create duplicate

    ### modelA  ########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = int(model_ft.fc.in_features)  ###

    ARG.modelA                       = Box()   #MODEL_TASK
    ARG.modelA.name                  = 'resnet18'
    ARG.modelA.nn_model              = model_ft
    ARG.modelA.layer_emb_id          = 'fc'

    ARG.modelA.architect             = [ embA_dim]  ###     ### head output
    ARG.modelA.architect.input_dim   = [train_config.BATCH_SIZE,3,224,224]   ### input : batch of 3 channel image.

    ###for fine tuning of the head
    ARG.modelA.dataset               = Box()
    ARG.modelA.dataset.dirin         = "/"
    ARG.modelA.dataset.coly          = 'ytarget'
    modelA = zzmodelA_create(ARG.modelA)



    ### modelB  ########################################################
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = Box()
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id          = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.architect.input_dim = [train_config.BATCH_SIZE,3,224,224]
    ARG.modelB.dataset       = Box()
    ARG.modelB.dataset.dirin = "/"
    ARG.modelB.dataset.coly  = 'ytarget'
    modelB = zzmodelB_create(ARG.modelB)


    # ### modelC  ########################################################
    from torchvision import  models
    model_ft                       = models.efficientnet_b0(pretrained=True)
    embC_dim                       = model_ft.classifier[1].in_features
    ARG.modelC                     = {}
    ARG.modelC.name                = 'efficientnet_b0'
    ARG.modelC.nn_model            = model_ft
    ARG.modelC.layer_emb_id        = 'fc'
    ARG.modelC.architect           = [ embC_dim ]   ### head size
    ARG.modelC.architect.input_dim = [train_config.BATCH_SIZE,3,28,28]
    ARG.modelC.dataset             = {}
    ARG.modelC.dataset.dirin       = "/"
    ARG.modelC.dataset.coly        = 'ytarget'
    modelC = model_create(ARG.modelC )


    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  : because it's merge
    ARG.merge_model           = Box()
    ARG.merge_model.name      = 'modelmerge1'

    #ARG.merge_model.architect = { 'layers_dim': [ embA_dim + embB_dim + embC_dim, 32, 1 ] }
    #ARG.merge_model.architect.merge_type= 'cat'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim + embC_dim

    #### Trainable Merge Head
    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [512, 32]   ### middle MLP to reduce embedding size
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [32, 8, 1]    #### Classifier for fine tuning
    ARG.merge_model.architect.head_custom      = None

    ### Fine tuning
    ARG.merge_model.dataset       = Box()
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    model_create_list = [modelA, modelB, modelC]
    model = model = MergeModel_create(ARG, model_create_list)
    #### Run Model   ###################################################
    # load_DataFrame = modelB_create.load_DataFrame
    # prepro_dataset = modelB_create.prepro_dataset
    model.build()
    model.training(load_DataFrame, prepro_dataset)

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,224,224)).to(model.device)
    outputs = model.predict(inputs)
    print(outputs)



def test2d():
    """
    """
    log('### test Merging pretrained CNN models with FashioMnist Dataset')
    from utilmy.deeplearning.ttorch import model_ensemble as me
    from box import Box ; from copy import deepcopy

    ####################################################################
    def load_DataFrame():
        return None

    ARG, train_config = init_ARG()


    def test_dataset_f_mnist(samples=100):
        """
        Docs:
            
            Dataset : FashionMNIST dataset and splitting.
            
        """  
        from sklearn.model_selection import train_test_split
        from torchvision import transforms, datasets
        # Generate the transformations
        train_list_transforms = [transforms.ToTensor(),transforms.Lambda(lambda x: x.repeat(3, 1, 1))]

        dataset1 = datasets.FashionMNIST(root="data",train=True,
                                         transform=transforms.Compose(train_list_transforms),download=True,)

        #sampling the requred no. of samples from dataset
        dataset1 = torch.utils.data.Subset(dataset1, np.arange(samples))
        X,Y    = [],  []
        for data, targets in dataset1:
            X.append(data)
            Y.append(targets)

        #Converting list to tensor format
        X,y = torch.stack(X),torch.Tensor(Y)


        train_r, test_r, val_r  = train_config.TRAIN_RATIO, train_config.TEST_RATIO,train_config.VAL_RATIO
        train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_r)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_r / (test_r + val_r))
        return (train_X, train_y, valid_X, valid_y, test_X , test_y)


    def prepro_dataset(self,df:pd.DataFrame=None):
        """
        Docs:
            
            Dataset : Preparing random Image dataset for torchvision models
        
        """  
        train_X ,train_y,valid_X ,valid_y,test_X, test_y = test_dataset_f_mnist(samples=100)
        return train_X ,train_y,valid_X ,valid_y,test_X,test_y



    ######################################################################
    #### SEPARATE the models completetly, and create duplicate

    ### modelA  ##########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA                     = {}     #MODEL_TASK
    ARG.modelA.name                = 'resnet18'
    ARG.modelA.nn_model            = model_ft
    ARG.modelA.layer_emb_id        = 'fc'
    ARG.modelA.architect           = [ embA_dim]  ### head s
    ARG.modelA.architect.input_dim = [train_config.BATCH_SIZE,3,28,28]
    ARG.modelA.dataset             = {}
    ARG.modelA.dataset.dirin       = "/"
    ARG.modelA.dataset.coly        = 'ytarget'
    modelA = model_create(ARG.modelA)


    ### modelB  ##########################################################
    from torchvision import  models
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB                     = {}
    ARG.modelB.name                = 'resnet50'
    ARG.modelB.nn_model            = model_ft
    ARG.modelB.layer_emb_id        = 'fc'
    ARG.modelB.architect           = [embB_dim ]   ### head size
    ARG.modelB.architect.input_dim = [train_config.BATCH_SIZE,3,28,28]
    ARG.modelB.dataset             = {}
    ARG.modelB.dataset.dirin       = "/"
    ARG.modelB.dataset.coly        = 'ytarget'
    modelB = model_create(ARG.modelB )


    # ### modelC  ########################################################
    from torchvision import  models
    model_ft                       = models.efficientnet_b0(pretrained=True)
    embC_dim                       = model_ft.classifier[1].in_features
    ARG.modelC                     = {}
    ARG.modelC.name                = 'efficientnet_b0'
    ARG.modelC.nn_model            = model_ft
    ARG.modelC.layer_emb_id        = 'fc'
    ARG.modelC.architect           = [ embC_dim ]   ### head size
    ARG.modelC.architect.input_dim = [train_config.BATCH_SIZE,3,28,28]
    ARG.modelC.dataset             = {}
    ARG.modelC.dataset.dirin       = "/"
    ARG.modelC.dataset.coly        = 'ytarget'
    modelC = model_create(ARG.modelC )

    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  : because it's merge
    ARG.merge_model           = {}
    ARG.merge_model.name      = 'modelmerge1'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim + embC_dim

    ARG.merge_model.architect.merge_type       = 'cat'         #### Common to all tasks
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [128, 1]  ### Input embedding is 768
    ARG.merge_model.architect.head_custom      = None


    ARG.merge_model.dataset       = {}
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    model = MergeModel_create(ARG, model_create_list=  [modelA, modelB, modelC] )


    #### Run Model   ###################################################
    model.build()
    model.training(load_DataFrame, prepro_dataset)

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    log(outputs)


##MultiClassMultiLable
def test3():
   log('### test MultiClassMultiHead with single Class')
   from box import Box ; from copy import deepcopy
   from torch.utils.data import DataLoader, TensorDataset

   ##################################################################
   ARG, train_config = init_ARG()


   ####################################################################
   def load_DataFrame():
       return None

   def test_dataset_f_mnist(samples=100):
       """
       Docs:
            
        Dataset : FashionMNIST dataset and splitting.
            
       """  
       from sklearn.model_selection import train_test_split
       from torchvision import transforms, datasets
       # Generate the transformations
       train_list_transforms = [transforms.ToTensor(),transforms.Lambda(lambda x: x.repeat(3, 1, 1))]

       dataset1 = datasets.FashionMNIST(root="data",train=True,
                                        transform=transforms.Compose(train_list_transforms),download=True,)

       #sampling the requred no. of samples from dataset
       dataset1 = torch.utils.data.Subset(dataset1, np.arange(samples))
       X,Y    = [],  []
       for data, targets in dataset1:
           X.append(data)
           Y.append(targets)


       #Converting list to tensor format
       X,y = torch.stack(X),torch.Tensor(Y)

       train_r, test_r, val_r  = train_config.TRAIN_RATIO, train_config.TEST_RATIO,train_config.VAL_RATIO
       train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_r)
       valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_r / (test_r + val_r))
       return (train_X, train_y, valid_X, valid_y, test_X , test_y)


   def prepro_dataset(self,df:pd.DataFrame=None):
       train_X ,train_y,valid_X ,valid_y,test_X, test_y = test_dataset_f_mnist(samples=100)
       return train_X ,train_y,valid_X ,valid_y,test_X,test_y



   ### modelA  ########################################################
   from torchvision import  models
   model_ft = models.resnet18(pretrained=True)
   embA_dim = model_ft.fc.in_features  ###

   ARG.modelA               = {}
   ARG.modelA.name          = 'resnet18'
   ARG.modelA.nn_model      = model_ft
   ARG.modelA.layer_emb_id  = 'fc'
   ARG.modelA.architect     = [ embA_dim]  ### head s
   ARG.modelA.architect.input_dim        = [train_config.BATCH_SIZE, 3 ,28, 28]
   modelA = model_create(ARG.modelA)



   ### modelB  ########################################################
   from torchvision import  models
   model_ft = models.resnet50(pretrained=True)
   embB_dim = int(model_ft.fc.in_features)

   ARG.modelB               = {}
   ARG.modelB.name          = 'resnet50'
   ARG.modelB.nn_model      = model_ft
   ARG.modelB.layer_emb_id  = 'fc'
   ARG.modelB.architect     = [embB_dim ]   ### head size
   ARG.modelB.architect.input_dim  = [train_config.BATCH_SIZE, 3, 28, 28]
   modelB = model_create(ARG.modelB )




   ### merge_model  ###################################################
   ### EXPLICIT DEPENDENCY
   ARG.merge_model           = {}
   ARG.merge_model.name      = 'modelmerge1'

   ARG.merge_model.architect                  = {}
   ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim

   ARG.merge_model.architect.merge_type       = 'cat'
   ARG.merge_model.architect.merge_layers_dim = [1024, 768]  ### Common embedding is 768
   ARG.merge_model.architect.merge_custom     = None


   ### Custom head
   from utilmy.deeplearning.ttorch.util_model import MultiClassMultiLabel_Head

   class_label_dict =  {'gender': 2}  ##5 n_unique_label
   ARG.merge_model.architect.head_layers_dim  = [ 768, 256]    ### Specific task
   head_custom = MultiClassMultiLabel_Head(layers_dim=    ARG.merge_model.architect.head_layers_dim,
                                        class_label_dict= class_label_dict,
                                        use_first_head_only= True)
   ARG.merge_model.architect.head_custom      = head_custom
   ARG.merge_model.architect.loss_custom = torch.nn.BCELoss() ###another loss func torch.nn.L1Loss()


   ARG.merge_model.dataset       = {}
   ARG.merge_model.dataset.dirin = "/"
   ARG.merge_model.dataset.coly = 'ytarget'
   ARG.merge_model.train_config  = train_config


   model = MergeModel_create(ARG, model_create_list= [modelA, modelB ] )
   model.build()



   #### Run Model   ###################################################
   model.training(load_DataFrame, prepro_dataset)

   model.save_weight('ztmp/model_x5.pt')
   model.load_weights('ztmp/model_x5.pt')
   inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
   outputs = model.predict(inputs)
   print(outputs)


def test4():
   log('### test MultiClassMultiHead with Multi Class Multi lable')
   from box import Box ; from copy import deepcopy
   from torch.utils.data import DataLoader, TensorDataset, Dataset

   ##################################################################
   ARG, train_config = init_ARG()


   ####################################################################
   samples = 1000 ##Fake data samples
   def prepro_dataset():
      """
        Docs:
            
            Dataset : Preparing Dataset for MultiClassMultiLable model
            
      """  
      train_X = torch.rand(int(samples*train_config.TRAIN_RATIO),3,28,28)
      valid_X = torch.rand(int(samples*train_config.VAL_RATIO),3,28,28)
      test_X = torch.rand(int(samples*train_config.TEST_RATIO),3,28,28)
      train_y =  { 'gender': torch.rand(int(samples*train_config.TRAIN_RATIO), 2),
                   'season': torch.rand(int(samples*train_config.TRAIN_RATIO), 4),
                   'style': torch.rand(int(samples*train_config.TRAIN_RATIO), 3),
                   'age': torch.rand(int(samples*train_config.TRAIN_RATIO), 5),
                   'colour': torch.rand(int(samples*train_config.TRAIN_RATIO), 7)
                  }

      valid_y =  { 'gender': torch.rand(int(samples*train_config.VAL_RATIO), 2),
                   'season': torch.rand(int(samples*train_config.VAL_RATIO), 4),
                   'style': torch.rand(int(samples*train_config.VAL_RATIO), 3),
                   'age': torch.rand(int(samples*train_config.VAL_RATIO), 5),
                   'colour': torch.rand(int(samples*train_config.VAL_RATIO), 7)
                  }

      test_y =  { 'gender': torch.rand(int(samples*train_config.TEST_RATIO), 2),
                   'season': torch.rand(int(samples*train_config.TEST_RATIO), 4),
                   'style': torch.rand(int(samples*train_config.TEST_RATIO), 3),
                   'age': torch.rand(int(samples*train_config.TEST_RATIO), 5),
                   'colour': torch.rand(int(samples*train_config.TEST_RATIO), 7)}

      return train_X ,train_y,valid_X ,valid_y,test_X,test_y



   train_X ,train_y,valid_X ,valid_y,test_X,test_y = prepro_dataset()
   class_label_dict =  {'gender': 2,'season':4, 'colour': 7}  ##5 n_unique_label


   ############## Custom Data Loader #############################
   def custom_dataloader():
       """
        Docs:
            
            Dataloader : Custom dataloader for MultiClassMultiLable model
            
       """  

       class CustomImageDataset(Dataset):
           def __init__(self,data=None,lables=None,class_lable_dict=None):
               self.data    = data
               self.lables  = lables
               self.classes = class_lable_dict

           def __len__(self):
               return len(self.data)

           def __getitem__(self, idx):
               train_X = self.data[idx]
               train_y = {}
               assert(len(self.classes) != 0)
               for classname, n_unique_label in self.classes.items():
                   train_y[classname] = self.lables[classname][idx]
               return (train_X, train_y)

       if train_X is not None and valid_X is not None and test_X is not None:
            train_dataloader = DataLoader(CustomImageDataset(data=train_X,lables=train_y,class_lable_dict=class_label_dict), batch_size=64,
                                            shuffle=True, num_workers=0,drop_last=True)
            valid_dataloader = DataLoader(CustomImageDataset(data=valid_X,lables=valid_y,class_lable_dict=class_label_dict), batch_size=64,
                                            shuffle=True, num_workers=0,drop_last=True)
            test_dataloader  = DataLoader(CustomImageDataset(data=test_X, lables=test_y,class_lable_dict=class_label_dict), batch_size=64,
                                            shuffle=True, num_workers=0,drop_last=True)
       else :
            raise Exception("Can't read data and lables, Custom Dataset")
       return train_dataloader, valid_dataloader, test_dataloader


   ### modelA  ########################################################
   from torchvision import  models
   model_ft = models.resnet18(pretrained=True)
   embA_dim = model_ft.fc.in_features  ###

   ARG.modelA               = {}
   ARG.modelA.name          = 'resnet18'
   ARG.modelA.nn_model      = model_ft
   ARG.modelA.layer_emb_id  = 'fc'
   ARG.modelA.architect     = [ embA_dim]  ### head s
   ARG.modelA.architect.input_dim        = [train_config.BATCH_SIZE, 3 ,28, 28]
   modelA = model_create(ARG.modelA)



   ### modelB  ########################################################
   from torchvision import  models
   model_ft = models.resnet50(pretrained=True)
   embB_dim = int(model_ft.fc.in_features)

   ARG.modelB               = {}
   ARG.modelB.name          = 'resnet50'
   ARG.modelB.nn_model      = model_ft
   ARG.modelB.layer_emb_id  = 'fc'
   ARG.modelB.architect     = [embB_dim ]   ### head size
   ARG.modelB.architect.input_dim  = [train_config.BATCH_SIZE, 3, 28, 28]
   modelB = model_create(ARG.modelB )


   ### merge_model  ###################################################
   ### EXPLICIT DEPENDENCY
   ARG.merge_model           = {}
   ARG.merge_model.name      = 'modelmerge1'

   ARG.merge_model.architect                  = {}
   ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim

   ARG.merge_model.architect.merge_type       = 'cat'
   ARG.merge_model.architect.merge_layers_dim = [1024, 768]  ### Common embedding is 768
   ARG.merge_model.architect.merge_custom     = None


   ### Custom head
   from utilmy.deeplearning.ttorch.util_model import MultiClassMultiLabel_Head

   ARG.merge_model.architect.head_layers_dim  = [ 768, 256]    ### Specific task
   head_custom = MultiClassMultiLabel_Head(layers_dim=    ARG.merge_model.architect.head_layers_dim,
                                        class_label_dict= class_label_dict,
                                        use_first_head_only= False)
   ARG.merge_model.architect.head_custom      = head_custom
   ARG.merge_model.architect.loss_custom = head_custom.get_loss


   ARG.merge_model.dataset       = {}
   ARG.merge_model.dataset.dirin = "/"
   ARG.merge_model.dataset.coly = 'ytarget'
   ARG.merge_model.train_config  = train_config


   model = MergeModel_create(ARG, model_create_list= [modelA, modelB ] )
   model.build()


   #### Run Model   ###################################################
   model.training(dataloader_custom = custom_dataloader )
   model.save_weight('ztmp/model_x5.pt')
   model.load_weights('ztmp/model_x5.pt')
   inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
   outputs = model.predict(inputs)
   print(outputs)


def test5():
    """ Multihead class fine tuning with Fashion Dataset
    """
    from utilmy.deeplearning.ttorch import  util_torch as ut
    import glob


    ##################################################################
    ARG, train_config = init_ARG()

    dirtmp      = "./"
    col_img     = 'id'
    label_list  = ['gender', 'masterCategory', 'subCategory' ]  #### Actual labels



    def custom_label(arg:dict=None):
        """
        Docs:
            
           Download Dataset and split the data
            
        """  
        ########## Downloading Dataset######
        dataset_url = "https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip"

        from utilmy.deeplearning.ttorch import  util_torch as ut
        dataset_path = ut.dataset_download(dataset_url, dirout=dirtmp)

        train_img_path = dirtmp + 'data_fashion_small/train'
        test_img_path  = dirtmp + 'data_fashion_small/test'
        label_path     = dirtmp + "data_fashion_small/csv/styles.csv"


        ########### label file in CSV  ########################
        df         = pd.read_csv(label_path,error_bad_lines=False, warn_bad_lines=False)
        label_dict       = {ci: df[ci].unique()  for ci in label_list}   ### list of cat values
        label_dict_count = {ci: df[ci].nunique() for ci in label_list}   ### count unique

        ########### Image files FASHION MNIST
        df = ut.dataset_add_image_fullpath(df, col_img=col_img, train_img_path=train_img_path, test_img_path=test_img_path)


        ########### Train Test Split
        df_train, df_val, df_test = ut.dataset_traintest_split(df, train_ratio=0.6, val_ratio=0.2)

        return df_train, df_val, df_test, label_dict, label_dict_count


    df_train, df_val, df_test, label_dict,label_dict_count = custom_label()



    def custom_dataloader():
        """
        Docs:
            
            Dataloader : Custom dataloader of FashionMnist for MultiClassMultiLable model
            
        """  
        ######CUSTOM DATASET#############################################
        # isexist(df_train, df_test, df_val, label_dict, col_img)

        from util_torch import ImageDataset
        # col_img        = 'id'
        batch_size     =  train_config.BATCH_SIZE
        FashionDataset = ImageDataset


        tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
        transform_train  = transforms.Compose(tlist)

        tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
        transform_test   = transforms.Compose(tlist)

        train_dataloader = DataLoader(FashionDataset( label_dir=df_train, label_dict=label_dict, col_img=col_img, transforms=transform_train),
                           batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

        val_dataloader   = DataLoader(FashionDataset( label_dir=df_val,   label_dict=label_dict, col_img=col_img, transforms=transform_train),
                           batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

        test_dataloader  = DataLoader(FashionDataset( label_dir=df_test,   label_dict=label_dict, col_img=col_img, transforms=transform_test),
                           batch_size=batch_size, shuffle= False ,num_workers=0, drop_last=True)

        return train_dataloader,val_dataloader,test_dataloader



    ### modelA  ########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA               = {}
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id  = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    ARG.modelA.architect.input_dim        = [train_config.BATCH_SIZE, 3 ,28, 28]
    modelA = model_create(ARG.modelA)

    ### modelB  ########################################################
    from torchvision import  models
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = {}
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id  = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.architect.input_dim  = [train_config.BATCH_SIZE, 3, 28, 28]
    modelB = model_create(ARG.modelB )


    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY
    ARG.merge_model           = {}
    ARG.merge_model.name      = 'modelmerge1'

    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim

    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]  ### Common embedding is 768
    ARG.merge_model.architect.merge_custom     = None


    ### Custom head
    from utilmy.deeplearning.ttorch.util_model import MultiClassMultiLabel_Head
    ARG.merge_model.architect.head_layers_dim  = [ 768, 256]    ### Specific task

    head_custom = MultiClassMultiLabel_Head(layers_dim          = ARG.merge_model.architect.head_layers_dim,
                                            class_label_dict    = label_dict_count,
                                            use_first_head_only = False)

    ARG.merge_model.architect.head_custom = head_custom
    ARG.merge_model.architect.loss_custom = head_custom.get_loss


    ARG.merge_model.dataset       = {}
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config


    model = MergeModel_create(ARG, model_create_list= [modelA, modelB ] )
    model.build()


    #### Run Model   ###################################################
    model.training(dataloader_custom = custom_dataloader )
    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    ######To predict lables
    for i in range(train_config.BATCH_SIZE):
        sum = {}
        for key, val in outputs.items():
            sum[key] = outputs[key].sum()
        Keymax = max(zip(sum.values(), sum.keys()))[1]
        print(Keymax)

    print(outputs)


def test6():
    """ Multihead class fine tuning with Fashion Dataset
    """
    from utilmy.deeplearning.ttorch import  util_torch as ut
    ARG = Box({
        'MODE'   : 'mode1',
        'DATASET': {},
        'MODEL_INFO' : {},
    })
    PARAMS = {}

    ##################################################################
    if ARG.MODE == 'mode1':
        ARG.MODEL_INFO.TYPE = 'dataonly'
        train_config                           = Box({})
        train_config.LR                        = 0.0001
        train_config.SEED                      = 42
        train_config.DEVICE                    = 'cpu'
        train_config.BATCH_SIZE                = 4
        train_config.EPOCHS                    = 1
        train_config.EARLY_STOPPING_THLD       = 10
        train_config.VALID_FREQ                = 1
        train_config.SAVE_FILENAME             = './model.pt'
        train_config.TRAIN_RATIO               = 0.7
        train_config.VAL_RATIO                 = 0.2
        train_config.TEST_RATIO                = 0.1

    dirtmp      = "./"
    col_img     = 'id'
    label_list  = ['gender', 'masterCategory', 'subCategory' ]  #### Actual labels



    def custom_label(arg:dict=None):
        ########## Downloading Dataset######
        dataset_url = "https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip"
        dataset_path = ut.dataset_download(dataset_url, dirout=dirtmp)

        train_img_path = dirtmp + 'data_fashion_small/train'
        test_img_path  = dirtmp + 'data_fashion_small/test'
        label_path     = dirtmp + "data_fashion_small/csv/styles.csv"


        ########### label file in CSV  ########################
        df         = pd.read_csv(label_path,error_bad_lines=False, warn_bad_lines=False)
        label_dict       = {ci: df[ci].unique()  for ci in label_list}   ### list of cat values
        label_dict_count = {ci: df[ci].nunique() for ci in label_list}   ### count unique

        ########### Image files FASHION MNIST
        df = ut.dataset_add_image_fullpath(df, col_img=col_img, train_img_path=train_img_path, test_img_path=test_img_path)
        ########### Train Test Split
        df_train, df_val, df_test = ut.dataset_traintest_split(df, train_ratio=0.6, val_ratio=0.2)

        return df_train, df_val, df_test, label_dict, label_dict_count

    df_train, df_val, df_test, label_dict,label_dict_count = custom_label()



    def custom_dataloader():
        """
        Docs:

            Dataloader : Custom dataloader of FashionMnist for MultiClassMultiLable model

        """
        ######CUSTOM DATASET#############################################
        # isexist(df_train, df_test, df_val, label_dict, col_img)

        from util_torch import ImageDataset
        # col_img        = 'id'
        batch_size     =  train_config.BATCH_SIZE
        FashionDataset = ImageDataset


        tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
        transform_train  = transforms.Compose(tlist)

        tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
        transform_test   = transforms.Compose(tlist)

        train_dataloader = DataLoader(FashionDataset( label_dir=df_train, label_dict=label_dict, col_img=col_img, transforms=transform_train),
                           batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

        val_dataloader   = DataLoader(FashionDataset( label_dir=df_val,   label_dict=label_dict, col_img=col_img, transforms=transform_train),
                           batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

        test_dataloader  = DataLoader(FashionDataset( label_dir=df_test,   label_dict=label_dict, col_img=col_img, transforms=transform_test),
                           batch_size=batch_size, shuffle= False ,num_workers=0, drop_last=True)

        return train_dataloader,val_dataloader,test_dataloader



    ### modelA  ########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA               = {}
    ARG.modelA.name          = 'resnet18'
    ARG.modelA.nn_model      = model_ft
    ARG.modelA.layer_emb_id  = 'fc'
    ARG.modelA.architect     = [ embA_dim]  ### head s
    ARG.modelA.architect.input_dim        = [train_config.BATCH_SIZE, 3 ,28, 28]
    modelA = model_create(ARG.modelA)

    ### modelB  ########################################################
    from torchvision import  models
    model_ft = models.resnet50(pretrained=True)
    embB_dim = int(model_ft.fc.in_features)

    ARG.modelB               = {}
    ARG.modelB.name          = 'resnet50'
    ARG.modelB.nn_model      = model_ft
    ARG.modelB.layer_emb_id  = 'fc'
    ARG.modelB.architect     = [embB_dim ]   ### head size
    ARG.modelB.architect.input_dim  = [train_config.BATCH_SIZE, 3, 28, 28]
    modelB = model_create(ARG.modelB )


    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY
    ARG.merge_model           = {}
    ARG.merge_model.name      = 'modelmerge1'

    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embB_dim

    ARG.merge_model.architect.merge_type       = 'cat'
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]  ### Common embedding is 768
    ARG.merge_model.architect.merge_custom     = None


    ### Custom head
    from utilmy.deeplearning.ttorch.util_model import MultiClassMultiLabel_Head
    ARG.merge_model.architect.head_layers_dim  = [ 768, 256]    ### Specific task

    head_custom = MultiClassMultiLabel_Head(layers_dim          = ARG.merge_model.architect.head_layers_dim,
                                            class_label_dict    = label_dict_count,
                                            use_first_head_only = False)

    ARG.merge_model.architect.head_custom = head_custom
    ARG.merge_model.architect.loss_custom = head_custom.get_loss


    ARG.merge_model.dataset       = {}
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config


    model = MergeModel_create(ARG, model_create_list= [modelA, modelB ] )
    model.build()


 #########################EMBEDDING ####################################
    def custom_embedding_data():
         """
         Docs:

            Selecting specific class and lable from MultiClassMultiLable model for embeddings

         """
         dataset_url = "https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip"
         ut.dataset_download(dataset_url, dirout=dirtmp)
         train_img_path  = dirtmp + 'data_fashion_small/train'
         label_path     = dirtmp + "data_fashion_small/csv/styles.csv"
         df   = pd.read_csv(label_path,error_bad_lines=False, warn_bad_lines=False)
         df = ut.dataset_add_image_fullpath(df, col_img='id', train_img_path=train_img_path)

         ########### Train Test Split
         df_train, _ , _ = ut.dataset_traintest_split(df, train_ratio=0.9, val_ratio=0.1)

         ##############TRANFORM IMAGE############
         tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
         transform  = transforms.Compose(tlist)

         ###Loads image and imagename(to save the embedding with image name)####
         label_dict = {"gender":"Men"}
         dataset = ut.ImageDataset(label_dir=df_train, label_dict=label_dict, col_img='id', transforms=transform, return_img_id  = True)
         return dataset

    dataset      = custom_embedding_data()
    train_loader = DataLoader(dataset,batch_size=4, drop_last=True)


    print("Before Training")
    tag   ='multi'
    dirout= "./temp"

    dfsim = ut.model_embedding_extract_check(model=model.net.eval(), dirout=dirout, data_loader=train_loader, tag=tag,
                                             force_getlayer= False, pos_layer=-2)

    print(dfsim)

    ue.embedding_create_vizhtml(dirin=dirout + f"/df_emb_{tag}.parquet",
                                dirout=dirout + "/out/", dim_reduction='mds', nmax=200, ntrain=df_train.shape[0],
                                num_clusters=2,
                                )
    # ue.embedding_create_vizhtml(dirin=dirout + f"/df_emb_{tag}.parquet",
    #                             dirout=dirout + "/out1/", dim_reduction='umap', nmax=200, ntrain=df_train.shape[0],
    #                             num_clusters=2,
    #                             )
    #### Run Model   ###################################################
    model.training(dataloader_custom = custom_dataloader )
    model.save_weight( 'ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    #print(outputs)


    print("After Training")
    tag   ='multi-finetuned'

    #model=model.net.eval()
    dfsim = ut.model_embedding_extract_check(model=model.net.eval(), dirout=dirout, data_loader=train_loader, tag=tag,
                                     force_getlayer= False, pos_layer=-2)

    ue.embedding_create_vizhtml(dirin=dirout + f"/df_emb_{tag}.parquet",
                                dirout=dirout + "/out/", dim_reduction='mds', nmax=200, ntrain=df_train.shape[0],
                                num_clusters=2,
                                )

    # ue.embedding_create_vizhtml(dirin=dirout + f"/df_emb_{tag}.parquet",
    #                             dirout=dirout + "/out1/", dim_reduction='umap', nmax=200, ntrain=df_train.shape[0],
    #                             num_clusters=2,
    #                             )
    print(dfsim)


##### LSTM #################################################################################
def test2_lstm():
    log('\n\n\n\nLSTM Version')
    from utilmy.deeplearning.ttorch import model_ensemble as me
    from box import Box ; from copy import deepcopy


    ####################################################################
    def load_DataFrame():
        return None

    ARG, train_config = init_ARG()

    def test_dataset_f_mnist(samples=100):
        """function test_dataset_f_mnist
        """
        from sklearn.model_selection import train_test_split
        from torchvision import transforms, datasets
        # Generate the transformations
        train_list_transforms = [transforms.ToTensor(),transforms.Lambda(lambda x: x.repeat(3, 1, 1))]

        dataset1 = datasets.FashionMNIST(root="data",train=True,
                                         transform=transforms.Compose(train_list_transforms),download=True,)

        #sampling the requred no. of samples from dataset
        dataset1 = torch.utils.data.Subset(dataset1, np.arange(samples))
        X,Y    = [],  []
        for data, targets in dataset1:
            X.append(data)
            Y.append(targets)

        #Converting list to tensor format
        X,y = torch.stack(X),torch.Tensor(Y)


        train_r, test_r, val_r  = train_config.TRAIN_RATIO, train_config.TEST_RATIO,train_config.VAL_RATIO
        train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_r)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_r / (test_r + val_r))
        return (train_X, train_y, valid_X, valid_y, test_X , test_y)


    def prepro_dataset(self,df:pd.DataFrame=None):
        """function prepro_dataset
        """
        train_X ,train_y,valid_X ,valid_y,test_X, test_y = test_dataset_f_mnist(samples=100)
        return train_X ,train_y,valid_X ,valid_y,test_X,test_y


    ######################################################################
    #### SEPARATE the models completetly, and create duplicate
    ### modelA  ##########################################################
    from torchvision import  models
    model_ft = models.resnet18(pretrained=True)
    embA_dim = model_ft.fc.in_features  ###

    ARG.modelA                     = {}     #MODEL_TASK
    ARG.modelA.name                = 'resnet18'
    ARG.modelA.nn_model            = model_ft
    ARG.modelA.layer_emb_id        = 'fc'
    ARG.modelA.architect           = [ embA_dim]  ### head s
    ARG.modelA.architect.input_dim = [train_config.BATCH_SIZE,3,28,28]
    ARG.modelA.dataset             = {}
    ARG.modelA.dataset.dirin       = "/"
    ARG.modelA.dataset.coly        = 'ytarget'
    modelA = model_create(ARG.modelA)


    # ### model lSTM  ########################################################
    class LSTM(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers, num_classes, dropout):
            super(LSTM, self).__init__()
            self.num_layers = num_layers
            self.input_size = input_size
            self.hidden_size = hidden_size
            self.num_classes = num_classes
            self.dropout = dropout

            self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers,
                                dropout = self.dropout, batch_first=True)
            self.fc = nn.Linear(self.hidden_size, self.num_classes)

        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            out, _ = self.lstm(x, (h0,c0))
            out = out[:,-1,:]
            out = self.fc(out)
            return out

    lstm = LSTM(input_size=28, hidden_size=128, num_layers=2, num_classes=2, dropout=0.0)
    #from util_models.LSTM import lstm
    model_ft                 = lstm
    embD_dim                 = int(model_ft.fc.in_features)

    ##Reshape input to be compatible with Sequence Model
    seq_reshaper = SequenceReshaper(from_='vision')
    model_ft = torch.nn.Sequential(seq_reshaper,	model_ft )


    ARG.modelD               = Box()
    ARG.modelD.name          = 'LSTM'
    ARG.modelD.nn_model      = model_ft
    ARG.modelD.layer_emb_id  = 'fc'
    ARG.modelD.architect     = [ embD_dim ]   ### head size
    ARG.modelD.architect.input_dim = [train_config.BATCH_SIZE,28,28]
    ARG.modelD.dataset       = Box()
    ARG.modelD.dataset.dirin = "/"
    ARG.modelD.dataset.coly  = 'ytarget'
    modelD = zzmodelD_create(ARG.modelD)

    ### merge_model  ###################################################
    ### EXPLICIT DEPENDENCY  : because it's merge
    ARG.merge_model           = {}
    ARG.merge_model.name      = 'modelmerge1'
    ARG.merge_model.architect                  = {}
    ARG.merge_model.architect.input_dim        =  embA_dim + embD_dim

    ARG.merge_model.architect.merge_type       = 'cat'         #### Common to all tasks
    ARG.merge_model.architect.merge_layers_dim = [1024, 768]
    ARG.merge_model.architect.merge_custom     = None

    ARG.merge_model.architect.head_layers_dim  = [128, 1]  ### Input embedding is 768
    ARG.merge_model.architect.head_custom      = None


    ARG.merge_model.dataset       = {}
    ARG.merge_model.dataset.dirin = "/"
    ARG.merge_model.dataset.coly = 'ytarget'
    ARG.merge_model.train_config  = train_config
    model = MergeModel_create(ARG, model_create_list=  [modelA, modelD] )


    #### Run Model   ###################################################
    model.build()
    model.training(load_DataFrame, prepro_dataset)

    model.save_weight('ztmp/model_x5.pt')
    model.load_weights('ztmp/model_x5.pt')
    inputs = torch.randn((train_config.BATCH_SIZE,3,28,28)).to(model.device)
    outputs = model.predict(inputs)
    log(outputs)








##############################################################################################
class SequenceReshaper(nn.Module):
    def __init__(self, from_ = 'vision'):
        """ Reshape output to fit the merge flatenning
        """
        super(SequenceReshaper,self).__init__()
        self.from_ = from_

    def forward(self, x):
        if self.from_ == 'vision':
            x = x[:,0,:,:]
            x = x.squeeze()
            return x
        else:
            return x

class model_template_MLP(torch.nn.Module):
    def __init__(self,layers_dim=[20,100,16]):
        super(model_template_MLP, self).__init__()
        self.layers_dim = layers_dim
        self.output_dim = layers_dim[-1]
        # self.head_task = nn.Sequential()
        self.head_task = []
        input_dim = layers_dim[0]
        for layer_dim in layers_dim[:-1]:
            self.head_task.append(nn.Linear(input_dim, layer_dim))
            self.head_task.append(nn.ReLU())
            input_dim = layer_dim
        self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))   #####  Do not use Sigmoid
        self.head_task = nn.Sequential(*self.head_task)

    def forward(self, x,**kwargs):
        return self.head_task(x)


##############################################################################################
class BaseModel(object):
    """This is BaseClass for model create
    Method:
        create_model : Initialize Model (torch.nn.Module)
        evaluate:
        prepro_dataset:  (conver pandas.DataFrame to appropriate format)
        create_loss :   Initialize Loss Function
        training:   starting training
        build: create model, loss, optimizer (call before training)
        train: equavilent to model.train() in pytorch (auto enable dropout,vv..vv..)
        eval: equavilent to model.eval() in pytorch (auto disable dropout,vv..vv..)
        device_setup:
        load_DataFrame: read pandas
        load_weight:
        save_weight:
        predict :
    """

    def __init__(self,arg):
        self.arg      = Box(arg)
        self._device  = self.device_setup(arg)
        self.losser   = None
        self.is_train = False

    @abstractmethod
    def create_model(self,) -> torch.nn.Module:
    #   raise NotImplementedError
        log("       model is building")
    @abstractmethod
    def evaluate(self):
        raise NotImplementedError

    @abstractmethod
    def prepro_dataset(self,csv) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def create_loss(self,) -> torch.nn.Module:
        log("       loss is building")
        # raise NotImplementedError

    @abstractmethod
    def training(self,):
        raise NotImplementedError

    @property
    def device(self,):
        return self._device

    @device.setter
    def device(self,value):
        if isinstance(value,torch.device):
          self._device = value
        elif isinstance(value,str):
          self._device = torch.device(value)
        else:
          raise TypeError("device must be str or torch.device")

    def build(self,):
        self.net       = self.create_model().to(self.device)
        self.loss_calc = self.create_loss().to(self.device)
        # self.loss_calc=
        self.is_train = False

    def train(self): # equivalent model.train() in pytorch  ### Just wwrapping the base nn.module train
        self.is_train = True
        self.net.train()

    def eval(self):     # equivalent model.eval() in pytorch
        self.is_train = False
        self.net.eval()

    def device_setup(self,arg):
        device = getattr(arg,'device','cpu')
        seed   = arg.seed if hasattr(arg,'seed') else 42
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

        if 'gpu' in device :
            try :
                torch.cuda.manual_seed(seed)
                torch.cuda.manual_seed_all(seed)
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
            except Exception as e:
                log(e)
                device = 'cpu'
        return device

    def load_DataFrame(self,path=None)-> pd.DataFrame:
        if path:
            log(f"reading csv from {path}")
            self.df = pd.read_csv(path,delimiter=';')
            return self.df
        if os.path.isfile(self.arg.dataset.path):
            log(f"reading csv from arg.DATASET.PATH :{self.arg.dataset.path}")
            self.df = pd.read_csv(self.arg.dataset.path,delimiter=';')
            return self.df
        else:
            import requests
            import io
            r = requests.get(self.arg.dataset.url)
            log(f"Reading csv from arg.DATASET.URL")
            if r.status_code ==200:
                self.df = pd.read_csv(io.BytesIO(r.content),delimiter=';')
            else:
                raise Exception("Can't read data, status_code: {r.status_code}")

            return self.df


    def load_weights(self, path):
        assert os.path.isfile(path),f"{path} does not exist"
        try:
          ckp = torch.load(path,map_location=self.device)
        except Exception as e:
          log(e)
          log(f"can't load the checkpoint from {path}")
        if isinstance(ckp,collections.OrderedDict):
          self.net.load_state_dict(ckp)
        else:
          self.net.load_state_dict(ckp['state_dict'])

    def save_weight(self,path,meta_data=None):
      os.makedirs(os.path.dirname(path),exist_ok=True)
      ckp = {
          'state_dict':self.net.state_dict(),
      }
      if meta_data:
        if isinstance(meta_data,dict):
            ckp.update(meta_data)
        else:
            ckp.update({'meta_data':meta_data,})
      torch.save(ckp,path)

    def grad_check(self,):
        """
        Docs:
            
            Assuring Pre-trainined Models's(Merge) parameters to not to be trainable
            
            Advice: Dont freeze all the layer in pre-trained, keep un-freeze 1 or 2 layers.
                    weight changes a little : more adapting to the final head.
                     
                    
            Reason : only get the embedding from different pipelines or from database.
                     Freeze
                     Complete Decoupling : only common is embedding.  imageID --> embedding.
                     
                     
                    
                    
        """
        for i in range(len(self.net.models_nets)):
            net_model = self.net.models_nets[i]
            kk = 0
            for param1, param2 in zip(self.models_list[i].net.parameters(),
                                           net_model.parameters()):
                if kk > 5 : break
                kk = kk + 1
                # torch.testing.assert_close(param1.data, param2.data)
                if(param2.requires_grad==True):
                   raise Exception("Gradients are updated in models_nets {}".format(i) )


    def validate_dim(self,train_loader,val_loader):
        """
        Docs:
            
            Asserting dimensions of Train and Validation Datasets
        
        """
        train = iter(train_loader)
        train_inp, _ = next(train)

        #Validating sizes of train data loader
        for i in range(len(self.models_list)):
            expeted_size = self.models_list[i].arg.architect.input_dim
            for dim in range(train_inp.dim()):
                pass
                #assert expeted_size[dim] == train_inp.size()[dim],"invalid train data for model{}".format(i)

         #Validating sizes of val_loader
        val = iter(val_loader)
        val_input, _ = next(val)
        assert val_input.size()[1:] == train_inp.size()[1:],"invalid validating data"



    def predict(self,x,**kwargs):
        # raise NotImplementedError
        output = self.net(x,**kwargs)
        return output


class MergeModel_create(BaseModel):
    """
    """
    def __init__(self,arg:dict=None, model_create_list = None):
        """
        """
        super(MergeModel_create,self).__init__(arg)
        self.models_list = []
        if(len(model_create_list)!=0):
            for i in range(len(model_create_list)):
                if model_create_list[i] is not None:
                    self.models_list.append(model_create_list[i])

        #To handle if all models are selected as None
        if len(self.models_list)==0 or len(model_create_list)==0:
            raise Exception("No models are selected for embeddings")


    def create_model(self,):
        super(MergeModel_create,self).create_model()
        models_list           = self.models_list

        self.input_dim        = self.arg.merge_model.architect.input_dim

        self.merge_type =      self.arg.merge_model.get('merge_type','cat')
        self.merge_layers_dim= self.arg.merge_model.architect.get('merge_layers_dim', [1024, 768] )
        self.merge_custom=     self.arg.merge_model.architect.get('merge_custom', None)

        self.head_layers_dim=  self.arg.merge_model.architect.get('head_layers_dim', [512, 128, 10] )
        self.head_custom=      self.arg.merge_model.architect.get('head_custom', None)

        self.loss_merge_custom = self.arg.merge_model.architect.get('loss_custom', None)



        class Modelmerge(torch.nn.Module):
            def __init__(self, models_list=None,
                         input_dim = 1200,  ### embA + embB + embC
                         merge_type       = 'cat',
                         merge_layers_dim = [1024, 768],
                         merge_custom     = None,
                         head_layers_dim  = [512, 128, 10],  ## 10 classe
                         head_custom      = None
                         ):
                super(Modelmerge, self).__init__()

                self.merge_type = merge_type ### merge type
                self.input_dim  = input_dim
                # assert head_layers_dim[0] == merge_layers_dim[-1]

                #### Create instance of each model   ############################
                self.models_nets = [None] * len(models_list)

                for i in range(len(models_list)):
                    if(models_list[i] is not None):
                        #self.models_nets.append(None)
                        self.models_nets[i] = copy.deepcopy(models_list[i].net)
                        self.models_nets[i].load_state_dict(models_list[i].net.state_dict())

                ##### Merge    #################################################
                if merge_custom is None :   ### Default merge
                    self.merge_task = []
                    input_dim = self.input_dim
                    for layer_dim in merge_layers_dim[1:-1]:
                        self.merge_task.append(nn.Linear(input_dim, layer_dim))
                        self.merge_task.append(nn.ReLU())
                        input_dim = layer_dim
                    self.merge_task.append(nn.Linear(input_dim, merge_layers_dim[-1]))

                    ##### MLP merge task
                    self.merge_task = nn.Sequential(*self.merge_task)
                else:
                    self.merge_task = merge_custom

                ##### Head Task   #############################################
                if head_custom is None :   ### Default head
                    self.head_task = []
                    input_dim = merge_layers_dim[-1]
                    for layer_dim in head_layers_dim[0:-1]:
                        self.head_task.append(nn.Linear(input_dim, layer_dim))
                        self.head_task.append(nn.ReLU())
                        input_dim = layer_dim
                    self.head_task.append(nn.Linear(input_dim, head_layers_dim[-1]))

                    ###### Not good in model due to compute errors, keep into Losss
                    # self.head_task.append(nn.Sigmoid())  #### output layer

                    ##### MLP Head task
                    self.head_task = nn.Sequential(*self.head_task)
                else:
                    self.head_task = head_custom

            def freeze_all(self,):
                for i in range(len(self.models_nets)):
                    if (self.models_nets[i] is not None):
                        for param in self.models_nets[i].parameters():
                                param.requires_grad = False

            def unfreeze_all(self,):
                for i in range(len(self.models_nets)):
                    if (self.models_nets[i] is not None):
                        for param in self.models_nets[i].parameters():
                                param.requires_grad = True

            def forward(self, x,**kw):
                z1 = self.forward_merge(x, **kw)
                z2 = self.head_task(z1)
                return z2    # predict absolute values


            def forward_merge(self, x,**kw):
                # merge: cat or add
                alpha = kw.get('alpha',0) # default only use YpredA
                scale = kw.get('scale',1)

                ## with torch.no_grad():
                embV = []
                for model in self.models_nets:
                    if model is not None:
                        #### Use the Pre-Trained model METHOD  get_embedding(x)
                        emb = model.get_embedding(x)
                        emb = torch_norm_l2(emb)
                        embV.append(emb)

                ###### Concatenerate   #############################
                if self.merge_type == 'cat_combine':
                    z = torch.cat((alpha*embV[1], (1-alpha)*embV[0]), dim=-1)

                elif self.merge_type == 'cat':
                    ### May need scale
                    z = torch.cat(embV, dim=-1)

                merge_emb = self.merge_task(z)
                return merge_emb


            def get_embedding(self, x,**kw):
                z1 = self.forward_merge(x, **kw)
                return z1

        return Modelmerge(models_list,
                          input_dim        = self.input_dim,  ### embA + embB + embC
                          merge_type=        self.merge_type,
                          merge_layers_dim = self.merge_layers_dim,
                          merge_custom=      self.merge_custom,
                          head_layers_dim=   self.head_layers_dim,  ## 10 classe
                          head_custom=       self.head_custom,
                          )


    def build(self):
        # super(MergeModel_create,self).build()

        for i in range(len(self.models_list)):
            log("model:{}".format(i))
            self.models_list[i].build() if self.models_list[i] is not None else None

        log("MergeModel:")
        self.net       = self.create_model().to(self.device)
        self.loss_calc = self.create_loss()#.to(self.device)

        #### BE cacreful to include all the params if COmbine loss.
        #### Here, only head_task
        # self.optimizer = torch.optim.Adam({ **self.net.merge_task.parameters() ,
        #                                    **self.net.head_task.parameters() ,  })
        #### contains all the params,  and pre-trained models are FREEZED
        self.optimizer = torch.optim.Adam(self.net.parameters())

        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode='min', factor=0.5, patience=5,
                         verbose=True, threshold=0.0001, threshold_mode='rel', 
                         cooldown=5,  ### cooldown : Loss is not decreasing --> reduce LR, wait for 5 steps.  
                         min_lr=0, eps=1e-08)
        #self.optimizer = torch.optim.Adam(self.head_task )


        #### Freeze modelA, modelB, to stop gradients.
        self.net.freeze_all()
        # self.freeze_all()



    def create_loss(self,):
        """ Simple Head task loss
           1) Only Head task loss : Classfieri head  ### Baseline
           Stop the gradient or not in modelA and modelB.
            embA_d = embA.detach()  ### Stop the gradient
            modelA_loss(x_a, embA)
        """
        super(MergeModel_create,self).create_loss()

        if self.loss_merge_custom is None :
           loss =  torch.nn.BCEWithLogitsLoss()
        else :
            loss = self.loss_merge_custom
        return loss


    def prepro_dataset(self,df:pd.DataFrame=None):
        if df is None:
            df = self.df     # if there is no dataframe feeded , get df from model itself

        coly = 'y'
        y    = df[coly].values
        X    = df.drop([coly], axis=1).values
        nsamples = X.shape[0]

        ##### Split   #########################################################################
        seed= 42
        train_ratio = self.arg.merge_model.train_config.TRAIN_RATIO
        test_ratio  = self.arg.merge_model.train_config.TEST_RATIO
        val_ratio   = self.arg.merge_model.train_config.TEST_RATIO
        train_X, test_X, train_y, test_y = train_test_split(X,  y,  test_size=1 - train_ratio, random_state=seed)
        valid_X, test_X, valid_y, test_y = train_test_split(test_X, test_y, test_size= test_ratio / (test_ratio + val_ratio), random_state=seed)
        return (train_X, train_y, valid_X,  valid_y, test_X,  test_y, )


    def training(self,load_DataFrame=None,prepro_dataset=None, dataloader_custom=None):
        """ Train Loop
        Docs:
             # training with load_DataFrame and prepro_data function or default funtion in self.method
        """

        batch_size = self.arg.merge_model.train_config.BATCH_SIZE
        EPOCHS     = self.arg.merge_model.train_config.EPOCHS
        path_save  = self.arg.merge_model.train_config.SAVE_FILENAME


        if dataloader_custom is None :
            df = load_DataFrame() if load_DataFrame else self.load_DataFrame()
            if prepro_dataset:
                train_X, train_y, valid_X,  valid_y, test_X,  test_y  = prepro_dataset(self,df)
            else:
                train_X, train_y, valid_X,  valid_y, test_X,  test_y = self.prepro_dataset(df)

            train_loader, valid_loader, test_loader =  dataloader_create(train_X, train_y, valid_X,  valid_y,
                                                                        test_X,  test_y,
                                                                        device=self.device, batch_size=batch_size)
        else :
            train_loader, valid_loader, test_loader = dataloader_custom()


        self.validate_dim(train_loader,valid_loader)
        for epoch in range(1,EPOCHS+1):
            self.train()
            loss_train = 0
            with torch.autograd.set_detect_anomaly(True):  ### debugging stuff.
                for inputs,targets in train_loader:
                    self.optimizer.zero_grad()
                    predict = self.predict(inputs)
                    
                    #### Supservised Classifier: dont do it here --> Do it a the model level.
                    #### Keep consistency for forward / backward.
                    if torch.is_tensor(predict) and predict.size() != targets.size():
                       predict = torch.reshape(predict,(predict.shape[0],))
                       
                    loss    = self.loss_calc(predict, targets)
                    # loss.grad
                    loss.backward()
                    self.optimizer.step()   ### Gradient update.
                    loss_train += loss * inputs.size(0)  ### Casting Type into tensor 
                loss_train /= len(train_loader.dataset) # mean on dataset

            ### Call Scheduler : need scheduler: for faster training (dynamic learning rate)
            ### High LR --> small LR,   Sinus /Cosinus LR
            # self.scheduler.step(loss_train) 
            self.grad_check()
            
            ##### Evaluation #######################################
            loss_val = 0
            self.eval()
            with torch.no_grad():
                for inputs,targets in valid_loader:
                    predict = self.predict(inputs)
                    if torch.is_tensor(predict) and predict.size() != targets.size():
                       predict = torch.reshape(predict,(predict.shape[0],))
                    self.optimizer.zero_grad()
                    loss = self.loss_calc(predict,targets)
                    loss_val += loss * inputs.size(0)
            loss_val /= len(valid_loader.dataset) # mean on dataset

            self.save_weight(  path = path_save, meta_data = { 'epoch' : epoch, 'loss_train': loss_train, 'loss_val': loss_val, } )


class model_create(BaseModel):
    """ modelA
    """
    def __init__(self,arg):
        super(model_create,self).__init__(arg)

    def create_model(self, modelA_nn:torch.nn.Module=None):
        super(model_create,self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id      = self.arg.layer_emb_id

        #if not modelA_nn: return modelA_nn

        ### Default version
        class modelA(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0):
                super(modelA, self).__init__()
                self.head_task = []
                self.layer_id  = layer_id  ##flag meaning ????  layer

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #setattr(self.nn_model_base, self.layer_id, self.head_task)  #### head
                    self.head_task = self.nn_model_base
                    return

                ###### Normal MLP Head   #########################################
                self.layers_dim = layers_dim
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()

                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self, x,**kwargs):
                layer_l2= ut.model_getlayer(self.head_task, pos_layer=-2)
                embA = self.forward(x)
                embA = layer_l2.output.squeeze()
                return embA

        return modelA(layers_dim, nn_model_base, layer_id)

    def create_loss(self, loss_fun=None) -> torch.nn.Module:
        super(model_create,self).create_loss()
        if not loss_fun : loss_fun
        return torch.nn.BCELoss()


from utilmy.deeplearning.ttorch.util_model import MultiClassMultiLabel_Head


#################################################################################################
def device_setup(arg, device='cpu', seed=67):
    """function device_setup
    """
    device = arg.get('device', device)
    seed   = arg.get('seed', seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if 'gpu' in device :
        try :
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        except Exception as e:
            log(e)
            device = 'cpu'
    return device


def dataloader_create(train_X=None, train_y=None, valid_X=None, valid_y=None, test_X=None, test_y=None,
                            device='cpu', batch_size=16,)->torch.utils.data.DataLoader:
    """function dataloader_create
    Args:
        train_X:
        train_y:
        valid_X:
        valid_y:
        test_X:
        test_y:
        arg:
    Returns:
    """
    train_loader, valid_loader, test_loader = None, None, None

    if train_X is not None :
        train_X, train_y = torch.tensor(train_X, dtype=torch.float32, device=device), torch.tensor(train_y, dtype=torch.float32, device=device)
        train_loader = DataLoader(TensorDataset(train_X, train_y), batch_size=batch_size, shuffle=True,drop_last=True)
        log("data size", len(train_X) )

    if valid_X is not None :
        valid_X, valid_y = torch.tensor(valid_X, dtype=torch.float32, device=device), torch.tensor(valid_y, dtype=torch.float32, device=device)
        valid_loader = DataLoader(TensorDataset(valid_X, valid_y), batch_size=valid_X.shape[0])
        log("data size", len(valid_X)  )

    if test_X  is not None :
        test_X, test_y   = torch.tensor(test_X,  dtype=torch.float32, device=device), torch.tensor(test_y, dtype=torch.float32, device=device)
        test_loader  = DataLoader(TensorDataset(test_X, test_y), batch_size=test_X.shape[0])
        log("data size:", len(test_X) )

    return train_loader, valid_loader, test_loader


def torch_norm_l2(X):
    """
    normalize the torch  tensor X by L2 norm.
    """
    X_norm = torch.norm(X, p=2, dim=1, keepdim=True)
    X_norm = X / X_norm
    return X_norm




def test_dataset_fashionmnist_get_torchdataloader(nrows=1000, batch_size=64, num_workers=8, transform_custom=None):
    """
       return dataloader_train,  dataloader_test
    """
    from torchvision import transforms, datasets, models
    from torch.utils import data

    transform = transform_custom
    if transform_custom is None :
        # transform to normalize the data
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize((0.5,), (0.5,))])


    dataset_train = datasets.FashionMNIST(root='fashion-mnist',
                                          train=True, download=True,transform=transform)

    dataset_test  = datasets.FashionMNIST(root='fashion-mnist',
                                         train=False, download=True, transform=transform)

    permutation = np.random.permutation(np.arange(len(dataset_train)))
    indices_rnd = permutation[:nrows]
    dt_train_rnd = data.DataLoader(dataset_train,
                                   batch_size=batch_size,
                                   sampler=data.SubsetRandomSampler(indices_rnd),
                                   num_workers= num_workers)

    permutation = np.random.permutation(np.arange(len(dataset_train)))
    indices_rnd = permutation[:nrows]
    dt_test_rnd  = data.DataLoader(dataset_test,
                                   batch_size=batch_size,
                                   sampler=data.SubsetRandomSampler(indices_rnd),
                                   num_workers= num_workers)

    return dt_train_rnd, dt_test_rnd




#################################################################################################
class zzmodelA_create(BaseModel):
    """ modelA
    """
    def __init__(self,arg):
        super(zzmodelA_create, self).__init__(arg)

    def create_model(self, modelA_nn:torch.nn.Module=None):
        super(zzmodelA_create, self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id      = self.arg.layer_emb_id

        #if not modelA_nn: return modelA_nn

        ### Default version
        class modelA(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  ):
                super(modelA, self).__init__()
                self.head_task = []
                self.layer_id  = layer_id  ##flag meaning ????  layer

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #setattr(self.nn_model_base, self.layer_id, self.head_task)  #### head
                    self.head_task = self.nn_model_base
                    return

                ###### Normal MLP Head   #########################################
                self.layers_dim = layers_dim
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()

                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)


            def forward(self, x,**kwargs):
                return self.head_task(x)


            def get_embedding(self, x,**kwargs):
                layer_l2= ut.model_getlayer(self.head_task, pos_layer=-2)
                embA = self.forward(x)
                embA = layer_l2.output.squeeze()
                return embA

        return modelA(layers_dim, nn_model_base, layer_id)

    def create_loss(self, loss_fun=None) -> torch.nn.Module:
        super(zzmodelA_create, self).create_loss()
        if not loss_fun : loss_fun
        return torch.nn.BCELoss()


class zzmodelB_create(BaseModel):
    """ modelB Creatio
    """
    def __init__(self,arg):
        super(zzmodelB_create, self).__init__(arg)
        self.nn_model_base = arg.nn_model

    def create_model(self):
        super(zzmodelB_create, self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id        = self.arg.layer_emb_id

        class modelB(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  )   :
                super(modelB, self).__init__()
                self.head_task = [None]
                self.layer_id    = layer_id

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #### Adding head task on top of
                    ## setattr(self.nn_model_base, self.layer_id, self.head_task)
                    self.head_task = self.nn_model_base
                    return

                ###### Normal MLP Head   #########################################
                self.head_task = []
                self.layers_dim = layers_dim
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()
                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self,x, **kwargs):
                layer_l2= ut.model_getlayer(self.head_task, pos_layer=-2)
                embB = self.forward(x)
                embB = layer_l2.output.squeeze()
                return embB
        return modelB(layers_dim, nn_model_base, layer_id )


    def create_loss(self) -> torch.nn.Module:
        super(zzmodelB_create, self).create_loss()
        return torch.nn.BCELoss()


class zzmodelC_create(BaseModel):
    """ modelC Creatio
    """
    def __init__(self,arg):
        super(zzmodelC_create, self).__init__(arg)
        self.nn_model_base = arg.nn_model

    def create_model(self):
        super(zzmodelC_create, self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id        = self.arg.layer_emb_id

        class modelC(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  )   :
                super(modelC, self).__init__()
                self.head_task = [None]
                self.layer_id    = layer_id

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #### Adding head task on top of
                    ## setattr(self.nn_model_base, self.layer_id, self.head_task)
                    self.head_task = self.nn_model_base
                    return

                ###### Normal MLP Head   #########################################
                self.head_task = []
                self.layers_dim = layers_dim
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()
                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self,x, **kwargs):
                layer_l2= ut.model_getlayer(self.head_task, pos_layer=-2)
                embC = self.forward(x)
                embC = layer_l2.output.squeeze()
                return embC
        return modelC(layers_dim, nn_model_base, layer_id )

    def create_loss(self) -> torch.nn.Module:
        super(zzmodelC_create, self).create_loss()
        return torch.nn.BCELoss()


class zzmodelD_create(BaseModel):
    """ modelD Creatio
    """
    def __init__(self,arg):
        super(zzmodelD_create, self).__init__(arg)
        self.nn_model_base = arg.nn_model

    def create_model(self):
        super(zzmodelD_create, self).create_model()
        layers_dim    = self.arg.architect
        nn_model_base = self.arg.nn_model
        layer_id        = self.arg.layer_emb_id

        class modelD(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0  )   :
                super(modelD, self).__init__()
                self.head_task = [None]
                self.layer_id    = layer_id

                ##### Pre-trained model   #########################################
                if len(self.layer_id) !=0 :
                    self.nn_model_base = nn_model_base
                    #### Adding head task on top of
                    ## setattr(self.nn_model_base, self.layer_id, self.head_task)
                    self.head_task = self.nn_model_base
                    return

                ###### Normal MLP Head   #########################################
                self.head_task = []
                self.layers_dim = layers_dim
                self.output_dim = layers_dim[-1]
                # self.head_task = nn.Sequential()
                input_dim = layers_dim[0]
                for layer_dim in layers_dim[:-1]:
                    self.head_task.append(nn.Linear(input_dim, layer_dim))
                    self.head_task.append(nn.ReLU())
                    input_dim = layer_dim
                self.head_task.append(nn.Linear(input_dim, layers_dim[-1]))
                self.head_task = nn.Sequential(*self.head_task)

            def forward(self, x,**kwargs):
                return self.head_task(x)

            def get_embedding(self,x, **kwargs):
                layer_l3= ut.model_getlayer(self.head_task, pos_layer=-2)
                embD = self.forward(x)
                embD = layer_l3.output[0][:,-1,:].squeeze() #Because LSTM cell gives 3D batched output
                return embD
        return modelD(layers_dim, nn_model_base, layer_id )

    def create_loss(self) -> torch.nn.Module:
        super(zzmodelD_create, self).create_loss()
        return torch.nn.BCELoss()


###############################################################################################################
if __name__ == "__main__":
    #import fire
    #fire.Fire()
    test6()


