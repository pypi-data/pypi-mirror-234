# -*- coding: utf-8 -*-
""" Utils for torch
Doc::

    utilmy/deeplearning/ttorch/util_torch.py
    -------------------------functions----------------------
    ImageDataloader(df = None, batch_size = 64, label_list = ['gender', 'masterCategory', 'subCategory' ], col_img = 'id', train_img_path   =  'data_fashion_small/train', test_img_path    =  'data_fashion_small/test', train_ratio = 0.5, val_ratio = 0.2, transform_train = None, transform_test = None, )
    cos_similar_embedding(embv  =  None, img_names = None)
    dataloader_create(train_X = None, train_y = None, valid_X = None, valid_y = None, test_X = None, test_y = None, batch_size = 64, shuffle = True, device = 'cpu', batch_size_val = None, batch_size_test = None)
    dataset_add_image_fullpath(df, col_img = 'id', train_img_path = "./", test_img_path = './')
    dataset_download(url    = "https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip", dirout  =  "./")
    dataset_traintest_split(anyobject, train_ratio = 0.6, val_ratio = 0.2)
    device_setup(device = 'cpu', seed = 42, arg:dict = None)
    embedding_load_parquet(dirin = "df.parquet", colid =  'id', col_embed =  'emb', nmax  = None)
    embedding_torchtensor_to_parquet(model  =  None, dirout  =  './', data_loader = None, tag = "")
    model_evaluate(model, loss_task_fun, test_loader, arg, )
    model_load(dir_checkpoint:str, torch_model = None, doeval = True, dotrain = False, device = 'cpu', input_shape = None, **kw)
    model_load_partially_compatible(model, dir_weights = '', device = 'cpu')
    model_load_state_dict_with_low_memory(model: nn.Module, state_dict: dict)
    model_save(torch_model = None, dir_checkpoint:str = "./checkpoint/check.pt", optimizer = None, cc:dict = None, epoch = -1, loss_val = 0.0, show = 1, **kw)
    model_summary(model, **kw)
    model_train(model, loss_calc, optimizer = None, train_loader = None, valid_loader = None, arg:dict = None)
    pd_to_onehot(dflabels: pd.DataFrame, labels_dict: dict  =  None)


    -------------------------methods----------------------
    DataForEmbedding.__getitem__(self, idx: int)
    DataForEmbedding.__init__(self, df = None, col_img: str = 'id', transforms = None, transforms_image_size_default = 64, img_loader = None)
    DataForEmbedding.__len__(self)
    ImageDataset.__getitem__(self, idx: int)
    ImageDataset.__init__(self, img_dir:str = "images/", col_img: str = 'id', label_dir:str    = "labels/mylabel.csv", label_dict:dict  = None, transforms = None, transforms_image_size_default = 64, check_ifimage_exist = False, img_loader = None)
    ImageDataset.__len__(self)


    Utils for torch training
    TVM optimizer
    https://spell.ml/blog/optimizing-pytorch-models-using-tvm-YI7pvREAACMAwYYz

    https://github.com/szymonmaszke/torchlayers

    https://github.com/Riccorl/transformers-embedder

    https://github.com/szymonmaszke/torchfunc


"""
import os, random, numpy as np, os, pandas as pd
from copy import deepcopy
from box import Box

import sklearn.datasets
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, TensorDataset


from utilmy.deeplearning.ttorch.util_model import (
    model_getlayer
)
#############################################################################################
from utilmy import log, os_module_name
from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob
MNAME = os_module_name(__file__)

def help():
    """function help"""
    from utilmy import help_create
    ss = help_create(MNAME)
    log(ss)


#############################################################################################
def test_all():
    """function test_all"""
    ztest1()
    ztest4()
    ztest5()


def ztest1():
    log('### test dataloader_create, model_train, model_evaluate')
    X, y = sklearn.datasets.make_classification(n_samples=100, n_features=50)
    train_loader, val_dl, tt_dl = dataloader_create(train_X=X, train_y=y, valid_X=X, valid_y=y, test_X=X, test_y=y)

    model = nn.Sequential(nn.Linear(50, 20), nn.Linear(20, 1))
    args  = {'model_info': {'simple':None}, 'lr':1e-3, 'epochs':2, 'model_type': 'simple',
            'dir_modelsave': 'model.pt', 'valid_freq': 1}

    model_train(model=model,   loss_calc=nn.MSELoss(), train_loader=train_loader, valid_loader=train_loader, arg=args)
    model_evaluate(model=model,loss_task_fun=nn.CrossEntropyLoss(), test_loader=train_loader, arg=args)


    log('### test model_save, model_load, model_summary, model_load_state_dict_with_low_memory')
    from torchvision import models
    model = models.resnet50()
    os.makedirs('./tests_temp_dir/', exist_ok=True)
    dir_checkpoint = model_save(model, dir_checkpoint='./tests_temp_dir/check.pt', cc=model.state_dict())
    model = model_load(dir_checkpoint=dir_checkpoint, torch_model=model, doeval=True)
    model = model_load(dir_checkpoint=dir_checkpoint, torch_model=model, doeval=False, dotrain=True)

    kwargs = {'input_size': (1, 3, 224, 224)}
    model_summary(model=model, **kwargs)
    model_load_state_dict_with_low_memory(model=model, state_dict=model.state_dict())


    log('### test device_setup, dataset_traintest_split, pd_to_onehot')
    device_setup(device='cpu', seed=123)
    assert torch.initial_seed() == 123, 'Seed assigning failed.'
    train_subset, val_subset, test_subset = dataset_traintest_split(range(10), train_ratio=.7, val_ratio=.2)
    assert len(train_subset) == 7 and len(val_subset) == 2 and len(test_subset) == 1, 'Dataset split failed.'

    _ = pd_to_onehot(pd.DataFrame({'gender': [1, 0, 1, 0, 1, 1, 0]}), labels_dict={'gender': [0, 1]})


def ztest4():
    log("### test torch_metric_accuracy, torch_pearson_coeff  ")
    model  = torch.hub.load('pytorch/vision:v0.10.0', 'alexnet', pretrained=True)
    data   = torch.rand(64, 3, 224, 224)
    output = model(data)
    labels = torch.randint(1000, (64,)) # random labels
    acc    = torch_metric_accuracy(output=output, labels=labels) 

    x1 = torch.rand(100,)
    x2 = torch.rand(100,)
    r = torch_pearson_coeff(x1, x2)

    x = torch.rand(100, 30)
    r_pairs = torch_pearson_coeff_pairs(x)

    data = torch.rand(64, 3, 224, 224)
    output = model(data)

    # This is just an example where class coded by 999 has more occurences
    # No train test splits are applied to lead to the overrepresentation of class 999 
    p = [(1 - 0.05) / 1000] * 999
    p.append(1 - sum(p))
    labels = np.random.choice(list(range(1000)), size=(10000,), p=p) # imbalanced 1000-class labels
    labels = torch.Tensor(labels).long()
    weight, label_weight = torch_class_weights(labels)
    loss = torch.nn.CrossEntropyLoss(weight = weight)
    # l = loss(output, labels[:64])


def ztest5():
    log('### test dataset_download, ImageDataloader, pd_to_onehot, dataset_add_image_fullpath, embedding_load_parquet')
    dataset_path = dataset_download(url="https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip")
    df = pd.read_csv(dataset_path + '/csv/styles_df.csv')
    train_subset, val_subset, test_subset = ImageDataloader(df)
    _ = dataset_add_image_fullpath(df)
    # _ = embedding_load_parquet(dataset_path + '/csv/styles_df.csv', col_embed='articleType')









###############################################################################################
def device_setup( device='cpu', seed=42, arg:dict=None):
    """Setup 'cpu' or 'gpu' for device and seed for torch
        
    """
    device = arg.device if arg is not None else device
    seed   = arg.seed   if arg is not None else seed
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







###############################################################################################
def dataloader_create(train_X=None, train_y=None, valid_X=None, valid_y=None, test_X=None, test_y=None,  
                     batch_size=64, shuffle=True, device='cpu', batch_size_val=None, batch_size_test=None):
    """dataloader_create
    Doc::

         Example

        
    """
    train_loader, valid_loader, test_loader = None, None, None

    batch_size_val  = valid_X.shape[0] if batch_size_val is None else batch_size_val
    batch_size_test = valid_X.shape[0] if batch_size_test is None else batch_size_test

    if train_X is not None :
        train_X, train_y = torch.tensor(train_X, dtype=torch.float32, device=device), torch.tensor(train_y, dtype=torch.float32, device=device)
        train_loader = DataLoader(TensorDataset(train_X, train_y), batch_size=batch_size, shuffle=shuffle)
        log("train size", len(train_X) )

    if valid_X is not None :
        valid_X, valid_y = torch.tensor(valid_X, dtype=torch.float32, device=device), torch.tensor(valid_y, dtype=torch.float32, device=device)
        valid_loader = DataLoader(TensorDataset(valid_X, valid_y), batch_size= batch_size_val)
        log("val size", len(valid_X)  )

    if test_X  is not None :
        test_X, test_y   = torch.tensor(test_X,  dtype=torch.float32, device=device), torch.tensor(test_y, dtype=torch.float32, device=device)
        test_loader  = DataLoader(TensorDataset(test_X, test_y), batch_size=batch_size_test) # modified by Abrham
        # test_loader  = DataLoader(TensorDataset(test_X, test_y), batch_size=test_X.shape[0]) 
        log("test size:", len(test_X) )

    return train_loader, valid_loader, test_loader


def dataset_download(url="https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip",
                     dirout = "./"):
    """ Downloading Dataset from github  and unzip it


    """
    import requests
    from zipfile import ZipFile

    fname = dirout + url.split("/")[-1]
    dname = dirout + "/".join( fname.split(".")[:-1])

    isdir = os.path.isdir(dname)
    if isdir == 0:
        r = requests.get(url)
        open(fname , 'wb').write(r.content)
        flag = os.path.exists(fname)
        if(flag):
            print("Dataset is Downloaded")
            zip_file = ZipFile(fname)
            zip_file.extractall()
        else:
            raise Exception("Dataset is not downloaded")
    else:
        print("dataset is already presented")
    return dname


def dataset_traintest_split(anyobject, train_ratio=0.6, val_ratio=0.2):
    """
    Docs:
        
        Dataset : Splitting dataset as Train & val by the ratios provided



    """
    #### Split anything
    val_ratio = val_ratio + train_ratio
    if isinstance(anyobject, pd.DataFrame):
        df = anyobject
        itrain,ival = int(len(df)* train_ratio), int(len(df)* val_ratio)
        df_train = df.iloc[0:itrain,:]
        df_val   = df.iloc[itrain:ival,:]
        df_test  = df.iloc[ival:,:]
        return df_train, df_val, df_test

    else :  ## if isinstance(anyobject, list):
        df = anyobject
        itrain,ival = int(len(df)* train_ratio), int(len(df)* val_ratio)
        df_train = df[0:itrain]
        df_val   = df[itrain:ival]
        df_test  = df[ival:]
        return df_train, df_val, df_test





###############################################################################################
####### Embedding #############################################################################
def model_diagnostic(model, data_loader, dirout="", tag="before_training"):
    """  output model otuput, embedding.

    """
    pass



def model_embedding_extract_check(model=None,  dirin=None, dirout=None, data_loader=None, tag="", colid='id', colemb='emb',
                                  force_getlayer= True,
                                  pos_layer=-2):
    """
    Docs:

        model : Pytorch requires  get_embedding(X)  method to extract embedding



    """
    if dirin is not None:
        embv1, img_names,df = embedding_load_parquet(dirin=f"{dirin}/df_emb_{tag}.parquet",
                                                     colid= colid, col_embed= colemb)
    else :
        emb_list = model_embedding_extract_to_parquet(model, dirout, data_loader, tag=tag, colid=colid, colemb=colemb,
                                            force_getlayer= force_getlayer, pos_layer=pos_layer)
        embv1    = [ x[1] for x in emb_list]


    dfsim = embedding_cosinus_scores_pairwise(embv1, name_list=None, is_symmetric=False)
    
    if dirout is not None:
        pd_to_file(dfsim, dirout +"/df_emb_cosim.parquet", show=1)
    return dfsim


def model_embedding_extract_to_parquet(model=None, dirout=None, data_loader=None, tag="", colid='id', colemb='emb',
                                       force_getlayer= True, pos_layer=-2):
    """
    Docs:

        model : Pytorch requires  get_embedding(X)  method to extract embedding



    """
    if force_getlayer == True:

       model_embed_extract_fun = model_getlayer(model, pos_layer=pos_layer)
    else:
       model_embed_extract_fun = model.get_embedding

    llist= []
    for X , lable, id_sample in data_loader:
        with torch.no_grad():
            #emb = model.get_embedding(X)   #### Need to get the layer !!!!!
            if force_getlayer == True:
               emb = model(X)
               emb = model_embed_extract_fun.output.squeeze()
            else:
                emb = model_embed_extract_fun(X)
            for i in range(emb.size()[0]):
                ss = emb[i].numpy()
                llist.append([ id_sample[i], ss])


    if dirout is not None :
        df2 = [ (k, np_array_to_str(v) )  for (k,v) in llist ]    ####  array as string
        df2 = pd.DataFrame(df2, columns= ['id', 'emb'])
        dirout2 = dirout + f"/df_emb_{tag}.parquet"
        pd_to_file(df2, dirout2, show=1 )

    return llist


def embedding_load_parquet(dirin="df.parquet", colid='id', col_embed= 'emb', nmax =None ):
    """  Required columns : id, emb (string , separated)
    
    """
    import glob

    log('loading', dirin)
    flist = list( glob.glob(dirin) )
    
    assert(flist is not None)
    df  = pd_read_file( flist, npool= max(1, int( len(flist) / 4) ) )
    if nmax is None:
        nmax  = len(df)   ### 5000
    df  = df.iloc[:nmax, :]
    df  = df.rename(columns={ col_embed: 'emb'})
    
    df  = df[ df['emb'].apply( lambda x: len(x)> 10  ) ]  ### Filter small vector
    log(df.head(5).T, df.columns, df.shape)
    log(df, df.dtypes)    


    ###########################################################################
    ###### Split embed numpy array, id_map list,  #############################
    vi      = [ float(v) for v in df['emb'][0].split(',')]
    embs    = np_str_to_array(df['emb'].values, mdim =len(vi) )
    id_map  = { name: i for i,name in enumerate(df[colid].values) }     
    log(",", str(embs)[:50], ",", str(id_map)[:50] )
    
    #####  Keep only label infos  ####
    del df['emb']                  
    return embs, id_map, df 



def embedding_cosinus_scores_pairwise(embs:np.ndarray, name_list:list=None, is_symmetric=False, sort=True):
    """ Pairwise Cosinus Sim scores
    Example:
        Doc::

           embs   = np.random.random((10,200))
           idlist = [str(i) for i in range(0,10)]
           df = sim_scores_fast(embs:np, idlist, is_symmetric=False)
           df[[ 'id1', 'id2', 'sim_score'  ]]

    """
    import copy, numpy as np
    # from sklearn.metrics.pairwise import cosine_similarity
    n= len(embs)
    name_list = np.arange(0, n) if name_list is None else name_list
    dfsim = []
    for i in  range(0, len(name_list) - 1) :
        vi = embs[i]
        normi = np.sqrt(np.dot(vi,vi))
        for j in range(i+1, len(name_list)) :
            # simij = cosine_similarity( embs[i,:].reshape(1, -1) , embs[j,:].reshape(1, -1)     )
            vj = embs[j]
            normj = np.sqrt(np.dot(vj, vj))
            simij = np.dot( vi ,  vj  ) / (normi * normj)
            dfsim.append([name_list[i], name_list[j], simij])
            # dfsim2.append([ nwords[i], nwords[j],  simij[0][0]  ])

    dfsim  = pd.DataFrame(dfsim, columns= ['id1', 'id2', 'sim_score' ] )

    if sort: dfsim = dfsim.sort_values(['id1','sim_score'], ascending=[1,0]  )

    if is_symmetric:
        ### Add symmetric part
        dfsim3 = copy.deepcopy(dfsim)
        dfsim3.columns = ['id2', 'id1', 'sim_score' ]
        dfsim          = pd.concat(( dfsim, dfsim3 ))
    return dfsim



def embedding_topk(embs = None, emb_name_list=None, topk=5):
    """ Pairwise Cosinus Sim scores(Numpy Implementation)
    Example:
        Doc::

           embs   = np.random.random((10,200))
           idlist = [str(i) for i in range(0,10)]
           df[[ 'id1', 'id2', 'sim_score'  ]]

    """
    dfsim = embedding_cosinus_scores_pairwise(embs, name_list= emb_name_list, sort=True)
    len( dfsim[[ 'id1', 'id2', 'sim_score']])

    def to_list(dfi):
        ### only top 5 are included
        ss = ",".join([str(t) for t in  dfi['id2'].values][:topk])
        return ss

    df2 = dfsim.groupby('id1').apply(lambda  dfi : to_list(dfi)).reset_index()
    df2.columns = ['id', 'similar']
    return df2

    """
    from sklearn.metrics.pairwise import cosine_similarity
    similar_emb = []
    n = len(embs)
    emb_name_list = np.arange(0, n) if emb_name_list is None else emb_name_list

    for i, emb1 in enumerate(embs):
        res = []
        for emb2 in embs:
            res.append(cosine_similarity([emb1],[emb2]))
        res[i] = -1
        max_value = max(res)
        img_name = emb_name_list[res.index(max_value)]
        similar_emb.append(img_name)

    df = pd.DataFrame(data = emb_name_list, columns=['id'])
    df['similar'] = similar_emb
    return df
    """




###############################################################################################
####### Image #################################################################################
def pd_to_onehot(dflabels: pd.DataFrame, labels_dict: dict = None) -> pd.DataFrame:
    """ Label INTO 1-hot encoding   {'gender': ['one', 'two']  }


    """
    if labels_dict is not None:
        for ci, catval in labels_dict.items():
            dflabels[ci] = pd.Categorical(dflabels[ci], categories=catval)

    labels_col = labels_dict.keys()

    for ci in labels_col:
        dfi_1hot = pd.get_dummies(dflabels, columns=[ci])  ### OneHot
        dfi_1hot = dfi_1hot[[t for t in dfi_1hot.columns if ci in t]]  ## keep only OneHot
        dflabels[ci + "_onehot"] = dfi_1hot.apply(lambda x: ','.join([str(t) for t in x]), axis=1)
        #####  0,0,1,0 format   log(dfi_1hot)
    return dflabels


def dataset_add_image_fullpath(df, col_img='id', train_img_path="./", test_img_path='./'):
    """ Get Correct image path from image id

    """
    import glob
    img_list = df[col_img].values

    if "/" in str(img_list[0]) :
        train_img_path = ''
        test_img_path  = ''
        log('id already contains the path')
    else :
        train_img_path = train_img_path + "/"
        test_img_path  = test_img_path  + "/"

    img_list_ok = []

    for fi in img_list :
        fifull = ''
        flist = glob.glob(train_img_path + str(fi) + "*"  )
        if len(flist) >0  :
           fifull = flist[0]

        flist = glob.glob(test_img_path  + str(fi) + "*"  )
        if len(flist) >0  :
           fifull = flist[0]

        img_list_ok.append(fifull)

    df[col_img] = img_list_ok
    df = df[ df[col_img] != '' ]
    # df = df.dropna(how='any',axis=0)
    return df



class ImageDataset(Dataset):
    """Custom DataGenerator using Pytorch Sequence for images
        df_label format :
        id, gender, gender_onehot_onehot, ....
    """
    def __init__(self, img_dir:str="images/",
                col_img: str='id',
                label_dir:str   ="labels/mylabel.csv",
                label_dict:dict =None,
                transforms=None, transforms_image_size_default=64,
                check_ifimage_exist=False,
                img_loader=None,
                return_img_id  = False
                 ):
        """ Image Datast :  labels + Images path on disk
        Docs:

            img_dir (Path(str)): String path to images directory
            label_dir (DataFrame): Dataset for Generator
            label_dict (dict):    {label_name : list of values }
            transforms (str): type of transformations to perform on images. Defaults to None.
            return_img_id : return image path
        """
        self.image_dir  = img_dir
        self.col_img    = col_img
        self.transforms = transforms
        self.return_img_id  = return_img_id

        if img_loader is None :  ### Use default loader
           from PIL import Image
           self.img_loader = Image.open


        if transforms is None :
              from torchvision import transforms
              self.transforms = [transforms.ToTensor(),transforms.Resize((transforms_image_size_default, transforms_image_size_default))]


        #### labels ############################################################################
        from utilmy import pd_read_file
        dflabel     = pd_read_file(label_dir)
        dflabel     = dflabel.dropna()
        assert col_img in dflabel.columns

        ##### Filter out label #####################
        for ci, label_list in label_dict.items():
           label_list = [label_list] if isinstance(label_list, str) else label_list
           dflabel[ci] = dflabel[ dflabel[ci].isin(label_list)][ci]


        if check_ifimage_exist :
           #### Bugggy, not working
           dflabel = dataset_add_image_fullpath(dflabel, col_img=col_img, train_img_path=img_dir, test_img_path= img_dir)

        self.dflabel       = dflabel
        self.label_cols    = list(label_dict.keys())
        self.label_img_dir = [ t.replace("\\", "/") for t in   self.dflabel[self.col_img].values ]


        self.label_dict = {}
        if self.return_img_id  == False:
            ####lable Prep  #######################################################################
            self.label_df      = pd_to_onehot(dflabel, labels_dict=label_dict)  ### One Hot encoding
            #
    
            for ci in self.label_cols:
                y1hot = [x.split(",") for x in self.label_df[ci + "_onehot"]]
                y1hot = np.array([[int(t) for t in vlist] for vlist in y1hot])
                self.label_dict[ci] = torch.tensor(y1hot,dtype=torch.float)

        else:
            #### Validation purpose, wiht image_name_id
            label_col = self.label_cols[0]
            # lable = label_dict[label_col]
            # self.dflabel = self.dflabel.loc[self.dflabel[label_col] == lable]
            self.dflabel = self.dflabel[[col_img,label_col]]
            # self.label_img_dir = self.dflabel[self.col_img].values
            ##Buggy 
            self.label_dict[label_col] = torch.ones(len(self.label_img_dir),dtype=torch.float)


    def __len__(self) -> int:
        return len(self.label_img_dir)


    def __getitem__(self, idx: int):
        ##### Load Image
        # train_X = self.data[idx]
        img_dir = self.label_img_dir[idx]
        img     = self.img_loader(img_dir)
        train_X = self.transforms(img)


        train_y = {}
        for classname, n_unique_label in self.label_dict.items():
            train_y[classname] = self.label_dict[classname][idx]

        if self.return_img_id == True: ##Data for Embeddings' extraction
            # img_dir  = img_dir.replace('\\','/')
            img_name = img_dir.split('/')[-1]
            return (train_X, train_y, img_name)

        return (train_X, train_y)



def ImageDataloader(df=None, batch_size=64,
                    label_list=['gender', 'masterCategory', 'subCategory' ],
                    col_img='id',
                    train_img_path  = 'data_fashion_small/train',
                    test_img_path   = 'data_fashion_small/test',
                    train_ratio=0.5, val_ratio=0.2,
                    transform_train=None,
                    transform_test=None,
                    ):
    """

    """
    from utilmy.deeplearning.ttorch import util_torch as ut

    #label_list  = label_list.split(",")   #### Actual labels

    assert len(df[col_img]) > 0 , 'error'
    assert len(df[label_list]) > 0 , 'error'


    ########### label file in CSV  ##################################
    label_dict       = {ci: df[ci].unique()  for ci in label_list}   ### list of cat values
    label_dict_count = {ci: df[ci].nunique() for ci in label_list}   ### count unique


    ########### Check Image path   ###################################
    df = ut.dataset_add_image_fullpath(df, col_img=col_img, train_img_path=train_img_path, test_img_path=test_img_path)


    ############ Train Test Split ####################################
    df_train, df_val, df_test = ut.dataset_traintest_split(df, train_ratio=train_ratio, val_ratio=val_ratio)


    #################TRAIN DATA##################
    # tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
    # transform_train  = transforms.Compose(tlist)

    # tlist = [transforms.ToTensor(),transforms.Resize((64,64))]
    # transform_test   = transforms.Compose(tlist)

    train_dataloader = DataLoader(ImageDataset( label_dir=df_train, label_dict=label_dict, col_img=col_img, transforms=transform_train),
                       batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

    val_dataloader   = DataLoader(ImageDataset( label_dir=df_val,   label_dict=label_dict, col_img=col_img, transforms=transform_train),
                       batch_size=batch_size, shuffle= True ,num_workers=0, drop_last=True)

    test_dataloader  = DataLoader(ImageDataset( label_dir=df_test,   label_dict=label_dict, col_img=col_img, transforms=transform_test),
                       batch_size=batch_size, shuffle= False ,num_workers=0, drop_last=True)

    return train_dataloader,val_dataloader,test_dataloader


###############################################################################################
########### Save, load, train, evaluate, summary ##############################################
def model_save(torch_model=None, dir_checkpoint:str="./checkpoint/check.pt", optimizer=None, cc:dict=None,
               epoch=-1, loss_val=0.0, show=1, **kw):
    """function model_save
    Doc::

        dir_checkpoint = "./check/mycheck.pt"
        model_save(model, dir_checkpoint, epoch=1,)
    """
    from copy import deepcopy
    dd = {}
    dd['model_state_dict'] = deepcopy(torch_model.state_dict())
    dd['epoch'] = cc.get('epoch',   epoch)
    dd['loss']  = cc.get('loss_val', loss_val)
    dd['optimizer_state_dict']  = optimizer.state_dict()  if optimizer is not None else {}

    torch.save(dd, dir_checkpoint)
    if show>0: log(dir_checkpoint)
    return dir_checkpoint


def model_load(dir_checkpoint:str, torch_model=None, doeval=True, dotrain=False, device='cpu', input_shape=None, **kw):
    """function model_load from checkpoint
    Doc::

        dir_checkpoint = "./check/mycheck.pt"
        torch_model    = "./mymodel:NNClass.py"   ### or Torch Object
        model_load(dir_checkpoint, torch_model=None, doeval=True, dotrain=False, device='cpu')
    """

    if isinstance(torch_model, str) : ### "path/mymodule.py:myModel"
        torch_class_name = load_function_uri(uri_name= torch_model)
        torch_model      = torch_class_name() #### Class Instance  Buggy
        log('loaded from file ', torch_model)

    if 'http' in dir_checkpoint :
       #torch.cuda.is_available():
       map_location = torch.device('gpu') if 'gpu' in device else  torch.device('cpu')
       import torch.utils.model_zoo as model_zoo
       model_state = model_zoo.load_url(dir_checkpoint, map_location=map_location)
    else :   
       checkpoint = torch.load( dir_checkpoint)
       model_state = checkpoint['model_state_dict']
       log( f"loss: {checkpoint.get('loss')}\t at epoch: {checkpoint.get('epoch')}" )
       
    torch_model.load_state_dict(state_dict=model_state)

    if doeval:
      ## Evaluate
      torch_model.eval()
      # x   = torch.rand(1, *input_shape, requires_grad=True)
      # out = torch_model(x)

    if dotrain:
      torch_model.train()  

    return torch_model 


def model_load_state_dict_with_low_memory(model: nn.Module, state_dict: dict):
    """  using 1x RAM for large model
    Doc::

        model = MyModel()
        model_load_state_dict_with_low_memory(model, torch.load("checkpoint.pt"))

        # free up memory by placing the model in the `meta` device
        https://github.com/FrancescoSaverioZuppichini/Loading-huge-PyTorch-models-with-linear-memory-consumption


    """

    def get_keys_to_submodule(model: nn.Module) -> dict:
        keys_to_submodule = {}
        # iterate all submodules
        for submodule_name, submodule in model.named_modules():
            # iterate all paramters in each submobule
            for param_name, param in submodule.named_parameters():
                # param_name is organized as <name>.<subname>.<subsubname> ...
                # the more we go deep in the model, the less "subname"s we have
                splitted_param_name = param_name.split('.')
                # if we have only one subname, then it means that we reach a "leaf" submodule, 
                # we cannot go inside it anymore. This is the actual parameter
                is_leaf_param = len(splitted_param_name) == 1
                if is_leaf_param:
                    # we recreate the correct key
                    key = f"{submodule_name}.{param_name}"
                    # we associate this key with this submodule
                    keys_to_submodule[key] = submodule
                    
        return keys_to_submodule

    # free up memory by placing the model in the `meta` device
    model.to(torch.device("meta"))
    keys_to_submodule = get_keys_to_submodule(model)
    for key, submodule in keys_to_submodule.items():
        # get the valye from the state_dict
        val = state_dict[key]
        # we need to substitute the parameter inside submodule, 
        # remember key is composed of <name>.<subname>.<subsubname>
        # the actual submodule's parameter is stored inside the 
        # last subname. If key is `in_proj.weight`, the correct field if `weight`
        param_name = key.split('.')[-1]
        param_dtype = getattr(submodule, param_name).dtype
        val = val.to(param_dtype)
        # create a new parameter
        new_val = torch.nn.Parameter(val)
        setattr(submodule, param_name, new_val)


def model_load_partially_compatible(model, dir_weights='', device='cpu'):
    current_model=model.state_dict()
    keys_vin=torch.load(dir_weights,map_location=device)

    new_state_dict={k:v if v.size()==current_model[k].size()  else  current_model[k] for k,v in zip(current_model.keys(), keys_vin['model_state_dict'].values())
                    }
    current_model.load_state_dict(new_state_dict)
    return current_model


def model_train(model, loss_calc, optimizer=None, train_loader=None, valid_loader=None, arg:dict=None ):
    """One liner for training a pytorch model.
    Doc::

       import utilmy.deepelearning.ttorch.util_torch as ut
       cc= Box({})
       cc=0

       model= ut.test_model_dummy2()
       log(model)

       ut.model_train(model,
            loss_calc=
            optimizer= torch.optim.Adam(model.parameters(), lr= cc.lr)


    """
    arg   = Box(arg)  ### Params
    histo = Box({})  ### results


    arg.lr     = arg.get('lr', 0.001)
    arg.epochs = arg.get('epochs', 1)
    arg.early_stopping_thld    = arg.get('early_stopping_thld' ,2)
    arg.seed   = arg.get('seed', 42)
    model_params   = arg.model_info[ arg.model_type]

    metric_list = arg.get('metric_list',  ['mean_squared_error'] )


    #### Optimizer model params
    if optimizer is None:
       optimizer      = torch.optim.Adam(model.parameters(), lr= arg.lr)


    #### Train params
    counter_early_stopping = 1
    log('saved_filename: {}\n'.format( arg.dir_modelsave))
    best_val_loss = float('inf')


    for epoch in range(1, arg.epochs+1):
      model.train()
      for batch_train_x, batch_train_y in train_loader:
        batch_train_y = batch_train_y.unsqueeze(-1)
        optimizer.zero_grad()

        ###### Base output #########################################
        output    = model(batch_train_x) .view(batch_train_y.size())


        ###### Loss Rule perturbed input and its output
        loss = loss_calc(output, batch_train_y) # Changed by Abrham


        ###### Total Losses
        loss.backward()
        optimizer.step()


      # Evaluate on validation set
      if epoch % arg.valid_freq == 0:
        model.eval()
        with torch.no_grad():
          for val_x, val_y in valid_loader:
            val_y = val_y.unsqueeze(-1)

            output = model(val_x).reshape(val_y.size())
            val_loss_task = loss_calc(output, val_y).item()

            val_loss = val_loss_task
            y_true = val_y.cpu().numpy()
            y_score = output.cpu().numpy()
            y_pred = np.round(y_score)

            y_true = y_pred.reshape(y_true.shape[:-1])
            y_pred = y_pred.reshape(y_pred.shape[:-1])
            val_acc = metrics_eval(y_pred, ytrue=y_true, metric_list= metric_list)


          if val_loss < best_val_loss:
            counter_early_stopping = 1
            best_val_loss = val_loss
            best_model_state_dict = deepcopy(model.state_dict())
            torch.save({
                'epoch': epoch,
                'model_state_dict': best_model_state_dict,
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_val_loss
            }, arg.dir_modelsave)
          else:
            log( f'[Valid] Epoch: {epoch} Loss: {val_loss} ')
            if counter_early_stopping >= arg.early_stopping_thld:
              break
            else:
              counter_early_stopping += 1


def model_evaluate(model, loss_task_fun, test_loader, arg, ):
    """function model_evaluation
    Doc::

        Args:
            model:
            loss_task_func:
            arg:
            dataset_load1:
            dataset_preprocess1:
        Returns:
            utilmy.deeplearning.util_dl.metrics_eval(ypred: Optional[numpy.ndarray] = None, ytrue: Optional[numpy.ndarray] = None, metric_list: list = ['mean_squared_error', 'mean_absolute_error'], ypred_proba: Optional[numpy.ndarray] = None, return_dict: bool = False, metric_pars: Optional[dict] = None)→ pandas.core.frame.DataFrame

        https://arita37.github.io/myutil/en/zdocs_y23487teg65f6/utilmy.deeplearning.html#utilmy.deeplearning.util_dl.metrics_eval
    """
    from utilmy.deeplearning.util_dl import metrics_eval
    dfmetric = pd.DataFrame()

    model.eval()

    with torch.no_grad():
        for Xval, yval in test_loader:
            yval = yval.unsqueeze(-1)
            ypred = model(Xval) 
            loss_val = loss_task_fun(ypred, yval)
            ypred = torch.argmax(ypred, dim=1)
            dfi = metrics_eval(ypred.numpy(), yval.numpy(), metric_list=['accuracy_score'])
            dfmetric = pd.concat((dfmetric, dfi, pd.DataFrame([['loss', loss_val]], columns=['name', 'metric_val'])))
    return dfmetric


def model_summary(model, **kw):
    """   PyTorch model to summarize.
    Doc::

        https://pypi.org/project/torch-summary/
        #######################
        import torchvision
        model = torchvision.models.resnet50()
        summary(model, (3, 224, 224), depth=3)
        #######################
        model (nn.Module):
                PyTorch model to summarize.

        input_data (Sequence of Sizes or Tensors):
                Example input tensor of the model (dtypes inferred from model input).
                - OR -
                Shape of input data as a List/Tuple/torch.Size
                (dtypes must match model input, default is FloatTensors).
                You should NOT include batch size in the tuple.
                - OR -
                If input_data is not provided, no forward pass through the network is
                performed, and the provided model information is limited to layer names.
                Default: None

        batch_dim (int):
                Batch_dimension of input data. If batch_dim is None, the input data
                is assumed to contain the batch dimension.
                WARNING: in a future version, the default will change to None.
                Default: 0

        branching (bool):
                Whether to use the branching layout for the printed output.
                Default: True

        col_names (Iterable[str]):
                Specify which columns to show in the output. Currently supported:
                ("input_size", "output_size", "num_params", "kernel_size", "mult_adds")
                If input_data is not provided, only "num_params" is used.
                Default: ("output_size", "num_params")

        col_width (int):
                Width of each column.
                Default: 25

        depth (int):
                Number of nested layers to traverse (e.g. Sequentials).
                Default: 3

        device (torch.Device):
                Uses this torch device for model and input_data.
                If not specified, uses result of torch.cuda.is_available().
                Default: None

        dtypes (List[torch.dtype]):
                For multiple inputs, specify the size of both inputs, and
                also specify the types of each parameter here.
                Default: None

        verbose (int):
                0 (quiet): No output
                1 (default): Print model summary
                2 (verbose): Show weight and bias layers in full detail
                Default: 1

        *args, **kwargs:
                Other arguments used in `model.forward` function.

    Return:
        ModelStatistics object
                See torchsummary/model_statistics.py for more information.
    """
    from torchinfo import summary

    return summary(model, **kw)





###############################################################################################
########### Metrics  ##########################################################################
from utilmy.deeplearning.util_dl import metrics_eval

"""
def metrics_cosinus_similarity(emb_list1=None, emb_list2=None, name_list=None):
    ##Compare 2 list of vectors return cosine similarity score

    Docs
        cola (str): list of embedding
        colb (str): list of embedding
        model (model instance): Pretrained sentence transformer model

    Returns:
        pd DataFrame: 'cosine_similarity' column and return df
    
    from sklearn.metrics.pairwise import cosine_similarity

    results = list()
    for emb1,emb2 in zip(emb_list1, emb_list2):

        #if isinstance(emb1, torch.Tensor) :
        #    emb1 = emb1

        result = cosine_similarity([emb1],[emb2])
        results.append(result[0])

    df = pd.DataFrame(results, columns=['cos_sim'])

    if name_list is not None :
        df['name'] = name_list
    return df
"""


def torch_pearson_coeff(x1, x2):
    '''Computes pearson correlation coefficient between two 1D tensors
    with torch
    
    Input
    -----
    x1: 1D torch.Tensor of shape (N,)
    
    x2: 1D torch.Tensor of shape (N,)
    
    Output
    ------
    r: scalar pearson correllation coefficient 
    '''
    cos = torch.nn.CosineSimilarity(dim = 0, eps = 1e-6)
    r = cos(x1 - x1.mean(dim = 0, keepdim = True), 
            x2 - x2.mean(dim = 0, keepdim = True))
    
    return r


def torch_pearson_coeff_pairs(x): 
    '''Computes pearson correlation coefficient across 
    the 1st dimension of a 2D tensor  
    
    Input
    -----
    x: 2D torch.Tensor of shape (N,M)
    correlation coefficients will be computed between 
    all unique pairs across the first dimension
    x[1,M] x[2,M], ...x[i,M] x[j,M], for unique pairs (i,j)

    Output
    ------
    r: list of tuples such that r[n][0] scalar denoting the 
    pearson correllation coefficient of the pair of tensors with idx in 
    tuple r[n][1] 
    '''
    from itertools import combinations 
    all_un_pair_comb = [comb for comb in combinations(list(range(x.shape[0])), 2)]
    r = []
    for aupc in all_un_pair_comb:
        current_r = torch_pearson_coeff(x[aupc[0], :], x[aupc[1], :])    
        r.append((current_r, (aupc[0], aupc[1])))
    
    return r


def torch_metric_accuracy(output = None, labels = None):
    ''' Classification accuracy calculation as acc = (TP + TN) / nr total pred
    
    Input
    -----
    output: torch.Tensor of size (N,M) where N are the observations and 
        M the classes. Values must be such that highest values denote the 
        most probable class prediction.
    
    labels: torch.Tensor tensor of size (N,) of int denoting for each of the N
        observations the class that it belongs to, thus int must be in the 
        range 0 to M-1
    
    Output
    ------
    acc: float, accuracy of the predictions    
    '''
    _ , predicted = torch.max(output.data, 1)
    total = labels.size(0)
    correct = (predicted == labels).sum().item()
    acc = 100*(correct/total)

    return acc 


def torch_class_weights(labels):
    '''Compute class weights for imbalanced classes
    
    Input
    -----
    labels: torch.Tensor of shape (N,) of int ranging from 0,1,..C-1 where
        C is the number of classes
    
    Output
    ------
    weights: torch.Tensor of shape (C,) where C is the number of classes 
        with the weights of each class based on the occurence of each class
        NOTE: computed as weights_c = min(occurence) / occurence_c
        for class c
    
    labels_weights: dict, with keys the unique int for each class and values
        the weight assigned to each class based on the occurence of each class    
    '''
    labels_unique = torch.unique(labels)
    occurence = [len(torch.where(lu == labels)[0]) for lu in labels_unique]
    weights = [min(occurence) / o for o in occurence]
    labels_weights = {lu.item():w for lu,w in zip(labels_unique, weights)}
    weights = torch.Tensor(weights)
    
    return weights, labels_weights


def torch_effective_dim(X, center = True):
        '''Compute the effective dimension based on the eigenvalues of X
        
        Input
        -----
        X: tensor of shape (N,M) where N the samples and M the features
        
        center: bool, default True, indicating if X should be centered or not
        
        Output
        ------
        ed: effective dimension of X
        '''
        pca = torch.pca_lowrank(X, 
                                q = min(X.shape), 
                                center = center)
        eigenvalues = pca[1]
        eigenvalues = torch.pow(eigenvalues, 2) / (X.shape[0] - 1)
        li = eigenvalues /torch.sum(eigenvalues)
        ed = 1 / torch.sum(torch.pow(li, 2))
        
        return ed






#############################################################################################
########### Utils  ##########################################################################
from utilmy.utilmy_base import load_function_uri


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def test_load_function_uri():
    uri_name = "./testdata/ttorch/models.py:SuperResolutionNet"
    myclass = load_function_uri(uri_name)
    log(myclass)


def test_create_model_pytorch(dirsave=None, model_name=""):
    """   Create model classfor testing purpose

    
    """    
    ss = """import torch ;  import torch.nn as nn; import torch.nn.functional as F
    class SuperResolutionNet(nn.Module):
        def __init__(self, upscale_factor, inplace=False):
            super(SuperResolutionNet, self).__init__()

            self.relu = nn.ReLU(inplace=inplace)
            self.conv1 = nn.Conv2d(1, 64, (5, 5), (1, 1), (2, 2))
            self.conv2 = nn.Conv2d(64, 64, (3, 3), (1, 1), (1, 1))
            self.conv3 = nn.Conv2d(64, 32, (3, 3), (1, 1), (1, 1))
            self.conv4 = nn.Conv2d(32, upscale_factor ** 2, (3, 3), (1, 1), (1, 1))
            self.pixel_shuffle = nn.PixelShuffle(upscale_factor)

            self._initialize_weights()

        def forward(self, x):
            x = self.relu(self.conv1(x))
            x = self.relu(self.conv2(x))
            x = self.relu(self.conv3(x))
            x = self.pixel_shuffle(self.conv4(x))
            return x

        def _initialize_weights(self):
            init.orthogonal_(self.conv1.weight, init.calculate_gain('relu'))
            init.orthogonal_(self.conv2.weight, init.calculate_gain('relu'))
            init.orthogonal_(self.conv3.weight, init.calculate_gain('relu'))
            init.orthogonal_(self.conv4.weight)    

    """
    ss = ss.replace("    ", "")  ### for indentation

    if dirsave  is not None :
        with open(dirsave, mode='w') as fp:
            fp.write(ss)
        return dirsave    
    else :
        SuperResolutionNet =  None
        eval(ss)        ## trick
        return SuperResolutionNet  ## return the class


def np_array_to_str(vv, ):
    """ array/list into  "," delimited string """
    vv= np.array(vv, dtype='float32')
    vv= [ str(x) for x in vv]
    return ",".join(vv)


def np_str_to_array(vv, mdim = 200, l2_norm_faiss=False, l2_norm_sklearn=True):
    """ Convert list of string into numpy 2D Array
    Docs::

            np_str_to_array(vv=[ '3,4,5', '7,8,9'],  mdim = 3)

    """

    X = np.zeros(( len(vv) , mdim  ), dtype='float32')
    for i, r in enumerate(vv) :
        try :
            vi      = [ float(v) for v in r.split(',')]
            X[i, :] = vi
        except Exception as e:
            log(i, e)


    if l2_norm_sklearn:
        from sklearn.preprocessing import normalize
        normalize(X, norm='l2', copy=False)

    if l2_norm_faiss:
        import faiss   #### pip install faiss-cpu
        faiss.normalize_L2(X)  ### Inplace L2 normalization
        log("Normalized X")
    return X


def np_matrix_to_str2(m, map_dict:dict):
    """ 2D numpy into list of string and apply map_dict.

    Doc::
        map_dict = { 4:'four', 3: 'three' }
        m= [[ 0,3,4  ], [2,4,5]]
        np_matrix_to_str2(m, map_dict)

    """
    res = []
    for v in m:
        ss = ""
        for xi in v:
            ss += str(map_dict.get(xi, "")) + ","
        res.append(ss[:-1])
    return res


def np_matrix_to_str(m):
    res = []
    for v in m:
        ss = ""
        for xi in v:
            ss += str(xi) + ","
        res.append(ss[:-1])
    return res


def np_matrix_to_str_sim(m):   ### Simcore = 1 - 0.5 * dist**2
        res = []
        for v in m:
            ss = ""
            for di in v:
                ss += str(1-0.5*di) + ","
            res.append(ss[:-1])
        return res




#############################################################################################
########### Test Utils  #####################################################################
class test_model_dummy(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=4):
        super(test_model_dummy, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.net = nn.Sequential(nn.Linear(input_dim, hidden_dim),
                                nn.ReLU(),
                                nn.Linear(hidden_dim, output_dim))

    def forward(self, x):
        return self.net(x)


class test_model_dummy2(nn.Sequential):
    def __init__(self):
        super().__init__()
        self.in_proj = nn.Linear(2, 10)
        self.stages = nn.Sequential(
            nn.Linear(10, 10),
            nn.Linear(10, 10)
        )
        self.out_proj = nn.Linear(10, 2)


def test_dataset_classification_fake(nrows=500):
    """function test_dataset_classification_fake
    Args:
        nrows:
    Returns:

    """
    from sklearn import datasets as sklearn_datasets
    ndim    =11
    coly    = 'y'
    colnum  = ["colnum_" +str(i) for i in range(0, ndim) ]
    colcat  = ['colcat_1']
    X, y    = sklearn_datasets.make_classification(n_samples=nrows, n_features=ndim, n_classes=1,
                                                    n_informative=ndim-2)
    df         = pd.DataFrame(X,  columns= colnum)
    df[coly]   = y.reshape(-1, 1)

    for ci in colcat :
        df[ci] = np.random.randint(0,1, len(df))

    pars = { 'colnum': colnum, 'colcat': colcat, "coly": coly }
    return df, pars


def test_dataset_fashion_mnist(samples=100, random_crop=False, random_erasing=False,
                                convert_to_RGB=False,val_set_ratio=0.2, test_set_ratio=0.1,num_workers=1):
        """function test_dataset_f_mnist
        """

        from torchvision.transforms import transforms
        from torchvision import datasets

        # Generate the transformations
        train_list_transforms = [
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]

        test_list_transforms = [
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]

        # Add random cropping to the list of transformations
        if random_crop:
            train_list_transforms.insert(0, transforms.RandomCrop(28, padding=4))

        # Add random erasing to the list of transformations
        if random_erasing:
            train_list_transforms.append(
                transforms.RandomErasing(
                    p=0.5,
                    scale=(0.02, 0.33),
                    ratio=(0.3, 3.3),
                    value="random",
                    inplace=False,
                )
            )
        #creating RGB channels
        if convert_to_RGB:
            convert_to_RGB = transforms.Lambda(lambda x: x.repeat(3, 1, 1))
            train_list_transforms.append(convert_to_RGB)
            test_list_transforms.append(convert_to_RGB)

        # Train Data
        train_transform = transforms.Compose(train_list_transforms)

        train_dataset = datasets.FashionMNIST(
                        root="data", train=True, transform=train_transform, download=True)

        # Define the size of the training set and the validation set
        train_set_length = int(  len(train_dataset) * (100 - val_set_ratio*100) / 100)
        val_set_length = int(len(train_dataset) - train_set_length)

        train_set, val_set = torch.utils.data.random_split(
            train_dataset, (train_set_length, val_set_length)
        )

        #Custom data samples for ensemble model training
        train_set_smpls = int(samples - (val_set_ratio*100))
        val_set_smpls   = int(samples - train_set_smpls)
        test_set_smpls  = int(samples*test_set_ratio)

        #train dataset loader
        train_loader = torch.utils.data.DataLoader(
            train_set,
            batch_size=train_set_smpls,
            shuffle=True,
            num_workers=num_workers,
        )

        #validation dataset dataloader
        val_loader = torch.utils.data.DataLoader(
                        val_set, batch_size=val_set_smpls, shuffle=True, num_workers=1,
                    )


        # Test Data
        test_transform = transforms.Compose(test_list_transforms)

        test_set = datasets.FashionMNIST(
            root="./data", train=False, transform=test_transform, download=True
        )

        test_loader = torch.utils.data.DataLoader(
            test_set,
            batch_size=test_set_smpls,
            shuffle=False,
            num_workers=num_workers,
        )

        #Dataloader iterators, provides number of samples
        #configured in respective dataloaders
        #returns tensors of size- (samples*3*28*28)
        train_X, train_y = next(iter(train_loader))
        valid_X, valid_y = next(iter(val_loader))
        test_X, test_y = next(iter(test_loader))

        return train_X, train_y,   valid_X, valid_y,   test_X , test_y


###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()
