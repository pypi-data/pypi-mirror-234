""" Simulator
Docs::

   python src/simulation/simulation.py test1

   python src/simulation/simulation.py simulation_run2

"""
import time, os, sys
from typing import Dict, List, Optional, Tuple, Type, Union
from copy import deepcopy

import torch,  numpy as np, pandas as pd, fire

from src.utils.utilmy_log import log, logw
#######################################################################################



#########################################################################################################
def simulation_create_report(res:dict, dirout:str=""):
    """ Create HTML report from simulation
    Docs::

        ['clicks_algo_cum', 'creativeid_clicks_cum_0', 'creativeid_clicks_cum_1', 'creativeid_clicks_cum_2'] 
        ['clicks_algo_avg', 'creativeid_clicks_avg_0', 'creativeid_clicks_avg_1', 'creativeid_clicks_avg_2']
        log(coly1, coly2)

    """
    from utilmy import pd_to_file, date_now, os_makedirs

    df       = res['df']
    n_arms   = res['n_arms']
    proba    = res['proba_arms_expected']  #### proba  = [ 0.10, 0.15, 0.17] if proba is None else proba
    max_step = res['max_steps']


    def hash_df(df, nlen=5):
       return str(abs( hash(str(df)[:1000]) ))[:nlen]


    #### Column Selection
    coly1 = ['reward_algo_cum']  + [f"arms_reward_cum_{i}" for i in range(n_arms) ]
    coly2 = ['reward_algo_avg']  + [f"arms_reward_avg_{i}" for i in range(n_arms) ]

    #### Columns renaming
    cols = list( df.columns)
    df.columns = [ ci.replace("arms", 'creativeid').replace("reward", "clicks")  for ci in cols ]
    coly1      = [ ci.replace("arms", 'creativeid').replace("reward", "clicks")  for ci in coly1 ]
    coly2      = [ ci.replace("arms", 'creativeid').replace("reward", "clicks")  for ci in coly2 ]
    ####################################################################################################
    df['date'] =  pd.date_range("2022-01-01", periods= len(df), freq="min")


    nmax2  = max_step
    date1  = date_now(fmt="%Y%m%d")
    hashdf = f"{hash_df(df)}"

    dir0   = f"{dirout}ztmp/bandit_report/{date1}/"
    os_makedirs(dir0)



    #### df.head()
    n_arms = sum([ 1 for ci in df.columns if "_avg_" in ci ] )  # len( df['arms_reward'].values[0].split(",") )
    log('n_arms', n_arms)


    #### Save data
    tag1 = f"{str(int(time.time()))[5:]}"
    pd_to_file(df, f"{dir0}/df_{tag1}.parquet")

    ### Metrics
    ctr_list = [ np.round( 100*df[f'creativeid_clicks_avg_{i}'].values[-1], 1) for i in range(n_arms)  ]


    #######################################################################################################
    from utilmy.viz import vizhtml as vi
    doc = vi.htmlDoc(title='Analysis',css_name = "border")

    doc.h1('Simulation of one Banner Optimizer ')
    doc.h1('Data Table')
    doc.table(df.iloc[:100,:], use_datatable=True, table_id="test", custom_css_class='intro')

    doc.hr(); doc.br();doc.br();doc.br();

    doc.h1(f"""
        Simulation Assumption:<br>  
        Each creative_id (ie banner) has a FIXED CTR in %  : {ctr_list}  "
    """)


    doc.br();doc.br();doc.br();

    doc.h1('Cumulative Clicks : 1 creative_id ') 
    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate='date', date_format= None, 
                    coly1=['creativeid_clicks_cum_0'],  coly2=[],
                    title = "Cumulative click",cfg={},mode='highcharts',
                    figsize=(14,12)  )


    doc.br();  doc.hr() ; doc.br()


    doc.h1(' CTR Estimate : 1 creative_id ') 
    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate='date', date_format= None, 
                    coly1= ['creativeid_clicks_avg_0'],  coly2=[],
                    title = "CTR Estimate",cfg={},mode='highcharts',
                    figsize=(14,12)   )
    doc.hr() ;doc.br();doc.br();doc.br();doc.br();doc.br();doc.br();


    #######################################################################################################
    doc.h1( f'Cumulative Clicks :  {n_arms} different creative_id ) ') 
    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate = 'date', date_format= None, 
                    coly1   = [ f'creativeid_clicks_cum_{i}' for i in range(n_arms) ] ,    coly2=[],
                    title   = "Cumulative click",cfg={},mode='highcharts',
                    figsize = (14,12)  )

    doc.br();  doc.hr() ; doc.br()


    doc.h1( f' CTR Estimate :   {n_arms}  different creative_id ') 
    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate = 'date', date_format= None, 
                    coly1    = [ f'creativeid_clicks_avg_{i}' for i in range(n_arms) ]  ,  coly2=[],
                    title    = "CTR Estimate",cfg={},mode='highcharts',
                    figsize  = (14,12)   )

    doc.hr();doc.br();doc.br();doc.br();doc.br();doc.br();doc.br();


    #######################################################################################################
    doc.h1(f'Cumulative Clicks :  Bandit Agent  vs   {n_arms} individual creative_id  ') 
    doc.h1(""" Agent does not know the actual CTR at start ...   """)

    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate='date', date_format= None, 
                    coly1=coly1,    coly2=[],
                    title = "Cumulative click",cfg={},mode='highcharts',
                    figsize=(14,12)  )


    doc.br();  doc.hr() ; doc.br()


    doc.h1(f' CTR Estimate :   Bandit Algo vs   {n_arms} individual creative_id   ') 
    doc.plot_tseries(df.iloc[100:nmax2, :]
                    ,coldate='date', date_format= None, 
                    coly1=coly2,  coly2=[],
                    title = "CTR Estimate",cfg={},mode='highcharts',
                    figsize=(14,12)   )
    doc.hr()


    tag2 = f"{int(time.time())}_{n_arms}_{nmax2}"
    doc.save( f'{dir0}/simul_{tag1}_{tag2}.html')


def simulation_run(arms_proba:list=None, max_steps=6000, policy_type=""):

    arms_proba =  [0.035, 0.041, 0.042, 0.05 ] if arms_proba is None else arms_proba

    #### Env Simul params
    arm_means = torch.tensor(arms_proba)  ###
    n_arms    = arm_means.shape[0]
    best_mean = arm_means.max().item()
    log(f'######## Probs: {arm_means}')


    ### Env Simulation
    env_simulator    = BernoilliMAB(max_steps, arm_means)


    ### Policy : Algo which takes decision
    if policy_type == 'torch_random':
       from src.frame.mab_torch.mab_algorithm import RandomActionsAlgo
       algo = RandomActionsAlgo(n_arms=n_arms )

    else :
       from src.frame.mab_torch.tsampling import BernoulliBetaT
       algo = BernoulliBetaT(n_arms=n_arms)

    ### Evaluate
    ddict = simul_eval_single_policy_torch(env_simulator,algo, update_every = 2,
                                           freeze_scores_btw_updates=True )

    return ddict


def simulation_run2(arms_proba:list=None, max_steps=10, policy_type=""):
    """
    Args:
        arms_proba:
        max_steps:
        policy_type:

    """
    #### Env Simul params
    arms_proba = [0.035, 0.041, 0.042, 0.05 ] if arms_proba is None else arms_proba
    n_arms     = len(arms_proba)
    arms_ids   = [10*i for i in range(1, n_arms+1) ]


    log(f'######## Probs: {arms_proba}')
    best_mean  = max(arms_proba)


    ### Env Simulation
    arm_probaT = torch.tensor(arms_proba)  ###
    env_simulator    = BernoilliMAB(max_steps, probs=arm_probaT,arm_ids= arms_ids)


    ### Policy : Algo which takes decision
    from src.frame.mab_torch.tsampling import TSsampling
    pars   = {}                               ### Dict[str, str]
    i = 0
    pars[ f"{i}:epsilon_init"]  = "1.0"
    pars[ f"{i}:epsilon_decay"] = "0.9"
    pars[ f"{i}:epsilon_min"]   = "0.01"
    pars[ f"{i}:arms"]          = ",".join([ str(i) for i in arms_ids])
    algo = TSsampling(policy_state=pars)

    ### Evaluate
    ddict = simul_eval_single_policy_torch_algoid(env_simulator,algo, update_every = 1,
                                                  freeze_scores_btw_updates=True )

    # log(ddict)
    return ddict



####################################################################################################
from src.frame.mab_torch.simulation import MAB
class BernoilliMAB(MAB):
    """
    A class that simulates a bandit

    Args:
        probs: A tensor of per-arm success probabilities
        max_steps: Max number os steps to simulate. This has to be specified because we pre-generate
            all the rewards at initialization (for speedup - generating random matrix once should be
            faster than generating random scalars in a loop)
    """

    def __init__(self, max_steps: int, probs: torch.Tensor,
        arm_ids: Optional[List[str]] = None,
    ) -> None:
        """ """
        assert probs.max() <= 1.0
        assert probs.min() >= 0.0
        super().__init__(max_steps=max_steps, expected_rewards=probs, arm_ids=arm_ids)
        self.rewards = torch.bernoulli(
            probs.repeat(max_steps, 1)
        )  # pre-generate all rewards ahead of time
        assert self.rewards.shape == (max_steps, len(probs))

        self.best_action_value = probs.max().item()

    def act(self, arm_id: str) -> float:
        """
        Sample a reward from a specific arm

        Args:
            arm_idx: Index of arm from which reward is sampled
        Returns:
            Sampled reward
        """
        arm_idx = self.arm_ids.index(arm_id)
        assert arm_idx <= (len(self.expected_rewards) - 1)
        assert self.t < self.max_steps
        val = self.rewards[self.t, arm_idx].item()
        self.t += 1
        return val



###################################################################################################
def simul_eval_single_policy_torch( env_simulator=None, algo=None, *,
    update_every: int = 1,
    freeze_scores_btw_updates: bool = True,
) -> Dict:
    """ Evaluate a env_simulator algorithm on a single env_simulator instance.
    Docs::

        env_simulator: Env instance on which we evaluate
        algo:   env_simulator algorithm to be evaluated
        update_every: How many steps between the model is updated. 1 is online learning, >1 is iterative batch learning.
        freeze_scores_btw_updates: If True, the scores are frozen between model updates, otherwise at each step we generate
            new scores even if the model wasn't updated. `False` doesn't make sense for UCB models since the scores are deterministic
            and wouldn't change until the model is updated. Use `False` only for models with non-deterministic scores, like Thompson sampling.

    """
    arms_proba       = []    
    arm_selected     = []
    rewards          = []
    expected_rewards = []

    max_steps = env_simulator.max_steps
    
    # iterate through model updates
    remaining_steps = env_simulator.max_steps
    for _ in range(0, env_simulator.max_steps, update_every):
        batch_n_obs_per_arm              = torch.zeros(env_simulator.n_arms)
        batch_sum_reward_per_arm         = torch.zeros(env_simulator.n_arms)
        batch_sum_squared_reward_per_arm = torch.zeros(env_simulator.n_arms)
        steps_before_update = min( remaining_steps, update_every )  # take this many steps until next model update
        
        arm_id    = ( algo.get_action())  # this action will be reused until next model update if freeze_scores_btw_updates
        arm_proba = algo.get_scores()  

        for i in range(steps_before_update):
            # iterate through steps without updating the model
            if (not freeze_scores_btw_updates) and (i > 0):
                # if scores are not frozen, we choose new action at each step
                # (except first, because we've already chosen the first action above)
                arm_id    = algo.get_action()    ## arm_id: image_id to show  
                arm_proba = algo.get_scores()    ## 1D vector of scores


            arm_idx = algo.arm_ids.index(arm_id)

            ### Env Is click or NOT for this action
            reward  = env_simulator.act(arm_id)   
            rewards.append(reward)

            #### Store the hitorical data : reward,  impression, ...
            arm_selected.append( arm_id )
            arms_proba.append( to_numpy( arm_proba ) )

            expected_rewards.append(env_simulator.expected_rewards[arm_idx].item())
            batch_n_obs_per_arm[arm_idx]      += 1
            batch_sum_reward_per_arm[arm_idx] += reward
            batch_sum_squared_reward_per_arm[arm_idx] += reward**2
        
        assert sum(batch_n_obs_per_arm) == steps_before_update

        #### Fit the Algo  in mini-Batch pdate
        algo.add_batch_observations( batch_n_obs_per_arm, batch_sum_reward_per_arm, batch_sum_squared_reward_per_arm, )
        remaining_steps -= steps_before_update
    
    ######### Store all the simulation data  ################################################ 
    assert remaining_steps == 0
    assert len(rewards) == env_simulator.max_steps
    per_step_pseudo_regret = env_simulator.best_action_value - np.array(expected_rewards)


    reward_per_arm0 = env_simulator.rewards.numpy()  
    reward_per_arm = [ reward_per_arm0[i, :]  for i in range(len(reward_per_arm0) )  ]

    reward_algo_cum = np.cumsum(rewards)
    steps           = np.arange(1,max_steps+1)

    df = {   #### Env feedback
             'steps'  :      np.arange(1, 1+len(rewards))  
            ,'regret':       per_step_pseudo_regret
            ,"regret_cum" :  np.cumsum(per_step_pseudo_regret)
            ,"reward_expected" :  expected_rewards    

             ### Algo related
            ,"reward_algo"     :  rewards
            ,"reward_algo_cum" :  reward_algo_cum
            #,"reward_algo_avg" :  np_rolling(  rewards, window=500 )  #reward_algo_cum / steps
            ,"reward_algo_avg" :  reward_algo_cum / steps

            ,'arm_selected_algo' : arm_selected   #### == image_id shown
            ,"arm_selected_proba":  [  np.max(v) for v in arms_proba ] 

            ### List of List : 3 arms per row  
            ,"arms_proba"  :  np_2d_to_strlist( arms_proba ) 
            ,'arms_reward' :  np_2d_to_strlist( reward_per_arm, sep=",")       #### list of list
    }

    df = pd.DataFrame(df)
    # df['reward_algo_avg'] = df['reward_algo'].rolling(100).sum()  / 100
    # log('Expect reward', expected_rewards)
    # for key,val in df.items():
    #    log(key, len(val))

    ### Add individual arms
    n_arms = len(reward_per_arm[0] )
    for i in range(n_arms):
       df[f"arms_reward_cum_{i}"] = np.cumsum( reward_per_arm0[:,i] )
       df[f"arms_reward_avg_{i}"] = df[f"arms_reward_cum_{i}"] / df['steps']
       # df[f'arms_reward_avg_{i}']  = np_rolling(  reward_per_arm0[:,i], window=500 )


    ddict = {
        ### Fixed part
        'max_steps'  :  env_simulator.max_steps
       ,'freq_steps' :  update_every
       ,'n_arms'     :  n_arms
       ,'proba_arms_expected': env_simulator.expected_rewards


       , 'df' :df        ### All Histo

       ### Agg values
       , 'batch_n_obs_per_arm':       batch_n_obs_per_arm
       , 'batch_sum_reward_per_arm' : batch_sum_reward_per_arm
    }
    return ddict



def simul_eval_single_policy_torch_algoid( env_simulator=None, algo=None,update_every: int = 1,
    freeze_scores_btw_updates: bool = True, algoid0=0,
) -> Dict:
    """ Evaluate a env_simulator algorithm on a single env_simulator instance.
    Docs::

        env_simulator: Env instance on which we evaluate
        algo:   env_simulator algorithm to be evaluated
        update_every: How many steps between the model is updated. 1 is online learning, >1 is iterative batch learning.
        freeze_scores_btw_updates: If True, the scores are frozen between model updates, otherwise at each step we generate
            new scores even if the model wasn't updated. `False` doesn't make sense for UCB models since the scores are deterministic
            and wouldn't change until the model is updated. Use `False` only for models with non-deterministic scores, like Thompson sampling.

    """
    arms_proba       = []
    arm_selected     = []
    rewards          = []
    expected_rewards = []

    max_steps = env_simulator.max_steps
    n_arms    = env_simulator.n_arms

    # iterate through model updates
    remaining_steps = max_steps
    for _ in range(0, max_steps, update_every):
        batch_n_obs_per_arm              = torch.zeros(n_arms)
        batch_sum_reward_per_arm         = torch.zeros(n_arms)
        batch_sum_squared_reward_per_arm = torch.zeros(n_arms)
        steps_before_update = min( remaining_steps, update_every )  # take this many steps until next model update

        arm_id    = (algo.get_action(algoid=algoid0))  # this action will be reused until next model update if freeze_scores_btw_updates
        arm_proba = algo.get_scores(algoid=algoid0)

        for i in range(steps_before_update):
            # iterate through steps without updating the model
            if (not freeze_scores_btw_updates) and (i > 0):
                # if scores are not frozen, we choose new action at each step
                # (except first, because we've already chosen the first action above)
                arm_id    = algo.get_action(algoid=algoid0)    ## arm_id: image_id to show
                arm_proba = algo.get_scores(algoid=algoid0)    ## 1D vector of scores


            arm_idx = algo.algoid_get_arm_idx(algoid=algoid0, arm_id=arm_id)

            ### Env Is click or NOT for this action
            reward  = env_simulator.act(arm_id)
            rewards.append(reward)

            #### Store the hitorical data : reward,  impression, ...
            arm_selected.append( arm_id )
            arms_proba.append( to_numpy( arm_proba ) )

            expected_rewards.append(env_simulator.expected_rewards[arm_idx].item())
            batch_n_obs_per_arm[arm_idx]      += 1
            batch_sum_reward_per_arm[arm_idx] += reward
            batch_sum_squared_reward_per_arm[arm_idx] += reward**2

        assert sum(batch_n_obs_per_arm) == steps_before_update

        #### Fit the Algo  in mini-Batch pdate
        Ximp    = batch_n_obs_per_arm
        Xreward = batch_sum_reward_per_arm
        algo.train_batch(algoid=algoid0, Ximp=Ximp, Xreward= Xreward)
        #algo.add_batch_observations( batch_n_obs_per_arm, batch_sum_reward_per_arm, batch_sum_squared_reward_per_arm, )
        remaining_steps -= steps_before_update

    ######### Store all the simulation data  ################################################
    best_action_value = env_simulator.best_action_value
    reward_per_arm0   = env_simulator.rewards.numpy()

    assert remaining_steps == 0
    assert len(rewards) == max_steps
    per_step_pseudo_regret = best_action_value - np.array(expected_rewards)

    reward_per_arm  = [ reward_per_arm0[i, :]  for i in range(len(reward_per_arm0) )  ]
    reward_algo_cum = np.cumsum(rewards)
    steps           = np.arange(1,max_steps+1)

    df = {   #### Env feedback
             'steps'  :      np.arange(1, 1+len(rewards))
            ,'regret':       per_step_pseudo_regret
            ,"regret_cum" :  np.cumsum(per_step_pseudo_regret)
            ,"reward_expected" :  expected_rewards

             ### Algo related
            ,"reward_algo"     :  rewards
            ,"reward_algo_cum" :  reward_algo_cum
            #,"reward_algo_avg" :  np_rolling(  rewards, window=500 )  #reward_algo_cum / steps
            ,"reward_algo_avg" :  reward_algo_cum / steps

            ,'arm_selected_algo' : arm_selected   #### == image_id shown
            ,"arm_selected_proba":  [  np.max(v) for v in arms_proba ]

            ### List of List : 3 arms per row
            ,"arms_proba"  :  np_2d_to_strlist( arms_proba )
            ,'arms_reward' :  np_2d_to_strlist( reward_per_arm, sep=",")       #### list of list
    }

    # log('Expect reward', expected_rewards)
    # for key,val in df.items():
    #    log(key, len(val))

    df = pd.DataFrame(df)

    ### Add individual arms
    n_arms = len(reward_per_arm[0] )
    for i in range(n_arms):
       df[f"arms_reward_cum_{i}"] = np.cumsum( reward_per_arm0[:,i] )
       df[f"arms_reward_avg_{i}"] = df[f"arms_reward_cum_{i}"] / df['steps']
       # df[f'arms_reward_avg_{i}']  = np_rolling(  reward_per_arm0[:,i], window=500 )

    ddict = {
        ### Fixed part
        'max_steps'  :  max_steps
       ,'freq_steps' :  update_every
       ,'n_arms'     :  n_arms
       ,'proba_arms_expected': expected_rewards

       , 'df' :df        ### All Histo

       ### Agg values
       , 'batch_n_obs_per_arm':       batch_n_obs_per_arm
       , 'batch_sum_reward_per_arm' : batch_sum_reward_per_arm
    }
    return ddict



###########################################################################################################
def to_numpy(X):
    if isinstance(X, torch.Tensor):
       return X.cpu().detach().numpy()

    elif isinstance(X, pd.DataFrame):
       return X.values 
    else : 
       return X


def np_strlist_to_array(strlist, sep=","):
   return np.array([ [ float(xi) for xi in vk.split(sep)   ] for vk in strlist ] )


def np_2d_to_strlist(array2d, sep=","):
    return [ ",".join([ str(xi) for xi in v  ]) for v in   array2d ]  


def np_rolling(arr, window=100):
  return pd.Series(arr).rolling(window, min_periods=5).sum().fillna(method='backfill').values  / window


#### To plot the results
def plot_ax(ax, x, y, label):
    ax.plot(x, y, label=label)


def plot_results(name, alg_rewards, arm_rewards, exp_name, cum=True):
    from matplotlib import pyplot as plt
    from cycler import cycler
    # figure params
    plt.rcParams['figure.figsize']   = 6,4
    plt.rcParams['mathtext.default'] = 'regular'
    plt.rcParams['font.size']        = 12
    plt.rcParams['lines.linewidth']  = 2
    plt.rcParams['axes.prop_cycle']  = (cycler('color', ['r', 'g', 'b', 'y']) +  cycler('linestyle', ['-', '--', ':', '-.']))
    max_steps = alg_rewards.shape[0]
    steps = np.arange(1,max_steps+1)
    fig, ax  = plt.subplots(nrows=1, ncols=1)
    for i in range(arm_rewards.shape[1]):
        res = arm_rewards[:,i].cumsum()
        if not cum:
            res = res/steps
        plot_ax(ax, steps, res, f'Image_id {i}')

    res = alg_rewards.cumsum()
    if not cum:
        res = res/steps
    plot_ax(ax, steps, res, name)
    ax.grid()
    ax.legend()
    if cum:
        ax.set_title('Average cumulative Click ')
    else:
        ax.set_title('Average CTR ')
    fig.show()




###################################################################################################
if __name__ == "__main__":
    fire.Fire()





