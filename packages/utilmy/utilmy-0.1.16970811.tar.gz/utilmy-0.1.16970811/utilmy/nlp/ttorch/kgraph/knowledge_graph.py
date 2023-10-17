""" Generate Embedding from raw text using Graph Neural Network.
Docs::

    -- Separate in 3 parts  (classes)
        raw text --> NER extraction
        The dataset consisting of Questions, Answers and metadata gets processed entirely and
        the individual entities and relations are extracted.

        NER  --> KGraph training + embedding generation/
        The next step is to produce the embeddings from the entities and relations from the
        graph provided by ntx. Other properties such as centers and means of centers may be
        computed in the knowledge_grapher class. This might be useful for different applications

        KG Embedding Losses

        Reason :
        make the code modular, easy to change when needed.
        make thing independant.

     -- Code:
        url = 'https://github.com/arita37/data/raw/main/kgraph_pykeen_small/data_kgraph_pykeen.zip'
        dname = dataset_download(url=url)
        dname = dname.replace("\\", "/")
        path  = os.path.join(dname, 'final_dataset_clean_v2 .tsv')
        df    = pd.read_csv(path, delimiter='\t')
        dname = os.path.join(dname, 'embed')

        if not os.path.exists(dname):
            os.makedirs(dname)

        log('##### NER extraction from text ')

        # Check the model_name param since the appropriate spacy model
        # should be loaded when changing the language of the dataset

        extractor = NERExtractor(dirin_or_df=df, dirout=dname, model_name="ro_core_news_sm")
        extractor.extract_triples(max_text=-1)
        extractor.export_data()
        # If the data_kgf.csv isn't present in the data folder then
        # run the line below
        # data_kgf  = extractor.extractTriples(max_text=-1)
        # extractor.export_data(data_kgf)


        log('##### Build Knowledge Graph')
        data_kgf_path = os.path.join(dname, 'data_kgf.tsv')
        grapher = knowledge_grapher(embedding_dim=10)
        grapher.load_data(data_kgf_path)
        grapher.build_graph()
        # data_kgf = knowledge_grapher.load_data(data_kgf_path)
        #grapher = knowledge_grapher(data_kgf=data_kgf,embedding_dim=10, load_spacy=True)



        log('##### Build KG Embeddings')
        dirout_emb = dname
        embedder = KGEmbedder(graph= grapher.graph, dirin=dname, embedding_dim=10, dirout= dirout_emb)
        # If you have the trained model to be saved then pass a non existing dir to compute_embeddings()
        embedder.compute_embeddings('none', batch_size=1024)
        embedder.save_embeddings()


        log('##### load KG Embeddings')
        embedder.load_embeddings('none')


"""
import sys, os, numpy as np, pandas as pd
from typing import Tuple, Any, Dict, Union, List
import matplotlib.pyplot as plt
from tqdm import tqdm
from box import Box

#### Text
import networkx as ntx
import spacy
from spacy.matcher import Matcher

import torch

#####
import pykeen as pyk

### pip install python-box
from utilmy import (log,log2, pd_to_file, pd_read_file)



######################################################################################################
def test_all():
    ztest1()


def ztest1(dirin='final_dataset_clean_v2 .tsv'):

    """
    Doc::

        cd utilmy/nlp/tttorch/kgraph
        python knowledge_graph test1 --dirin mydirdata/
    """
    url = 'https://github.com/arita37/data/raw/main/kgraph_pykeen_small/data_kgraph_pykeen.zip'
    dname = dataset_download(url=url)
    dname = dname.replace("\\", "/")
    path  = os.path.join(dname, 'final_dataset_clean_v2 .tsv')
    df    = pd.read_csv(path, delimiter='\t')
    dname = os.path.join(dname, 'embed')

    if not os.path.exists(dname):
        os.makedirs(dname)

    log('##### NER extraction from text ')
    extractor = NERExtractor(dirin_or_df=df, dirout=dname, model_name="ro_core_news_sm")
    extractor.extract_triples(max_text=-1)
    extractor.export_data()
    # data_kgf  = extractor.extractTriples(max_text=-1)
    # extractor.export_data(data_kgf)


    log('##### Build Knowledge Graph')
    data_kgf_path = os.path.join(dname, 'data_kgf.tsv')
    grapher = knowledge_grapher(embedding_dim=10)
    grapher.load_data(data_kgf_path)
    grapher.build_graph()
    # data_kgf = knowledge_grapher.load_data(data_kgf_path)
    #grapher = knowledge_grapher(data_kgf=data_kgf,embedding_dim=10, load_spacy=True)



    log('##### Build KG Embeddings')
    dirout_emb = dname
    embedder = KGEmbedder(graph= grapher.graph, dirin=dname, embedding_dim=10, dirout= dirout_emb)
    # If you have the trained model to be saved then pass a non existing dir to load_embeddings()
    embedder.compute_embeddings('none', batch_size=1024)
    embedder.save_embeddings()


    log('##### load KG Embeddings')
    embedder.load_embeddings('none')



def runall(config=None, config_field=None,  dirin='', dirout='', embed_dim=10, batch_size=64 ):

    """  Run all steps to generate dirin
    Doc::

        cd utilmy/nlp/tttorch/kgraph
        python knowledge_graph.py runall  --dirin mydirdata/


    """

    #### Config  ##############################
    from utilmy import config_load
    cfg =  config_load(config, config_field_name= config_field)
    embed_dim = cfg.get('embed_dim', embed_dim)
    dirin     = cfg.get('dirin',  dirin)
    dirout    = cfg.get('dirout', dirout)



    df    = pd_read_file(dirin)

    log('##### NER extraction from text ')
    extractor = NERExtractor(dirin_or_df=df, dirout=dirout, model_name="ro_core_news_sm")
    extractor.extract_triples(max_text=-1)
    extractor.export_data()


    log('##### Build Knowledge Graph')
    data_kgf_path = os.path.join(dirout, 'data_kgf.tsv')
    grapher = knowledge_grapher(embedding_dim= embed_dim)
    grapher.load_data( data_kgf_path)
    grapher.build_graph()


    log('##### Build KG Embeddings')
    dirout_emb = dirout
    embedder = KGEmbedder(graph= grapher.graph, dirin=dirout, embedding_dim=embed_dim, dirout= dirout_emb)
    # If you have the trained model to be saved then pass a non existing dir to load_embeddings()
    embedder.compute_embeddings('none', batch_size= batch_size)
    embedder.save_embeddings()


    log('##### load KG Embeddings')
    embedder.load_embeddings('none')



######################################################################################################
class knowledge_grapher():
    def __init__(self, embedding_dim:int=14,
                dirin:str="./mydatain/",
                 dirout:str="./mydataout/",
                 ) -> None:
        """knowledge_grapher:
        Docs:

                This class wraps around the ntx library to produce a graph from the extracted entities and relations
                coming from NERExtractor. Outputs the graph the pykeen will then take as an input.

                data_kgf     :      pd.DataFrame, dataframe with triples entity, relation, entity
                embedding_dim:      int, number of dimensions in the embedding space
                dirin        :      PathLike, where to read input data from in the form of a tsv file containing 
                                    entitie and relation triples
                dirout       :      PathLike, where to store results. Currently no output. Methods for saving
                                    centrality or means could be implemented if required

                
        """
        self.embedding_dim = embedding_dim
        self.dirin = dirin
        self.dirout = dirout

    def build_graph(self, relation = None)->None:
        """build knowledge graph
        Docs:

                relation:   str, build graph isolating a particular relation for visualization purposes.

        """
        if relation:
            self.graph = ntx.from_pandas_edgelist(self.data_kgf[self.data_kgf['edge']==relation], "source", "target",
                         edge_attr=True, create_using=ntx.MultiDiGraph())
        else:
            self.graph = ntx.from_pandas_edgelist(self.data_kgf, "source", "target",
                         edge_attr=True, create_using=ntx.MultiDiGraph())

    def plot_graph(self)->None:
        """plot the knowledge graph using a networkx method, other ways are posible

        """
        plt.figure(figsize=(14, 14))
        posn = ntx.spring_layout(self.graph)
        ntx.draw(self.graph, with_labels=True, node_color='green', edge_cmap=plt.cm.Blues, pos = posn)
        plt.savefig(self.dirout +"/"+'graphPlot.jpg')
        plt.close()

    def compute_centrality(self,)->None:
        """compute the centrality metric for each node using diferent methods,
        refer to the networkx documentation for more info

        """
        self.centrality_dict = ntx.degree_centrality(self.graph)
        self.in_centrality_dict = ntx.in_degree_centrality(self.graph)
        self.out_centrality_dict = ntx.out_degree_centrality(self.graph)
        # self.eigenvector_centrality_dict = ntx.katz_centrality(self.graph)

    #@staticmethod
    def load_data(self, path)->pd.DataFrame:
        """load the data_kgf dataframe
        Docs:

                path:   PathLike, where the data is stored in parquet format

        """
        try:
            df = pd.read_csv(path, delimiter="\t")
            self.data_kgf  = df

        except Exception as e:
            log(e)
            log('Data format may be incorrect')

        cols =['source', 'target', 'edge']
        assert len(df[cols])>0 , "error missing columns"
        # self.buildGraph(data_kgf)


    def get_centers(self, max_centers:int=5)->None:

        """ get the nodes with the higher centrality metric for each methods
        Docs:

                max_centers:    int, how many centers to include in the top

        """
        sorted_dict = sorted(self.centrality_dict.items(), key=lambda x: x[1])[::-1]
        in_sorted_dict = sorted(self.in_centrality_dict.items(), key=lambda x: x[1])[::-1]
        out_sorted_dict = sorted(self.out_centrality_dict.items(), key=lambda x: x[1])[::-1]

        degree_centers = sorted_dict[:max_centers]

        in_degree_centers = in_sorted_dict[:max_centers]
        out_degree_centers = out_sorted_dict[:max_centers]

        degree_adjacency = {u:self.graph[u] for u,_ in degree_centers}

        in_degree_adjacency = {u:self.graph[u] for u,_ in in_degree_centers}
        out_degree_adjacency = {u:self.graph[u] for u,_ in out_degree_centers}

        self.center_dict = {'degree':{'centers':degree_centers, 'adjacency': degree_adjacency},
                            'in_degree':{'centers':in_degree_centers, 'adjacency': in_degree_adjacency},
                            'out_degree':{'centers':out_degree_centers, 'adjacency':out_degree_adjacency},}

    def map_centers_anchors(self,embedding_df:pd.DataFrame, _type:str)->None:
       """ map centers to anchors (embeddings)
       Docs::

            embedding_df:   pd.DataFrame, map from nodes to embeddings
            type_       :   str, which method to use of the calculated centers
       """
       self.embedding_df = embedding_df
       _aux = self.center_dict[_type]
       centers = _aux['centers']
       adjacency = _aux['adjacency']

       self.mean_anchor_dict = {}
       for center, _ in centers:
            center_embedding = self.embedding_df[str(center)]
            num_embeddings = len(list(adjacency[center].keys()))
            adjacency_embeddings = np.ndarray((num_embeddings, self.embedding_dim))
            for i, (node, adj_dict) in enumerate(adjacency[center].items()):
                adjacency_embeddings[i,:] = self.embedding_df[str(node)]
            self.mean_anchor_dict[center] = {'center': center_embedding.values, 'anchor':adjacency_embeddings.mean(axis = 0)}



class NERExtractor:

    def __init__(self, dirin_or_df:pd.DataFrame,
                 dirout:str="./mydataout/",
                 model_name="ro_core_news_sm"
                 ):
        """NERExtractor: named entity extractor
        Docs::

            This class applies a language model from spacy to parse the text searching for
            entities and relations between them. The objective is to parse the corpus of questions to get said relations.
            Basic NLP techniques such as cleaning the text are applied by it's methods.


                data    : pd.DataFrame, with the corpus of text from which to extract entities
                dirin   : where to load the input data. Where the corpus of text is stored
                dirout  : where to save the output. The resulting data_kgf file containing the triples 
                          that then will constitute the knowledge_graph built by knowledge_grapher.

        """

        self.nlp = spacy.load(model_name)
        # self.dirin = dirin
        self.dirout = dirout.replace("\\", "/")

        if isinstance(dirin_or_df, pd.DataFrame):
            self.data = dirin_or_df
        else :
            from utilmy import pd_read_file
            self.data = pd_read_file(dirin_or_df)


        cols = ['paragraph']
        assert len(self.data[cols])> 0, 'not ok'


    def extract_entities(self, sents:List[str])->pd.DataFrame:
        """extracting entities for a series of sentences of cleaned text
        Docs:
                sents: List[str], cleaned Text from which to extract the entities
        """
        # chunk one
        enti_one = ""
        enti_two = ""
        dep_prev_token = "" # dependency tag of previous token in sentence
        txt_prev_token = "" # previous token in sentence
        prefix = ""
        modifier = ""
        for tokn in self.nlp(sents):
            # chunk two
            ## move to next token if token is punctuation
            if tokn.dep_ != "punct":
                #  check if token is compound word or not
                if tokn.dep_ == "compound":
                    prefix = tokn.text
                    # add the current word to it if the previous word is 'compound’
                    if dep_prev_token == "compound":
                        prefix = txt_prev_token + " "+ tokn.text
                # verify if token is modifier or not
                if tokn.dep_.endswith("mod") == True:
                    modifier = tokn.text
                    # add it to the current word if the previous word is 'compound'
                    if dep_prev_token == "compound":
                        modifier = txt_prev_token + " "+ tokn.text
                # chunk3
                if tokn.dep_.find("subj") == True:
                    enti_one = modifier +" "+ prefix + " "+ tokn.text
                    prefix = ""
                    modifier = ""
                    dep_prev_token = ""
                    txt_prev_token = ""
                # chunk4
                if tokn.dep_.find("obj") == True:
                    enti_two = modifier +" "+ prefix +" "+ tokn.text
                # chunk 5
                # update variable
                dep_prev_token = tokn.dep_
                txt_prev_token = tokn.text
        return [enti_one.strip(), enti_two.strip()]

    def obtain_relation(self,sent):
        """extracting relations for a series of sentences of cleaned text
        Docs:

                sents: List[str], cleaned Text from which to extract the relations
        """
        doc = self.nlp(sent)
        matcher = Matcher(self.nlp.vocab)
        pattern = [{'DEP':'ROOT'},
                {'DEP':'prep','OP':"?"},
                {'DEP':'agent','OP':"?"},
                {'POS':'ADJ','OP':"?"}]
        matcher.add(key="matching_1", patterns = [pattern])
        matcher = matcher(doc)
        h = len(matcher) - 1
        try:
            assert matcher
            span = doc[matcher[h][1]:matcher[h][2]]
            return span.text
        except AssertionError:
            print('No match found for this entry!')
            return None

    def extract_triples(self, max_text:int, return_val=False) -> pd.DataFrame:

        """extracting triples of the form [source relation target]
        Docs:

                max_text: int, how many of the corpus rows to consume
                returs:
                    pd.DataFrame where each row is a triple of the same form
        """
        max_text = len(self.data) if max_text<0 else max_text
        pairs_of_entities = [self.extract_entities(i) for i in tqdm(self.data['paragraph'][:max_text])]
        relations = [self.obtain_relation(j) for j in tqdm(self.data['paragraph'][:max_text])]
        indexes = [x for x, z in enumerate(relations) if z is not None]
        relations = [x for x in relations if x is not None]

        # subject extraction
        source = [j[0] for j in pairs_of_entities]
        source = [source[i] for i in indexes]

        #object extraction
        target = [k[1] for k in pairs_of_entities]
        target = [target[i] for i in indexes]

        self.data_kgf = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
        if return_val: return self.data_kgf


    def export_data(self, dirout=None):

        """extracting relations for a series of sentences of cleaned text
        Docs:

                data_kgf: pd.DataFrame of the form [source relation target]
                returns
                    Tuple[pd.DataFrame] with traning, validation and testing datasets

        """

        from utilmy import pd_to_file
        train_df, val_df, test_df = dataset_traintest_split(self.data_kgf, train_ratio=0.6, val_ratio=0.2)


        dirout = dirout if dirout is not None else self.dirout
        # pd_to_file(train_df,   dirout + '/train_data.parquet', )
        # pd_to_file(test_df,    dirout + '/test_data.parquet',  )
        # pd_to_file(val_df,     dirout + '/val_data.parquet',   )
        # pd_to_file(self.data_kgf,   dirout + '/data_kgf.parquet',   )

        #Pykeen Requires data to be loaded in csv format!
        pd_to_file(train_df,   dirout + '/train_data.csv', sep="\t")
        pd_to_file(test_df,    dirout + '/test_data.csv', sep="\t" )
        pd_to_file(val_df,     dirout + '/validation_data.csv',  sep="\t" )
        pd_to_file(self.data_kgf,   dirout + '/data_kgf.csv',  sep="\t" )


        # train_df.to_csv(self.dirout +"/"+'train_data.tsv'), sep="\t")
        # test_df.to_csv(self.dirout +'/test_data.tsv'), sep="\t")
        # val_df.to_csv(self.dirout +"/"+  'validation_data.tsv'), sep="\t")
        # self.data_kgf.to_csv(self.dirout +"/"+'data_kgf.tsv'), sep="\t")
        # return train_df, test_df, val_df



class KGEmbedder:
    def __init__(self, graph:ntx.MultiDiGraph, embedding_dim:int,
                 dirin:str="./mydatain/",
                 dirout:str="./mydataout/",

                 )->None:

        """KGEmbedder: produces the KG embeddings using pyKeen:

        Docs:

                Several changes to the pyKeen pipeline could be made. Experimentation with the current
                dataset found out that the chosen elements (mainly the training loop and optimizer) are
                the most performant.

                https://pykeen.readthedocs.io/en/stable/
                graph           : ntx.MultiDiGraph the knowledge graph itself
                embedding_dim   : int, number of dimensions of the embedding space
                dirin           : where to load the input data. No input data required, only
                                  value to load is the NN model for the embedding which should be provided separately.
                dirout          : where to save the output. This being the weights from the model representing the knowledge graph
                                  embeddings 

        """
        self.graph = graph
        self.embed_dim = embedding_dim

        train_path = os.path.join(dirin,'train_data.tsv')
        test_path  = os.path.join(dirin,'test_data.tsv')
        val_path   = os.path.join(dirin,'validation_data.tsv')
        data_path  = os.path.join(dirin,'data_kgf.tsv')

        self.dirin  = dirin
        self.dirout = dirout
        self.training = pyk.triples.TriplesFactory.from_path(train_path)

        self.testing = pyk.triples.TriplesFactory.from_path(test_path,
                                            entity_to_id  = self.training.entity_to_id,
                                            relation_to_id= self.training.relation_to_id)

        self.validation = pyk.triples.TriplesFactory.from_path(val_path,
                                            entity_to_id  = self.training.entity_to_id,
                                            relation_to_id= self.training.relation_to_id)


    def model_init(self, dirmodel_in=None, do_train=False ):
        """set up the training pipeline for pykeen or load the trained model
        """
        # entity_representations = pyk.nn.representation.LabelBasedTransformerRepresentation.from_triples_factory(training)

        if dirmodel_in is not None:
            self.model = torch.loadd(dirmodel_in +'/trained_model.pkl')
            self.trained = True
        else:
            self.model = pyk.models.ERModel(triples_factory=self.training,
                                 interaction='distmult',
                                 # entity_representations=entity_representations
                                 entity_representations_kwargs   = dict(embedding_dim=self.embed_dim, dropout=0.1),
                                 relation_representations_kwargs = dict(embedding_dim=self.embed_dim, dropout=0.1)
                                 )

            self.optimizer = torch.optim.Adam(params=self.model.get_grad_params())

            self.training_loop = pyk.training.LCWATrainingLoop(
                model=self.model,
                triples_factory=self.training,
                optimizer=self.optimizer,
            )
            self.trained = False

    def compute_embeddings(self, path_to_embeddings, batch_size, n_epochs=8)->Tuple:

        """set up the training pipeline for pykeen or load the trained model
        Docs:

                path_to_embeddings: PathLike
                batch_size        : int, batch_size for the pykeen nn
        """
        self.model_init(dirmodel_in=path_to_embeddings)
        if not self.trained:
            losses = self.training_loop.train(
                                triples_factory=self.training,
                                num_epochs=n_epochs,
                                checkpoint_name='myCheckpoint.pt',
                                checkpoint_frequency=5,
                                batch_size=batch_size,
                                )
            torch.save(self.model, self.dirout +'/trained_model.pkl')
        else:
            losses = None

        # Pick an evaluator
        evaluator = pyk.evaluation.RankBasedEvaluator()
        
        # Get triples to test
        mapped_triples = self.testing.mapped_triples
        
        # Evaluate
        results = evaluator.evaluate( model=self.model,
            mapped_triples=mapped_triples,
            batch_size=batch_size,
            additional_filter_triples=[  self.training.mapped_triples,  self.validation.mapped_triples, ],
        )
        return losses, results


    def load_embeddings(self, path_to_embeddings:str):
        """load the embedding parquet files
        """
        self.embedding_df = pd_read_file(self.dirout +'/entityEmbeddings.parquet')
        self.relation_df  = pd_read_file(self.dirout +'/relationEmbeddings.parquet')
        return None, None
        #else:
        #    return self.compute_embeddings(path_to_embeddings, batch_size=1024)

    def save_embeddings(self,):
        """save the embedding parquet files
        """
        entities      = tuple(self.graph.nodes.values())
        tripleFactory = self.training

        entities_to_ids:Dict = tripleFactory.entity_id_to_label
        relation_to_ids:Dict = tripleFactory.relation_id_to_label

        # TransE model has only one embedding per entity/relation
        entity_embeddings   = self.model.entity_representations[0]
        relation_embeddings = self.model.relation_representations[0]

        self.relation_dict = pykeen_get_embeddings(relation_to_ids, relation_embeddings)
        self.entity_dict   = pykeen_get_embeddings(entities_to_ids, entity_embeddings)
        df_entities = pykeen_embedding_to_df(self.entity_dict,   'entity')
        df_relation = pykeen_embedding_to_df(self.relation_dict, 'relation')


        pd_to_file( df_entities, self.dirout +'/entityEmbeddings.parquet')
        pd_to_file( df_relation, self.dirout +'/relationEmbeddings.parquet')




######################################################################################################
def dataset_traintest_split(anyobject:Any, train_ratio:float=0.6, val_ratio:float=0.2):
    #### Split anything
    """train test split Any

    """
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




def dataset_download(url    = "https://github.com/arita37/data/raw/main/fashion_40ksmall/data_fashion_small.zip",
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




def pykeen_get_embeddings(id_to_label:Dict[int, str], embedding):
    """parse the triple [label id embedding] from the pykeen API
    Docs:

            id_to_label: Dict[int, str] mapping from ids to labels
            embedding  : torch.tensor produced embeddings
            returns
                dict with the requested triple
    """
    aux = {label:{'_id': id_} for id_, label in id_to_label.items()}
    for id_, label in id_to_label.items():
        idx_tensor = torch.tensor([id_]).to(dtype=torch.int64)

        aux[label]['embedding'] = embedding.forward(indices = idx_tensor).detach().numpy()
    return aux



def pykeen_embedding_to_df(embeddingDict:Dict[str, Dict[str, Union[int, torch.tensor]]], entityOrRelation:str)->pd.DataFrame:
    """turn the results from pykeen in a more manageable format
    Docs:

            embeddingDict   :   Dict[str, Dict[str, Union[int, torch.tensor]]],
                                mapping from labels to ids and embeddings
            entityOrRelation:   Wether to use the relation or the entity column name

    """
    aux = []
    for label, dict_ in embeddingDict.items():
        vals = [label, dict_['_id'], dict_['embedding'].flatten()]
        aux.append(vals)
    df = pd.DataFrame(aux, columns=[entityOrRelation, 'id', 'embedding'])
    return df




if __name__=="__main__":
    import fire
    fire.Fire()
    # runall()
