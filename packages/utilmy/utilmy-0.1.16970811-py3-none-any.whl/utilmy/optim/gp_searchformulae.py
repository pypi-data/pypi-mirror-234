""" Search  mathematical Formulae using Genetic Algorithm , Genetic Programming


Docs::

    Install  DCGP

          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire utilmy sympy

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
            import utilmy.optim.gp_formulaesearch as gp
            from numpy import (sin, cos, log, exp, sqrt )

            ## 1) Define Problem Class with get_cost methods
                myproblem1 = myProblem()
                ## myproblem1.get_cost(formulae_str, symbols  )

                ## 2) Param Search
                p               = Box({})
                ...


            ## 3) Run Search
            gp.search_formulae_algo1(myproblem1, pars_dict=p, verbose=1)


            #### Parallel version   ------------------------------------
            gp.search_formulae_dcgpy_v1_parallel(myproblem=myproblem1, pars_dict=p, verbose=1, npool=3 )


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



####################################################################################################
def test_all():
    """function test_all
    """
    test1()
    test2()
    test3()
    test4_newton()
    test5()
    test6()
    test7()

    test1_parallel()
    test1_parallel2()
    test1_parallel_island()



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
    myproblem1 = myProblem2()

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

def test1():
    """Test search_formulae_dcgpy_v1
    """
    myproblem       = myProblem2()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff","sin"]
    p.symbols       = ["x0","x1"]

    p.n_exp         = 4
    p.max_step      = 1000  ## per expriemnet
    p.offsprings    = 20

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662799885.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings



    #### Run Search
    res = search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

def test2():
    """Test search_formulae_dcgpy_v1
    """
    myproblem       = myProblem1()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff","sin","cos"]
    p.symbols       = ["x0","x1"]

    p.max_step      = 5
    p.n_exp         = 5
    p.offsprings    = 10

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662800328.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings


    #### Run Search
    res = search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

def test3():
    """Test search_formulae_dcgpy_v1
    """
    from box import Box
    myproblem       = myProblem5()

    p               = Box({})
    p.log_file      = 'trace4.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 2  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul","pdiv"]
    p.symbols       = ["x0","x1"]

    p.max_step      = 5
    p.n_exp         = 1
    p.offsprings    = 10
    p.n_eph         = 3
    p.verbose       = 1


    #### Run Search
    res = search_formulae_dcgpy_Xy_regression_v1(myproblem, pars_dict=p, verbose=1)

def test4_newton(x=5):
    """Test search_formulae_dcgpy_newton with 3 variables
    Docs::

        cd  myuutil/utilmy/optim
        python  gp_searchformulae.py  test4  --x 10     ### pip install fire 



    """
    

    myproblem       = myProblem6()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff"]
    p.symbols       = ["x0","x1","x2"]

    p.n_exp         = 10
    p.max_step      = 500  ## per expriemnet
    p.offsprings    = 20
    p.n_eph         = 1

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662743807.pickle" # path
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings

    #### Run Search
    res = search_formulae_dcgpy_newton(myproblem, pars_dict=p, verbose=1)


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
    res = search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

def test6():
    """Test the myProblem4 class,

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

    p.n_exp         = 1
    p.max_iter      = 5
    p.offsprings    = 10
    search_formulae_dcgpy_v1(problem = myproblem, pars_dict=p, verbose=False, )


def test7():
    """Test the myProblem3 class,

    """
    myproblem       = myProblem3()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff","sin","cos"]
    p.symbols       = ["theta","omega","c"]

    p.n_exp         = 1
    p.max_iter      = 5
    p.offsprings    = 10


    search_formulae_dcgpy_v1(problem = myproblem, pars_dict=p, verbose=False, )

def test8(): 
    """Test the myProblem7 class,

    """
    myproblem       = myProblem7()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "diff"]
    p.symbols       = ["x0", "x1", "x2"]

    p.n_exp         = 20
    p.max_step      = 1000
    p.offsprings    = 10

    search_formulae_dcgpy_v1(problem = myproblem, pars_dict=p, verbose=1)

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
    res = search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

def test1_parallel():
    """Test of search_formulae_dcgpy_v1_parallel
    """
    myproblem1,p = test_pars_values()

    search_formulae_dcgpy_v1_parallel(myproblem=myproblem1, pars_dict=p, verbose=False, npool=3 )


def test1_parallel2():
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


def test1_parallel_island():
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




###################################################################################################
class myProblem1:
    def __init__(self,n_sample = 5,kk = 1.0,nsize = 100,):
        """  Define the problem and cost calculation using formulae_str
        Docs::


            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

        """
        import numpy as np
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
        #yt is the true expression
        yt = np.cos(self.x1)/self.x1 + self.x0*self.x1 + self.x1
        x0 = self.x0  
        x1 = self.x1
        y = eval(expr(symbols)[0])
        err = yt-y
        check = 3
        return sum(err*err), check


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
        import numpy as np
        x0 = np.random.random(50)*10 - 5.0
        x1 = np.random.random(50)*10 - 5.0

        self.x0 = x0
        self.x1 = x1
        self.ytrue =  np.sin(x1 * x0) + x0**2 + x1*x0  #This is the true expression


    def get_cost(self, expr, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """

        x0 = self.x0
        x1 = self.x1

        y     = eval(expr(symbols)[0])
        cost  = np.sum((self.ytrue-y)**2)

        check = 3
        return cost, check


class myProblem3:
    def __init__(self):
        pass

    def get_cost(self, dCGP, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        from random import random
        from dcgpy import kernel_set_gdual_vdouble as kernel_set
        from dcgpy import expression_gdual_vdouble as expression
        from pyaudi import gdual_vdouble as gdual
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


class myProblem5:
    def __init__(self):
        """  Define the problem and cost calculation using formulae_str
        Docs::


            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

        """
        pass

    def get_data(self):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """

        #Insert your data here 
        X = np.linspace(0,15, 100)
        Y = X * ((X**3) - 18 * X + 32) / 32
        Y[X>2] = 1. / X[X>2]**2
        X = np.reshape(X, (100,1))
        Y = np.reshape(Y, (100,1))
        return X,Y


class myProblem6:
    def __init__(self):
        """  Define the problem and cost calculation using formulae_str
        Docs::


            myProblem.get_cost(   )

            ---- My Problem
            2)  list with scores (ie randomly generated)
            We use 1 formulae to merge  2 list --> merge_list with score
               Ojective to maximize  correlation(merge_list,  True_ordered_list)

        """
        from pyaudi import gdual_vdouble as gdual

        # x = np.linspace(1,3,10)

        # ### Formulae Space
        # x = gdual(x)
        # yt =  x**5 - np.pi*x**3 + 2*x
        x0 = np.random.random(1000)
        x1 = np.random.random(1000)
        x2 = np.random.random(1000)
        x0 = gdual(x0)
        x1 = gdual(x1)
        x2 = gdual(x2)

        ### target function
        yt =  3*x0*x1 - np.pi*x1 + np.pi**2 *x2

        self.x  = [x0,x1,x2]
        self.yt = yt

    def get_data_symbolic(self):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        #Insert your data here
        return self.x


    def get_cost_symbolic(self,dCGP):
        """  should pass the symbolic function DCGP 
            and retur the cost.

        """
        #y    = dCGP([self.x])[0]
        y    = dCGP([self.x[0],self.x[1],self.x[2]])[0]
        cost = (y-self.yt)**2
        return cost


class myProblem7:
    def __init__(self):
        """  Define the problem and cost calculation using formulae_str
        Docs::


            myProblem.get_cost(   )

            ---- My Problem
            Finding PID values of a controller function. Given true values of 
            controller, calculate Kp, Kd and Ki values for the PID controller.
            Here true values are calculated using some specific PID values.  
            In real life true values could be values from manual control. 
        """
        import numpy as np
        x0 = np.random.random(50) # errors of the controller
        x0 = -np.sort(-x0) # it is more sensible if they are descending
        x1 = [0] + [(x - px) for (x, px) in zip(x0[1:], x0[:-1])] # derivatives of errors
        x1 = np.array(x1) 
        x2 = [np.sum(x0[:i + 1]) for i in range(len(x0))] # integral of errors
        x2 = np.array(x2)

        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        Kp, Kd, Ki = 0.1, 0.01, 0.5
        self.ytrue = Kp * x0 + Kd * x1 + Ki * x2  #This is the true value of controller output.


    def get_cost(self, dCGP, symbols):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            dCGP            : dCGP expression whose cost has to be minimized
            symbols         : Symbols

        """
        #These needs to be defined to be used in eval function. 
        x0 = self.x0
        x1 = self.x1
        x2 = self.x2
        y     = eval(dCGP(symbols)[0])
        cost  = np.sum((self.ytrue-y)**2)

        check = 3
        return cost, check


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
            s1 =  eval(formulae_str)

            x0 = rlist2[i]
            x1 = rlist[i]
            s2 =  eval(formulae_str)
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
        costSimple = len(formulae_str) * 0.003
        for i in range(2): 
            x0 = l1[i]
            x1 = l2[i]
            try:
                s1 = eval(formulae_str)
            except:
                s1 = 10000

            x0 = l2[i]
            x1 = l1[i]
            try:
                s2 = eval(formulae_str)
            except:
                s2 = 10000
            diff += abs(s1 - s2)
        if diff > 0.1: 
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
def search_formulae_dcgpy_v1(problem=None, pars_dict:dict=None, verbose=1, ):
    """ Search Optimal Formulae
    Docs::

        -- Install
          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire utilmy sympy

          python -c "from dcgpy import test; test.run_test_suite(); import pygmo; pygmo.mp_island.shutdown_pool(); pygmo.mp_bfe.shutdown_pool()"


          https://darioizzo.github.io/dcgp/installation.html#python

          https://darioizzo.github.io/dcgp/notebooks/real_world1.html


        -- Usagge
            import utilmy.optim.gp_formulaesearch as gp
            from numpy import (sin, cos, log, exp, sqrt )

            -- 1) Define Problem Class with get_cost methods
                myproblem       = gp.myProblem2()

                p               = Box({})
                p.log_file      = 'trace.log'
                p.print_after   = 5
                p.print_best    = True


                p.nvars_in      = 2  ### nb of variables
                p.nvars_out     = 1
                p.operators     = ["sum", "mul", "div", "diff","sin"]
                p.symbols       = ["x0","x1"]

                p.n_exp         = 4
                p.max_step      = 1000  ## per expriemnet
                p.offsprings    = 20
                p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

                #### Re-use old problem setting
                p.load_old_weights  = "ztmp/dcpy_weight_1662799885.pickle" # path
                p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings


                --- Run Search
                res = gp.search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

                --- Parallel version
                gp.search_formulae_dcgpy_v1_parallel(myproblem=myproblem, pars_dict=p, verbose=1, npool=3 )




            --  Custom Problem

                class myProblem2:
                    def __init__(self,n_sample = 5,kk = 1.0,nsize = 100,):
                        x0 = np.random.random(50)*10 - 5.0
                        x1 = np.random.random(50)*10 - 5.0

                        self.x0 = x0
                        self.x1 = x1
                        self.ytrue =  np.sin(x1 * x0) + x0**2 + x1*x0  #This is the true expression


                    def get_cost(self, expr, symbols):
                        x0,x1 = self.x0, self.x1

                        ### Eval New Formulae
                        y     =  eval(expr(symbols)[0])
                        cost  =  np.sum((self.ytrue-y)**2)

                        check = 3
                        return cost, check


        -- Add constraints in the functional space

            https://darioizzo.github.io/dcgp/notebooks/phenotype_correction_ex.html
            https://darioizzo.github.io/dcgp/notebooks/finding_prime_integrals.html


    """
    from lib2to3.pygram import Symbols
    from dcgpy import expression_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    from pyaudi import gdual_vdouble as gdual
    import random, pandas as pd
    from box import Box
    import pickle
    ######### Problem definition and Cost calculation


    #### Formulae GP Search params   #################
    p = Box(pars_dict)

    ### Problem
    nvars_in      = p.nvars_in  ### nb of variables
    nvars_out     = p.nvars_out
    operator_list = p.get('operators', ["sum", "mul", "div", "diff","sin","cos"])
    symbols       = p.get('symbols',['x0','x1','x2'])
    n_constant = 0 ## nb of constant to determine

    ### Log
    log_file      = p.get('log_file', 'log.log') # 'trace.py'


    ### search
    n_exp           = p.get('n_exp', 1)
    max_step        = p.get('max_step', 10)

    offsprings      = p.get('offsprings',10)
    pop_size        = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)

    seed            = p.get('seed', 23)
    load_old_weights    = p.get('load_old_weights', None)
    frac_old            = p.get('frac_old',0.1)
    save_new_weights    = p.get('save_new_weights', None)


    ### search DCGPY Algo

    from utilmy import os_makedirs
    os_makedirs(log_file)
    def print_file(*s,):
        ss = "\t".join([str(x) for x in  s])
        if verbose>0 : print(ss, flush=True)
        with open(log_file, mode='a') as fp :
            fp.write(ss +"\n")

    def load_save(path, mode='load', ddict:dict=None):

       if mode=='load':
            with open( path, 'rb') as handle:
                ddict = pickle.load(handle)
            ddict = Box(ddict)
            return ddict.best_weights, ddict.best_chromosome, ddict.best_fitness

       elif mode =='save' and path is not None:
                os_makedirs(path)
                with open(  path , 'wb') as handle:
                    pickle.dump(ddict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                llog('Saved', path )

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


                ##### Check is always=3,  Check documentation in DCGPY to remove it, a bit usless
                ##### 
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
                    best_weights = [0] 
            if best_fitness < 1e-3:
                break

        #### Already done in the loop, can be remove MAYBE. check from DCPGY  
        dCGP.set(best_chromosome)        
        return kstep, dCGP, best_fitness,best_weights,best_chromosome


    def search():
        """ Search for best possible solution using Genetic Algorithm
        Docs::

            classdcgpy.expression_double(inputs, outputs, rows, cols, levels_back, arity = 2, kernels, n_eph = 0, seed = randint)
            A CGP expression
            https://darioizzo.github.io/dcgp/docs/python/expression.html


        """

        kernels_new = kernel_set(operator_list)()
        isweight_ok = False


        if load_old_weights is not None:
            try:
                llog("Data loaded")
                loaded_weights, loaded_chromosome, loaded_fitness= load_save(path=load_old_weights, mode='load')

                ###  Check if works
                dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                    kernels=kernels_new,  seed = random.randint(0,234213213))
                dCGP.set(loaded_chromosome)
                llog("Old saved result is:")
                llog(dCGP.simplify(in_sym = symbols))
                isweight_ok = True

            except Exception as e:
                llog(e)
                llog("Error in loading old data, so creating expressions from scratch")
                isweight_ok = False

        #  n_exp experiments to accumulate statistic
        result = []
        if verbose>0:
            print_file( 'id_exp', 'niter', 'cost', 'formulae', )


        #Check results for new iterations
        for i in range(n_exp):
            dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                kernels=kernels_new,
                                seed = random.randint(0,234213213))

            ### Previous weights
            if ((load_old_weights is not None) & (i<=int(frac_old*n_exp)) & (isweight_ok)):
                dCGP.set(        loaded_chromosome)

            ### Get results
            kstep, dCGP, best_fitness,best_weights,best_chromosome = run_experiment(max_step=max_step, offsprings=10,
                                                                                    dCGP=dCGP, symbols=symbols,
                                                                                    verbose=False)


            form2 = dCGP.simplify(symbols)[0]
            result.append( ( i, kstep , best_fitness, form2   ) )

            if   verbose >=2 :
                form1 = dCGP(symbols)[0]
                print_file(i, kstep,  form1,  form2)

            elif verbose >=1 : print_file(i, kstep, form2, best_fitness)

        ##### Save Best: If the result is previous result then only save new results
        if load_old_weights is not None  and isweight_ok :
            if best_fitness > loaded_fitness:
                best_fitness    = loaded_fitness
                best_weights    = loaded_weights
                best_chromosome = loaded_chromosome

        ddict = {"best_chromosome":best_chromosome,"best_weights":list(np.array(best_weights)),"best_fitness":best_fitness}
        load_save(path=save_new_weights, mode='save', ddict=ddict)


        result = pd.DataFrame(result,  columns=['id_exp', 'niter', 'cost', 'formulae',   ])
        result = result.sort_values('cost', ascending=1)
        return result

    res = search()
    llog('Best\n',)
    llog( res.iloc[:2,:] )
    return res



############ Parallel version #################################################################
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
    search_formulae_dcgpy_v1(problem=myproblem, pars_dict=pars_dict[0], verbose=verbose, )




def search_formulae_dcgpy_v1_parallel_island(myproblem, ddict_ref
             , hyper_par_list   = ['pa',  ]  ### X[0],  X[1]
             , hyper_par_bounds = [ [0,0], [1.0,1.0 ] ]
             , pop_size=2
             , n_island=2
             , max_step=1
             , max_time_sec=100
             , dir_log="./logs/"
             , verbose=0
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
            df =  search_formulae_dcgpy_v1(myproblem, pars_dict=ddict_ref, verbose=verbose)   ### Cost

            cost = df['cost'].values[0]         #We select the1st  element and its cost
            expr = df['formulae'].values[0]
            print(expr)
            return [cost]   #### Put it as a list

        def get_bounds(self):
            return hyper_par_bounds

    import pygmo as pg, time

    prob  = pg.problem( meta_problem() )
    algo  = pg.de(10)  ### Differentail DE
    archi = pg.archipelago(algo = algo, prob = prob , pop_size = pop_size, n= n_island)

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




################################NEWTON VERSION#############################################
def search_formulae_dcgpy_newton(problem=None, pars_dict:dict=None, verbose=1, ):
    """ Search Optimal Formulae with constants using Newton Formulae
    Helps to obtain expression of equations with constants terms
    Docs::

        -- Install
          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire utilmy sympy

          python -c "from dcgpy import test; test.run_test_suite(); import pygmo; pygmo.mp_island.shutdown_pool(); pygmo.mp_bfe.shutdown_pool()"


          https://darioizzo.github.io/dcgp/installation.html#python

          https://darioizzo.github.io/dcgp/notebooks/real_world1.html


        -- Usagge
            import utilmy.optim.gp_formulaesearch as gp
            from numpy import (sin, cos, log, exp, sqrt )

            -- 1) Define Problem Class with get_cost methods
                myproblem       = myProblem6()

                p                       = Box({})
                p.log_file              = 'trace.log'
                p.print_after           = 5
                p.print_best            = True


                p.nvars_in               = 3  ### nb of variables
                p.nvars_out              = 1
                p.operators              = ["sum", "mul", "div", "diff"]
                p.symbols                = ["x0","x1","x2"]

                p.n_exp                  = 20     ## Number of experiments
                p.max_step               = 5000  ## per expriment
                p.offsprings             = 20
                p.n_eph                  = 1
                p.load_old_weights       = False
                p.frac_old               = 0.05   ##Fraction of chromosomes to be used from old learnings
                p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

                #### Re-use old problem setting
                p.load_old_weights  = "ztmp/dcpy_weight_1662743807.pickle" # path to saved pickle file
                p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings
                
                #### Run Search
                res = gp.search_formulae_dcgpy_newton(myproblem, pars_dict=p, verbose=1)



            --  Custom Problem

                    class myProblem6:
                        def __init__(self):
                            from pyaudi import gdual_vdouble as gdual
                            ##### Formulae Space
                            x0 = np.random.random(1000)
                            x1 = np.random.random(1000)
                            x2 = np.random.random(1000)
                            x0 = gdual(x0)
                            x1 = gdual(x1)
                            x2 = gdual(x2)
                            yt =  3*x0*x1 - np.pi*x1 + 2*x2
                            self.x  = [x0,x1,x2] ##Add all x0,x1,.. values in the self.x
                            self.yt = yt

                        def get_data_symbolic(self):

                            #Insert your data here
                            return self.x

                        def get_cost_symbolic(self,dCGP):
                            #y    = dCGP([self.x])[0]
                            y    = dCGP([self.x[0],self.x[1],self.x[2]])[0]
                            cost = (y-self.yt)**2
                            return cost


        -- Add constraints in the functional space

            https://darioizzo.github.io/dcgp/notebooks/phenotype_correction_ex.html
            https://darioizzo.github.io/dcgp/notebooks/finding_prime_integrals.html
            http://darioizzo.github.io/dcgp/notebooks/weighted_symbolic_regression.html
            

    """
    from pyaudi import gdual_vdouble as gdual
    from dcgpy import expression_weighted_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    import random, pandas as pd
    from box import Box
    import pyaudi 
    import pickle 
    from utilmy.utilmy_base import log as llog, log2 ### Conflicting with numpy.log


    #### Formulae GP Search params   #################
    p = Box(pars_dict)

    ### Problem
    nvars_in      = p.nvars_in  ### nb of variables
    nvars_out     = p.nvars_out
    operator_list = p.get('operators', ["sum", "mul", "div", "diff","sin","cos"])
    symbols       = p.get('symbols',['x0','x1'])
    n_constant = 0 ## nb of constant to determine

    ### Log
    log_file      = p.get('log_file', 'log.log') # 'trace.py'


    ### search
    n_exp               = p.get('n_exp', 1)
    max_step            = p.get('max_step', 10)

    offsprings          = p.get('offsprings',10)
    pop_size            = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)

    seed                = p.get('seed', 23)
    n_eph               = p.get('n_eph',0)
    load_old_weights    = p.get('load_old_weights', None)
    frac_old            = p.get('frac_old',0.1)
    save_new_weights    = p.get('save_new_weights', None)


    ### search DCGPY Algo    ########################################################
    from utilmy import os_makedirs
    os_makedirs(log_file)
    def print_file(*s,):
        ss = "\t".join([str(x) for x in  s])
        if verbose>0 : print(ss, flush=True)
        with open(log_file, mode='a') as fp :
            fp.write(ss +"\n")
    
    def collapse_vectorized_coefficient(x, N):
        if len(x) == N:
            return sum(x)
        return x[0] * N

    def newton(ex, f, xsym, p):
        n = ex.get_n()
        r = ex.get_rows()
        c = ex.get_cols()
        a = ex.get_arity()[0]
        v = np.zeros(r * c * a)
        # random initialization of weights
        w=[]
        for i in range(r*c):
            for j in range(a):
                w.append(gdual([np.random.normal(0,1)]))
        ex.set_weights(w)
        wi = ex.get_weights()

        # get active weights
        an = ex.get_active_nodes()
        is_active = [False] * (n + r * c) # bool vector of active nodes
        for k in range(len(an)):
            is_active[an[k]] = True
        aw=[] # list of active weights
        for k in range(len(an)):
            if an[k] >= n:
                for l in range(a):
                    aw.append([an[k], l]) # pair node/ingoing connection
        if len(aw)<2:
            return

        for i in range(p['steps']):
            w = ex.get_weights() # initial weights

            # random choice of the weights w.r.t. which we'll minimize the error
            num_vars = np.random.randint(2, min(3, len(aw)) + 1) # number of weights (2 or 3)
            awidx = np.random.choice(len(aw), num_vars, replace = False) # indexes of chosen weights
            ss = [] # symbols
            for j in range(len(awidx)):
                ss.append("w" + str(aw[awidx[j]][0]) + "_" + str(aw[awidx[j]][1]))
                idx = (aw[awidx[j]][0] - n) * a + aw[awidx[j]][1]
                w[idx] = gdual(w[idx].constant_cf, ss[j], 2)
            ex.set_weights(w)

            # compute the error
            E = f(ex)
            Ei = sum(E.constant_cf)

            # get gradient and Hessian
            dw = np.zeros(len(ss))
            H = np.zeros((len(ss),len(ss)))
            for k in range(len(ss)):
                #print(len(xsym1[0].constant_cf))
                try:
                    #len(xsym[0].constant_cf)) gives error when n_eph = 1
                    dw[k] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 1}), len(xsym[0].constant_cf))
                    H[k][k] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 2}), len(xsym[0].constant_cf))
                    for l in range(k):
                        H[k][l] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 1, "d"+ss[l]: 1}), len(xsym[0].constant_cf))
                        H[l][k] = H[k][l]
                except:
                    dw[k] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 1}), len(xsym.constant_cf))
                    H[k][k] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 2}), len(xsym.constant_cf))
                    for l in range(k):
                        H[k][l] = collapse_vectorized_coefficient(E.get_derivative({"d"+ss[k]: 1, "d"+ss[l]: 1}), len(xsym.constant_cf))
                        H[l][k] = H[k][l]

            det = np.linalg.det(H)
            if det == 0: # if H is singular
                continue

            # compute the updates
            updates = - np.linalg.inv(H) @ dw

            # update the weights
            for k in range(len(updates)):
                idx = (aw[awidx[k]][0] - n) * a + aw[awidx[k]][1]
                ex.set_weight(aw[awidx[k]][0], aw[awidx[k]][1], w[idx] + updates[k])
            wfe = ex.get_weights()
            for j in range(len(awidx)):
                idx = (aw[awidx[j]][0] - n) * a + aw[awidx[j]][1]
                wfe[idx] = gdual(wfe[idx].constant_cf)
            ex.set_weights(wfe)

            # if error increased restore the initial weights
            Ef = sum(f(ex).constant_cf)
            if not Ef < Ei:
                for j in range(len(awidx)):
                    idx = (aw[awidx[j]][0] - n) * a + aw[awidx[j]][1]
                    w[idx] = gdual(w[idx].constant_cf)
                ex.set_weights(w)

    # Quadratic error of a dCGP expression. The error is computed over the input points xin (of type gdual, order 0 as
    # we are not interested in expanding the program w.r.t. these). The target values are contained in yt (of type gdual,
    # order 0 as we are not interested in expanding the program w.r.t. these)


    def load_save(path, mode='load', ddict:dict=None):

       if mode=='load':
            with open( path, 'rb') as handle:
                ddict = pickle.load(handle)
            ddict = Box(ddict)
            return ddict.best_weights, ddict.best_chromosome, ddict.best_fitness

       elif mode =='save' and path is not None:
                os_makedirs(path)
                with open(  path , 'wb') as handle:
                    pickle.dump(ddict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                llog('Saved', path )


    def run_experiment(problem, max_step, offsprings, dCGP, symbols,newtonParams, verbose=False):
        """Run the Experiment in max_step
        Docs::
            max_step        : Maximum Generations
            offsprings      : Number of offsprings
            dCGP            : dCGP object : hold the formulae
            symbols   : list of variable as string


        """
        chromosome      = [1] * offsprings
        fitness         = [1] * offsprings
        weights         = [1] * offsprings
        best_chromosome = dCGP.get()
        best_fitness    = 1e10
        best_weights = dCGP.get_weights()
        best_fitness = sum(problem.get_cost_symbolic(dCGP).constant_cf)

        for kstep in range(max_step):
            for i in range(offsprings):
                dCGP.set(best_chromosome)
                dCGP.mutate_active(i+1) #  we mutate a number of increasingly higher active genes


                xsym  = problem.get_data_symbolic()     ####
                newton(dCGP, problem.get_cost_symbolic, xsym=xsym, p= newtonParams)


                costsym = problem.get_cost_symbolic(dCGP)
                fitness[i]    = sum(costsym.constant_cf)
                chromosome[i] = dCGP.get()
                weights[i]    = dCGP.get_weights()

            for i in range(offsprings):
                if fitness[i] <= best_fitness:
                    if (fitness[i] != best_fitness) and verbose:
                        dCGP.set(chromosome[i])
                        print("New best found: gen: ", kstep, " value: ", fitness[i], " ", dCGP.simplify())
                    best_chromosome = chromosome[i]
                    best_fitness = fitness[i]
                    best_weights = weights[i]
            if best_fitness < 1e-3:
                break

        dCGP.set(best_chromosome)
        return kstep, dCGP, best_fitness,best_weights,best_chromosome


    def search():
        """ Search for best possible solution using Genetic Algorithm
        Docs::

            classdcgpy.expression_double(inputs, outputs, rows, cols, levels_back, arity = 2, kernels, n_eph = 0, seed = randint)
            A CGP expression
            https://darioizzo.github.io/dcgp/docs/python/expression.html


        """

        kernels_new = kernel_set(operator_list)()
        newtonParams = {'steps': 100,}
        isweight_ok = False
        if load_old_weights is not None:
            try:
                llog("Data loaded")
                loaded_weights, loaded_chromosome, loaded_fitness= load_save(path=load_old_weights, mode='load')

                ###  Check if works
                dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                    kernels=kernels_new,  seed = random.randint(0,234213213))
                dCGP.set_weights(loaded_weights)
                dCGP.set(loaded_chromosome)
                llog("Old saved result is:")
                llog(dCGP.simplify(in_sym = symbols,subs_weights=True))
                isweight_ok = True

            except Exception as e:
                llog(e)
                llog("Error in loading old data, so creating expressions from scratch")
                isweight_ok = False

        #  n_exp experiments to accumulate statistic
        result = []
        if verbose>0:
            print_file( 'id_exp', 'niter', 'weights', 'formulae', )


        #Check results for new iterations
        for i in range(n_exp):
            dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                kernels=kernels_new,
                                seed = random.randint(0,234213213))

            ### Previous weights
            if ((load_old_weights is not None) & (i<=int(frac_old*n_exp)) & (isweight_ok)):
                dCGP.set_weights(loaded_weights)
                dCGP.set(        loaded_chromosome)


            ### Constant setup
            for j in range(dCGP.get_n(), dCGP.get_n() + dCGP.get_rows() * dCGP.get_cols()):
                for k in range(dCGP.get_arity()[0]):
                    dCGP.set_weight(j, k, gdual([np.random.normal(0,1)]))


            ### Get results
            kstep, dCGP, best_fitness,best_weights,best_chromosome = run_experiment(problem=problem,max_step=max_step, offsprings=10,
                                                                                    dCGP=dCGP, symbols=symbols,
                                                                                    newtonParams= newtonParams, verbose=False)

            form2 = dCGP.simplify(symbols,True)
            result.append((i, kstep , best_fitness, form2))

            if  verbose >=2 :
                form1 = dCGP(symbols,True)
                print_file(i, kstep,  form1,  form2)

            elif verbose >=1 : print_file(i, kstep, best_fitness,form2)



        ##### Save Best: If the result is previous result then only save new results
        if load_old_weights is not None  and isweight_ok :
            if best_fitness > loaded_fitness:
                best_fitness    = loaded_fitness
                best_weights    = loaded_weights
                best_chromosome = loaded_chromosome

        ddict = {"best_chromosome":best_chromosome,"best_weights":list(np.array(best_weights)),"best_fitness":best_fitness}
        load_save(path=save_new_weights, mode='save', ddict=ddict)



        ##### Store thre results in a dataframe
        result = pd.DataFrame(result,  columns=['id_exp', 'niter', 'cost', 'formulae',])
        result = result.sort_values('cost', ascending=1)
        return result

    res = search()
    #llog('Best\n',)
    #llog( res.iloc[:2,:] )
    return res


#########################Symbolic Regression Version####################################
def search_formulae_dcgpy_Xy_regression_v1(problem=None, pars_dict:dict=None, verbose=1, ):
    """ Search Optimal Formulae
    Docs::

        -- Install
          conda create -n dcgp  python==3.8.1
          source activate dcgp
          conda install   -y  -c conda-forge dcgp-python  scipy
          pip install python-box fire utilmy sympy

          python -c "from dcgpy import test; test.run_test_suite(); import pygmo; pygmo.mp_island.shutdown_pool(); pygmo.mp_bfe.shutdown_pool()"


          https://darioizzo.github.io/dcgp/installation.html#python

          https://darioizzo.github.io/dcgp/notebooks/real_world1.html


        -- Usagge
            import utilmy.optim.gp_formulaesearch as gp
            from numpy import (sin, cos, log, exp, sqrt )

            -- 1) Define Problem Class with get_cost methods
                myproblem       = gp.myProblem5()

                p               = Box({})
                p.log_file      = 'trace.log'
                p.print_after   = 5
                p.print_best    = True


                p.nvars_in      = 2  ### nb of variables
                p.nvars_out     = 1
                p.operators     = ["sum", "mul", "div", "diff","sin"]
                p.symbols       = ["x0","x1"]

                p.n_exp         = 4
                p.max_step      = 1000  ## per expriemnet
                p.offsprings    = 20


                --- Run Search
                res = gp.search_formulae_dcgpy_Xy_regression_v1(myproblem, pars_dict=p, verbose=1)


            --  Custom Problem
                class myProblem5:
                    def __init__(self):
                        pass

                    def get_data(self):
                        #Insert your data here
                        X = np.linspace(0,15, 100)
                        Y = X * ((X**3) - 18 * X + 32) / 32
                        Y[X>2] = 1. / X[X>2]**2
                        X = np.reshape(X, (100,1))
                        Y = np.reshape(Y, (100,1))
                        return X,Y




        -- Add constraints in the functional space

            https://darioizzo.github.io/dcgp/notebooks/phenotype_correction_ex.html
            https://darioizzo.github.io/dcgp/notebooks/finding_prime_integrals.html
            https://darioizzo.github.io/dcgp/notebooks/real_world2.html


    """
    import dcgpy
    import pygmo as pg
    # Sympy is nice to have for basic symbolic manipulation.
    from sympy import init_printing
    #from sympy.parsing.sympy_parser import *
    from sympy.parsing.sympy_parser import parse_expr
    # Fundamental for plotting.
    from matplotlib import pyplot as plt
    ### Problem
    p             = Box(pars_dict)
    nvars_in      = p.nvars_in  ### nb of variables
    nvars_out     = p.nvars_out
    operator_list = p.get('operators', ["sum", "mul", "div", "diff","sin","cos"])
    symbols       = p.get('symbols',['x0','x1','x2'])


    ### Log
    print_after     = p.get('print_after', 20)
    print_best      = p.get('print_best', True)
    # max_iter      = p.get('max_iter', 2) #100000  ## Max iterations
    # seed          = p.get('seed', 43)
    log_file        = p.get('log_file', 'log.log') # 'trace.py'

    ### search
    n_exp           = p.get('n_exp', 1)
    max_step        = p.get('max_step', 10)

    offsprings      = p.get('offsprings',10)
    pop_size        = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)

    seed            = p.get('seed', 23)
    n_eph           = p.get('kernels_new',3)
    verbose         = p.get('verbose',1)



    from utilmy import os_makedirs
    os_makedirs(log_file)
    def print_file(*s,):
        ss = "\t".join([str(x) for x in  s])
        if verbose>0 : print(ss, flush=True)
        with open(log_file, mode='a') as fp :
            fp.write(ss +"\n")



    def run_experiment(udp, uda, verbose=1):
        prob = pg.problem(udp)
        algo = pg.algorithm(uda)
        # Set verbosity>0 for getting
        algo.set_verbosity(verbose-1)
        pop = pg.population(prob, 20)
        pop = algo.evolve(pop)
        idx = np.argmin(pop.get_f(), axis=0)[0]
        cost  = pop.get_f()[idx][0]
        expr = parse_expr(udp.prettier(pop.get_x()[idx]))
        return expr,cost

    def search():
        # Search for best possible solution using Genetic Algorithm

        kernels_new = dcgpy.kernel_set_double(operator_list)()
        X, Y = problem.get_data()
        udp = dcgpy.symbolic_regression(points = X, labels = Y, kernels=kernels_new, n_eph=n_eph, rows =1, cols=20, levels_back=21, multi_objective=True)
        uda  = dcgpy.momes4cgp(gen = 3000, max_mut = 4)
        expr,cost = run_experiment(udp,uda,verbose)
        if verbose>1:
            print_file(expr)
            print_file(cost)
        return [expr,cost]

    res = search()
    llog('Best Results',)
    llog( res )
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
    llog(pars_dict)
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






def zzz_search_formulae_dcgpy_cuckoo(myproblem=None, pars_dict:dict=None, verbose=False, ):
    """ Search Optimal Formulae
    Docs::

          NOT Working



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
        gp.search_formulae_algo1(myproblem1, pars_dict=p, verbose=1)


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
    llog(pars_dict)
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
        llog(operator_list)
        llog(symbols)


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
        # ex.mutate_active(2)   llog("Mutated expression:", ex(symbols)[0])
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
                llog(f'\n#{k}', f'{best_egg[1]}')

                if print_best :
                    llog(best_egg[0](symbols)[0])
                    #llog(best_egg[0].simplify(symbols))
                    llog('\n')

        expr = str(best_egg[0](symbols)[0])
        best_cost = best_egg[1]
        return best_cost, expr

    x =search()
    return x

