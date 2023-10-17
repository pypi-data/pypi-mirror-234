import pandas as pd
from knowledge_graph import knowledge_grapher

data = pd.read_csv('final_dataset_clean_v2 .tsv', delimiter='\t')
grapher = knowledge_grapher(data=data,embedding_dim=10, load_spacy=True)

data_kgf = grapher.extractTriples(-1)
grapher.buildGraph(data_kgf)
grapher.plot_graph()
grapher.prepare_data(data_kgf)
