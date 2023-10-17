"""

https://www.bnlearn.com/examples/useR19-tutorial/

> load("prepd-ortho.rda")
> str(ortho)




"""
library(bnlearn)
library(lattice)

#### User Input  ####################
dirin="./mydata/"
dirout="./out/"



#pdag = iamb(learning.test)
pdag.to_file( irin + "/tabular_data.csv" )


to_file() <- function(sstr) {
    ### Write results on disk
    with open(dirin +"/result.txt") as fp:
       fp.write(sstr)

}



BayesianNetwork <- function() {

  data(learning.test)
  pdag = iamb(learning.test)
  pdag



  #### Load CSV data from Disk
  df = load_csv(dirin + "/tabular_data.csv")


  #### Create DAG #########################
  nodes = list(df.columns)
  dag = pdag2dag(pdag, ordering = c(nodes ))


  #Setting the direction of undirected arcs
  print("Setting the direction of undirected arcs")
  # dag = set.arc(pdag, from = "B", to = "A")
  # dag = pdag2dag(pdag, ordering = c("A", "B", "C", "D", "E", "F"))

  #Fitting the parameters (Maximum Likelihood estimates)
  print("Fitting the parameters (Maximum Likelihood estimates)")
  fit = bn.fit(dag, learning.test)
  fit

  print(fit$D, perm = c("D", "C", "A"))

  png(filename="barplot1.png")
  bn.fit.barchart(fit$D)
  dev.off()

  png(filename="dotplot1.png")
  bn.fit.dotplot(fit$D)
  dev.off()

  #Continous data -Fitting the parameters of a Gaussian Bayesian network (e.g. the regression coefficients for each variable against its parents) is done in the same way.
  print("Continous data -Fitting params of a Gaussian Bayesian network (e.g. the reg. coeff. for each variable against its parents) is done in the same way.
")
  data(gaussian.test)
  pdag = iamb(gaussian.test)
  undirected.arcs(pdag)

  dag = set.arc(pdag, "D", "B")
  fit = bn.fit(dag, gaussian.test)
  fit

  to_file( coefficients(fit$F)   )
  str(residuals(fit$F))

  png(filename=  dirout + "qqplot1.png")
  bn.fit.qqplot(fit)
  dev.off()

  png(filename= dirout + "xyplot1.png")
  bn.fit.xyplot(fit)
  dev.off()

  png(filename= dirout +"histogram1.png")
  bn.fit.histogram(fit)
  dev.off()

  print("Hybrid data (mixed discrete and continuous)")
  data(clgaussian.test)
  dag = hc(clgaussian.test)
  fit = bn.fit(dag, clgaussian.test)
  fit

  png(filename=  dirout + "qqplot2.png")
  bn.fit.qqplot(fit$G)
  dev.off()

}


BayesianNetwork()
