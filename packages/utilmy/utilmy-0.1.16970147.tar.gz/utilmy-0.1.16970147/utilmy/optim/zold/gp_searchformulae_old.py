""" Search  mathematical Formulae using Genetic Algorithm , Genetic Programming

Docs::

    Install  DCGP

          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire utilmy

          python -c "from dcgpy import test; test.run_test_suite(); import pygmo; pygmo.mp_island.shutdown_pool(); pygmo.mp_bfe.shutdown_pool()"


          https://darioizzo.github.io/dcgp/installation.html#python

          https://darioizzo.github.io/dcgp/notebooks/real_world1.html


    Install  DSO
           https://github.com/brendenpetersen/deep-symbolic-optimization

           https://iclr.cc/virtual/2021/poster/2578



    Install  Operon

        https://github.com/heal-research/pyoperon

        https://github.com/heal-research/pyoperon/blob/main/example/operon-bindings.py



    Docs:
        https://esa.github.io/pygmo2/archipelago.html#pygmo.archipelago.status



    -- Test Problem
        cd $utilmy/optim/
        python gp_searchformulae.py  test1

        2) Goal is to find a formulae, which make merge_list as much sorted as possible
        Example :
            ## 1) Define Problem Class with get_cost methods
            myproblem1 = myProblem()
            ## myproblem1.get_cost(formulae_str, symbols  )

            ## 2) Param Search
            p               = Box({})
            ...


            ## 3) Run Search
            from utilmy.optim.gp_formulaesearch import search_formulae_algo1
            search_formulae_algo1(myproblem1, pars_dict=p, verbose=True)


            #### Parallel version   ------------------------------------
            for i in range(npool):
                p2         = copy.deepcopy(p)
                p2.f_trace = f'trace_{i}.log'
                input_list.append(p2)

            #### parallel Runs
            from utilmy.parallel import multiproc_run
            multiproc_run(search_formulae_dcgpy, input_fixed={"myproblem": myproblem1, 'verbose':False},
                          input_list=input_list,
                          npool=3)



"""
import os, random, math, numpy as np, warnings, copy
import scipy.stats
from operator import itemgetter
from copy import deepcopy
from box import Box

from matplotlib import pyplot as plt
import numpy as np
from numpy import sin, cos

np.seterr(all='ignore') 

####################################################################################################
from utilmy.utilmy_base import log, log2

# def log(*s):
#     """Log/Print"""
#     print(*s, flush=True)


def help():
    from utilmy import help_create
    print(help_create(__file__) )



####################################################################################################
def test_all():
    """function test_all
    """
    test1()


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

    return myproblem1, p


def test1():
    """Test search_formulae_dcgpy_v1
    """
    from lib2to3.pygram import Symbols
    from dcgpy import expression_gdual_double as expression
    from pyaudi import gdual_double as gdual


    myproblem1,p = test_pars_values()

    #### Run Search
    search_formulae_dcgpy_v1(myproblem1, pars_dict=p, verbose=True)


def test2():
    """Test of search_formulae_dcgpy_v1_parallel
    """
    myproblem1,p = test_pars_values()

    search_formulae_dcgpy_v1_parallel(myproblem=myproblem1, pars_dict=p, verbose=False, npool=3 )


def test3():
    """Test parralel run of search_formulae_dcgpy_v1, in customize parallle version.
    """
    from utilmy.parallel import multiproc_run

    myproblem1,p = test_pars_values()

    npool= 3
    input_list = []
    for i in range(npool):
        p2 = copy.deepcopy(p)
        p2['log_file'] = f'trace_{i}.log'
        input_list.append(p2)

    ### parallel Runs
    multiproc_run(_search_formulae_dcgpy_v1_wrapper,
                  input_fixed={"myproblem": myproblem1, 'verbose':False},
                  input_list=input_list,
                  npool=npool)



def test4():
    """Test search_formulae_dcgpy_v1_parallel_island
    """
    myproblem1,p = test_pars_values()

    #### Run Search
    search_formulae_dcgpy_v1_parallel_island(myproblem1, ddict_ref=p
                       ,hyper_par_list  = ['pa',  ]    ### X[0],  X[1]
                       ,hyper_par_bounds = [ [0], [ 0.6 ] ]
                       ,pop_size=6
                       ,n_island=2
                       ,dir_log="./logs/"
                      )


def test5():
    """Test the myProblem2 class

    """
    myproblem = myProblem2()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "diff", "div", "mul", 'sin']

    p.max_iter      = 10
    p.pop_size      = 20  ## Population (Suggested: 10~20)
    p.pa            = 0.3  ## Parasitic Probability (Suggested: 0.3)
    p.kmax          = 100000  ## Max iterations
    p.nc, p.nr       = 10,1  ## Graph columns x rows
    p.arity         = 2  # Arity
    p.seed          = 43

    search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=True)



def test6():
    """Test the myProblem3 class, parrallel version

    """
    myproblem       = myProblem4()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff"]
    p.symbols       = ["x","v","k"]
    p.max_iter      = 10
    p.nexp          = 100
    p.offsprings    = 10
    p.stop          = 2000
    search_formulae_dcgpy_v3_custom(myproblem = myproblem, pars_dict=p, verbose=False,)


def test7():
    """Test the myProblem4 class, parrallel version

    """
    myproblem      = myProblem3()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff","sin","cos"]
    p.symbols       = ["theta","omega","c"]
    p.max_iter      = 10
    p.nexp          = 100
    p.offsprings    = 10
    p.stop          = 2000
    search_formulae_dcgpy_v3_custom(problem = myproblem, pars_dict=p, verbose=False,)


####################################################################################################
class myProblem:
    def __init__(self,n_sample = 5,kk = 1.0,nsize = 100,ncorrect1 = 40,ncorrect2 = 50,adjust=1.0):
        """  Define the problem and cost calculation using formulae_str
        Docs::

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
        self.n_sample  = n_sample
        self.kk        = kk
        self.nsize     = nsize
        self.ncorrect1 = ncorrect1
        self.ncorrect2 = ncorrect2
        self.adjust    = adjust



    def get_cost(self, expr:None, symbols):
        """ Cost Calculation, Objective to Maximize   
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        try:
            correlm = self.get_correlm(formulae_str=expr(symbols)[0])
        except:
            correlm = 1.0

        return(correlm)


    def get_correlm(self, formulae_str:str):
        """  Compare 2 lists lnew, ltrue and output correlation.
             Goal is to find rank_score such Max(correl(lnew(rank_score), ltrue ))

        Docs: 
            formulae_str            : Formulae String 
        
        """
        ##### True list
        ltrue = [ str(i)  for i in range(0, 100) ]   

        #### Create noisy list 
        ltrue_rank = {i:x for i,x in enumerate(ltrue)}
        list_overlap =  ltrue[:70]  #### Common elements
        
        
        correls = []
        for i in range(self.n_sample):
            ll1  = self.rank_generate_fake(ltrue_rank, list_overlap,nsize=self.nsize, ncorrect=self.ncorrect1)
            ll2  = self.rank_generate_fake(ltrue_rank, list_overlap,nsize=self.nsize, ncorrect=self.ncorrect2)

            #### Merge them using rank_score
            lnew = self.rank_merge_v5(ll1, ll2, formulae_str= formulae_str)
            lnew = lnew[:100]
            # log(lnew) 

            ### Eval with True Rank
            correls.append(scipy.stats.spearmanr(ltrue,  lnew).correlation)

        correlm = np.mean(correls)
        return -correlm  ### minimize correlation val


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
        random_vals = []
        while len(random_vals) <= nsize - len(list_overlap):
            rand = random.sample(list(dict_full), 1)
            if (rand not in random_vals and rand not in list_overlap):
                random_vals.append(rand[0])

        # next create list as aggregate of random_vals and list_overlap
        list2 = random_vals + list_overlap
        
        # shuffle nsize - ncorrect elements from list2 
        copy = list2[0:nsize - ncorrect]
        random.shuffle(copy)
        list2[0:nsize - ncorrect] = copy

        # ensure there are ncorrect elements in correct places
        if ncorrect == 0: 
            return list2
        rands = random.sample(list(dict_full)[0:nsize + 1], ncorrect + 1)
        for r in rands:
            list2[r] = list(dict_full)[r]
        return list2



class myProblem2:
    def __init__(self,n_sample = 5,kk = 1.0,nsize = 100,):
        """  Define the problem and cost calculation using formulae_str
        Docs::


            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

        """
        self.n_sample  = 1
        self.kk        = kk
        self.nsize     = nsize

        self.x0 = np.random.random(50)*10 - 5.0
        self.x1 = np.random.random(50)*10 - 5.0


    def get_cost(self, expr, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        formulae_str=expr(symbols)[0]

        metrics = []
        for i in range(self.n_sample):
            ####
            lnew, ltrue = self.rank_score(formulae_str= formulae_str)
            # log(lnew)

            ### Eval with MSE
            metrics.append( np.mean( (ltrue -  lnew)**2 )  )
            # metrics.append(scipy.stats.spearmanr(ltrue,  lnew).correlation)

        cost =  +np.mean(metrics)
        return cost  ### minimize cost


    def rank_score(self, formulae_str:str):
        """  Generate 2 lists: yeval, ytrue from formulae_str
        Docs::

        """

        x0 = self.x0
        x1 = self.x1

        scores_true =  np.sin(x1) + x0+x1  #### True Formulae to find
        scores_new  =  eval(formulae_str)


        return scores_new, scores_true



class myProblem3:
    def __init__(self):
        pass



    def get_cost(self, dCGP, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        n_points = 50
        omega = []
        theta = []
        c = []
        for i in range(n_points):
            omega.append(random()*10 - 5)
            theta.append(random()*10 - 5)
            c.append(random()*10)

        

        theta = gdual(theta,symbols[0],1)
        omega = gdual(omega,symbols[1],1)
        c = gdual(c)
        res = dCGP([theta,omega,c])[0]
        derivative_symbols = ['d'+item for item in symbols]
        dPdtheta = np.array(res.get_derivative({derivative_symbols[0]: 1}))
        dPdomega = np.array(res.get_derivative({derivative_symbols[1]: 1}))
        thetacoeff = np.array(theta.constant_cf)
        omegacoeff = np.array(omega.constant_cf)
        ccoeff = np.array(c.constant_cf)
        err = dPdtheta/dPdomega + (-ccoeff * np.sin(thetacoeff)) / omegacoeff
        check = sum(dPdtheta*dPdtheta + dPdomega*dPdomega)
        return sum(err * err ), check



class myProblem4:
    def __init__(self):
        pass

    def get_cost(self, dCGP, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            DCGP            : Formulae Expression Object
            symbols         : Symbols  [ 'x1', 'x2', 'x3' ]

        """
        import random
        from dcgpy import kernel_set_gdual_vdouble as kernel_set
        from dcgpy import expression_gdual_vdouble as expression
        from pyaudi import gdual_vdouble as gdual

        n_points = 50

        ###### Variable numerical  ################################
        x = np.random.random(n_points)*2 +2
        v = np.random.random(n_points)*2 +2
        k = np.random.random(n_points)*2 +2
        #for i in range(n_points):
        #    x.append(random.random()*2 + 2)
        #    v.append(random.random()*2 + 2)
        #    k.append(random.random()*2 + 2)
        x = gdual(x,symbols[0], 1)
        v = gdual(v,symbols[1], 1)
        k = gdual(k)
        xcoeff = np.array(x.constant_cf)
        vcoeff = np.array(v.constant_cf)
        kcoeff = np.array(k.constant_cf)


        #### Derivatives numerical  ##############################
        derivative_symbols = ['d'+item for item in symbols]

        formul = dCGP([x,v,k])[0]

        ### formul_str = dCGP.simplify(symbols)
        ### formul_val = eval( formul_str )    ### numerical values

        dPdx = np.array(formul.get_derivative({derivative_symbols[0]: 1}))
        dPdv = np.array(formul.get_derivative({derivative_symbols[1]: 1}))


        ### Cost numerical
        err  = dPdx/dPdv - kcoeff * xcoeff / vcoeff
        cost = sum(err * err)
        return cost, 3



###################################################################################################
def search_formulae_dcgpy_v1(myproblem=None, pars_dict:dict=None, verbose=False, ):
    """ Search Optimal Formulae
    Docs::

        -- Install  DCGP
          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire

          python -c "from dcgpy import test; test.run_test_suite(); import pygmo; pygmo.mp_island.shutdown_pool(); pygmo.mp_bfe.shutdown_pool()"



        from utilmy.optim import gp_searchformulae as gp

        myproblem1 = gp.myProblem()
        ## myproblem1.get_cost(formulae_str, symbols  )

        p               = Box({})
        p.log_file      = 'trace.log'
        p.print_after   = 100
        p.print_best    = True


        p.nvars_in      = 2  ### nb of variables
        p.nvars_out     = 1
        p.operators            = ["sum", "diff", "div", "mul"]

        p.pop_size      = 20  ## Population (Suggested: 10~20)
        p.pa            = 0.3  ## Parasitic Probability (Suggested: 0.3)
        p.kmax          = 100000  ## Max iterations
        p.nc, p.nr       = 10,1  ## Graph columns x rows
        p.arity         = 2  # Arity
        p.seed          = 43

        #### Run Search
        gp.search_formulae_algo1(myproblem1, pars_dict=p, verbose=True)


        -- Add constraints in the functional space
        https://darioizzo.github.io/dcgp/notebooks/phenotype_correction_ex.html

        ### . So that we make sure the function actually passes through the points (-1,0) and (1,0).
        def pc_fun(x, g):
            alpha = - 0.5 * (g([-1])[0]+g([1])[0])
            beta = 0.5 * (g([-1])[0]-g([1])[0])
            return [g(x)[0]+alpha+x[0]*beta]

        for loop in range(10):
            ex.mutate_random(20)
            for i,it in enumerate(x):
                y[i] = ex([it])[0]
            plt.plot(x,y)
        plt.ylim([-1,1])
        plt.grid("on")



    """
    from lib2to3.pygram import Symbols
    from dcgpy import expression_gdual_double as expression
    from dcgpy import kernel_set_gdual_double
    from pyaudi import gdual_double as gdual

    from box import Box
    ######### Problem definition and Cost calculation
    #myproblem = myProblem()


    #### Formulae GP Search params   #################
    log(pars_dict)
    p = Box(pars_dict)

    ### Problem
    nvars_in      = p.nvars_in  ### nb of variables
    nvars_out     = p.nvars_out
    operator_list = kernel_set_gdual_double(p.get("operators", ["sum", "diff", "div", "mul"] ))

    ### Log
    print_after   = p.get('print_after', 20)
    print_best    = p.get('print_best', True)
    pop_size      = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)
    max_iter      = p.get('max_iter', 2) #100000  ## Max iterations
    seed          = p.get('seed', 43)
    log_file      = p.get('log_file', 'log.log') # 'trace.py'

    ### search
    pa            = p.get( 'pa', 0.3)  # 0.3  ## Parasitic Probability (Suggested: 0.3)
    nc,nr         = p.nc, p.nr # 10,1  ## Graph columns x rows
    arity         = p.get( 'arity', 2)   #2  # Arity
    n_cuckoo_eggs = round(p.pa*p.pop_size)
    n_replace     = round(p.pa*p.pop_size)


    ######### Define expression symbols  #######################
    symbols = []
    for i in range(nvars_in):
        symbols.append(f"x{i}")

    ######### Check   ##########################################
    if verbose:
        log(operator_list)
        log(symbols)


    def get_random_solution():
        """Generate Random Formulae Expression

        """
        return expression(inputs = nvars_in,
                            outputs     = nvars_out,
                            rows        = nr,
                            cols        = nc,
                            levels_back = nc,
                            arity       = arity,
                            kernels     = operator_list(),
                            n_eph       = 0,
                            seed        = seed )

    def search():
        """Search for best possible Formulae using Cuckoo Search Algorithm
        """
        def levyFlight(u):
            return (math.pow(u,-1.0/3.0)) # Golden ratio = 1.62

        def randF():
            return (random.uniform(0.0001,0.9999))

        ########### Init  ##########################################################
        var_levy = []
        for i in range(1000):
            var_levy.append(round(levyFlight(randF())))
        var_choice = random.choice

        # Initialize the nest
        nest = []
        for i in range(pop_size):
            expr = get_random_solution()
            cost = myproblem.get_cost(expr=expr, symbols=symbols)
            nest.append((expr, cost))

        # Sort nest
        nest.sort(key = itemgetter(1))


        # # 5 - Mutate the expression with 2 random mutations of active genes and print
        # ex.mutate_active(2)   log("Mutated expression:", ex(symbols)[0])
        # global best_egg, k, dic_front
        ls_trace = []

        ########### Main Loop  ####################################################
        for k in range(max_iter + 1):
            # Lay cuckoo eggs
            for i in range(n_cuckoo_eggs):
                idx         = random.randint(0,pop_size-1)
                egg         = deepcopy(nest[idx]) # Pick an egg at random from the nest
                cuckoo      = egg[0].mutate_active(var_choice(var_levy))
                if (cuckoo is not None):
                    cost_cuckoo = myproblem.get_cost(expr=cuckoo, symbols=symbols)
                    if (cost_cuckoo <= egg[1]): # Check if the cuckoo egg is better
                        nest[idx] = (cuckoo,cost_cuckoo)

            nest.sort(key = itemgetter(1)) # Sorting

            # Store ratioA for trace
            ls_trace.append(nest[0][1])

            for i in range(n_replace):
                expr = get_random_solution()
                nest[(pop_size-1)-(i)] = (expr, myproblem.get_cost(expr=expr, symbols=symbols))

            # Iterational printing
            if (k%print_after == 0):

                with open(log_file,'a') as f:
                    for x in ls_trace:
                        f.write(str(round(x, 3))+'\n')
                ls_trace = [] # dump and restart

                nest.sort(key = itemgetter(1)) # Rank nests and find current best
                best_egg  = deepcopy(nest[0])
                #best_cost = deepcopy(nest[1])
                log(f'\n#{k}', f'{best_egg[1]}')

                if print_best :
                    log(best_egg[0](symbols)[0])
                    #log(best_egg[0].simplify(symbols))
                    log('\n')

        expr = str(best_egg[0](symbols)[0])
        best_cost = best_egg[1]
        return best_cost, expr

    x =search()
    return x


def search_formulae_dcgpy_v1_parallel(myproblem=None, pars_dict:dict=None, verbose=False, npool=2 ):
    """Parallel run of search_formulae_dcgpy_v1
    Docs::

        from utilmy.optim import gp_searchformulae as gp
        myproblem1,p = gp.test_pars_values()
        gp.search_formulae_dcgpy_v1_parallel(myproblem=myproblem1, pars_dict=p, verbose=False, npool=3 )


        npool: 2 : Number of parallel runs
    """
    from utilmy.parallel import multiproc_run

    input_list = []
    for i in range(npool):
        p2 = copy.deepcopy(pars_dict)

        fsplit = p2['log_file'].split("/")
        fsplit[-1] = f'trace_{i}.log'
        fi         = "/".join(fsplit)
        p2['log_file'] = fi
        input_list.append(p2)


    ### parallel Run
    multiproc_run(_search_formulae_dcgpy_v1_wrapper,
                  input_fixed={"myproblem": myproblem, 'verbose':False},
                  input_list=input_list,
                  npool=npool)



def _search_formulae_dcgpy_v1_wrapper( pars_dict:dict=None, myproblem=None, verbose=False, ):
    """ Wrapper for parallel version, :
    Docs::

        1st argument should the list of parameters: inverse order
        pars_dict is a list --> pars_dict[0]: actual dict
    """
    search_formulae_dcgpy_v1(myproblem=myproblem, pars_dict=pars_dict[0], verbose=verbose, )



###############################################################################################
def search_formulae_dcgpy_v1_parallel_island(myproblem, ddict_ref
             , hyper_par_list   = ['pa',  ]  ### X[0],  X[1]
             , hyper_par_bounds = [ [0], [1.0 ] ]
             , pop_size=2
             , n_island=2
             , max_step=1
             , max_time_sec=100
             , dir_log="./logs/"
             ):
    """ Use PYGMO Island model + DCGPY for mutiple parallel Search of formulae
    Docs::

      from utilmy.optim import gp_searchformulae as gp
      myproblem1,p = gp.test_pars_values()
      # p ={}

      #### Run Search
      gp.search_formulae_dcgpy_v1_parallel_island(myproblem1, ddict_ref=p
                       ,hyper_par_list   = [ 'pa',  ]    ### X[0],  X[1]
                       ,hyper_par_bounds = [ [0], [ 0.6 ] ]
                       ,pop_size=6
                       ,n_island=2
                       ,dir_log="./logs/"
                      )

       https://esa.github.io/pygmo2/archipelago.html
       https://esa.github.io/pygmo2/tutorials/coding_udi.html


    """
    os.makedirs(dir_log, exist_ok=True)

    class meta_problem(object):
        def fitness(self,X):
            # ddict = {  'pa': X[0] }
            ddict = {  hyper_par_list[i]:  X[i] for i in range( len(X)) }

            ddict = {**ddict_ref, **ddict}
            (cost, expr) =  search_formulae_dcgpy_v1(myproblem, pars_dict=ddict, verbose=True)   ### Cost

            ss = str(cost) + "," + str(expr)
            #try :
            #  with open(dir_log + "/log.txt", mode='a') as fp:
            #    fp.write(ss)
            #except :
            #    print(ss)

            return [cost]   #### Put it as a list

        def get_bounds(self):
            return hyper_par_bounds
            #return ([0.0]*len(X),[1.0]*len(X))

    import pygmo as pg, time

    prob  = pg.problem( meta_problem() )
    algo  = pg.de(10)  ### Differentail DE
    archi = pg.archipelago(algo = algo, prob =prob , pop_size = pop_size, n= n_island)

    archi.evolve(max_step)

    t0 = time.time()
    isok= True
    while isok :
        # https://esa.github.io/pygmo2/archipelago.html#pygmo.archipelago.status
        #status = archi.status()
        #isok   = True if status not in 'idle' else False
        status = archi.status
        isok   = True if status != pg.evolve_status.idle else False
        if time.time()-t0 > max_time_sec :  isok=False
        time.sleep(30)
    # archi.wait_check()


    ##### Let us inspect the results
    fs = archi.get_champions_f()
    xs = archi.get_champions_x()
    print(fs, xs)

    with open(dir_log +"/result.txt", mode='a') as fp:
        fp.write( "cost_min," + str(fs))
        fp.write( "xmin," + str(xs))
    return fs, xs




###################################################################################################
def search_formulae_dcgpy_v3_custom(problem=None, pars_dict:dict=None, verbose=False, ):
    """ Search Optimal Formulae
    Docs::

        conda install  dcgpy

        nvars_in      = p.nvars_in  ### nb of variables
        nvars_out     = p.nvars_out
        operator_list = kernel_set(p.operators, ["sum", "diff", "div", "mul"] )

        ### Log
        print_after   = p.get('print_after', 20)
        print_best    = p.get('print_best', True)
        pop_size      = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)
        max_iter      = p.get('max_iter', 2) #100000  ## Max iterations
        seed          = p.get('seed', 43)
        log_file      = p.get('log_file', 'log.log') # 'trace.py'

        -- Add constraints in the functional space

        https://darioizzo.github.io/dcgp/notebooks/phenotype_correction_ex.html


    """
    ###https://darioizzo.github.io/dcgp/notebooks/finding_prime_integrals.html
    from lib2to3.pygram import Symbols
    #from dcgpy import expression_gdual_double as expression
    #from dcgpy import kernel_set_gdual_double as kernel_set
    #from pyaudi import gdual_double as gdual
    from dcgpy import expression_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    from pyaudi import gdual_vdouble as gdual

    import random
    from box import Box
    ######### Problem definition and Cost calculation


    #### Formulae GP Search params   #################
    p = Box(pars_dict)

    ### Problem
    nvars_in      = p.nvars_in  ### nb of variables
    nvars_out     = p.nvars_out
    operator_list = p.get('operators', ["sum", "mul", "div", "diff","sin","cos"])

    ### Log
    print_after   = p.get('print_after', 20)
    print_best    = p.get('print_best', True)
    pop_size      = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)
    max_iter      = p.get('max_iter', 2) #100000  ## Max iterations
    seed          = p.get('seed', 43)
    log_file      = p.get('log_file', 'log.log') # 'trace.py'

    ### search
    nexp            = p.get('nexp', 100) 
    offsprings      = p.get('offsprings',10)
    max_step        = p.get('stop', 2000)
    symbols         = p.get('symbols',['x0','x1','x2'])
    seed            = p.get('seed', 23)


    def run_experiment(max_step, offsprings, dCGP, symbols, verbose=False):
        """Run the Experiment in max_step
        Docs::
            max_step        : Maximum Generations
            offsprings      : Number of offsprings
            dCGP            : dCGP object : hold the formulae
            symbols   : list of variable as string


        """
        chromosome      = [1] * offsprings
        fitness         = [1] * offsprings
        best_chromosome = dCGP.get()
        best_fitness    = 1e10


        for kstep in range(max_step):
            for i in range(offsprings):
                check = 0
                while(check < 1e-3):
                    dCGP.set(best_chromosome)
                    dCGP.mutate_active(i+1) #  we mutate a number of increasingly higher active genes
                    fitness[i], check = problem.get_cost(dCGP, symbols)
                chromosome[i] = dCGP.get()

            for i in range(offsprings):
                if fitness[i] <= best_fitness:
                    if (fitness[i] != best_fitness) and verbose:
                        dCGP.set(chromosome[i])
                        print("New best found: gen: ", kstep, " value: ", fitness[i], " ", dCGP.simplify(symbols))
                    best_chromosome = chromosome[i]
                    best_fitness = fitness[i]
            if best_fitness < 1e-3:
                break

        dCGP.set(best_chromosome)
        return kstep, dCGP


    def search():
        # Search for best possible solution using Genetic Algorithm

        kernels_new = kernel_set(operator_list)()
        # dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2, kernels=kernels_new, seed = seed)

        #  nexp experiments to accumulate statistic
        result = []
        print("restart: \t gen: \t expr1: \t expr2")
        for i in range(nexp):
            dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2, kernels=kernels_new, seed = random.randint(0,234213213))
            kstep, dCGP = run_experiment(max_step=max_step, offsprings=10, dCGP=dCGP, symbols=symbols, verbose=False)
            # res.append(kstep)
            # print("g ",g)
            if kstep < (max_step-1):
                form1 = dCGP(symbols)
                form2 = dCGP.simplify(symbols)
                print(i, "\t\t", kstep, "\t", form1, "   \t ", form2)

                result.append(form2)
        # res = np.array(res)
        # print(one_sol.simplify(symbols))
        return result

    res = search()
    return res



####################################################################################################
def search_formulae_operon_v1(myproblem=None, pars_dict:dict=None, verbose=False, ):
    """ Search Optimal Formulae
    Docs::

        -- Install  OPERON
        https://github.com/heal-research/pyoperon

        https://github.com/heal-research/pyoperon/blob/main/example/operon-bindings.py

        https://github.com/heal-research/pyoperon/blob/cpp20/example/operon-bindings.py



    """
    ######### Problem definition and Cost calculation
    #myproblem = myProblem()


    #### Formulae GP Search params   #################
    log(pars_dict)
    p = Box(pars_dict)


    import random, time, sys, os, json
    import numpy as np
    import pandas as pd
    from scipy import stats

    import operon as Operon
    from pmlb import fetch_data

    # get some training data - see https://epistasislab.github.io/pmlb/
    D = fetch_data('1027_ESL', return_X_y=False, local_cache_dir='./datasets').to_numpy()

    # initialize a dataset from a numpy array
    ds             = Operon.Dataset(D)

    # define the training and test ranges
    training_range = Operon.Range(0, ds.Rows // 2)
    test_range     = Operon.Range(ds.Rows // 2, ds.Rows)

    # define the regression target
    target         = ds.Variables[-1] # take the last column in the dataset as the target

    # take all other variables as inputs
    inputs         = Operon.VariableCollection(v for v in ds.Variables if v.Name != target.Name)

    # initialize a rng
    rng            = Operon.RomuTrio(random.randint(1, 1000000))

    # initialize a problem object which encapsulates the data, input, target and training/test ranges
    problem        = Operon.Problem(ds, inputs, target.Name, training_range, test_range)

    # initialize an algorithm configuration
    config         = Operon.GeneticAlgorithmConfig(generations=1000, max_evaluations=1000000, local_iterations=0, population_size=1000, pool_size=1000, p_crossover=1.0, p_mutation=0.25, epsilon=1e-5, seed=1, time_limit=86400)

    # use tournament selection with a group size of 5
    # we are doing single-objective optimization so the objective index is 0
    selector       = Operon.TournamentSelector(objective_index=0)
    selector.TournamentSize = 5

    # initialize the primitive set (add, sub, mul, div, exp, log, sin, cos), constants and variables are implicitly added
    pset           = Operon.PrimitiveSet()
    pset.SetConfig(Operon.PrimitiveSet.Arithmetic | Operon.NodeType.Exp | Operon.NodeType.Log | Operon.NodeType.Sin | Operon.NodeType.Cos)

    # define tree length and depth limits
    minL, maxL     = 1, 50
    maxD           = 10

    # define a tree creator (responsible for producing trees of given lengths)
    btc            = Operon.BalancedTreeCreator(pset, inputs, bias=0.0)
    tree_initializer = Operon.UniformLengthTreeInitializer(btc)
    tree_initializer.ParameterizeDistribution(minL, maxL)
    tree_initializer.MaxDepth = maxD

    # define a coefficient initializer (this will initialize the coefficients in the tree)
    coeff_initializer = Operon.NormalCoefficientInitializer()
    coeff_initializer.ParameterizeDistribution(0, 1)

    # define several kinds of mutation
    mut_onepoint   = Operon.NormalOnePointMutation()
    mut_changeVar  = Operon.ChangeVariableMutation(inputs)
    mut_changeFunc = Operon.ChangeFunctionMutation(pset)
    mut_replace    = Operon.ReplaceSubtreeMutation(btc, coeff_initializer, maxD, maxL)

    # use a multi-mutation operator to apply them at random
    mutation       = Operon.MultiMutation()
    mutation.Add(mut_onepoint, 1)
    mutation.Add(mut_changeVar, 1)
    mutation.Add(mut_changeFunc, 1)
    mutation.Add(mut_replace, 1)

    # define crossover
    crossover_internal_probability = 0.9 # probability to pick an internal node as a cut point
    crossover      = Operon.SubtreeCrossover(crossover_internal_probability, maxD, maxL)

    # define fitness evaluation
    interpreter    = Operon.Interpreter() # tree interpreter
    error_metric   = Operon.R2()          # use the coefficient of determination as fitness
    evaluator      = Operon.Evaluator(problem, interpreter, error_metric, True) # initialize evaluator, use linear scaling = True
    evaluator.Budget = 1000 * 1000             # computational budget
    evaluator.LocalOptimizationIterations = 0  # number of local optimization iterations (coefficient tuning using gradient descent)

    # define how new offspring are created
    generator      = Operon.BasicOffspringGenerator(evaluator, crossover, mutation, selector, selector)

    # define how the offspring are merged back into the population - here we replace the worst parents with the best offspring
    reinserter     = Operon.ReplaceWorstReinserter(objective_index=0)
    gp             = Operon.GeneticProgrammingAlgorithm(problem, config, tree_initializer, coeff_initializer, generator, reinserter)

    # report some progress
    gen = 0
    max_ticks = 50
    interval = 1 if config.Generations < max_ticks else int(np.round(config.Generations / max_ticks, 0))
    t0 = time.time()

    def report():
        global gen
        best = gp.BestModel()
        bestfit = best.GetFitness(0)
        sys.stdout.write('\r')
        cursor = int(np.round(gen / config.Generations * max_ticks))
        for i in range(cursor):
            sys.stdout.write('\u2588')
        sys.stdout.write(' ' * (max_ticks-cursor))
        sys.stdout.write(f'{100 * gen/config.Generations:.1f}%, generation {gen}/{config.Generations}, train quality: {-bestfit:.6f}, elapsed: {time.time()-t0:.2f}s')
        sys.stdout.flush()
        gen += 1

    # run the algorithm
    gp.Run(rng, report, threads=16)

    # get the best solution and print it
    best = gp.BestModel()
    model_string = Operon.InfixFormatter.Format(best.Genotype, ds, 6)
    print(f'\n{model_string}')







###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()

