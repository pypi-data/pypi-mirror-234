import os
import pandas as pd
from knowledge_graph import knowledge_grapher, NERExtractor, KGEmbedder
def runall(dirin='final_dataset_clean_v2 .tsv'):

    """
    Doc::
        cd utilmy/nlp/tttorch/kgraph
        python knowledge_graph runall --dirin mydirdata/
    """
    data = pd.read_csv('final_dataset_clean_v2 .tsv', delimiter='\t')
    extractor = NERExtractor(data, 'pykeen_data', load_spacy=True)
    data_kgf = extractor.extract_triples(-1)
    extractor.prepare_data(data_kgf)

    data_kgf_path = os.path.join('pykeen_data', 'data_kgf.tsv')
    data_kgf = knowledge_grapher.load_data(data_kgf_path)
    grapher = knowledge_grapher(data_kgf=data_kgf,embedding_dim=10, load_spacy=True)
    grapher.build_graph()
    grapher.plot_graph('plots')

    embedder = KGEmbedder('pykeen_data', grapher.graph, embedding_dim=10)
    # If you have the trained model to be saved then pass a non existing dir to load_embeddings()
    embedder.load_embeddings('none')
    entity_ids = embedder.save_embeddings()
