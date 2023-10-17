"""
Linear Decision tree
Docs::

    https://towardsdatascience.com/linear-tree-the-perfect-mix-of-linear-model-and-decision-tree-2eaed21936b7


    Linear Tree Regression
    from sklearn.linear_model import LinearRegression
    from lineartree import LinearTreeRegressor
    from sklearn.datasets import make_regression
    X, y = make_regression(n_samples=100, n_features=4,
                           n_informative=2, n_targets=1,
                           random_state=0, shuffle=False)
    regr = LinearTreeRegressor(base_estimator=LinearRegression())
    regr.fit(X, y)
    Linear Tree Classification
    from sklearn.linear_model import RidgeClassifier
    from lineartree import LinearTreeClassifier
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=4,
                               n_informative=2, n_redundant=0,
                               random_state=0, shuffle=False)
    clf = LinearTreeClassifier(base_estimator=RidgeClassifier())
    clf.fit(X, y)
    Linear Forest Regression
    from sklearn.linear_model import LinearRegression
    from lineartree import LinearForestRegressor
    from sklearn.datasets import make_regression
    X, y = make_regression(n_samples=100, n_features=4,
                           n_informative=2, n_targets=1,
                           random_state=0, shuffle=False)
    regr = LinearForestRegressor(base_estimator=LinearRegression())
    regr.fit(X, y)
    Linear Forest Classification
    from sklearn.linear_model import LinearRegression
    from lineartree import LinearForestClassifier
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=4,
                               n_informative=2, n_redundant=0,
                               random_state=0, shuffle=False)
    clf = LinearForestClassifier(base_estimator=LinearRegression())
    clf.fit(X, y)
    Linear Boosting Regression
    from sklearn.linear_model import LinearRegression
    from lineartree import LinearBoostRegressor
    from sklearn.datasets import make_regression
    X, y = make_regression(n_samples=100, n_features=4,
                           n_informative=2, n_targets=1,
                           random_state=0, shuffle=False)
    regr = LinearBoostRegressor(base_estimator=LinearRegression())
    regr.fit(X, y)
    Linear Boosting Classification
    from sklearn.linear_model import RidgeClassifier
    from lineartree import LinearBoostClassifier
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=100, n_features=4,
                               n_informative=2, n_redundant=0,
                               random_state=0, shuffle=False)
    clf = LinearBoostClassifier(base_estimator=RidgeClassifier())
    clf.fit(X, y)



"""





def sklearn_tree_to_code(tree, feature_names):
    """  Export Decision Tree INTO Code

    Docs::



    """
    from sklearn.tree import _tree

    nn=0

    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    #print ("def tree({}):" .format(", " .join(feature_names)))

    def recurse(node, depth):
        indent = "    " * depth

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            table = 'X_train'
            name = table+"['"+feature_name[node]+"']"


            threshold = tree_.threshold[node]
            print ("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print ("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            def increment():
                global nn
                nn=nn+1
            increment()
            print ("{}return 'Node_{}'".format(indent, nn))

    recurse(0, 1)















