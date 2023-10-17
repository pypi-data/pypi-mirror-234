# -*- coding: utf-8 -*-
"""Copy of numpyro  conversion effect.ipynb
Docs::

    https://colab.research.google.com/drive/1N69wrHaU383V-Js3JQ4yegIKvYMrv8AZ


    python $utilmy/tabular/bayesian/abtest_inference.py   test1

    run_analysis(df_dirin=None, n_sample=200, n_warmup=1500, n_chains=1, confidence_level=0.95, device='cpu')

    !pip install utilmy
    !pip install numpy_indexed
    !pip install numpyro

"""
import os, sys
from box import Box
from typing import Tuple
import pandas as pd
from jax import random
import jax.numpy as jnp
from jax.scipy.special import expit
from jax.interpreters.xla import DeviceArray
import numpy as np
import numpyro
from numpyro.diagnostics import hpdi
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS



########################################################################################################
def test_all():
    pass


def test1():
    run_analysis(df_dirin=None, n_sample=200, n_warmup=1500, n_chains=1, confidence_level=0.95, device='cpu')



########################################################################################################
def generate_dataframe(N, pTarget=0.1, pTreatment=0.67, rng_key: DeviceArray=None):
  """
  Docs::

       N = number of samples = number of rows in the table
       pTarget and pTreatment are the proportions of 1s we need to generate for the target and treatment columns respectively

  """

  key1, key2, key3 = random.split(rng_key, 3)

  effects = {}
  effects['gender']  = dist.Bernoulli(0.5).sample(key1, sample_shape=(N, ))
  effects['religion']  = dist.Bernoulli(0.03).sample(key2, sample_shape=(N, ))
  # effects['other_effects'] = dist.Normal(0.0, jnp.ones(N)).sample(key3)

  data_dict = {}
  data_dict['target'] = np.random.choice([0, 1], size=(N,), p=[1-pTarget, pTarget]).reshape(-1,)
  data_dict['treatment'] = np.random.choice([0, 1], size=(N,), p=[1-pTreatment, pTreatment]).reshape(-1,)

  for key, value in effects.items():
    data_dict[key]  = value

  df = pd.DataFrame.from_dict(data_dict)

  return df, list(effects.keys())




def get_dataset(df: pd.DataFrame, target: str = None, treatment: str=None, covariates: list = [])-> Tuple[jnp.ndarray, jnp.ndarray]:
    """ Parse dataframe
    Docs::

        df: a dataframe with target/outcome, treatment and covariate columns

        target: the name of the target/outcome column in the dataframe df

        treatment: the name of the treatment column in the dataframe df

        All other columns will be treated as covariates

    """

    if treatment and target:
      df['treatment'] = df[[treatment]]
      df['target'] = df[[target]]
      df['target_treatment'] = df.target & df.treatment
    else:
      df['target_treatment'] = df.target & df.treatment

    treatment_array  = jnp.array(df.treatment.to_numpy())
    target_treatment = jnp.array(df.target_treatment.to_numpy())

    if len(covariates) > 0:
      stack = [jnp.array(df[covariate].to_numpy()).reshape(-1, 1) for covariate in covariates]
    else:
      stack = []


    stack.insert(0,  treatment_array.reshape(-1, 1))
    stack.insert(0,  jnp.ones((len(treatment_array), 1)))


    design_matrix = jnp.hstack(stack)

    return design_matrix, target_treatment


def model(design_matrix: jnp.ndarray, outcome: jnp.ndarray = None) -> None:
    """  Model
    Docs::

        Model definition: Log odds of making a purchase is a linear combination
        of covariates. Specify a Normal prior over regression coefficients.

        :param design_matrix: Covariates. All categorical variables have been one-hot encoded.
        :param outcome:       Binary response variable. In this case, whether or not the  customer made a purchase.
    """

    beta = numpyro.sample( "coefficients",
        dist.MultivariateNormal(  loc=0.0, covariance_matrix=jnp.eye(design_matrix.shape[1])), )
    logits = design_matrix.dot(beta)

    with numpyro.plate("data", design_matrix.shape[0]):
        numpyro.sample("obs", dist.Bernoulli(logits=logits), obs=outcome)



def plot_covariable_distribution(covariable, lower: int, upper: int, covariable_name: str = None):
  import matplotlib.pyplot as plt

  plt.figure(dpi=100)
  plt.title(f"{covariable_name}: ({lower:.2f}, {upper:.2f})")
  plt.plot(covariable)
  plt.axhline(y=lower, color='r', linestyle='--')
  plt.axhline(y=upper, color='r', linestyle='--')
  plt.show()
  return None



def print_results(coef: jnp.ndarray, interval_size: float = 0.95, covariates: list = []) -> None:
    """
    Print the confidence interval for the effect size with interval_size
    probability mass.
    """

    print(coef)
    print("\n")

    baseline_response   = expit(coef[:, 0])
    response_with_calls = expit(coef[:, 0] + coef[:, 1])

    print( response_with_calls )
    print( baseline_response )
    print("\n")

    impact_on_probability = hpdi( response_with_calls - baseline_response, prob=interval_size)

    # effect_of_gender = hpdi(coef[:, 2], prob=interval_size)


    print(
        f"There is a {interval_size * 100}% probability that calling customers "
        "increases the chance they'll make a purchase by "
        f"{(100 * impact_on_probability[0]):.2f} to {(100 * impact_on_probability[1]):.2f} percentage points."
    )

    if len(covariates) > 0:
      for i, covariate in enumerate(covariates):
        effect_of_covariate = hpdi(coef[:, 2+i], prob=interval_size)
        lower = effect_of_covariate[0]
        upper = effect_of_covariate[1]

        # if num_is_between(lower, 0, upper):
        #   print(
        #   f"There is a {interval_size * 100}% probability the effect of {covariate} on the log odds of conversion "
        #   f"lies in the interval ({lower:.2}, {upper:.2f})."
        #   f" Since this interval contains 0, we can conclude {covariate} does not impact the conversion rate."
        #   )
        # else:
        #   print(
        #   f"There is a {interval_size * 100}% probability the effect of {covariate} on the log odds of conversion "
        #   f"lies in the interval ({lower:.2}, {upper:.2f})."
        #   f" Since this interval does not contain 0, {covariate} may have an impact on the conversion rate."
        #   )

        plot_covariable_distribution(coef[:, 2+i], lower, upper, covariate)



def run_inference(design_matrix: jnp.ndarray, outcome: jnp.ndarray, rng_key: jnp.ndarray, num_warmup: int,
    num_samples: int, num_chains: int,
    interval_size: float = 0.95, covariates: list = []
) -> None:
    """
    Estimate the effect size.


    """
    kernel = NUTS(model)
    mcmc = MCMC( kernel, num_warmup=num_warmup,
        num_samples=num_samples,
        num_chains=num_chains,
        progress_bar=False if "NUMPYRO_SPHINXBUILD" in os.environ else True, )
    mcmc.run(rng_key, design_matrix, outcome)

    # 0th column is intercept (not getting called)
    # 1st column is effect of getting called
    # 2nd column is effect of gender (should be none since assigned at random)
    coef = mcmc.get_samples()["coefficients"]
    print_results(coef, interval_size, covariates)

    #### Saving All on disk



def run_analysis(df_dirin=None, n_sample=200, n_warmup=1500, n_chains=1, confidence_level=0.95, device='cpu'):
    """ Run Full analyzsiz


    """
    assert numpyro.__version__.startswith("0.9.2")
    from box import Box
    from utilmy import pd_read_file

    numpyro.set_platform(device)
    numpyro.set_host_device_count(n_chains)
    rng_key, _ = random.split(random.PRNGKey(3))


    if df_dirin is None :
        df, cov_names = generate_dataframe(N=10000, pTarget=0.3, pTreatment=0.6, rng_key=rng_key)

    elif isinstance(df_dirin, pd.DataFrame):
        df = df_dirin
        cov_names = list(df.columns).remove(['target', 'treatment'])

    elif isinstance(df_dirin, str):  #### path on disk
       df = pd_read_file(df_dirin)
       cov_names = list(df.columns).remove(['target', 'treatment'])


    design_matrix, response = get_dataset(df=df, target='target', treatment='treatment', covariates=cov_names)

    run_inference( design_matrix, response,
        rng_key,
        n_warmup,
        n_sample,
        n_chains,
        confidence_level,
        cov_names,
    )



########################################################################################################
def np_is_between(lower, num,  upper):
  is_between = (lower <= num <= upper) or (upper <= num <= lower)
  return is_between





if __name__=="__main__":
    import fire
    fire.Fire()
    # runall()

