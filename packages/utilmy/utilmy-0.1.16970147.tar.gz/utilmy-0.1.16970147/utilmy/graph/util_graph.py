""" Network DAG Processing

Docs::

  https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages

  The benchmark was carried out using a Google Compute n1-standard-16 instance (16vCPU Haswell 2.3GHz, 60 GB memory). I compare 5 different packages:

  graph-tool
  igraph
  networkit
  networkx
  snap

  Full results can be seen from the table below:


  dataset	Algorithm	graph-tool	igraph	networkit	networkx	snap
  Google	connected components	0.32	2.23	0.65	21.71	2.02
  Google	k-core	0.57	1.68	0.06	153.21	1.57
  Google	loading	67.27	5.51	17.94	39.69	9.03
  Google	page rank	0.76	5.24	0.12	106.49	4.16
  Google	shortest path	0.20	0.69	0.98	12.33	0.30

  Pokec	connected components	1.35	17.75	4.69	108.07	15.28
  Pokec	k-core	5.73	10.87	0.34	649.81	8.87
  Pokec	loading	119.57	34.53	157.61	237.72	59.75
  Pokec	page rank	1.74	59.55	0.20	611.24	19.52
  Pokec	shortest path	0.86	0.87	6.87	67.15	3.09

https://networkit.github.io/


https://pyvis.readthedocs.io/en/latest/index.html#


https://deepgraph.readthedocs.io/en/latest/what_is_deepgraph.html


https://towardsdatascience.com/pyviz-simplifying-the-data-visualisation-process-in-python-1b6d2cb728f1


https://graphviz.org/





"""
import os, glob, sys, math, time, json, functools, random, yaml, gc, copy, pandas as pd, numpy as np
import datetime
from box import Box
from typing import Union
import warnings
from warnings import simplefilter  ; simplefilter(action='ignore', category=FutureWarning)
with warnings.catch_warnings():
    pass


from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob, json_load


#############################################################################################
from utilmy import log, log2, os_module_name

def help():
    """function help        """
    from utilmy import help_create
    print( help_create(__file__) )



#############################################################################################
def test_all() -> None:
    """ python  $utilmy/deeplearning/util_topk.py test_all         """
    log(os_module_name(__file__))
    test1()


def test1():
    pass


def test_get_amazon():
    # https://drive.google.com/file/d/1WuLFU595Bh2kd9lEWX_Tv43FYWW5BUW2/view?usp=sharing
    file_id = '1WuLFU595Bh2kd9lEWX_Tv43FYWW5BUW2' #<-- You add in here the id from you google drive file, you can find it


    from utilmy.util_download import google_download
    google_download(url_or_id= file_id , fielout='amazon0302.txt')




def test_pd_create_dag(nrows=1000, n_nodes=100):
    aval = np.random.choice([ str(i) for i in range(n_nodes)], nrows )
    bval = np.random.choice([ str(i) for i in range(n_nodes)], nrows )

    w    = np.random.random(nrows )

    d = {'a': aval, 'b': bval, 'w': w }
    df = pd.DataFrame(d )
    return df



############################################################################################################################
class  GraphDataLoader(object):
    def __init__(self,):
        """
        Load/save/convert data into parquet, pandas dataframe

            mygraph242423/
                edges.parquet
                nodes.parquet
                meta.json
                    

        load(dirin,  )
            -->  edges: pd.Dataframe ( 'node_a', 'node_b' 'weight', 'edge_type' ] 
                verteex :  pd.daframe('node_id'  , 'node_int',  'col1', 'col2' ]
                meta : dict of metatada
                            
                
        save(dirout)
            os.makedirs

        convert
            (edget, node, meta) --->   networkit or networkx
        """

        self.edges = pd.DafraFrame()
        self.nodes = pd.datarFrame()
        self.nodes_index = {}  #node_idint --> infos
        self.meta = {'cola':  'cola', 'colb': 'cola', 'colvertex': 'colvertex'}



    def load(self, dirin, from='networkit/networkx'):
        """ Load from disk

        """
        self.nodes = pd_read_file(dirin +"/nodes.parquet")
        self.edges = pd_read_file(dirin +"/edges.parquet")  ### graph        
        self.meta =  json_load(dirin    +"/meta.json")
        self.nodes_index = {}  #node_idint --> infos


        dd = {}
        for x in self.nodex[ 'node_id' ].values :
           dd[ hash(x) ] = x
        self.nodes_index = dd  #node_idint --> infos


    def convert_from(self, graph, from='networkit/networkx'):
        """ Get From existing network in Memory

        """
        self.nodes = pd.datarFrame()
        self.edges = pd.DafraFrame()

        self.nodes_index = {}  #node_idint --> infos
        self.meta = {}


    def save(self, dirout):
        pass


    def convert_to(self, target='networkit/networkx'):


       if target == 'networkit':
           graph, index = dag_networkit_convert(df_or_file= self.nodes, 
                                 cola= self.meta['cola'], 
                                 colb= self.meta['cola'], colvertex= self.meta['colvertex'], nrows=1000000000)

       return graph, index












############################################################################################################################
############################################################################################################################
def test_networkit(net):
    """Compute PageRank as a measure of node centrality by receiving a NetworkKit graph.


    Docs::
        net  :   NetworkKit graph

        https://networkit.github.io/dev-docs/notebooks/Centrality.html


    """
    import networkit as nk

    df = test_pd_create_dag()

    G, imap = dag_networkit_convert(df_or_file=df, cola='a', colb='b')
    dag_networkit_save(G)

    nk.overview(G)

    ### PgeRank
    pr = nk.centrality.PageRank(net)
    pr.run()
    print( pr.ranking())


def dag_networkit_convert(df_or_file: pd.DataFrame, cola='cola', colb='colb', colvertex="", nrows=1000):
    """Convert a panadas dataframe into a NetworKit graph
      and return a NetworKit graph.


    Docs::
                    df   :    dataframe[[ cola, colb, colvertex ]]
      cola='col_node1'  :  column name of node1
      colb='col_node2'  :  column name of node2
      colvertex=""      :  column name of weight

      https://networkit.github.io/dev-docs/notebooks/User-Guide.html#The-Graph-Object


    """
    import networkit as nk, gc
    from utilmy import pd_read_file

    if isinstance(df_or_file, str):
      df = pd_read_file(df_or_file)
    else :
      df = df_or_file
      del df_or_file

    #### Init Graph
    # nodes   = set(df[cola].unique()) + set(df[colb].unique())
    nodes   = set(df[cola].unique()).union(set(df[colb].unique()))
    n_nodes = len(nodes)

    graph = nk.Graph(n_nodes, edgesIndexed=False, weighted = True )
    if colvertex != "":
      weights = df[colvertex].values
    else :
      weights = np.ones(len(df))

    #### Add to Graph
    dfGraph = df[[cola, colb]].values

    # print(df[cola])

    #### Map string ---> Integer, save memory
    # print(str(df))
    if 'int' not in str(df[cola].dtypes):
      index_map = { hash(x):x for x in nodes }
      # for i in range(len(df)):

      for i in range(len(df[[cola, colb]].values)):
          ai = df.iloc[i, 0]
          bi = df.iloc[i, 1]
          graph.addEdge( int(index_map.get( ai, ai)), int(index_map.get( bi, bi)), weights[i])
    else :
      index_map = {   }
      for i in range(len(df)):
          ai = df.iloc[i, 0]
          bi = df.iloc[i, 1]
          graph.addEdge( ai, bi, weights[i])

    return graph, index_map




def dag_networkit_save(net, dirout, format='metis/gml/parquet', tag="", cols= None, index_map=None,n_vertex=1000):
    """Save a NetworkKit graph.


    Docs::
        net     :   NetworkKit graph
        dirout  :   output folder
        format  :   file format 'metis/gml/parquet'
        tag     :   folder suffix

        https://networkit.github.io/dev-docs/notebooks/IONotebook.html


    """
    import json, os, pandas as pd
    dirout = dirout if tag == "" else dirout + "/" + tag + "/"
    os.makedirs(dirout, exist_ok=True)

    ##### Metadata in json  ########################################
    dinfo = {}
    try :
        nodes   = set(df[cola].unique()).union(set(df[colb].unique()))
        n_nodes = len(nodes)
        dinfo = { 'cola':  cola, 'colb': colb, 'colvertex':colvertex, 'n_rows': nrows, 'n_nodes': n_nodes}
    except : pass
    json.dump(dinfo, open(dirout + "/network_meta.json", mode='w'), )


    #####  Main data     ##########################################
    if 'parquet' in format:
          df = np.zeros((n_vertex,2) )
          for i,edge in enumerate(net) :
              df[i,0] = edge[0]
              df[i,1] = edge[1]
              df[i,2] = edge[2]
          cols = cols if cols is not None else ['a', 'b', 'weight']
          df   = pd.DataFrame(df, columns=cols)

          if isinstance(index_map, dict):

            df[cols[0]] = df[cols[0]].apply(lambda x : index_map.get(x, x) )
            df[cols[1]] = df[cols[1]].apply(lambda x : index_map.get(x, x) )
          from utilmy import pd_to_file
          pd_to_file(df, dirout + "/network_data.parquet", show=1)

    else :
        import networkit as nk
        ddict = { 'metis': nk.Format.METIS, 'gml': nk.Format.GML }
        nk.graphio.writeGraph(net, dirout + f'/network_data.{format}' ,  ddict.get(format, 'metis') )

    return dirout


def dag_networkit_load(dirin="", model_target='networkit', nrows=1000, cola='cola', colb='colb', colvertex=''):
    """  Load into network data INTO a framework

    Docs::
            dirin  :   input folder

            https://networkit.github.io/dev-docs/notebooks/IONotebook.html

    """
    import pandas as pd, glob, json
    ddict = { 'metis',  'gml', 'parquet' }

    def is_include(fi, dlist):
        for ext in dlist :
            if ext in fi : return True
        return False
    print(dirin)
    flist0 = glob.glob(dirin, recursive= True)
    print(flist0)
    flist  = [ fi for fi in flist0 if   is_include(fi, ddict )  ]

    if len(flist) == 0 : return None

    if ".parquet" in  flist[0] :
        djson = {}
        try :
           fjson = [fi for fi in flist0 if ".json" in flist0]
           djson = json.load(open(fjson[0], mode='r') )
        except : pass

        cola      = djson.get('cola', cola)
        colb      = djson.get('colb', cola)
        colvertex = djson.get('colvertex', colvertex)


        if model_target == 'networkit':
           net = dag_create_networkit(df_or_file= flist, cola=cola, colb=colb, colvertex=colvertex, nrows=nrows)
        print("return")
        return net

    elif model_target == 'networkit':
        import networkit as nk
        ddict = { 'metis': nk.Format.METIS, 'gml': nk.Format.GML  }
        ext =   flist[0].split("/")[-1].split(".")[-1]
        net = nk.readGraph(dirin, ddict[ext])
        print("return1")
        return net
    else :
      print("return2")
      raise Exception('not supported')









############################################################################################################################
def pd_plot_network(df:pd.DataFrame, cola: str='col_node1', 
                    colb: str='col_node2', coledge: str='col_edge',
                    colweight: str="weight",html_code:bool = True):
    """  Function to plot network https://pyviz.org/tools.html
    Docs::

            df                :        dataframe with nodes and edges
            cola='col_node1'  :        column name of node1
            colb='col_node2'  :        column name of node2
            coledge='col_edge':        column name of edge
            colweight="weight":        column name of weight
            html_code=True    :        if True, return html code
    """

    def convert_to_networkx(df:pd.DataFrame, cola: str="", colb: str="", colweight: str=None):
        """
        Convert a panadas dataframe into a networkx graph
        and return a networkx graph
        Docs::

                df                :        dataframe with nodes and edges
        """
        import networkx as nx
        import pandas as pd
        g = nx.Graph()
        for index, row in df.iterrows():
            g.add_edge(row[cola], row[colb], weight=row[colweight],)

        nx.draw(g, with_labels=True)
        return g


    def draw_graph(networkx_graph, notebook:bool =False, output_filename='graph.html',
                   show_buttons:bool =True, only_physics_buttons:bool =False,html_code:bool  = True):
        """  This function accepts a networkx graph object, converts it to a pyvis network object preserving
        its node and edge attributes,
        and both returns and saves a dynamic network visualization.
        Valid node attributes include:
            "size", "value", "title", "x", "y", "label", "color".
            (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)

        Docs::

                networkx_graph: The graph to convert and display
                notebook: Display in Jupyter?
                output_filename: Where to save the converted network
                show_buttons: Show buttons in saved version of network?
                only_physics_buttons: Show only buttons controlling physics of network?
        """
        from pyvis import network as net
        import re
        # make a pyvis network
        pyvis_graph = net.Network(notebook=notebook)

        # for each node and its attributes in the networkx graph
        for node, node_attrs in networkx_graph.nodes(data=True):
            pyvis_graph.add_node(str(node), **node_attrs)

        # for each edge and its attributes in the networkx graph
        for source, target, edge_attrs in networkx_graph.edges(data=True):
            # if value/width not specified directly, and weight is specified, set 'value' to 'weight'
            if not 'value' in edge_attrs and not 'width' in edge_attrs and 'weight' in edge_attrs:
                # place at key 'value' the weight of the edge
                edge_attrs['value'] = edge_attrs['weight']
            # add the edge
            pyvis_graph.add_edge(str(source), str(target), **edge_attrs)

        # turn buttons on
        if show_buttons:
            if only_physics_buttons:
                pyvis_graph.show_buttons(filter_=['physics'])
            else:
                pyvis_graph.show_buttons()

        # return and also save
        pyvis_graph.show(output_filename)
        if html_code:

          def extract_text(tag: str,content: str)-> str:
            reg_str = "<" + tag + ">\s*((?:.|\n)*?)</" + tag + ">"
            extracted = re.findall(reg_str, content)[0]
            return extracted
          with open(output_filename) as f:
            content = f.read()
            head = extract_text('head',content)
            body = extract_text('body',content)
            return head, body
    networkx_graph = convert_to_networkx(df, cola, colb, colweight=colweight)
    head, body = draw_graph(networkx_graph, notebook=False, output_filename='graph.html',
               show_buttons=True, only_physics_buttons=False,html_code = True)
    return head, body







###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




