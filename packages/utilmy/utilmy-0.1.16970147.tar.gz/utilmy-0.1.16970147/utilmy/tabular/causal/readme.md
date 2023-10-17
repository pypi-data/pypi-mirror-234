```














Structure learning


causica methods.

https://github.com/microsoft/showwhy



https://causal-learn.readthedocs.io/en/latest/search_methods_index/index.html



https://github.com/ignavierng/golem

https://github.com/ignavierng/golem/blob/main/src/golem.py#L50


https://github.com/huawei-noah/trustworthyAI/tree/master/gcastle





https://benchpressdocs.readthedocs.io/en/latest/available_structure_learning_algorithms.html


https://causalpy.readthedocs.io/en/latest/



https://medium.com/@felixleopoldorios/structure-learning-using-benchpress-826847db0aa8

https://github.com/felixleopoldo/benchpress


Python causal ecosystem grows rapidly. While writing my book (https://causalpython.io) I analyzed it thoroughly, looking for packages that have stable support, enthusiastic contributors and simply do their job. Here are my four recommendations:

⭕ 𝗗𝗼𝗪𝗵𝘆 (https://lnkd.in/dcZ_YkzV)
This package originally from Microsoft Research has now moved to an independent project. Provides a unified interface for causal inference using structural causal models, graphical models, and more. It has a user-friendly API and can handle both observational and experimental data. Very comprehensive! A great candidate for the Sci-kit Learn of Causality!
Learn DoWhy - check the blog post! (https://lnkd.in/d3x9t5Yv)

⭕ 𝗘𝗰𝗼𝗻𝗠𝗟 (https://lnkd.in/dumHpNx8)
DoWhy’s sister package built with conditional treatment effect estimation in mind. Supported by Microsoft. Integrates smoothly with DoWhy’s casual flow, whichj is a great advantage! The greatest competitor of another amazing package - Uber’s CausalML

⭕ 𝗴𝗖𝗮𝘀𝘁𝗹𝗲 (https://lnkd.in/ezRq5QkS)
A causal discovery super-hero! Supported by Huawei, it’s the only package out there that implements the most recent causal discovery and causal structure learning methods, including gradient-based and reinforcement-learning-based stuff! Great for benchmarking.
Want to learn more? - Check the blog post! (https://lnkd.in/duqJmBaZ)

⭕ 𝗖𝗮𝘂𝘀𝗮𝗹𝗣𝘆 (https://lnkd.in/dVQu93PH)
A new kid on the block released less than two months ago. CausalPy is based on PyMC Labs' PyMC - a well-established probabilistic programming framework in Python. CausalPy has been developed by PyMC’s prolific Dr Benjamin Vincent with contributions from Wolt’s excellent data scientist Juan Camilo Orduz. CausalPy implements a bunch of methods to work with quasi-experimental data. Everything in Bayesian fashion! Watch out as it’s still in beta (!) yet a great candidate for the best new causal package of 2023!






###################################################
Docs:


        https://pypi.org/project/confounds/


        https://github.com/darya-chyzhyk/confound_prediction






        Bayesian Network Learning:


        https://erdogant.github.io/bnlearn/pages/html/UseCases.html

        https://causalnex.readthedocs.io/en/latest/



        #### ShowWhy Front end usage of Causal discovery
        https://github.com/microsoft/showwhy/tree/main


        https://github.com/microsoft/causica/issues/64




        causica microsoft

        End to End causal inference


        Main issues :
        Variable explanation should not include Collider, ...
        --> Bias in estimation.




        https://github.com/microsoft/causica/blob/main/examples/multi_investment_sales_attribution.ipynb

        Double ML

        https://blog-about-people-analytics.netlify.app/posts/2023-09-03-dag-and-double-ml/

        https://colab.research.google.com/drive/1AFPuqOCwj2VVPbWNTNdHFnFrwmoBaRQR#scrollTo=BRCTTGPzsxAt



        https://proceedings.mlr.press/v218/schacht23a/schacht23a.pdf



        ### EcoML : estimate of ATE by Double Machine Learning



        ### DoWhy : test stability

        https://github.com/py-why/EconML/blob/main/notebooks/CustomerScenarios/Case%20Study%20-%20Multi-investment%20Attribution%20at%20A%20Software%20Company%20-%20EconML%20+%20DoWhy.ipynb



```