# coding=utf-8
"""Fast Hypothesis and Statistical Testing in Python

Doc::

    --- Analysis of Variance
        * One-way Analysis of Variance (ANOVA)
        * One-way Multivariate Analysis of Variance (MANOVA)
        * Bartlett's Test for Homogenity of Variances
        * Levene's Test for Homogenity of Variances
        * Van Der Waerden's (normal scores) Test


    --- Contingency Tables and Related Tests
        * Chi-square test of independence
        * Fisher's Exact Test
        * McNemar's Test of paired nominal data
        * Cochran's Q test
        * D critical value (used in the Kolomogorov-Smirnov Goodness-of-Fit test).


    --- Critical Value Tables and Lookup Functions
        * Chi-square statistic
        * r (one-sample runs test and Wald-Wolfowitz runs test) statistic
        * Mann-Whitney U-statistic
        * Wilcoxon Rank Sum W-statistic


    --- Descriptive Statistics
        * Kurtosis
        * Skewness
        * Mean Absolute Deviation
        * Pearson Correlation
        * Spearman Correlation
        * Covariance
          - Several algorithms for computing the covariance and covariance matrix of
            sample data are available
        * Variance
          - Several algorithms are also available for computing variance.
        * Simulation of Correlation Matrices
          - Multiple simulation algorithms are available for generating correlation matrices.


    --- Factor Analysis
        * Several algorithms for performing Factor Analysis are available, including principal components, principal
              factors, and iterated principal factors.

    --- Hypothesis Testing
        * Binomial Test
        * t-test
          - paired, one and two sample testing


    --- Nonparametric Methods
        * Friedman's test for repeated measures
        * Kruskal-Wallis (nonparametric equivalent of one-way ANOVA)
        * Mann-Whitney (two sample nonparametric variant of t-test)
        * Mood's Median test
        * One-sample Runs Test
        * Wald-Wolfowitz Two-Sample Runs Test
        * Sign test of consistent differences between observation pairs
        * Wald-Wolfowitz Two-Sample Runs test
        * Wilcoxon Rank Sum Test (one sample nonparametric variant of paired and one-sample t-test)


    --- Normality and Goodness-of-Fit Tests
        * Chi-square one-sample goodness-of-fit
        * Jarque-Bera test


    --- Post-Hoc Analysis
        * Tukey's Honestly Significant Difference (HSD)
        * Games-Howell (nonparametric)


    --- Helpful Functions
        * Add noise to a correlation or other matrix
        * Tie Correction for ranked variables
        * Contingency table marginal sums
        * Contingency table expected frequencies
        * Runs and count of runs


    --- Code
    https://github.com/pranab/beymani
    https://github.com/topics/hypothesis-testing?l=python&o=desc&s=stars
    https://pypi.org/project/pysie/#description



    Hypothesis testing using utilmy.ipynb

    https://colab.research.google.com/drive/1yIucO552adP4DaWhKvokIYrTuytHLUcS

    importpandas as pd
    import numpy as np
    import utilmy.stats.hypothesis as test
    import utilmy.stats.statistics as stats


    - 1) Mc Nemar Test

    - create random sample data
    data = [['Toyota', 'Toyota'] for i in range(55)] + \
           [['Toyota', 'Mitsubishi'] for i in range(5)] + \
           [['Mitsubishi', 'Toyota'] for i in range(15)] + \
           [['Mitsubishi', 'Mitsubishi'] for i in range(25)]
    df = pd.DataFrame(data, columns = ['Before Ad Screening', 'After Ad Screening'])

    - create contingency table
    data_crosstab = pd.crosstab(df['Before Ad Screening'],
                                df['After Ad Screening'],
                                margins=True, margins_name="Total")
    data_crosstab

    -P0 : The true proportion of customers who prefer Toyota before the ad screening
    -P1 : The true proportion of customers who prefer Toyota after the ad screening
    -To test:
    -H0 : P1 = P2
    -H1 : P1 != P2

    m = test.contingency.McNemarTest([[25, 5], [15, 55]], continuity=True)
    m.test_summary
    - As p-value < 0.05, we reject H0.
    - True proportion of customers who prefer Toyota before and after the ad screening is not the same, at 5% significant level.

    - 2) Chi-square Test

    - Let's say we're testing whether a die is fair or not.
    - H0: Die is fair
    - H1: Die is unfair

    np.random.seed(10)
    die_roll = [np.random.randint(1, 7) for _ in range(100)]
    observed = pd.Series(die_roll).value_counts()
    observed

    ch = test.gof.ChiSquareTest(observed)
    ch.test_summary
    - P-value = 0.2942 > 5% level of significance, we fail to reject H0.
    - We don't have enough statistical evidence that die is unfair.

    - 3) Student's t-test

    np.random.seed(10)
    Population = [np.random.randint(10, 100) for _ in range(1000)]
    Sample = [np.random.randint(11, 99) for _ in range(25)]
    Population_Mean = round(sum(Population)/len(Population))
    Population_Mean

    - To test whether sample has come from a population with mean 54
    - H0: μ = 54
    - H1: μ != 54

    ttest = test.hypothesis.tTest(Sample, mu = Population_Mean)
    ttest.test_summary

    - As p-value is < 5% Level of significance, we reject H0.
    - The sample has not come from a population with mean 54.

    - 4) Kruskal Wallis Test

    np.random.seed(10)
    - generate three independent samples
    data1 = 5 * np.random.randn(100) + 50
    data2 = 5 * np.random.randn(100) + 50
    data3 = 5 * np.random.randn(100) + 50

    - To test: Whether the three distributions are similar or not
    - H0: All sample distribution are similar
    - H1: Atleast one pair of sample distributions is different

    kw = test.nonparametric.KruskalWallis(data1, data2, data3)
    kw.test_summary

    - p-value > 5% level of significance. Thus, fail to reject H0
    - No statistical evidence to prove that the sample distributions are different.

    - 5) Shapiro - Wilk test for normality

    weight = np.random.triangular(left = 40, right = 70, mode = 60, size = 1000)
    roll = [i for i in range(1000)]
    df = pd.DataFrame({
        "Movie": roll,
        "Weight": weight
        })

    df.head()

    - To test: Whether the marks are normally distributed.
    - H0: Distribution is normally distributed.
    - H1: Distribution is not normally distributed.

    stats.test_normality2(df, "Weight", "Shapiro")

    - p-value is 0, reject H0.
    - The distribution of weight is not normal.

    - 6) ANOVA

    - Time (in minutes) to solve a puzzle
    - Grouped based on what beverage they drank before solving
    coffee = [8,20,26,36,39,23,25,28,27,25]
    coke = [25,26,27,29,25,23,22,27,29,21]
    tea = [14,25,23,27,28,21,26,30,31,34]

    - To test whether there is variation in solving time based on beverage intake
    - H0: No variation in the solving time based on the beverages
    - H1: Variation in the solving time based on the beverages

    aov = test.aov.AnovaOneWay(coffee, tea, coke)
    aov.test_summary

    - As p-value > 0.05, we fail to reject H0
    - No significant statistical evidence to prove variation in the three groups.

    - 7) Friedman Test

    group1 = [4, 6, 3, 4, 3, 2, 2, 7, 6, 5]
    group2 = [5, 6, 8, 7, 7, 8, 4, 6, 4, 5]
    group3 = [2, 4, 4, 3, 2, 2, 1, 4, 3, 2]

    - Test whether the samples are same
    - H0: Mean for each population is equal
    - H1: Atleast one population mean is different

    Friedman = test.nonparametric.FriedmanTest(group1, group2, group3, group = None)
    Friedman.test_summary

    - P-value < 5%. Reject H0
    - Atleast one population mean is different.

    - 8) WaldWolfowitz

    data1 = [20, 55, 29, 24, 75, 56, 31, 45]
    data2 = [23, 8, 24, 15, 8, 6, 15, 15, 21, 23, 16, 15, 24, 15, 21, 15, 18, 14, 22, 15, 14]

    - Test whether the samples are same
    - H0: The two samples are same
    - H1: The two samples are different

    ww = test.nonparametric.WaldWolfowitz(x = data1, y = data2)
    ww.test_summary

    - P-value > 5%. Fail to Reject H0
    - Data may be similar.

    - 9) Cochran's Q test

    - three columns for 3 sessions
    - 1 represents depression
    - 0 represents no more depression

    cases = np.array([[0, 0, 0],
                      [1, 0, 0],
                      [1, 1, 0],
                      [1, 1, 1]])

    count = np.array([ 6,  16, 4,  2])
    data = np.repeat(cases, count, 0)
    data[:,0]

    -Is there a difference in depression cases over the 3 subsequent courses of therapy
    - H0: No difference in depression cases
    - H1: Difference in depression cases

    cq = test.contingency.CochranQ(data[:,0],data[:,1],data[:,2])
    cq.test_summary

    - p-value < 0.05. There is a statistical difference in the batches of patients
    - experiencing depression and no depression between the different number of sessions.

    - 10 Mann Whitney Test

    - create dataframe
    - for 'Vegan', 1 stands for vegan food.
    data = pd.DataFrame({'Vegan':[1,1,1,0,0,0,1,0,1,0,1,0],
                                'Stars':[5.0,2.5,1.5,3.5,4.75,3.0,4.0,3.0,3.0,2.75,1.0,1.0]})
    data.head()

    - Is there difference in ratings for vegan and non-vegan food?
    - H0: No difference in the stars
    - H0: There is a difference in stars

    mw = test.nonparametric.MannWhitney(group=data.Vegan, y1=data.Stars)
    mw.test_summary

    - With a p-value > 0.05, we fail to reject the null hypothesis that there is no
    - difference in rating between vegan and non-vegan food.

    ```

    If follows normal distrbution :  Shapiro-Wilk Test


    Tests whether two samples have a linear relationship.  : Pearson test

    2 samples have Monotonic relationship :  Spearman’s Rank Correlation



    Chi-Squared Test
    Tests whether two categorical variables are related or independent.




    Augmented Dickey-Fuller Unit Root Test
    Tests whether a time series has a unit root, e.g. has a trend or more generally is autoregressive.



    Student’s t-test
    Tests whether the means of two independent samples are significantly different.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample are normally distributed.
    Observations in each sample have the same variance.
    Interpretation

    H0: the means of the samples are equal.






    Paired Student’s t-test
    Tests whether the means of two paired samples are significantly different.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample are normally distributed.
    Observations in each sample have the same variance.
    Observations across each sample are paired.
    Interpretation

    H0: the means of the samples are equal.








    Analysis of Variance Test (ANOVA)
    Tests whether the means of two or more independent samples are significantly different.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample are normally distributed.
    Observations in each sample have the same variance.
    Interpretation

    H0: the means of the samples are equal.




    Nonparametric Statistical Hypothesis Tests
    Mann-Whitney U Test
    Tests whether the distributions of two independent samples are equal or not.

    Assumptions
    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample can be ranked.

    Interpretation
    H0: the distributions of both samples are equal.







    Wilcoxon Signed-Rank Test
    Tests whether the distributions of two paired samples are equal or not.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample can be ranked.
    Observations across each sample are paired.
    Interpretation

    H0: the distributions of both samples are equal.





    Kruskal-Wallis H Test
    Tests whether the distributions of two or more independent samples are equal or not.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample can be ranked.
    Interpretation

    H0: the distributions of all samples are equal.





    Friedman Test
    Tests whether the distributions of two or more paired samples are equal or not.

    Assumptions

    Observations in each sample are independent and identically distributed (iid).
    Observations in each sample can be ranked.
    Observations across each sample are paired.
    Interpretation

    H0: the distributions of all samples are equal.




"""
import os, sys, pandas as pd, numpy as np
from tqdm import tqdm
from typing import List, Union
from scipy import stats
from box import Box


from utilmy.utilmy_base import pd_generate_data
from utilmy.prepro.util_feature import  pd_colnum_tocat, pd_colnum_tocat_stat
import utilmy.stats.hypothesis as test




#################################################################################################
from utilmy.utilmy_base import log, log2

def help():
    from utilmy import help_create
    print(help_create(__file__) )


#################################################################################################
def test_all():
    test1()



def test4():
    from utilmy import adatasets  as da
    df = da.test_dataset_classifier_fake(nrows=100)

    Xtrain, Xtest =da.train_test_split(df,0.5)


    def test():
        log("Testing normality...")
        from utilmy.stats  import statistics as m
        hypopred_error_test_normality(df["yield"])


        df1 = pd_generate_data(7, 100)
        m.test_anova(df1,'cat1','cat2')
        m.hypotest_is_normal_distribution(df1, cols=df.columns[0])
        m.test_plot_qqplot(df1, '1')


        log("Testing heteroscedacity...")
        log(m.hypopred_error_test_heteroscedacity(Xtest[:,0], Xtrain[:,1]))


        log("Testing test_mutualinfo()...")
        df1 = pd_generate_data(7, 100)
        m.hypopred_error_test_residual_mutualinfo(df1["0"], df1[["1", "2", "3"]],)

        log("Testing hypothesis_test()...")
        X1 = np.random.random(100)
        X2 = np.random.random(100)
        log(m.hypotest_independance(X1, X2))

    def custom_stat(values, axis=1):
        #stat_val = np.mean(np.asmatrix(values),axis=axis)
        # stat_val = np.std(np.asmatrix(values),axis=axis)p.mean
        stat_val = np.sqrt(np.mean(np.asmatrix(values*values),axis=axis))
        return stat_val

    def test_estimator():
        log("Testing estimators()...")
        ypred = np.random.random(100)
        log(confidence_interval_normal_std(ypred))
        log(confidence_interval_boostrap_bayes(ypred))
        confidence_interval_bootstrap(ypred, custom_stat=custom_stat)


    def test_np_utils():
        log("Testing np_utils ...")
        from utilmy.stats.statistics import np_col_extractname, np_conv_to_one_col, np_list_remove
        import numpy as np
        arr = np.array([[1, 2, 3], [4, 5, 6]])
        np_col_extractname(["aa_","bb-","cc"])
        np_list_remove(arr,[1,2,3], mode="exact")
        np_conv_to_one_col(arr)

    test()
    test_estimator()
    #test_drift_detect()
    test_np_utils()


def test0():
    """ .
    """
    df = pd_generate_data(7, 100)
    test_anova(df, 'cat1', 'cat2')
    hypotest_is_normal_distribution(df, '0', "Shapiro")
    test_plot_qqplot(df, '1')
    '''TODO: import needed
    NameError: name 'pd_colnum_tocat' is not defined
    test_mutualinfo(df["0"],df[["1","2","3"]],colname="test")
    '''


def test1():
    """
    """
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.model_selection import train_test_split
    from utilmy import adatasets as ad

    df = ad.test_dataset_classifier_fake(500)
    model = DecisionTreeRegressor(random_state=1)
    y = df['y'] ; del df['y']
    X = df.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)
    model.fit(X_train, y_train)
    ypred = model.predict(X_test)

    hypopred_error_test_normality(df["y"])
    log(hypopred_error_test_heteroscedacity(y_test, ypred))
    #log(hypotest_is_all_independant(X_train, X_test))
    log(confidence_interval_normal_std(ypred))
    log(confidence_interval_boostrap_bayes(ypred))



def test3():
    """ .

    """
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    np_col_extractname(["aa_","bb-","cc"])
    np_list_remove(arr,[1,2,3], mode="exact")
    np_conv_to_one_col(arr)


def test_check_mean():
    """function test_check_mean.
    Doc::

    """
    n = 100
    df = pd.DataFrme({'id' :  np.arange(0, n)})
    df['c1'] = np.random.random(n )
    df['c2'] = np.random.random(n )
    df['c3'] = np.random.random(n )
    df['c4'] = np.random.random(n )
    df['c5'] = np.random.random(n )


    log("##- 2 columns")
    hypotest_is_mean_equal(df, cols = ['c1', 'c2'],  alpha=0.05)


    log("##- 5 columns ")
    hypotest_is_mean_equal(df, cols=['c1', 'c2', 'c3', 'c4', 'c5'],  alpha=0.05)


    log("##- 6 columsn not same")
    df['d6'] = np.random.random(n ) +0.3
    hypotest_is_mean_equal(df, cols=['c1', 'c2', 'c3', 'c4', 'd6'],  alpha=0.05)



###############################################################################################
#########- Helpers on test  ###################################################################
def hypotest_rconclusion(p_value, alpha=0.05, res=None ):
    """ Conclusion  """
    log("Test summary", res)
    log(f"""\nP-value = {p_value} ,   P-critical = {alpha}""")
    if p_value <= alpha: s, concl = "<=", "reject"
    else: s, concl = ">", "accept"
    log(f"""As {round(p_value, 2)} {s} {alpha}, we {concl} H0\n""")



def hypotest_is_1_mean_equal_fixes(df, col='mycol', mean_target=4, alpha=0.05):
    """- To test whether sample has come from a population with mean 54
    Docs::

        - H0: μ = 54     AND  - H1: μ != 54
        ##- One sample test (parameter estimation)
        Population = [np.random.randint(10, 100) for _ in range(1000)]
        Sample = [np.random.randint(11, 99) for _ in range(25)]
        Population_Mean = round(sum(Population)/len(Population))
    """
    if isinstance(df, pd.DataFrame):  samples = df[col].values
    else :                            samples = df  ##- list

    log("""1) Student's t-test (One sample)""")
    log(f"{col} has to be normally distributed and independent sample\n")
    dd = test.hypothesis.tTest(samples, mu = mean_target)
    hypotest_rconclusion(dd.p_value, alpha=alpha,   res=dd.test_summary )
    return dd



def hypotest_is_2_mean_equal(df_or_2dlist, cols=None, alpha=0.05) :
    """ 2 samples tests, H0: The two samples are same
    Docs ::

        hypotest_is_2_mean_equal(df_or_2dlist, cols=['col1', 'col2'], alpha=0.05)


    """
    ddict= Box({})
    if isinstance(df_or_2dlist, pd.DataFrame): v1, v2 = df_or_2dlist[cols[0]].values, df_or_2dlist[cols[1]].values
    else :                                     v1, v2 = df_or_2dlist[0], df_or_2dlist[1]  ##- list of lists


    log("WaldWolfowitz test is used when response variable is dichotomous")
    dd = test.nonparametric.WaldWolfowitz(x = v1, y = v2)
    ddict.waldo = dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha= alpha,  res=dd.test_summary  )


    log("For Studen-t 2 samples test the columns have to be approx. normally distributed and independent with equal variances")
    dd = test.hypothesis.tTest(v1, v2)
    ddict.student = dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha=alpha,  res=dd.test_summary )

    return ddict



def hypotest_is_all_means_equal(df, cols = None, alpha=0.05):
    """- To test whether All columns have same means.

    """
    vlist = []
    if isinstance(df, pd.DataFrame):
        if cols == None:
          cols = df.columns
        for coli in cols:
            vlist.append(df[coli].values)
    elif isinstance(df, list):
       vlist = df

    ddict = Box({})

    log("For ANOVA, The samples should be independent and normally distributed.")
    dd = test.aov.AnovaOneWay(*vlist)
    ddict.anova = dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha=alpha, res= dd.test_summary )


    log("Friedman test assumes same subjects show up in each group")
    dd = test.nonparametric.FriedmanTest(*vlist, group = None)
    ddict.friedman  =dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha=alpha, res= dd.test_summary )


    log("Cochran's Q test is applicable when response variable can only take two values")
    dd = test.contingency.CochranQ(*vlist)
    ddict.cochran = dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha=alpha, res= dd.test_summary )

    return ddict



def hypotest_is_all_group_means_equal(df, cols=['col_group', 'val'], alpha=0.05):
    """- To test whether All columns have same means.
    Docs::

        - Is there difference in ratings for vegan and non-vegan food?
        - H0: No difference in the stars
        - H0: There is a difference in stars
        - create dataframe
        - for 'Vegan', 1 stands for vegan food.
        data = pd.DataFrame({'Vegan':[1,1,1,0,0,0,1,0,1,0,1,0],
                                    'Stars':[5.0,2.5,1.5,3.5,4.75,3.0,4.0,3.0,3.0,2.75,1.0,1.0]})
        data.head()

        - With a p-value > 0.05, we fail to reject the null hypothesis that there is no
        - difference in rating between vegan and non-vegan food.
    """
    vlist = []
    if isinstance(df, pd.DataFrame):
        for coli in cols:
            vlist.append(df[coli].values)

    elif isinstance(df, list):
       vlist = df
    ddict = Box({})

    log("Mann Whitney Test")
    log("Observations should not be normally distributed and groups should be independent")
    dd = test.nonparametric.MannWhitney(group=vlist[0], y1=vlist[1] )
    ddict.mann = dd
    hypotest_rconclusion(dd.p_value, alpha=alpha, res = dd.test_summary)
    return ddict



def hypotest_is_mean_pergroup_equal(df, col1=None, col2=None, alpha = 0.05):
    """
    Docs ::

        - create random sample data
        data = [['Toyota', 'Toyota'] for i in range(55)] + \
            [['Toyota', 'Mitsubishi'] for i in range(5)] + \
            [['Mitsubishi', 'Toyota'] for i in range(15)] + \
            [['Mitsubishi', 'Mitsubishi'] for i in range(25)]
        df = pd.DataFrame(data, columns = ['Before Ad Screening', 'After Ad Screening'])

        - create contingency table
        data_crosstab = pd.crosstab(df['Before Ad Screening'],
                                    df['After Ad Screening'],
                                    margins=True, margins_name="Total")
        data_crosstab
        #P0 : The true proportion of customers who prefer Toyota before the ad screening
        #P1 : The true proportion of customers who prefer Toyota after the ad screening
        #To test:
        #H0 : P1 = P2
        #H1 : P1 != P2

    """
    if col1 == None or col2 == None:
      col1, col2 = df.columns

    data = pd.crosstab(df[col1], df[col2])
    v1, v2 = df[col1].unique()
    log("#- 1) Mc Nemar Test")
    log(f"Assumption: {col1} is dichotomous variable and {col2} is independent variable with two connected groups")
    m = test.contingency.McNemarTest([data[v1], data[v2]], continuity=True)
    hypotest_rconclusion(m.mcnemar_p_value, alpha=alpha,res= m.test_summary )



def hypotest_is_mean_equal(df: pd.DataFrame, cols=None,  alpha=0.05) :
    """Test if same mean for all columns
    Doc::

       https://towardsdatascience.com/why-is-anova-essential-to-data-science-with-a-practical-example-615de10ba310
    """
    p_values = []
    cols = df.columns  if cols is None else cols

    if len(cols) == 2:
        ddict = hypotest_is_2_mean_equal(df, cols=cols, alpha= alpha)

    else :   ##> 3 values
        ddict = hypotest_is_all_means_equal(df, cols, alpha=alpha)



###############################################################################################
def hypotest_is_all_same_distribution(df, cols = None):
    """Tests to determine if data distributions are similar or not
     Docs::

        np.random.seed(10)
        - generate three independent samples
        data1 = 5 * np.random.randn(100) + 50
        data2 = 5 * np.random.randn(100) + 50
        data3 = 5 * np.random.randn(100) + 50

        - To test: Whether the three distributions are similar or not
        - H0: All sample distribution are similar
        - H1: Atleast one pair of sample distributions is different
    """
    vlist = []
    if isinstance(df, pd.DataFrame):
      if cols == None:
        cols = df.columns
      for coli in cols:
        vlist.append(df[coli].values)

    elif isinstance(df, list):
       vlist = df
    ddict = Box({})

    log("""- 1) Kruskal Wallis Test""")
    log("If not normally distributed, use KruskalWallis")
    kw = test.nonparametric.KruskalWallis(*vlist)
    ddict.KruskalWallis = kw.test_summary
    hypotest_rconclusion(kw.p_value, alpha=0.05, res=kw.test_summary )


    log("""- 2) ANOVA""")
    log("If normally distributed, use ANOVA")
    dd = test.aov.AnovaOneWay(*vlist)
    ddict.anova = dd.test_summary
    hypotest_rconclusion(dd.p_value, alpha=0.05, res = dd.test_summary )

    return ddict


def hypotest_independance(df: pd.DataFrame, cols=None, threshold=0.1) -> List[float]:
    """Run ANOVA Test of independance.
    Doc::


    """
    p_values = []
    cols = df.columns  if cols is None else cols

    p_values = test_anova(df, cols)

    return p_values



def hypotest_independance_Xinput_vs_ytarget(df: pd.DataFrame, colsX=None, coly='y', ) :
    """Run multiple T tests of Independance.
    Doc::

               p_values = multiple_comparisons(data)
    """
    p_values = []
    colsX = df.columns  if colsX is None else colsX
    for c in colsX:
        if c.startswith(coly):
            continue
        group_a = df[df[c] == 0][coly]
        group_b = df[df[c] == 1][coly]

        _, p = stats.ttest_ind(group_a, group_b, equal_var=False)
        p_values.append((c, p) )

    return p_values



def hypotest_is_normal_distribution(df:pd.DataFrame, column,):
    """.
    Doc::

            Function to check Normal Distribution of a Feature by 3 methods
            Input dfframe, feature name, and a test type
            Three types of test
            1)'Shapiro'
            2)'Normal'
            3)'Anderson'

            output the statistical test score and result whether accept or reject
            Accept mean the feature is Gaussain
            Reject mean the feature is not Gaussain
    """
    from scipy.stats import shapiro, normaltest, anderson

    log('Shapiro')
    stat, p = shapiro(df[column])
    log('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:    log(column,' looks Gaussian (fail to reject H0)')
    else:            log(column,' does not look Gaussian (reject H0)')


    log('Normal')
    stat, p = normaltest(df[column])
    log('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha: log(column,' looks Gaussian (fail to reject H0)')
    else:         log(column,' does not look Gaussian (reject H0)')


    log('Anderson')
    result = anderson(df[column])
    log('Statistic: %.3f' % result.statistic)
    p = 0
    for i in range(len(result.critical_values)):
        sl, cv = result.significance_level[i], result.critical_values[i]
        if result.statistic < result.critical_values[i]:
            log(sl,' : ',cv,' ',column,' looks normal (fail to reject H0)')
        else:
            log(sl,' : ',cv,' ',column,' does not looks normal (fail to reject H0)')




def hypotest_bonferoni_adjuster(p_values, threshold=0.1):
    """Bonferroni correction.
    Doc::

        log('Total number of discoveries is: {:,}'  .format(sum([x[1] < threshold / n_trials for x in p_values])))
        log('Percentage of significant results: {:5.2%}'  .format(sum([x[1] < threshold / n_trials for x in p_values]) / n_trials))

        - Benjamini–Hochberg procedure
        p_values.sort(key=lambda x: x[1])

        for i, x in enumerate(p_values):
            if x[1] >= (i + 1) / len(p_values) * threshold:
                break
        significant = p_values[:i]

        log('Total number of discoveries is: {:,}' .format(len(significant)))
        log('Percentage of significant results: {:5.2%}'.format(len(significant) / n_trials))
    """
    p_values.sort(key=lambda x: x[1])
    for i, x in enumerate(p_values):
        if x[1] >= (i + 1) / len(p_values) * threshold:
            break
    pvalues_significant = p_values[:i]
    return pvalues_significant





#################################################################################################
###########- Actual tests########################################################################
def test_chisquare(df_obs:pd.DataFrame, df_true:pd.DataFrame, method='chisquare', **kw):
    """ Hypothesis betweeb Obs and true values.
    Doc::
                https://github.com/aschleg/hypothetical/blob/master/tests/test_contingency.py
    """
    if method == 'chisquare' :
        c = test.contingency.ChiSquareContingency(df_obs, df_true)
        return c



def test_anova(df:pd.DataFrame, col1, col2):
    """.
    Doc::

            ANOVA test two categorical features
            Input dfframe, 1st feature and 2nd feature
    """
    import scipy.stats as stats

    ov=pd.crosstab(df[col1],df[col2])

    dfb       = df[[col1, col2]]
    groups    = dfb.groupby(col1).groups
    edu_class = dfb[col2]
    lis_group = groups.keys()
    lg=[]
    for i in groups.keys():
        globals()[i]  = edu_class[groups[i]].values
        lg.append(globals()[i])

    dfd = 0
    for m in lis_group:
        dfd=len(m)-1+dfd
    print(stats.f_oneway(*lg))

    stat_val = stats.f_oneway(*lg)[0]
    crit_val = stats.f.ppf(q=1-0.05, dfn=len(lis_group)-1, dfd=dfd)
    if stat_val >= crit_val :
         print('Reject null hypothesies and conclude that atleast one group is different and the feature is releavant to the class.')
    else:
         print('Accept null hypothesies and conclude that atleast one group is same and the feature is not releavant to the class.')
    return { 'stat_val': stat_val, 'crit_val': crit_val  }



def test_plot_qqplot(df:pd.DataFrame, col_name):
    """.
    Doc::

            Function to plot boxplot, histplot and qqplot for numerical feature analyze
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.api as sm
    fig, axes = plt.subplots(1, 3, figsize=(18,5))
    fig.suptitle('Numerical Analysis'+" "+col_name)
    sns.boxplot(ax=axes[0], data=df,x=col_name)
    sns.histplot(ax=axes[1],data=df, x=col_name, kde=True)
    sm.qqplot(ax=axes[2],data=df[col_name], line ='45')
    print(df[col_name].describe())



def test_mutualinfo(error, Xtest, colname=None, bins=5):
    """.
    Doc::

               Test  Error vs Input Variable Independance byt Mutual ifno
               sklearn.feature_selection.mutual_info_classif(X, y, discrete_features='auto', n_neighbors=3, copy=True, random_state=None)

    """
    from sklearn.feature_selection import mutual_info_classif
    error = pd.DataFrame({"error": error})
    error_dis, _ = pd_colnum_tocat(error, bins=bins, method="quantile")
    - print(error_dis)

    res = mutual_info_classif(Xtest.values, error_dis.values.ravel())

    return dict(zip(colname, res))




####################################################################################################
###########- Residual error ########################################################################
def hypopred_independance_Xinput_vs_ytarget(df: pd.DataFrame, colsX=None, coly='y',  threshold=0.1) -> List[float]:
    """Run multiple T tests of Independance.
    Doc::

               p_values = multiple_comparisons(data)
    """
    p_values = []
    colsX = df.columns  if colsX is None else colsX
    for c in colsX:
        if c.startswith(coly):
            continue
        group_a = df[df[c] == 0][coly]
        group_b = df[df[c] == 1][coly]

        _, p = stats.ttest_ind(group_a, group_b, equal_var=False)
        p_values.append((c, p) )

    return p_values



def hypopred_error_test_heteroscedacity(ypred: np.ndarray, ytrue: np.ndarray, pred_value_only=1):
    """function test_heteroscedacity.
    Doc::

            Args:
                ytrue:
                ypred:
                pred_value_only:
            Returns:

    """
    ss = """
       Test  Heteroscedacity :  Residual**2  = Linear(X, Pred, Pred**2)
       F pvalues < 0.01 : Null is Rejected  ---> Not Homoscedastic
       het_breuschpagan

    """
    from statsmodels.stats.diagnostic import het_breuschpagan, het_white
    error    = ypred - ytrue

    ypred_df = pd.DataFrame({"pcst": [1.0] * len(ytrue), "pred": ypred, "pred2": ypred * ypred})
    labels   = ["LM Statistic", "LM-Test p-value", "F-Statistic", "F-Test p-value"]
    test1    = het_breuschpagan(error * error, ypred_df.values)
    test2    = het_white(error * error, ypred_df.values)
    ddict    = {"het-breuschpagan": dict(zip(labels, test1)),
             "het-white": dict(zip(labels, test2)),
             }

    return ddict


def hypopred_error_test_normality(ypred: np.ndarray, ytrue: np.ndarray, distribution="norm", test_size_limit=5000):
    """.
    Doc::

               Test  Is Normal distribution
               F pvalues < 0.01 : Rejected

    """
    from scipy.stats import shapiro, anderson, kstest


    error2 = ypred -  ytrue

    error2 = error2[np.random.choice(len(error2), 5000)]  # limit test
    test1  = shapiro(error2)
    ddict1 = dict(zip(["shapiro", "W-p-value"], test1))

    test2  = anderson(error2, dist=distribution)
    ddict2 = dict(zip(["anderson", "p-value", "P critical"], test2))

    test3  = kstest(error2, distribution)
    ddict3 = dict(zip(["kstest", "p-value"], test3))

    ddict  = dict(zip(["shapiro", "anderson", "kstest"], [ddict1, ddict2, ddict3]))

    return ddict


def hypopred_error_test_residual_mutualinfo(dfX:pd.DataFrame, ypred: np.ndarray, ytrue: np.ndarray, colsX=None, bins=5):
    """.
    Doc::

               Test  Error vs Input X Variable Independance byt Mutual ifno
               sklearn.feature_selection.mutual_info_classif(X, y, discrete_features='auto', n_neighbors=3, copy=True, random_state=None)

    """
    from sklearn.feature_selection import mutual_info_classif
    dferror = pd.DataFrame({"error": ypred - ytrue })
    error_dis, _ = pd_colnum_tocat(dferror, bins=bins, method="quantile")
    # print(error_dis)

    colsX = colsX if colsX is not None else dfX.columns
    dfX = dfX[colsX].values
    res = mutual_info_classif(dfX, error_dis.values.ravel())

    return dict(zip(colsX, res))






####################################################################################################
########- Confidence interval ######################################################################
def confidence_interval_normal_std(err:np.ndarray, alpha=0.05, ):
    """function estimator_std_normal.
    Doc::

            Args:
                err:
                alpha:   confidence level
                :
            Returns:   std_err,

    """
    # estimate_std( err, alpha=0.05, )
    from scipy import stats
    n = len(err)  # sample sizes
    s2 = np.var(err, ddof=1)  # sample variance
    df = n - 1  # degrees of freedom
    upper = np.sqrt((n - 1) * s2 / stats.chi2.ppf(alpha / 2, df))
    lower = np.sqrt((n - 1) * s2 / stats.chi2.ppf(1 - alpha / 2, df))

    return np.sqrt(s2), (lower, upper)


def confidence_interval_boostrap_bayes(err:np.ndarray, alpha=0.05, ):
    """function estimator_boostrap_bayes.
    Doc::

            Args:
                err:
                alpha:
                :
            Returns:

    """
    from scipy.stats import bayes_mvs
    mean, var, std = bayes_mvs(err, alpha=alpha)
    return mean, var, std


def confidence_interval_bootstrap(err:np.ndarray, custom_stat=None, alpha=0.05, n_iter=10000):
    """.
    Doc::

              def custom_stat(values, axis=1):
              - stat_val = np.mean(np.asmatrix(values),axis=axis)
              - stat_val = np.std(np.asmatrix(values),axis=axis)p.mean
              stat_val = np.sqrt(np.mean(np.asmatrix(values*values),axis=axis))
              return stat_val
    """
    try :
       import bootstrapped.bootstrap as bs
    except:
        log('pip install bootsrapped') ; 1/0
    res = bs.bootstrap(err, stat_func=custom_stat, alpha=alpha, num_iterations=n_iter)
    return res




####################################################################################################
######- Utils ######################################################################################
def np_col_extractname(col_onehot):
    """.
    Doc::

            Column extraction from onehot name
            col_onehotp
            :return:
    """
    colnew = []
    for x in col_onehot:
        if len(x) > 2:
            if x[-2] == "_":
                if x[:-2] not in colnew:
                    colnew.append(x[:-2])

            elif x[-2] == "-":
                if x[:-3] not in colnew:
                    colnew.append(x[:-3])

            else:
                if x not in colnew:
                    colnew.append(x)
    return colnew


def np_list_remove(cols, colsremove, mode="exact"):
    """.
    Doc::

    """
    if mode == "exact":
        for x in colsremove:
            try:
                cols.remove(x)
            except BaseException:
                pass
        return cols

    if mode == "fuzzy":
        cols3 = []
        for t in cols:
            flag = 0
            for x in colsremove:
                if x in t:
                    flag = 1
                    break
            if flag == 0:
                cols3.append(t)
        return cols3


def np_conv_to_one_col(np_array, sep_char="_"):
    """.
    Doc::

            converts string/numeric columns to one string column
            np_array: the numpy array with more than one column
            sep_char: the separator character
    """
    def row2string(row_):
        return sep_char.join([str(i) for i in row_])

    np_array_=np.apply_along_axis(row2string,1,np_array)
    return np_array_[:,None]



if __name__ == '__main__':
    import fire
    fire.Fire()


