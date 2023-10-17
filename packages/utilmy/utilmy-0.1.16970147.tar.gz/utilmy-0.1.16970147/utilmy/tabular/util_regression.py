"""  Advanced Linear Regression

Docs::



    https://www.xlstat.com/en/solutions/features/partial-least-squares-regression#:~:text=The%20Partial%20Least%20Squares%20regression,used%20to%20perfom%20a%20regression.&text=Some%20programs%20differentiate%20PLS%201,is%20only%20one%20dependent%20variable.

    Partial Least Squares Regression (PLS)
    Partial Least Squares regression (PLS) is a quick, efficient and optimal regression method based on covariance. It is recommended in cases of regression where the number of explanatory variables is high, and where it is likely that there is multicollinearity among the variables, i.e. that the explanatory variables are correlated.

    XLSTAT provides a complete PLS regression method to model and predict your data in excel. XLSTAT proposes several standard and advanced options that will let you gain a deep insight on your data:

    Choose several response variables in one analysis
    Use the leave one out (LOO) cross validation option
    Automatically choose the number of components to be kept using one of multiple criteria or choose this number manually
    Choose between the fast algorithm and the more precise one.
    What is Partial Least Squares regression?
    The Partial Least Squares regression (PLS) is a method which reduces the variables, used to predict, to a smaller set of predictors. These predictors are then used to perfom a regression.

    The idea behind the PLS regression is to create, starting from a table with n observations described by p variables, a set of h components with the PLS 1 and PLS 2 algorithms

    Some programs differentiate PLS 1 from PLS 2. PLS 1 corresponds to the case where there is only one dependent variable. PLS 2 corresponds to the case where there are several dependent variables. The algorithms used by XLSTAT are such that the PLS 1 is only a particular case of PLS 2.

    Partial Least Squares regr


    Partial Least Squares regression model equations
    In the case of the Ordinary Least Squares (OLS) and Principale Component Regression (PCR) methods, if models need to be computed for several dependent variables, the computation of the models is simply a loop on the columns of the dependent variables table Y. In the case of PLS regression, the covariance structure of Y also influences the computations.

    The equation of the PLS regression model writes:

    Y = ThC’h + Eh = XWh*C’h + Eh = XWh (P’hWh)-1 C’h + Eh

    where Y is the matrix of the dependent variables, X is the m


    https://mbpls.readthedocs.io/en/latest/index.html




"""


def test1():
    """


    """
    import numpy as np
    from mbpls.mbpls import MBPLS

    num_samples = 40
    num_features_x1 = 200
    num_features_x2 = 250

    # Generate two random data matrices X1 and X2 (two blocks)
    x1 = np.random.rand(num_samples, num_features_x1)
    x2 = np.random.rand(num_samples, num_features_x2)

    # Generate random reference vector y
    y = np.random.rand(num_samples, 1)

    # Establish prediction model using 3 latent variables (components)
    mbpls = MBPLS(n_components=3)
    mbpls.fit([x1, x2],y)
    y_pred = mbpls.predict([x1, x2])

    # Use built-in plot method for exploratory analysis of multiblock pls models
    mbpls.plot(num_components=3)


