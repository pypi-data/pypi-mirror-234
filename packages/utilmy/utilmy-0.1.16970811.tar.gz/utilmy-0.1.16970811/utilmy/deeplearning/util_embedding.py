# -*- coding: utf-8 -*-
"""# Embedding visualizer in 2D Graph
Doc::

    --  pip install umap-learn mpld3

    from utilmy.deeplearning import util_embedding as ue
    dirtmp ="./ztmp/"
    dd = ue.test_create_fake_df(dirout= dirtmp, nrows=1000)
    log(dd)

    ue.embedding_create_vizhtml(dirin=dirtmp + "/emb_parquet/*.parquet",
                                dirout=dirtmp + "/out/", dim_reduction='mds', nmax=200, ntrain=200,
                                num_clusters=2,
                                )

    ue.embedding_create_vizhtml(dirin=dirtmp + "/emb_parquet/*.parquet",
                                dirout=dirtmp + "/out/", dim_reduction='umap', nmax=200, ntrain=200,
                                num_clusters=2,
                                )


"""
import os, sys, datetime, glob, random, time, warnings
import numpy as np, pandas as pd
from box import Box

warnings.filterwarnings("ignore")
from warnings import simplefilter  ; simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    import matplotlib.pyplot as plt
    from sklearn.metrics.pairwise import cosine_similarity
    

from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob


#### Optional imports
# try :
#     pass
#     #import hdbscan, umap
#     # import diskcache as dc
#     # import faiss
#     # import mpld3
#
# except:
#     print("pip install faiss-cpu  diskcache faiss mpld3 hdbscan umap")
#     1/0



#############################################################################################
from utilmy import log, os_module_name
def help():
    """function help        """
    from utilmy import help_create
    print( help_create(__file__) )



#############################################################################################
def test_all() -> None:
    """ python  $utilmy/deeplearning/util_embedding.py test_all         """
    test1()


def test1() -> None:
    """Test    embedding_create_vizhtml
    """
    dirtmp ="./ztmp/"

    dd = test_create_fake_df(dirout= dirtmp, nrows=1000)
    log(dd)

    embedding_create_vizhtml(dirin=dirtmp + "/emb_parquet/*.parquet",
                                dirout=dirtmp + "/out/", dim_reduction='mds', nmax=200, ntrain=200,
                                num_clusters=2,
                                )

    embedding_create_vizhtml(dirin=dirtmp + "/emb_parquet/*.parquet",
                                dirout=dirtmp + "/out/", dim_reduction='umap', nmax=200, ntrain=200,
                                num_clusters=2,
                                )



#########################################################################################################
############### Visualize the embeddings ################################################################
def embedding_create_vizhtml(dirin="in/model.vec", dirout="ztmp/", dim_reduction='umap', nmax=100, ntrain=10,
                             num_clusters=5,):
   """Create HTML plot file of embeddings.
   Doc::

        dirin= "  .parquet OR  Word2vec .vec  OR  .pkl  file"
        embedding_create_vizhtml(dirin="in/model.vec", dirout="zhtmlfile/",
                                 dim_reduction='umap', nmax=100, ntrain=10)


   """
   tag     = f"{nmax}_{dim_reduction}"

   #### Generate HTML  ############################################
   log(dirin)

   myviz = EmbeddingViz(path = dirin, num_clusters=num_clusters,)
   myviz.load_data(nmax= nmax)
   myviz.run_all(dirout= dirout, dim_reduction=dim_reduction, nmax=nmax, ntrain=ntrain)



class EmbeddingViz:
    def __init__(self, path="myembed.parquet", num_clusters=2, sep=";", config:dict=None):
        """ Visualize Embedding
        Doc::

                Many issues with numba, numpy, pyarrow !!!!
                pip install  pynndescent==0.5.4  numba==0.53.1  umap-learn==0.5.1  llvmlite==0.36.0   numpy==1.19.1   --no-deps

                myviz = vizEmbedding(path = "C:/D/gitdev/cpa/data/model.vec")
                myviz.run_all(nmax=5000)

                myviz.dim_reduction(mode='mds')
                myviz.create_visualization(dir_out="ztmp/vis/")

        """
        self.path         = path
        self.sep          = sep
        self.num_clusters = num_clusters
        self.dist         = None

        ### Plot @D coordinate
        self.coordinate_xy:np.array = None

        ### Store the embeddings
        self.id_map    = None
        self.df_labels = None
        self.embs      = None


    def run_all(self, dim_reduction="mds", col_embed='embed', ndim=2, nmax= 5000, dirout="ztmp/", ntrain=10000):
       self.dim_reduction(dim_reduction, ndim=ndim, nmax= nmax, dirout=dirout, ntrain=ntrain)
       self.create_clusters(after_dim_reduction=True)
       self.create_visualization(dirout, mode='d3', cols_label=None, show_server=False)


    def load_data(self,  col_embed='embed', nmax= 5000,  npool=2 ):
        """  Load embedding vector from file.
        Doc::

                ip_map :     dict  0--N  Integer to  id_label
                df_labelss : pandas dataframe: id, label1, label2
                embs  :      list of np array


        """
        if ".vec"  in self.path :       embs, id_map, df_labels = embedding_load_word2vec(self.path, nmax= nmax)

        elif ".pkl" in self.path :      embs, id_map, df_labels = embedding_load_pickle(self.path,   nmax= nmax)

        elif ".parquet" in self.path :  embs, id_map, df_labels = embedding_load_parquet(self.path,  nmax= nmax)

        else : raise Exception('not implemented')

        assert isinstance(id_map, dict)
        assert isinstance(df_labels, pd.DataFrame)
        assert isinstance(embs, np.ndarray) or isinstance(embs, list)

        self.id_map    = id_map
        self.df_labels = df_labels
        self.embs      = embs

        log( 'embs shape:', embs.shape )


    def dim_reduction(self, mode="mds", ndim=2, nmax= 5000, dirout=None, ntrain=10000, npool=2):
        """  Reduce dimension of embedding into 2D X,Y for plotting.
        Doc::

             mode:   'mds', 'umap'  algo reduction.
             ntrain: 10000, nb of samples to train.
            
        """
        pos = None
        if mode == 'mds' :
            ### Co-variance matrix
            from sklearn.manifold import MDS
            # dist = 1 - cosine_similarity(self.embs)
            # mds = MDS(n_components=ndim, dissimilarity="precomputed", random_state=1)
            # pos = mds.fit_transform(dist)  # shape (n_components, n_samples)            
            # dist = 1 - cosine_similarity(self.embs)
            
            mds = MDS(n_components=ndim, dissimilarity="euclidean", random_state=1)
            pos = mds.fit_transform( self.embs )  # shape (n_components, n_samples)


        if mode == 'umap' :
            import umap
            y_label = None
            from umap import UMAP
            clf = UMAP( set_op_mix_ratio=0.25, ## Preserve outlier
                        densmap=False, dens_lambda=5.0,          ## Preserve density
                        n_components= ndim,
                        n_neighbors=7,  metric='euclidean',
                        metric_kwds=None, output_metric='euclidean',
                        output_metric_kwds=None, n_epochs=None,
                        learning_rate=1.0, init='spectral',
                        min_dist=0.0, spread=1.0, low_memory=True, n_jobs= npool,
                        local_connectivity=1.0,
                        repulsion_strength=1.0, negative_sample_rate=5,
                        transform_queue_size=4.0, a=None, b=None, random_state=None,
                        angular_rp_forest=False, target_n_neighbors=-1,
                        target_metric='categorical', target_metric_kwds=None,
                        target_weight=0.5, transform_seed=42, transform_mode='embedding',
                        force_approximation_algorithm= True, verbose=False,
                        unique=False,  dens_frac=0.3,
                        dens_var_shift=0.1, output_dens=False, disconnection_distance=None)

            clf.fit(self.embs[ np.random.choice(len(self.embs), size= ntrain)  , :], y=y_label)
            pos  = clf.transform( self.embs )

        self.coordinate_xy       = pos

        if dirout is not None :
            os.makedirs(dirout, exist_ok=True)
            df = pd.DataFrame(pos, columns=['x', 'y'] )
            for ci in [ 'x', 'y' ] :
               df[ ci ] = df[ ci ].astype('float32')

            # log(df, df.dtypes)
            pd_to_file(df.iloc[:100, :],  f"{dirout}/embs_xy_{mode}.csv" )
            pd_to_file(df,                f"{dirout}/embs_xy_{mode}.parquet" , show=1)


    def create_clusters(self, method='kmeans', after_dim_reduction=True):
        """ From Dim reduction vectors --> Create Clusters
        Docs::



        """
        if method == 'kmeans':
            from sklearn.cluster import KMeans
            km = KMeans(n_clusters=self.num_clusters)

            if after_dim_reduction :
               km.fit( self.coordinate_xy)
            else :
               km.fit( self.embs)

            self.clusters      = km.labels_.tolist()
            self.cluster_color = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(self.num_clusters)]
            self.cluster_names = {i: f'Cluster {i}' for i in range(self.num_clusters)}


        if method=='hdbscan':
            import hdbscan, umap
            #km = hdbscan.HDBSCAN(min_samples=3, min_cluster_size=10)  #.fit_predict(self.pos)


    def create_visualization(self, dirout="ztmp/", mode='d3', cols_label=None, start_server=False, **kw):
        """

        """
        import mpld3
        os.makedirs(dirout, exist_ok=True)
        cols_label          = [] if cols_label is None else cols_label
        text_label_and_text = []
        for i,x in self.df_labels.iterrows():
          ss = x["id"]
          for ci in cols_label:
             ss = ss + ":" + x[ci]
          text_label_and_text.append(ss)

        #######################################################################################
        # create data frame that has the result of the MDS plus the cluster numbers and titles
        df = pd.DataFrame(dict(x=self.coordinate_xy[:, 0],
                               y=self.coordinate_xy[:, 1],
                               clusters= self.clusters, title=text_label_and_text))
        df.to_parquet(f"{dirout}/embs_xy_cluster.parquet")


        # group by cluster
        groups_clusters = df.groupby('clusters')

        # set up plot
        fig, ax = plt.subplots(figsize=(25, 15))  # set size
        ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

        # iterate through groups to layer the plot
        # note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return
        # the appropriate color/label
        for name, group in groups_clusters:
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, label= self.cluster_names[name],
                    color=self.cluster_color[name],
                    mec='none')
            ax.set_aspect('auto')
            ax.tick_params(axis='x',  # changes apply to the x-axis
                           which='both',  # both major and minor ticks are affected
                           bottom='off',  # ticks along the bottom edge are off
                           top='off',  # ticks along the top edge are off
                           labelbottom='off')
            ax.tick_params(axis='y',  # changes apply to the y-axis
                           which='both',  # both major and minor ticks are affected
                           left='off',  # ticks along the bottom edge are off
                           top='off',  # ticks along the top edge are off
                           labelleft='off')

        ax.legend(numpoints=1)  # show legend with only 1 point

        # add label in x,y position with the label as the
        for i in range(len(df)):
            ax.text(df.loc[i]['x'], df.loc[i]['y'], df.loc[i]['title'], size=8)

        # uncomment the below to save the plot if need be
        plt.savefig(f'{dirout}/clusters_static-{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png', dpi=200)

        # Plot
        fig, ax = plt.subplots(figsize=(20, 15))  # set plot size
        ax.margins(0.03)  # Optional, just adds 5% padding to the autoscaling

        # iterate through groups to layer the plot
        for name, group in groups_clusters:
            points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=7, label= self.cluster_names[name], mec='none',
                             color=self.cluster_color[name])
            ax.set_aspect('auto')
            labels = [i for i in group.title]

            # set tooltip using points, labels and the already defined 'css'
            tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10, css=CSS)
            # connect tooltip to fig
            mpld3.plugins.connect(fig, tooltip, TopToolbar())

            # set tick marks as blank
            ax.axes.get_xaxis().set_ticks([])
            ax.axes.get_yaxis().set_ticks([])

            # set axis as blank
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)

        ax.legend(numpoints=1)  # show legend with only one dot


        ##### Export ############################################################
        mpld3.save_html(fig,  f"{dirout}/embeds.html")
        log(f"{dirout}/embeds.html")

        ### Windows specifc
        if os.name == 'nt': os.system(f'start chrome "{dirout}/embeds.html" ')


        if start_server :
           # mpld3.show(fig=None, ip='127.0.0.1', port=8888, n_retries=50, local=True, open_browser=True, http_server=None, **kwargs)[source]
           mpld3.show()  # show the plot


    def draw_cluster_hiearchy(self):
        """  Dendogram from distance

        """
        from scipy.cluster.hierarchy import ward, dendrogram
        linkage_matrix = ward(self.dist)  # define the linkage_matrix using ward clustering pre-computed distances
        fig, ax = plt.subplots(figsize=(15, 20))  # set size
        ax = dendrogram(linkage_matrix, orientation="right", labels=self.text_labels)
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.tight_layout()
        plt.savefig('dendogram_clusters.png', dpi=200)






#########################################################################################################
############## Loader of embeddings #####################################################################
def embedding_torchtensor_to_parquet(tensor_list,
                                     id_list:list, label_list, dirout=None, tag="",  nmax=10 ** 8 ):
    """ List ofTorch tensor to embedding stored in parquet
    Doc::

        yemb = model.encode(X)
        id_list = np.arange(0, len(yemb))
        ylabel = ytrue
        embedding_torchtensor_to_parquet(tensor_list= yemb,
                                     id_list=id_list, label_list=ylabel,
                                     dirout="./ztmp/", tag="v01"  )


    """
    n          =  len(tensor_list)
    id_list    = np.arange(0, n) if id_list is None else id_list
    label_list = [0]*n if label_list is None else id_list

    assert len(id_list) == len(tensor_list)

    df = []
    for idi, vecti, labeli in zip(id_list,tensor_list, label_list):
        ss = np_array_to_str(vecti.tonumpy())
        df.append([ idi, ss, labeli    ])

    df = pd.DataFrame(df, columns= ['id', 'emb', 'label'])


    if dirout is not None :
      log(dirout) ; os_makedirs(dirout)  ; time.sleep(4)
      dirout2 = dirout + f"/df_emb_{tag}.parquet"
      pd_to_file(df, dirout2, show=1 )
    return df


def embedding_rawtext_to_parquet(dirin=None, dirout=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):
    """FastText/ Word2Vec text file to parquet files.
    Docs::



    """

    log(dirout) ; os_makedirs(dirout)  ; time.sleep(4)

    if is_linevalid_fun is None : #### Validate line
        def is_linevalid_fun(w):
            return len(w)> 5  ### not too small tag

    i = 0; kk=-1; words =[]; embs= []; ntot=0
    with open(dirin, mode='r') as fp:
        while i < nmax+1  :
            i  = i + 1
            ss = fp.readline()
            if not ss  : break
            if i < skip: continue

            ss = ss.strip().split(" ")            
            if not is_linevalid_fun(ss[0]): continue

            words.append(ss[0])
            embs.append( ",".join(ss[1:]) )

            if i % 200000 == 0 :
              kk = kk + 1                
              df = pd.DataFrame({ 'id' : words, 'emb' : embs }  )  
              log(df.shape, ntot)  
              if i < 2: log(df)  
              pd_to_file(df, dirout + f"/df_emb_{kk}.parquet", show=0)
              ntot += len(df)
              words, embs = [], []  

    kk      = kk + 1                
    df      = pd.DataFrame({ 'id' : words, 'emb' : embs }  )  
    ntot   += len(df)
    dirout2 = dirout + f"/df_emb_{kk}.parquet"
    pd_to_file(df, dirout2, show=1 )
    log('ntotal', ntot, dirout2 )
    return os.path.dirname(dirout2)



def embedding_load_parquet(dirin="df.parquet",  colid= 'id', col_embed= 'emb',  nmax= 500,
                           return_type='numpy;pandas',
                           emb_dim=200
                           ):
    """  parquet -->  numpy array, dict map, labels
     Docs::

         id, emb  : embeeding in string "," delimited format
    
    """
    log('loading', dirin)
    flist = list( glob.glob(dirin) )
    
    df  = pd_read_file( flist, npool= max(1, int( len(flist) / 4) ) )
    nmax    = nmax if nmax > 0 else  len(df)   ### 5000
    df  = df.iloc[:nmax, :]
    df  = df.rename(columns={ col_embed: 'emb'})
    
    df  = df[ df['emb'].apply( lambda x: len(x)> 10  ) ]  ### Filter small vector
    log(df.head(5).T, df.columns, df.shape)
    log(df, df.dtypes)

    if return_type == 'pandas':
        return df


    ###########################################################################
    ###### Split embed numpy array, id_map list,  #############################
    vi      = [ float(v) for v in df['emb'][0].split(',')]
    embs    = np_str_to_array(df['emb'].values,  l2_norm_sklearn=True, mdim =len(vi))
    id_map  = { name: i for i,name in enumerate(df[colid].values) }     
    log(",", str(embs)[:50], ",", str(id_map)[:50] )
    
    #####  Keep only label infos  ####
    del df['emb']                  
    return embs, id_map, df 



def embedding_load_word2vec(dirin=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):
    """  Parse FastText/ Word2Vec to parquet files.
    Doc::

       dirin: .parquet files with cols:
       embs: 2D np.array, id_map: Dict, dflabel: pd.DataFrame


    """
    if is_linevalid_fun is None : #### Validate line
        def is_linevalid_fun(w):
            return len(w)> 5  ### not too small tag

    i = 0; kk=-1; words =[]; embs= []; ntot=0
    with open(dirin, mode='r') as fp:
        while i < nmax+1  :
            i  = i + 1
            ss = fp.readline()
            if not ss  : break
            if i < skip: continue

            ss = ss.strip().split(" ")
            if not is_linevalid_fun(ss[0]): continue

            words.append(ss[0])
            embs.append( ",".join(ss[1:]) )


    kk      = kk + 1
    df      = pd.DataFrame({ 'id' : words, 'emb' : embs }  )
    ntot   += len(df)


    embs   =  np_str_to_array( df['emb'].values  )  ### 2D numpy array
    id_map = { i : idi for i, idi in enumerate(df['id'].values)  }
    dflabel      = pd.DataFrame({ 'id' : words }  )
    dflabel['label1'] = 0

    return  embs, id_map, dflabel



def embedding_load_pickle(dirin=None, skip=0, nmax=10 ** 8,
                                 is_linevalid_fun=None):   ##   python emb.py   embedding_to_parquet  &
    """
       Load pickle from disk into embs, id_map, dflabel
    """
    import pickle

    embs = None
    flist =  glob_glob(dirin)
    for fi in flist :
        arr = pickle.load(fi)
        embs = np.concatenate((embs, arr)) if embs is not None else arr

    id_map  = {i: i for i in  range(0, len(embs))}
    dflabel = pd.DataFrame({'id': [] })
    return embs, id_map, dflabel



#########################################################################################################
############## Loader of embeddings #####################################################################
def embedding_extract_fromtransformer(model,Xinput:list):
    """ Transformder require Pooling layer to extract word level embedding.
    Doc::

        https://github.com/Riccorl/transformers-embedder
        import transformers_embedder as tre

        tokenizer = tre.Tokenizer("bert-base-cased")

        model = tre.TransformersEmbedder(
            "bert-base-cased", subword_pooling_strategy="sparse", layer_pooling_strategy="mean"
        )

        example = "This is a sample sentence"
        inputs = tokenizer(example, return_tensors=True)


        class TransformersEmbedder(torch.nn.Module):
                model: Union[str, tr.PreTrainedModel],
                subword_pooling_strategy: str = "sparse",
                layer_pooling_strategy: str = "last",
                output_layers: Tuple[int] = (-4, -3, -2, -1),
                fine_tune: bool = True,
                return_all: bool = True,
            )


    """
    import transformers_embedder as tre

    tokenizer = tre.Tokenizer("bert-base-cased")

    model = tre.TransformersEmbedder(
        "bert-base-cased", subword_pooling_strategy="sparse", layer_pooling_strategy="mean"
    )

    # X = "This is a sample sentence"
    X2 = tokenizer(Xinput, return_tensors=True)
    yout = model(X2)
    emb  = yout.word_embeddings.shape[1:-1]       # remove [CLS] and [SEP]
    # torch.Size([1, 5, 768])
    # len(example)
    return yout



def embedding_cosinus_scores_pairwise(embs:np.ndarray, name_list:list=None, is_symmetric=False):
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
        vi = embs[i,:]
        normi = np.sqrt(np.dot(vi,vi))
        for j in range(i+1, len(name_list)) :
            # simij = cosine_similarity( embs[i,:].reshape(1, -1) , embs[j,:].reshape(1, -1)     )
            vj = embs[j,:]
            normj = np.sqrt(np.dot(vj, vj))
            simij = np.dot( vi ,  vj  ) / (normi * normj)
            dfsim.append([name_list[i], name_list[j], simij])
            # dfsim2.append([ nwords[i], nwords[j],  simij[0][0]  ])

    dfsim  = pd.DataFrame(dfsim, columns= ['id1', 'id2', 'sim_score' ] )

    if is_symmetric:
        ### Add symmetric part
        dfsim3 = copy.deepcopy(dfsim)
        dfsim3.columns = ['id2', 'id1', 'sim_score' ]
        dfsim          = pd.concat(( dfsim, dfsim3 ))
    return dfsim







class torch_model_getlayer():
    """ Get a specific layer for embedding output
    Doc::

        model = models.resnet50()
        layerI= model_getlayer(model, pos_layer=-1)

        ### Forward pass
        Xin = torch.randn(4, 3, 224, 224)
        print( model(Xin) )

        print('emb')
        Xemb = layerI.output
        print(Xemb.shape)
        print(Xemb)

    """
    def __init__(self, network, backward=False, pos_layer=-2):
        self.layers = []
        self.get_layers_in_order(network)
        self.last_layer = self.layers[pos_layer]
        self.hook       = self.last_layer.register_forward_hook(self.hook_fn)

    def hook_fn(self, module1, input, output):
        self.input = input
        self.output = output

    def close(self):
        self.hook.remove()

    def get_layers_in_order(self, network):
      if len(list(network.children())) == 0:
        self.layers.append(network)
        return
      for layer in network.children():
        self.get_layers_in_order(layer)


"""
        class modelA(torch.nn.Module):
            def __init__(self,layers_dim=[20,100,16], nn_model_base=None, layer_id=0):
                super(modelA, self).__init__()
                self.head_task = []
                self.layer_id  = layer_id  ##flag meaning ????  layer


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
                layer_l2= model_getlayer(self.head_task, pos_layer=-2)
                self.forward(x)
                embA = layer_l2.output.squeeze()
                return embA



"""






###############################################################################################################
if 'utils_matplotlib':
    CSS = """
        text.mpld3-text, div.mpld3-tooltip {
          font-family:Arial, Helvetica, sans-serif;
        }
        g.mpld3-xaxis, g.mpld3-yaxis {
        display: none; }
        """

    try :
        import mpld3    
        class TopToolbar(mpld3.plugins.PluginBase):
            """Plugin for moving toolbar to top of figure"""

            JAVASCRIPT = """
            mpld3.register_plugin("toptoolbar", TopToolbar);
            TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
            TopToolbar.prototype.constructor = TopToolbar;
            function TopToolbar(fig, props){
                mpld3.Plugin.call(this, fig, props);
            };
            TopToolbar.prototype.draw = function(){
            // the toolbar svg doesn't exist
            // yet, so first draw it
            this.fig.toolbar.draw();
            // then change the y position to be
            // at the top of the figure
            this.fig.toolbar.toolbar.attr("x", 150);
            this.fig.toolbar.toolbar.attr("y", 400);
            // then remove the draw function,
            // so that it is not called again
            this.fig.toolbar.draw = function() {}
            }
            """

            def __init__(self):
                self.dict_ = {"type": "toptoolbar"}
    except : pass




if 'utils_vector':
    def db_load_dict(df, colkey='id', colval='item_tag', naval='0', colkey_type='str', colval_type='str', npool=5, nrows=900900900, verbose=True):
        """Load Pandas into dict




        """
        if isinstance(df, str):
           dirin = df
           log('loading', dirin)
           flist = glob_glob( dirin , 1000)
           log(  colkey, colval )
           df    = pd_read_file(flist, cols=[ colkey, colval  ], nrows=nrows,  n_pool=npool, verbose=True)

        log( df.columns )
        df = df.drop_duplicates(colkey)
        df = df.fillna(naval)
        log(df.shape)

        df[colkey] = df[colkey].astype(colkey_type)
        df[colval] = df[colval].astype(colval_type)


        df = df.set_index(colkey)
        df = df[[ colval ]].to_dict()
        df = df[colval] ### dict
        if verbose: log('Dict Loaded', len(df), str(df)[:100])
        return df


    def np_array_to_str(vv:np.ndarray, ):
        """ array/list into  "," delimited string """
        vv= np.array(vv, dtype='float32')
        vv= [ str(x) for x in vv]
        return ",".join(vv)


    def np_str_to_array(vv:list,   mdim = None, l2_norm_faiss=False, l2_norm_sklearn=True, l2_norm_numpy=False):
        """ Convert list of string into numpy 2D Array
        Docs::
             
             np_str_to_array(vv=[ '3,4,5', '7,8,9'],  mdim = 3)

             https://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors

        """
        if mdim is None :
             mdim= len( vv[0].split(","))

        X = np.zeros(( len(vv) , mdim  ), dtype='float32')
        for i, r in enumerate(vv) :
            try :
              vi      = [ float(v) for v in r.split(',')]
              X[i, :] = vi
            except Exception as e:
              log(i, e)

        if l2_norm_numpy:
            X /= np.hypot(X[:,0], X[:,1])

        if l2_norm_sklearn:
            from sklearn.preprocessing import normalize
            normalize(X, norm='l2', copy=False)

        if l2_norm_faiss:
            import faiss   #### pip install faiss-cpu
            faiss.normalize_L2(X)  ### Inplace L2 normalization
            log("Normalized X")
        return X


    def np_norm_l2(X, l2_norm_numpy=True, l2_norm_sklearn=False, l2_norm_faiss=False):
        """  L2 Normalize
        """
        if l2_norm_numpy:
            X /= np.hypot(X[:,0], X[:,1])

        if l2_norm_sklearn:
            from sklearn.preprocessing import normalize
            normalize(X, norm='l2', copy=False)

        if l2_norm_faiss:
            import faiss   #### pip install faiss-cpu
            faiss.normalize_L2(X)  ### Inplace L2 normalization

        return X


    def np_matrix_to_str2(array_2d, map_dict:dict=None):
        """ 2D numpy or List of List into list of string and apply map_dict.
        
        Doc::
            map_dict = { 4:'four', 3: 'three' }
            m= [[ 0,3,4  ], [2,4,5]]
            np_matrix_to_str2(m, map_dict)
            --> [ ",threee,four" ,   ",four," ]

        """
        map_dict = {} if map_dict is None else map_dict
        res = []
        for v in array_2d:
            ss = ""
            for xi in v:
                ss += str(map_dict.get(xi, "")) + ","
            res.append(ss[:-1])
        return res


    def np_matrix_to_str3(array_2d, map_dict: dict = None):
        """ 2D numpy or List of List into list of string and apply map_dict.

        Doc::
            map_dict = { 4:'four', 3: 'three' }
            m= [[ 0,3,4  ], [2,4,5]]
            np_matrix_to_str3(m, map_dict)
            --> [ ",threee,four" ,   ",four," ]

        """
        map_dict = {} if map_dict is None else map_dict
        res = []
        for v in array_2d:
            ss = ""
            for xi in v:
                ss += str(map_dict.get(str(xi), "")) + ","
            res.append(ss[:-1])
        return res


    def np_matrix_to_str(m):
        """ 2D numpy into list of string and apply map_dict.

        Doc::
            m= [[ 0,3,4  ], [2,4,5]]
            --> [ "0,3,4" ,   "2,4,5" ]

        """
        res = []
        for v in m:
            ss = ""
            for xi in v:
                ss += str(xi) + ","
            res.append(ss[:-1])
        return res            
                
    
    def np_matrix_to_str_sim(m):
        """
        Docs::

             Return Simcore = 1 - 0.5 * dist**2


        """
        res = []
        for v in m:
            ss = ""
            for di in v:
                ss += str(1-0.5*di) + ","
            res.append(ss[:-1])
        return res   



if 'custom_code':
    def os_unzip(dirin, dirout):
        # !/usr/bin/env python3
        import zipfile
        with zipfile.ZipFile(dirin, 'r') as zip_ref:
            zip_ref.extractall(dirout)

    def test_create_fake_df(dirout="./ztmp/", nrows=100):
        """ Creates a fake embeddingdataframe
        """
        res  = Box({})
        n    = nrows
        mdim = 50

        #### Create fake user ids
        word_list = [ 'a' + str(i) for i in range(n)]
        emb_list  = []
        for i in range(n):
            emb_list.append( ','.join([str(x) for x in np.random.random(mdim) ])  )

        df = pd.DataFrame()
        df['id']  = word_list
        df['emb'] = emb_list
        res.df    = df

        #### export on disk
        res.dir_parquet = dirout + "/emb_parquet/db_emb.parquet"
        pd_to_file(df, res.dir_parquet , show=1)

        #### Write on text:
        res.dir_text   = dirout + "/word2vec_export.vec"
        log( res.dir_text )
        with open(res.dir_text, mode='w') as fp:
            fp.write("word2vec\n")
            for i,x in df.iterrows():
              emb  = x['emb'].replace(",", "")
              fp.write(  f"{x['id']}  {emb}\n")

        return res


    def pd_add_onehot_encoding(dfref, img_dir, labels_col):
        """
           id, uri, cat1, cat2, .... , cat1_onehot

        """
        import glob
        fpaths = glob.glob(img_dir)
        fpaths = [fi for fi in fpaths if "." in fi.split("/")[-1]]
        log(str(fpaths)[:100])

        df = pd.DataFrame(fpaths, columns=['uri'])
        log(df.head(1).T)
        df['id'] = df['uri'].apply(lambda x: x.split("/")[-1].split(".")[0])
        df['id'] = df['id'].apply(lambda x: int(x))
        df = df.merge(dfref, on='id', how='left')

        # labels_col = [  'gender', 'masterCategory', 'subCategory', 'articleType' ]

        for ci in labels_col:
            dfi_1hot = pd.get_dummies(df, columns=[ci])  ### OneHot
            dfi_1hot = dfi_1hot[[t for t in dfi_1hot.columns if ci in t]]  ## keep only OneHot
            df[ci + "_onehot"] = dfi_1hot.apply(lambda x: ','.join([str(t) for t in x]), axis=1)
            #####  0,0,1,0 format   log(dfi_1hot)

        return df




    
###############################################################################################################
if __name__ == "__main__":
    import fire
    test_all()
    #fire.Fire()



    
