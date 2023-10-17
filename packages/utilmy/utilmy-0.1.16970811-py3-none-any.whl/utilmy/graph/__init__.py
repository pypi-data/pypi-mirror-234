""" Network

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


"""