
"""
Issues:
######Approach 1
a. The test6 function is highly hard coded and will requires substantial changes so maybe 
we will need to change search_formulae_dcgpy_v1 substantially.
The results of this as per my checking is good as it checks the results upto second
differential but this one is deprecated as per main docs of dcgpy
Reference: http://darioizzo.github.io/dcgp/notebooks/learning_constants2.html

b. test1 is working but is approximating to next nearest integer i.e. 3.14--->4
And has to be modified to give expressions with c1,c2...


c. test2  is also in same line as test6 with improvements in search_formulae_dcgpy_v1, 
still lot of changes needed and it is work under progress

######Approach 2 
test8  are running good now, but it  is dependant on search_formulae_dcgpy_Xy_regression_v1 
Reference: http://darioizzo.github.io/dcgp/notebooks/symbolic_regression_2.html
Note: With increase in number of constants, the final expression changes,
so needed to increase the number of n_exp to get consistent results.


##### Approach 3 
>Added test3, Newton method
http://darioizzo.github.io/dcgp/notebooks/weighted_symbolic_regression.html

>test 4 is sample with 3 variable
Results are not consistent and might need high value of max_step, and n_step

Will be merged with  gp_searchformulae once things become clear
"""
import os, random, math, numpy as np, warnings, copy, pickle, time
from unittest import loader
from re import X
from box import Box
from random import random
np.seterr(all='ignore') 
from numpy import (sin, cos, log, exp, sqrt )

def test6():
    from dcgpy import expression_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    from pyaudi import gdual_vdouble as gdual
    import pyaudi
    from matplotlib import pyplot as plt
    import numpy as np
    from random import randint

    ###http://darioizzo.github.io/dcgp/notebooks/learning_constants2.html



    def run_experiment(dCGP, offsprings, max_gen, x, yt, screen_output):
        # The offsprings chromosome, fitness and constant
        chromosome = [1] * offsprings
        fitness = [1] *offsprings
        constant = [[1.,1.1]]*offsprings
        # Init the best as the initial random dCGP
        best_chromosome = dCGP.get()
        best_constants = [1,1]
        fit, _ = err2(dCGP, x, yt, best_constants)
        best_fitness = fit
        # Main loop over generations
        for g in range(max_gen):
            for i in range(offsprings):
                dCGP.set(best_chromosome)
                cumsum=0
                dCGP.mutate_active(i+1)
                fit, constant[i] = err2(dCGP, x, yt, best_constants)
                fitness[i] = fit
                chromosome[i] = dCGP.get()
            for i in range(offsprings):
                if fitness[i] <= best_fitness:
                    if (fitness[i] != best_fitness):
                        best_chromosome = chromosome[i]
                        best_fitness = fitness[i]
                        best_constants = constant[i]
                        dCGP.set(best_chromosome)
                        if screen_output:
                            print("New best found: gen: ", g, " value: ", fitness[i],  dCGP.simplify(["x","c1","c2"]), "c =", best_constants)

            if best_fitness < 1e-14:
                break
        return g, best_chromosome, best_constants


    # This is used to sum over the component of a vectorized coefficient, accounting for the fact that if its dimension
    # is 1, then it could represent [a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a ...] with [a]
    def collapse_vectorized_coefficient(x, N):
        if len(x) == N:
            return sum(x)
        return x[0] * N

    # This is the quadratic error of a dCGP expression when the constant value is cin. The error is computed
    # over the input points xin (of type gdual, order 0 as we are not interested in expanding the program w.r.t. these)
    # The target values are contained in yt (of type gdual, order 0 as we are not interested in expanding the program w.r.t. these)
    def err(dCGP, xin, yt, c1, c2):
        y = dCGP([xin,c1,c2])[0]
        return (y-yt)**2 / len(xin.constant_cf)

    # This is the quadratic error of the expression when the value of the constants are learned using a, one step,
    # second order method.
    def err2(dCGP, xin, yt, constants):
        cin1 = constants[0]
        cin2 = constants[1]
        # Lets comupte the Taylor expansion (order 2) of the quadratic error around the point cin1, cin2
        c1 = gdual([cin1], "c1", 2)
        c2 = gdual([cin2], "c2", 2)
        error = err(dCGP, x, yt, c1, c2)
        #initial error for the current values of constants
        ierr = sum(error.constant_cf)
        # Number of points used in the data
        N = len(xin.constant_cf)

        # We try one step of the Newton method
        for i in range(1):
            G1 = error.get_derivative({"dc1":1})
            G2 = error.get_derivative({"dc2":1})
            H11 = error.get_derivative({"dc1":2})
            H22 = error.get_derivative({"dc2":2})
            H12 = error.get_derivative({"dc1":1, "dc2":1})
            G1 = collapse_vectorized_coefficient(G1, N)
            G2 = collapse_vectorized_coefficient(G2, N)
            H11 = collapse_vectorized_coefficient(H11, N)
            H22 = collapse_vectorized_coefficient(H22, N)
            H12 = collapse_vectorized_coefficient(H12, N)

            H = [[H11,H12],[H12, H22]]
            det = np.linalg.det(H)
            if det != 0:
                invH = np.linalg.inv(H)
                # We write the Newton update formula explicitly
                dc1 = - invH[0,0] * G1 - invH[0,1] * G2
                dc2 = - invH[1,0] * G1 - invH[1,1] * G2
                dc1*=1
                dc2*=1
                c1+=dc1
                c2+=dc2
                error = err(dCGP, x, yt, c1, c2)
            else:
                break

        # error after one Newton step
        aerr = sum(error.constant_cf)

        # if no improvement, take 5 steps of gradient descent with learing rate 0.05
        if aerr >= ierr:
            c1 = gdual([cin1], "c1", 1)
            c2 = gdual([cin2], "c2", 1)
            # We end up with a few gradient descent steps
            for i in range(5):
                G1 = sum(error.get_derivative({"dc1":1}))
                G2 = sum(error.get_derivative({"dc2":1}))
                dc1 = - G1
                dc2 = - G2
                dc1*=0.05
                dc2*=0.05
                c1+=dc1
                c2+=dc2
                error = err(dCGP, x, yt, c1, c2)

        aerr = sum(error.constant_cf)
        return aerr, [c1.constant_cf[0], c2.constant_cf[0]]

    def data_P1(x):
        return x**5 - np.pi*x**3 + x
    def data_P2(x):
        return x**5 - np.pi*x**3 + 2*np.pi / x
    def data_P3(x):
        return (np.e*x**5 + x**3)/(x + 1)
    def data_P4(x):
        return pyaudi.sin(np.pi * x) + 1./x
    def data_P5(x):
        return np.e * x**5 - np.pi*x**3 + np.sqrt(2) * x
    def data_P5(x):
        return np.e * x**5 - np.pi*x**3 + np.sqrt(2) * x


    def search():
        # We run nexp experiments and accumulate statistic for the ERT
        nexp = 100
        offsprings = 4
        max_gen=2000
        res = []
        kernels = kernel_set(["sum", "mul", "diff","div"])()
        print("restart: \t gen: \t expression:")
        for i in range(nexp):
            dCGP = expression(inputs=3, outputs=1, rows=1, cols=15, levels_back=16, arity=2, kernels=kernels, seed = randint(0,1233456))
            g, best_chromosome, best_constant = run_experiment(dCGP, offsprings,max_gen,x,yt, screen_output=False)
            res.append(g)
            dCGP.set(best_chromosome)
            if g < (max_gen-1):
                print(i, "\t\t", res[i], "\t", dCGP(["x","c1","c2"]), " a.k.a ", dCGP.simplify(["x","c1","c2"]), "c = ", best_constant)
        res = np.array(res)

    x = np.linspace(1,3,10)
    x = gdual(x)
    yt = data_P1(x)
    search()

def test8():
    """Test search_formulae_dcgpy_v1
    """
    from box import Box
    myproblem       = myProblem5()

    p               = Box({})
    p.log_file      = 'trace4.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 1  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul","pdiv"]
    p.symbols       = ["x0"]

    p.max_step      = 5
    p.n_exp         = 20
    p.offsprings    = 10
    p.n_eph         = 2
    p.verbose       = 1


    #### Run Search
    res = search_formulae_dcgpy_Xy_regression_v1(myproblem, pars_dict=p, verbose=1)

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
    p.operators     = ["sum", "mul", "div", "diff"]
    p.symbols       = ["x0","x1"]

    p.n_exp         = 20
    p.max_step      = 1000  ## per expriemnet
    p.offsprings    = 20
    p.n_eph         = 1

    #### Run Search
    res = search_formulae_dcgpy_v1(myproblem, pars_dict=p, verbose=1)

def test3():
    """Test search_formulae_dcgpy_newton with 1 variable
    """
    

    myproblem       = myProblem6()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 1  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff"]
    p.symbols       = ["x0"]

    p.n_exp         = 5
    p.max_step      = 5  ## per expriemnet
    p.offsprings    = 20
    p.n_eph         = 1
    #p.load_old_weights  = False
    p.problem_id    =  '3' ### Unique problem id for each new test expression 
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662743935.pickle" # path
    p.problem_id    =  '4' ### Unique problem id for each problem 
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings

    #### Run Search
    res = search_formulae_dcgpy_newton(myproblem, pars_dict=p, verbose=1)

def test4():
    """Test search_formulae_dcgpy_newton with 3 variables


    """
    

    myproblem       = myProblem7()

    p               = Box({})
    p.log_file      = 'trace.log'
    p.print_after   = 5
    p.print_best    = True


    p.nvars_in      = 3  ### nb of variables
    p.nvars_out     = 1
    p.operators     = ["sum", "mul", "div", "diff"]
    p.symbols       = ["x0","x1","x2"]

    p.n_exp         = 5
    p.max_step      = 500  ## per expriemnet
    p.offsprings    = 20
    p.n_eph         = 1

    p.save_new_weights = f"ztmp/dcpy_weight_{int(time.time())}.pickle" ###To save new results

    #### Re-use old problem setting
    p.load_old_weights  = "ztmp/dcpy_weight_1662743807.pickle" # path
    p.problem_id    =  '4' ### Unique problem id for each problem 
    p.frac_old      = 0.05 ###Fraction of chromosomes to be used from old learnings

    #### Run Search
    res = search_formulae_dcgpy_newton(myproblem, pars_dict=p, verbose=1)

###############################################################################################################

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
        #self.ytrue =  np.pi*x1 + x0**2 + x1*x0  #This is the true expression
        self.ytrue = x0**5 - 3.967*x0**3 + 8.756/ x0


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
        x = np.linspace(1,20,100)
        #Y = x**5 - np.pi*x**3 + 2*x
        #Y = x**5 - np.pi*x**3 + 2*np.pi / x
        Y = x**5 - 3.967*x**3 + 8.756/ x
        X = np.reshape(x, (100,1))
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

        x = np.linspace(1,3,10)

        # ### Formulae Space
        x = gdual(x)
        yt =  x**5 - np.pi*x**3 + 2*x
        self.yt = yt
        self.x = x

    def get_data_symbolic(self):
        """ Cost Calculation, Objective to minimize Cost
        Docs::

            expr            : Expression whose cost has to be maximized
            symbols         : Symbols

        """
        #Insert your data here
        return self.x


    def get_cost_symbolic(self,dCGP):
        y    = dCGP([self.x])[0]
        #y    = dCGP([self.x[0],self.x[1]])[0]
        cost = (y-self.yt)**2
        return cost

class myProblem7:
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
        #y    = dCGP([self.x])[0]
        y    = dCGP([self.x[0],self.x[1],self.x[2]])[0]
        cost = (y-self.yt)**2
        return cost

###################################################################################################3

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
    ######### Problem definition and Cost calculation


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
    n_exp           = p.get('n_exp', 1)
    max_step        = p.get('max_step', 10)

    offsprings      = p.get('offsprings',10)
    pop_size        = p.get("pop_size", 5) #20  ## Population (Suggested: 10~20)

    seed            = p.get('seed', 23)
    n_eph           = p.get('n_eph',0)


    ### search DCGPY Algo

    from utilmy import os_makedirs
    os_makedirs(log_file)
    def print_file(*s,):
        ss = "\t".join([str(x) for x in  s])
        if verbose>0 : print(ss, flush=True)
        with open(log_file, mode='a') as fp :
            fp.write(ss +"\n")



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
            #print(fitness)
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
        return kstep, dCGP, best_fitness


    def search():
        """ Search for best possible solution using Genetic Algorithm
        Docs::

            classdcgpy.expression_double(inputs, outputs, rows, cols, levels_back, arity = 2, kernels, n_eph = 0, seed = randint)
            A CGP expression
            https://darioizzo.github.io/dcgp/docs/python/expression.html


        """

        kernels_new = kernel_set(operator_list)()

        #  n_exp experiments to accumulate statistic
        result = []
        if verbose>0:
            print_file( 'id_exp', 'niter', 'cost', 'formulae', )
        for i in range(n_exp):
            dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                              kernels=kernels_new,
                              seed = random.randint(0,234213213))
            kstep, dCGP, best_fitness = run_experiment(max_step=max_step, offsprings=10, dCGP=dCGP, symbols=symbols, verbose=False)
            #idx = np.argmin(dCGP.get_f(), axis=0)[0]
            #cost  = dCGP.get_f()[idx][0]
            #expr = parse_expr(dCGP.prettier(pop.get_x()[idx]))

            form2 = dCGP.simplify(symbols)[0]
            result.append( ( i, kstep , best_fitness, form2   ) )

            if   verbose >=2 :
                form1 = dCGP(symbols)[0]
                print_file(i, kstep,  form1,  form2)

            elif verbose >=1 : print_file(i, kstep, form2, best_fitness)

            
        result = pd.DataFrame(result,  columns=['id_exp', 'niter', 'cost', 'formulae',   ])
        result = result.sort_values('cost', ascending=1)
        return result

    res = search()
    #llog('Best\n',)
    #llog( res.iloc[:2,:] )
    return res


def search_formulae_dcgpy_newton(problem=None, pars_dict:dict=None, verbose=1, ):
    """ Search Optimal Formulae with constants using Newton Formulae
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
                myproblem       = myProblem7()

                p                       = Box({})
                p.log_file              = 'trace.log'
                p.print_after           = 5
                p.print_best            = True


                p.nvars_in               = 3  ### nb of variables
                p.nvars_out              = 1
                p.operators              = ["sum", "mul", "div", "diff"]
                p.symbols                = ["x0","x1","x2"]

                p.n_exp                  = 20
                p.max_step               = 5000  ## per expriemnet
                p.offsprings             = 20
                p.n_eph                  = 1
                p.load_old_weights       = False
                p.problem_id             =  '4'   ## Unique problem id for each new test expression 
                p.frac_old               = 0.05   ##Fraction of chromosomes to be used from old learnings
                p.save_new_weights        = True  ##To save new results
                #### Run Search
                res = search_formulae_dcgpy_newton(myproblem, pars_dict=p, verbose=1)



            --  Custom Problem

                    class myProblem7:
                        def __init__(self):
                            from pyaudi import gdual_vdouble as gdual
                            # ### Formulae Space
                            x0 = np.linspace(1,10,1000)
                            x1 = np.linspace(1,10,1000)
                            x2 = np.linspace(1,10,1000)
                            x0 = gdual(x0)
                            x1 = gdual(x1)
                            x2 = gdual(x2)
                            yt =  3*x0*x1 - np.pi*x1 + 2*x2

                            self.x  = [x0,x1,x2]
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
            
        --My Issue:
            As the number of variables increases , we will need high values of max_step, and n_step,
            to get the correct expression

    """
    from pyaudi import gdual_vdouble as gdual
    from dcgpy import expression_weighted_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    import random, pandas as pd
    from box import Box
    import pyaudi 
    import pickle 
    from utilmy.utilmy_base import log as llog, log2
    ######### Problem definition and Cost calculation


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
    problem_id          = p.get('problem_id',2)
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

            return Box(ddict)

       elif mode =='save':
            if path is not None:
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
            #print(fitness)
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
        check_file = 1
        if load_old_weights is not None:
            try:
                check_file = 1
                w_old = load_save(path=load_old_weights, mode='load')

                loaded_weights     = w_old.best_weights
                loaded_choromosome = w_old.best_chromosome
                loaded_fitness     = w_old.best_fitness
                print("Data loaded")
                dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                    kernels=kernels_new,
                                    seed = random.randint(0,234213213))

                dCGP.set_weights(loaded_weights)
                dCGP.set(loaded_choromosome)
                print("Old saved result is:")
                print(dCGP.simplify(in_sym = symbols,subs_weights=True))

            except Exception as e:
                print(e)
                print("Error in loading old data, so creating expressions from scratch")
                check_file = 0

        #  n_exp experiments to accumulate statistic
        result = []
        if verbose>0:
            print_file( 'id_exp', 'niter', 'weights', 'formulae', )


        #Check results for new iterations
        for i in range(n_exp):
            if ((load_old_weights is not None) & (i<=int(frac_old*n_exp)) & (check_file!=0)):
                dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                kernels=kernels_new,
                                seed = random.randint(0,234213213))
                dCGP.set_weights(loaded_weights)
                dCGP.set(loaded_choromosome)
            else:
                dCGP = expression(inputs=nvars_in, outputs=nvars_out, rows=1, cols=15, levels_back=16, arity=2,
                                kernels=kernels_new,
                                seed = random.randint(0,234213213))

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


        #Load the weight and chormosome to obtain the results

        #If the result is previous result then only save new results
        if load_old_weights is not None  and check_file!=0 :
            if best_fitness > loaded_fitness:
                best_fitness    = loaded_fitness
                best_weights    = loaded_weights
                best_chromosome = loaded_choromosome


        best_weights = list(np.array(best_weights))
        #ddict = {problem_id:{"best_chromosome":best_chromosome,"best_weights":best_weights,"best_fitness":best_fitness} }
        ddict = {"best_chromosome":best_chromosome,"best_weights":best_weights,"best_fitness":best_fitness}
        load_save(path=save_new_weights, mode='save', ddict=ddict)


        ##### Store thre results in a dataframe
        result = pd.DataFrame(result,  columns=['id_exp', 'niter', 'cost', 'formulae',])
        result = result.sort_values('cost', ascending=1)
        return result

    res = search()
    #llog('Best\n',)
    #llog( res.iloc[:2,:] )
    return res



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
    n_eph           = p.get('n_eph',3)
    verbose         = p.get('verbose',1)



    from utilmy import os_makedirs
    os_makedirs(log_file)
    def print_file(*s,):
        ss = "\t".join([str(x) for x in  s])
        if verbose>0 : print(ss, flush=True)
        with open(log_file, mode='a') as fp :
            fp.write(ss +"\n")



    def run_experiment(udp, uda,n_eph, verbose=1):
        prob = pg.problem(udp)
        algo = pg.algorithm(uda)
        # Set verbosity>0 for getting
        algo.set_verbosity(verbose-1)
        pop = pg.population(prob, 20)
        pop = algo.evolve(pop)
        idx = np.argmin(pop.get_f(), axis=0)[0]
        cost  = pop.get_f()[idx][0]
        expr = parse_expr(udp.prettier(pop.get_x()[idx]))
        print("Expression",expr)
        if n_eph>0:
            for i in range(n_eph):
                print("Constant Value c{} is {}".format(i+1,pop.get_x()[idx][i]))
        return expr,cost

    def search():
        # Search for best possible solution using Genetic Algorithm

        kernels_new = dcgpy.kernel_set_double(operator_list)()
        X, Y = problem.get_data()
        udp = dcgpy.symbolic_regression(points = X, labels = Y, kernels=kernels_new, n_eph=n_eph, rows =1, cols=100, levels_back=80,multi_objective=True)
        uda  = dcgpy.momes4cgp(gen = 3000, max_mut = 4)
        expr,cost = run_experiment(udp,uda,n_eph,verbose)
        if verbose>1:
            print_file(expr)
            print_file(cost)
        return [expr,cost]

    res = search()
    #llog('Best Results',)
    #llog( res )
    return res


def test2():
    from dcgpy import expression_gdual_vdouble as expression
    from dcgpy import kernel_set_gdual_vdouble as kernel_set
    from pyaudi import gdual_vdouble as gdual
    import pyaudi
    from matplotlib import pyplot as plt
    import numpy as np
    from random import randint

    ###http://darioizzo.github.io/dcgp/notebooks/learning_constants2.html



    def run_experiment(dCGP, offsprings, max_gen, symbols,n_constants, screen_output):
        # The offsprings chromosome, fitness and constant
        chromosome = [1] * offsprings
        fitness = [1] *offsprings
        constant = [[1.,1.1]]*offsprings
        # Init the best as the initial random dCGP
        best_chromosome = dCGP.get()
        best_constants = [1,1]
        fit, _ = err2(dCGP, symbols, n_constants, best_constants)
        best_fitness = fit
        # Main loop over generations
        for g in range(max_gen):
            for i in range(offsprings):
                dCGP.set(best_chromosome)
                cumsum=0
                dCGP.mutate_active(i+1)
                fit, constant[i] = err2(dCGP, symbols,n_constants, best_constants)
                fitness[i] = fit
                chromosome[i] = dCGP.get()
            for i in range(offsprings):
                if fitness[i] <= best_fitness:
                    if (fitness[i] != best_fitness):
                        best_chromosome = chromosome[i]
                        best_fitness = fitness[i]
                        best_constants = constant[i]
                        dCGP.set(best_chromosome)
                        if screen_output:
                            print("New best found: gen: ", g, " value: ", fitness[i],  dCGP.simplify(symbols), "c =", best_constants)

            if best_fitness < 1e-14:
                break
        return g, best_chromosome, best_constants

    def get_data():
        x = np.linspace(1,3,10)
        x = gdual(x)
        yt = data_P1(x)
        return x,yt

    # This is used to sum over the component of a vectorized coefficient, accounting for the fact that if its dimension
    # is 1, then it could represent [a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a,a ...] with [a]
    def collapse_vectorized_coefficient(x, N):
        if len(x) == N:
            return sum(x)
        return x[0] * N

    # This is the quadratic error of a dCGP expression when the constant value is cin. The error is computed
    # over the input points xin (of type gdual, order 0 as we are not interested in expanding the program w.r.t. these)
    # The target values are contained in yt (of type gdual, order 0 as we are not interested in expanding the program w.r.t. these)
    def err(dCGP, xin, yt,n_constants, constant_collections):
        check_symbols = [xin]

        for i in range(n_constants):
            variable_name = 'c'+str(i+1)

            check_symbols.append(constant_collections[variable_name])
        y = dCGP(check_symbols)[0]
        return (y-yt)**2 / len(xin.constant_cf)

    # This is the quadratic error of the expression when the value of the constants are learned using a, one step,
    # second order method.
    def err2(dCGP, symbols,n_constants,constants):
        xin,yt = get_data()
        constant_collections    = {}
        derivative_names        = []
        first_var_names          = []
        second_var_names         = []
        mutual_var_names         = []
        for i in range(n_constants):
            cin                 = constants[i]
            variable_name       = 'c'+str(i+1)
            derivative_name     = 'dc'+str(i+1)
            first_var_name      =  'G'+str(i+1)
            second_var_name     =  'H'+str(i+1)
            derivative_names.append(derivative_name)
            first_var_names.append(first_var_name)
            second_var_names.append(second_var_name)
            constant_collections['variable_name'] = gdual([cin], variable_name, 2)
        error = err(dCGP, xin, yt, n_constants,constant_collections)
        ierr = sum(error.constant_cf)
        N = len(xin.constant_cf)

        #cin1 = constants[0]
        #cin2 = constants[1]
        # Lets comupte the Taylor expansion (order 2) of the quadratic error around the point cin1, cin2
        #c1 = gdual([cin1], "c1", 2)
        #c2 = gdual([cin2], "c2", 2)
        #error = err(dCGP, x, yt, c1, c2)
        #initial error for the current values of constants
        #ierr = sum(error.constant_cf)
        # Number of points used in the data
        #N = len(xin.constant_cf)
        for i in range(n_constants):
            for j in range(n_constants):
                mutual_var_name     =  'H'+str(i+1) + str(j+1)
                mutual_var_names.append(mutual_var_name)


        first_derivatives = {}
        H = []
        # We try one step of the Newton method
        for i in range(1):
            for j in range(n_constants):
                first_derivatives[first_var_names[j]] = error.get_derivative({derivative_names[j]:1})
                #second_derivatives[second_var_names[j]] = error.get_derivative({derivative_names[j]:1})
                H_1 = []
                for k in range(n_constants):
                    H_1.append( error.get_derivative({derivative_names[j]:1, derivative_names[k]:1}))
                #H = [[H1,H12,H13],[H12, H2,H3]] 
                H.append(H_1)

            # G1 = error.get_derivative({"dc1":1})
            # G2 = error.get_derivative({"dc2":1})
            # H11 = error.get_derivative({"dc1":2})
            # H22 = error.get_derivative({"dc2":2})
            # H12 = error.get_derivative({"dc1":1, "dc2":1})
            # G1 = collapse_vectorized_coefficient(G1, N)
            # G2 = collapse_vectorized_coefficient(G2, N)
            # H11 = collapse_vectorized_coefficient(H11, N)
            # H22 = collapse_vectorized_coefficient(H22, N)
            # H12 = collapse_vectorized_coefficient(H12, N)

            # H = [[H11,H12],[H12, H22]]
            # det = np.linalg.det(H)
            # if det != 0:
            #     invH = np.linalg.inv(H)
            #     # We write the Newton update formula explicitly
            #     dc1 = - invH[0,0] * G1 - invH[0,1] * G2
            #     dc2 = - invH[1,0] * G1 - invH[1,1] * G2
            #     dc1*=1
            #     dc2*=1
            #     c1+=dc1
            #     c2+=dc2
            #     error = err(dCGP, xin, yt, c1, c2)
            # else:
            #     break
            det = np.linalg.det(H)
            if det != 0:
                invH = np.linalg.inv(H)
                # We write the Newton update formula explicitly
                dc1 = - invH[0,0] * first_derivatives['G1'] - invH[0,1] * first_derivatives['G2']
                dc2 = - invH[1,0] * first_derivatives['G1'] - invH[1,1] * first_derivatives['G2']
                dc1*=1
                dc2*=1
                c1+=dc1
                c2+=dc2
                constant_collections['c1'] = c1
                constant_collections['c2'] = c2
                error = err(dCGP, xin, yt, n_constants, constant_collections)
            else:
                break

        # error after one Newton step
        aerr = sum(error.constant_cf)

        # if no improvement, take 5 steps of gradient descent with learing rate 0.05
        if aerr >= ierr:
            c1 = gdual([cin1], "c1", 1)
            c2 = gdual([cin2], "c2", 1)
            # We end up with a few gradient descent steps
            for i in range(5):
                G1 = sum(error.get_derivative({"dc1":1}))
                G2 = sum(error.get_derivative({"dc2":1}))
                dc1 = - first_derivatives['G1']
                dc2 = - first_derivatives['G2']
                dc1*=0.05
                dc2*=0.05
                c1+=dc1
                c2+=dc2
                constant_collections['c1'] = c1
                constant_collections['c2'] = c2
                error = err(dCGP, xin, yt, n_constants, constant_collections)

        aerr = sum(error.constant_cf)
        return aerr, [constant_collections['c1'] .constant_cf[0], constant_collections['c2'] .constant_cf[0]]

    def data_P1(x):
        return x**5 - np.pi*x**3 + x
    def data_P2(x):
        return x**5 - np.pi*x**3 + 2*np.pi / x
    def data_P3(x):
        return (np.e*x**5 + x**3)/(x + 1)
    def data_P4(x):
        return pyaudi.sin(np.pi * x) + 1./x
    def data_P5(x):
        return np.e * x**5 - np.pi*x**3 + np.sqrt(2) * x
    def data_P5(x):
        return np.e * x**5 - np.pi*x**3 + np.sqrt(2) * x


    def search():
        # We run nexp experiments and accumulate statistic for the ERT
        nexp = 100
        offsprings = 4
        max_gen=2000
        res = []
        symbols = ["x","c1","c2"]
        n_constants = 2
        kernels = kernel_set(["sum", "mul", "diff","div"])()
        print("restart: \t gen: \t expression:")
        for i in range(nexp):
            dCGP = expression(inputs=3, outputs=1, rows=1, cols=15, levels_back=16, arity=2, kernels=kernels, seed = randint(0,1233456))
            g, best_chromosome, best_constant = run_experiment(dCGP, offsprings,max_gen,symbols,n_constants, screen_output=False)
            res.append(g)
            dCGP.set(best_chromosome)
            if g < (max_gen-1):
                print(i, "\t\t", res[i], "\t", dCGP(symbols), " a.k.a ", dCGP.simplify(symbols), "c = ", best_constant)
        res = np.array(res)

    res = search()
    return res

###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()