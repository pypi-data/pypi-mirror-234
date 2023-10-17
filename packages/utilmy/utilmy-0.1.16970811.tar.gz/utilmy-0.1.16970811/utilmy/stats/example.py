# -*- coding: utf-8 -*-
"""Hypothesis testing using utilmy.ipynb
Docs ::

        https://colab.research.google.com/drive/1yIucO552adP4DaWhKvokIYrTuytHLUcS
"""
import pandas as pd
import numpy as np
import utilmy.stats.hypothesis as test
import utilmy.stats.statistics as stats
from box import Box

from utilmy import log



##################################################################################




### Test for checking goodness of fit
"""# 1) Chi-square Test"""

# Let's say we're testing whether a die is fair or not.
# H0: Die is fair
# H1: Die is unfair

np.random.seed(10)
die_roll = [np.random.randint(1, 7) for _ in range(100)]
observed = pd.Series(die_roll).value_counts()
observed

ch = test.gof.ChiSquareTest(observed)
ch.test_summary
# P-value = 0.2942 > 5% level of significance, we fail to reject H0. 
# We don't have enough statistical evidence that die is unfair.



