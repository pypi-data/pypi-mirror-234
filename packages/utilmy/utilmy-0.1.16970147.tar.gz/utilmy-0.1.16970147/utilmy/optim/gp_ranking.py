""" Search  mathematical Formulae using Genetic Algorithm , Genetic Programming



"""
import os, random, math, numpy as np, warnings, copy, time
from box import Box
from random import random
np.seterr(all='ignore') 


### Needs to evaluate formulae
# from numpy import (sin, cos, log, exp, sqrt )
from numpy import (sin, cos, log, exp, sqrt )


####################################################################################################
from utilmy.utilmy_base import log as llog, log2 ### Conflict with numpy.log

def help():
    from utilmy import help_create
    print(help_create(__file__) )

import utilmy.optim.gp_searchformulae as gp


####################################################################################################
def test_pars_values():
    """ return test params
    docs::

        myproblem1 = myProblem()

        p               = Box({})
        p.log_file      = 'trace.log'
        p.print_after   = 5
        p.print_best    = True


        p.nvars_in      = 2  ### nb of variables
        p.nvars_out     = 1
        p.operators     = ["sum", "diff", "div", "mul"]

        p.max_iter      = 10
        p.pop_size      = 20  ## Population (Suggested: 10~20)
        p.pa            = 0.3  ## Parasitic Probability (Suggested: 0.3)
        p.kmax          = 100000  ## Max iterations
        p.nc, p.nr       = 10,1  ## Graph columns x rows
        p.arity         = 2  # Arity
        p.seed          = 43

    """
    myproblem1 = myProblem_ranking()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff","sin"]
    p.symbols       = ["x0","x1"]


    p.n_exp         = 1
    p.max_step      = 100
    p.offsprings    = 10
    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662799885.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings


    return myproblem1, p


def test5():
    """Test search_formulae_dcgpy_v1 with myProblem_ranking
    """
    myproblem       = myProblem_ranking()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff", "exp", "log"]
    p.symbols       = ["x0","x1"]

    p.n_exp         = 10
    p.max_step      = 100  ## per expriemnet
    p.offsprings    = 5

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662801438.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings



    #### Run Search
    res = gp.search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)




def test9():
    """Test search_formulae_dcgpy_v1 with myProblem_ranking
    """
    myproblem       = myProblem_ranking_v2()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff", "exp", "log"]
    p.symbols       = ["x0","x1"]

    p.n_exp         = 10
    p.max_step      = 100  ## per expriemnet
    p.offsprings    = 5

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662801438.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings



    #### Run Search
    res = gp.search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)



""""

2 issues :
   Symmetric formulae : not yet, our cost for symmetric : not regular, pb of gradient, noisy.

   Compliexyt :  good,  len(expr)  :    dcgpy.simplify()  : 1/(x1+x1) ---. 1/(2*x1)   
                    print("New best found: gen: ", kstep, " value: ", fitness[i], " ", dCGP.simplify(symbols))

                    0.002* len(exprt)  --> force fomuale


We need to improve 
        self.check()  --> benchmark level  
          we dont how good is the new formulae.

--> Discover a new math formulae   by using the 



1) Add more manual baseline to see
 Manual :
   base1:  x0 + x1
   base2 : x0 * x1
   base3   log(x0) + log(x1)
   base3:  "random.random()"   --> random expr




   Cost very concentrated  around [9.0 - 10.0]

    def check(self):
        lexpr =[ ('x0 + x1', 'ok')  ,   ### symmetric
                 ('log(x0) + log(x1)', 'ok'),
                 'random.random()', 'rand'),

                 (' x0/x1', 'bad')  ### incorrect not symmetric




                 ....

        ]

        for expr in lexpr:
            cost = self.get_correlm(expr[0] )
            res.append([ expr[1], expr[0], cost ])

        dfr = pd.DataFrame(res, columns=['expr_type', 'expr', 'cst'])
        log(dfr)
        

        our formuale


#### later
### save our model and re-load inject back some formulae
  

  
2) Single variable formulae
   new problem defintion

     Good idea as start Force symmetric.
       r =  x0*x1  -->  f(r)    ---> some New direction == symmetric consistence.
       r  = x0+x1  -->  F(r)



       r = x0+x1 






   Newformulae - randomScore === Actual improvement

   NewFormCost - CostBase1
      Why trhe cost not symmetric is not so high ?




My guess:
   Symmetry Cost:  not force too much the symmetr, 
                  no linear, not smooeht --> pb of convergence.
     


        x0 = 1/(self.kk + rank1)  ### inverse of rank, decreasing in rank :  rank=1 --> high score.
        x1 = 1/(self.kk + rank2*self.adjust)

        x0 = rank2 / 100.0 in [0,1]
        x1 = rank1 / 100.0  in [0,1]
        

 

        scores_new =  eval(formulae_str)  ### formulaue 1 variable in r


 DCPY : GP + Gradient (NNeural cost)  --> gredient direction to smallest cost.  






"""


###################################################################################################
class myProblem_ranking:
    def __init__(self,n_sample = 100,kk = 1.0,nsize = 100,ncorrect1 = 50,ncorrect2 = 50,adjust=1.0):
        """  Define the problem and cost calculation using formulae_str
        Docs::

            Problem

            2 list of items,  out of  100 items.

                 A = [ 'a1', 'a10',   'a7',  'a100']    paritally orderd  Rank 0 :  A[0] = 'a1'   ### measure, signal

                 B = [ 'a7', 'a17',   'a29',  'a67']    paritally ordered  Rank 2   A[2] = 'a29'  ## measure


                 #### Dependance.
                 ScoreFormuale  = F( % of correct in A, % of correct in B,   Overlap between A and B,  ...)



            Goal is to merge them into a single list    and BEST WAY. --> need to use a score
            Cmerge = [ 'a1', 'a7',  ....  'a10',        ]


            ### TO DO, use a score function  (heuristic manually)
                score(item_k)  =  1/( 1+ rank_listA(item_k) )   + 1/(1 + rank_listB(item_k)   )  

                score('a7')  =  1/( 1+ rank_listA('a7') )   + 1/(1 + rank_listB('a7')   )  
                             =  1/(1 + 2)                         + 1/(1 + 0)

                score('a10')  =  1/( 1+ rank_listA('a10') )   + 1/(1 + rank_listB('a10')   )  
                             =  1/(1 + 1)                         + 1/(1 +  lenB)  


           #### Find Formulae , what the below doing.
              TrueList = [  ]
              correlationSPEARMN(TrueList, NewSample_mergeList)  --->  1.0   Better                  

            Conditions
                 formulae is SYmeetric   rankA, rankB    CANNOT 1/rank1 - 1/rank2  --> not symentric
                 Derivates negative in   Dformuale/drank < 0.0  

                 test8()



            n_sample        : Number of Samples list to be generated, default = 5
            kk              : Change the fake generated list rank , default = 1.0
            ncorrect1       : the number of correctly ranked objects for first list , default = 40
            ncorrect2       : the number of correctly ranked objects for second list , default = 50
            adjust

            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

            Goal is to find a formulae, which make merge_list as much sorted as possible

        """
        import random as randomize
        randomize.seed(100000)
        self.n_sample  = n_sample
        self.kk        = kk
        self.nsize     = nsize
        self.ncorrect1 = ncorrect1
        self.ncorrect2 = ncorrect2
        self.adjust    = adjust

        self.x0_list        = np.array([[randomize.randint(0,100) for _ in range(101)] for _ in range(self.n_sample)])
        self.x1_list        = np.array([[randomize.randint(0,100) for _ in range(101)] for _ in range(self.n_sample)])
        self.check()

    def check(self):
        expr = 'x0 + x1'
        correlm = self.get_correlm(expr)
        print("Cost for  'x0+x1' is",correlm)

        expr = 'log(x0) + log(x1)'
        correlm = self.get_correlm(expr)
        print("Cost for  'log(x0)+log(x1)' is",correlm)
        

    def get_cost(self, expr:None, symbols):
        """ Cost Calculation, Objective to Maximize
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        #try:
        correlm = self.get_correlm(formulae_str=expr(symbols)[0])
        #correlm = self.get_correlm(formulae_str=str(expr.simplify(symbols)[0]))
        #except:
            #correlm = 1.0
        check = 3
        return correlm,check


    def get_correlm(self, formulae_str):
        """  Compare 2 lists lnew, ltrue and output correlation.
             Goal is to find rank_score such Max(correl(lnew(rank_score), ltrue ))

        Docs:
            formulae_str            : Formulae String

        """
        #print("expression",formulae_str)
        #formulae_str = str(formulae_str)

        
        from scipy import stats
        ##### True list
        ltrue = np.arange(0,100, 1) #[ i  for i in range(0, 100) ]

        #### Create noisy list
        ltrue_rank = {i:x for i,x in enumerate(ltrue)}
        list_overlap =  np.random.choice(ltrue, 80) #ltrue[:80]  #### Common elements

        correls = []
        diff    = []
        difflist  = []

        rlist  = [ 1.0,  17.6, 37.5  ]
        rlist2 = [ 47.2,  4.7, 0.3  ]
        for i in range(2):
            x0 = rlist[i]
            x1 = rlist2[i]
            #s1 =  eval(formulae_str)
            try:
                s1 = eval(formulae_str)
            except:
                s1 = 10000

            x0 = rlist2[i]
            x1 = rlist[i]
            #s2 =  eval(formulae_str)
            try:
                s2 = eval(formulae_str)
            except:
                s2 = 10000
            difflist.append(abs(s1-s2))


        if np.sum(difflist) > 0.1 :  ###not symmetric --> put high cost, remove.
            cost =  10.0 *(1 + sum(difflist) * 5.0 )
            return cost

            #scores_new = 0.99 + np.zeros(len(rank1))
            #return scores_new
        else:
            for i in range(self.n_sample):
                #ll1  = self.rank_generate_fake(ltrue_rank, list_overlap,nsize=self.nsize, ncorrect=self.ncorrect1)
                #ll2  = self.rank_generate_fake(ltrue_rank, list_overlap,nsize=self.nsize, ncorrect=self.ncorrect2)

                ll1 = self.x0_list[i]
                ll2 = self.x1_list[i]

                #### Merge them using rank_score
                lnew = self.rank_merge_v5(ll1, ll2, formulae_str= formulae_str)
                lnew = lnew[:100]
                # llog(lnew)

                ### Eval with True Rank              #We can also use kendmall equation
            
                c1 = stats.spearmanr(ltrue,  lnew).correlation
                correls.append(c1)

                '''
                #### Symmetric Condiution   ############################################
                if i < 3:
                    ll1 = self.x1_list[i]
                    ll2 = self.x0_list[i]

                    #### Merge them using rank_score
                    lnew = self.rank_merge_v5(ll1, ll2, formulae_str= formulae_str)
                    lnew = lnew[:100]
                    # llog(lnew)

                    ### Eval with True Rank              #We can also use kendmall equation
                    c2 = stats.spearmanr(ltrue,  lnew).correlation

                    ### diff=0  IF formulae is symettric
                    diff.append( abs(c1-c2) )
                
                '''

        correlm = np.mean(correls)
        #diffsum = np.sum( diff )

        ###
        #cost  = 10.0*(1-correlm) + 100.0 * 1e4 * diffsum
        cost  = 10.0*(1-correlm)


        ### minimize cost
        return cost


    def rank_score(self, fornulae_str:str, rank1:list, rank2:list)-> list:
        """  ## Example of rank_scores0 = Formulae(list_ score1, list_score2)
             ## Take 2 np.array and calculate one list of float (ie NEW scores for position)
        Docs::

            list of items:  a,b,c,d, ...
            item      a,b,c,d,e
            rank1 :   1,2,3,4 ,,n     (  a: 1,  b:2, ..)
            rank2 :   5,7,2,1 ,,n     (  a: 5,  b:6, ..)

            scores_new :   a: -7.999,  b:-2.2323
            (item has new scores)

        """
        import random as randomize
        ### Check if formulae had number of x1 and x05
        '''
        
        
        rlist  = np.random.random(5)
        rlist2 = np.random.random(5)

        difflist  = []
        for i in range(5):
           x0 = rlist[i]
           x1 = rlist2[i]
           s1 =  eval(fornulae_str)

           x0 = rlist2[i]
           x1 = rlist[i]
           s2 =  eval(fornulae_str)
           difflist.append(abs(s1-s2))


        if np.sum(difflist) > 0.1 :  ###not symmetric --> put high cost, remove.
            scores_new = 0.99 + np.zeros(len(rank1))
            return scores_new

        '''

        ### numpy vector :  take inverse of rank As PROXT.
        x0 = 1/(self.kk + rank1)
        x1 = 1/(self.kk + rank2*self.adjust)
        scores_new =  eval(fornulae_str)


        return scores_new


    def rank_merge_v5(self, ll1:list, ll2:list, formulae_str:str):
        """ ## Merge 2 list using a FORMULAE
        Docs::

        l1              : 1st generated list
        l2:             : 2nd generated list
        formulae_str    : string
            Re-rank elements of list1 using ranking of list2
            20k dataframe : 6 sec ,  4sec if dict is pre-build
            Fastest possible in python
        """
        if len(ll2) < 1: return ll1
        n1, n2 = len(ll1), len(ll2)

        if not isinstance(ll2, dict) :
            ll2 = {x:i for i,x in enumerate( ll2 )  }  ### Most costly op, 50% time.

        adjust, mrank = (1.0 * n1) / n2, n2
        rank2 = np.array([ll2.get(sid, mrank) for sid in ll1])
        rank1 = np.arange(n1)
        rank3 = self.rank_score(fornulae_str=formulae_str, rank1=rank1, rank2= rank2) ### Score

        #### re-rank  based on NEW Scores.
        v = [ll1[i] for i in np.argsort(rank3)]
        return v  #### for later preprocess


    #### Generate fake list to be merged.
    def rank_generate_fake(self,dict_full, list_overlap, nsize=100, ncorrect=20):
        """  Returns a list of random rankings of size nsize where ncorrect elements have correct ranks
        Docs::

            dict_full    : a dictionary of 1000 objects and their ranks
            list_overlap : list items common to all lists
            nsize        : the total number of elements to be ranked
            ncorrect     : the number of correctly ranked objects
        """
        # first randomly sample nsize - len(list_overlap) elements from dict_full
        # of those, ncorrect of them must be correctly ranked
        import random as randomize
        random_vals = []
        while len(random_vals) <= nsize - len(list_overlap):
            rand = randomize.sample(list(dict_full), 1)
            if (rand not in random_vals and rand not in list_overlap):
                random_vals.append(rand[0])

        # next create list as aggregate of random_vals and list_overlap
        list_overlap = list(list_overlap)
        list2 = random_vals + list_overlap

        # shuffle nsize - ncorrect elements from list2
        copy1 = list2[0:nsize - ncorrect]
        randomize.shuffle(copy1)
        list2[0:nsize - ncorrect] = copy1

        # ensure there are ncorrect elements in correct places
        if ncorrect == 0:
            return list2
        rands = randomize.sample(list(dict_full)[0:nsize + 1], ncorrect + 1)
        for r in rands:
            list2[r] = list(dict_full)[r]
        return list2


class myProblem_ranking_v2:
    def __init__(self,n_sample = 100,kk = 1.0,nsize = 100,ncorrect1 = 50,ncorrect2 = 50,adjust=1.0):
        """  Define the problem and cost calculation using formulae_str
        Docs::

            Problem

            2 list of items,  out of  100 items.

                 A = [ 'a1', 'a10',   'a7',  'a100']    paritally orderd  Rank 0 :  A[0] = 'a1'   ### measure, signal

                 B = [ 'a7', 'a17',   'a29',  'a67']    paritally ordered  Rank 2   A[2] = 'a29'  ## measure


                 #### Dependance.
                 ScoreFormuale  = F( % of correct in A, % of correct in B,   Overlap between A and B,  ...)



            Goal is to merge them into a single list    and BEST WAY. --> need to use a score
            Cmerge = [ 'a1', 'a7',  ....  'a10',        ]


            ### TO DO, use a score function  (heuristic manually)
                score(item_k)  =  1/( 1+ rank_listA(item_k) )   + 1/(1 + rank_listB(item_k)   )  

                score('a7')  =  1/( 1+ rank_listA('a7') )   + 1/(1 + rank_listB('a7')   )  
                             =  1/(1 + 2)                         + 1/(1 + 0)

                score('a10')  =  1/( 1+ rank_listA('a10') )   + 1/(1 + rank_listB('a10')   )  
                             =  1/(1 + 1)                         + 1/(1 +  lenB)  


           #### Find Formulae , what the below doing.
              TrueList = [  ]
              correlationSPEARMN(TrueList, NewSample_mergeList)  --->  1.0   Better                  

            Conditions
                 formulae is SYmeetric   rankA, rankB    CANNOT 1/rank1 - 1/rank2  --> not symentric
                 Derivates negative in   Dformuale/drank < 0.0  

                 test8()



            n_sample        : Number of Samples list to be generated, default = 5
            kk              : Change the fake generated list rank , default = 1.0
            ncorrect1       : the number of correctly ranked objects for first list , default = 40
            ncorrect2       : the number of correctly ranked objects for second list , default = 50
            adjust

            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

            Goal is to find a formulae, which make merge_list as much sorted as possible

        """
        import random as randomize
        randomize.seed(100000)
        self.n_sample  = n_sample
        self.kk        = kk
        self.nsize     = nsize
        self.ncorrect1 = ncorrect1
        self.ncorrect2 = ncorrect2
        self.adjust    = adjust

        self.x0_list        = np.array([[randomize.randint(0,100) for _ in range(101)] for _ in range(self.n_sample)])
        self.x1_list        = np.array([[randomize.randint(0,100) for _ in range(101)] for _ in range(self.n_sample)])
        self.x0_rank_based_x1 = self.get_rank_based_other(self.x0_list, self.x1_list)
        self.x1_rank_based_x0 = self.get_rank_based_other(self.x1_list, self.x0_list)
        self.check()


    def check(self):
        import pandas as pd

        lexpr =[ ('x0 + x1', 'ok')  ,   ### symmetric
                 ('log(x0) + log(x1)', 'ok'),
                 #('exec("randomize.random()")', 'rand'),
                 (' x0/x1', 'bad'),  ### incorrect not symmetric,
                 ('x0/x1 + x1/x0','ok'),
                 ('x0/x1 - x1/x0','bad'),
                 ('x0**2/x1','bad'),
                 ('log(x0)','bad'),
                 ('sin(x0*x1)','good'),
                 ('(x0) / ((x0 - x0)*(x1 - x1))', 'bad'),
                 ('log(x0*(1 - 2*x0))', 'bad'),
                 ('x0*exp(-exp(x0))', 'bad'),
                 ('exp(x0*exp(-exp(x0)))', 'bad'),

                    ]
    
        res = []
        for expr in lexpr:
            cost = self.get_correlm(expr[0] )
            res.append([ expr[1], expr[0], cost ])

        dfr = pd.DataFrame(res, columns=['expr_type', 'expr', 'cst'])
        llog("Baseline Results")
        llog(dfr)


    def get_cost(self, expr:None, symbols):
        """ Cost Calculation, Objective to Maximize
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        correlm = self.get_correlm(formulae_str=expr(symbols)[0])
        check = 3
        return correlm,check


    def get_correlm(self, formulae_str:str):
        """  Compare 2 lists lnew, ltrue and output correlation.
             Goal is to find rank_score such Max(correl(lnew(rank_score), ltrue ))

        Docs:
            formulae_str            : Formulae String

        """
        l1  = [ 1.0,  17.6, 37.5  ]
        l2 = [ 47.2,  4.7, 0.3  ]
        diff = 0
        totalSum = 0 
        costSimple = len(formulae_str) * 0.003
        for i in range(2): 
            x0 = l1[i]
            x1 = l2[i]
            try:
                s1 = eval(formulae_str)
            except Exception as e:
                # the expression is not evaluatable -> must avoid this
                return 1e4

            x0 = l2[i]
            x1 = l1[i]
            try:
                s2 = eval(formulae_str)
            except Exception as e:
                return 1e4
            totalSum += s1 + s2
            diff += abs(s1 - s2)
        # if the expression gives very small results, then the diff will not be smaller than 0.1
        # -> the expression will be considered as symmetric even it is not -> we must avoid this
        if totalSum < 0.2: 
            return 1e4
        # if the expression gives nan result, then difference between two result is also 
        # nan which is smaller than 0.1 -> we must avoid this
        if diff > 0.1 or math.isnan(diff): 
            return 1e4

        from scipy import stats, signal
        ##### True list
        ltrue = np.arange(0,100, 1) #[ i  for i in range(0, 100) ]

        correls = []
        for i in range(self.n_sample):
            ll1 = self.x0_list[i]
            ll2 = self.x1_rank_based_x0[i]

            #### Merge them using rank_score
            lnew = self.rank_merge_v5(ll1, ll2, formulae_str=formulae_str)
            lnew = lnew[:100]

            ### Eval with True Rank              #We can also use kendmall equation
            # c1 = stats.spearmanr(ltrue,  lnew).correlation
            c1 = stats.kendalltau(ltrue, lnew).correlation
            correls.append(c1)


        correlm = np.mean(correls)
        cost  = 10.0*(1-correlm)
        cost = cost + costSimple

        ### minimize cost
        return cost


    def rank_score(self, formulae_str:str, rank1:list, rank2:list)-> list:
        """  ## Example of rank_scores0 = Formulae(list_ score1, list_score2)
             ## Take 2 np.array and calculate one list of float (ie NEW scores for position)
        Docs::

            list of items:  a,b,c,d, ...
            item      a,b,c,d,e
            rank1 :   1,2,3,4 ,,n     (  a: 1,  b:2, ..)
            rank2 :   5,7,2,1 ,,n     (  a: 5,  b:6, ..)

            scores_new :   a: -7.999,  b:-2.2323
            (item has new scores)

        """
        ### Check if formulae had number of x1 and x05
        """
        rlist  = np.random.random(5)
        rlist2 = np.random.random(5)

        difflist  = []
        for i in range(10):
           x0 = rlist[i]
           x1 = rlist2[i]
           s1 =  eval(fornulae_str)

           x0 = rlist2[i]
           x1 = rlist[i]
           s2 =  eval(fornulae_str)
           difflist.append(abs(s1-s2))


        if np.sum(difflist) > 0.1 :  ###not symmetric --> put high cost, remove.
             scores_new = 0.99 + np.zeros(len(rank1))
             return scores_new

        """

        ### numpy vector :  take inverse of rank As PROXT.
        x0 = 1/(self.kk + rank1)
        x1 = 1/(self.kk + rank2*self.adjust)



        scores_new =  eval(formulae_str)


        return scores_new

    def get_rank_based_other(self, l1: list, l2: list): 
        """
            Create the rank of all lists in l1 based on corresponding list in l2. 
        """
        rank_of_l1_based_l2 = []
        for i in range(len(l1)): 
            ll1, ll2 = l1[i], l2[i]
            n1, n2 = len(ll1), len(ll2)

            ll1 = dict(zip(ll1, range(len(ll1))))
            # ll1 = {x:i for i,x in enumerate( ll1 )  }  ### Most costly op, 50% time.

            mrank = n2
            rank = np.array([ll1.get(sid, mrank) for sid in ll2])
            rank_of_l1_based_l2.append(rank)
        return rank_of_l1_based_l2

    def rank_merge_v5(self, ll1:list, ll2:list, formulae_str):
        """ ## Merge 2 list using a FORMULAE
        Docs::

        l1              : 1st generated list
        l2:             : 2nd generated list
        formulae_str    : string
            Re-rank elements of list1 using ranking of list2
            20k dataframe : 6 sec ,  4sec if dict is pre-build
            Fastest possible in python
        """
        if len(ll2) < 1: return ll1
        n1, n2 = len(ll1), len(ll2)

        rank1 = np.arange(n1)
        rank2 = ll2
        rank3 = self.rank_score(formulae_str=formulae_str, rank1=rank1, rank2= rank2) ### Score

        #### re-rank  based on NEW Scores.
        v = np.array([ll1[i] for i in np.argsort(rank3)])
        return v  #### for later preprocess


    #### Generate fake list to be merged.
    def rank_generate_fake(self,dict_full, list_overlap, nsize=100, ncorrect=20):
        """  Returns a list of random rankings of size nsize where ncorrect elements have correct ranks
        Docs::

            dict_full    : a dictionary of 1000 objects and their ranks
            list_overlap : list items common to all lists
            nsize        : the total number of elements to be ranked
            ncorrect     : the number of correctly ranked objects
        """
        # first randomly sample nsize - len(list_overlap) elements from dict_full
        # of those, ncorrect of them must be correctly ranked
        import random as randomize
        random_vals = []
        while len(random_vals) <= nsize - len(list_overlap):
            rand = randomize.sample(list(dict_full), 1)
            if (rand not in random_vals and rand not in list_overlap):
                random_vals.append(rand[0])

        # next create list as aggregate of random_vals and list_overlap
        list_overlap = list(list_overlap)
        list2 = random_vals + list_overlap

        # shuffle nsize - ncorrect elements from list2
        copy1 = list2[0:nsize - ncorrect]
        randomize.shuffle(copy1)
        list2[0:nsize - ncorrect] = copy1

        # ensure there are ncorrect elements in correct places
        if ncorrect == 0:
            return list2
        rands = randomize.sample(list(dict_full)[0:nsize + 1], ncorrect + 1)
        for r in rands:
            list2[r] = list(dict_full)[r]
        return list2





###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()




