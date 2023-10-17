



utilmy/recsys/ab.py
-------------------------functions----------------------
_p_val(N_A, N_B, p_A, p_B)
_pooled_SE(N_A, N_B, X_A, X_B)
_pooled_prob(N_A, N_B, X_A, X_B)
ab_getstat(df, treatment_col = 'treatment', measure_col = 'metric', attribute_cols = 'attrib', control_label = 'A', variation_label = 'B', inference_method = 'means_delta', hypothesis = None, alpha = .05, experiment_name = 'exp', dirout = None, tag = None, **kwargs)
abplot_CI_bars(N, X, sig_level = 0.05, dmin = None)
funnel_CI_plot(A, B, sig_level = 0.05)
get_ab_test_data(vars_also = False)
help()
np_calculate_ab_dist(stderr, d_hat = 0, group_type = 'control')
np_calculate_confidence_interval(sample_mean = 0, sample_std = 1, sample_size = 1, sig_level = 0.05)
np_calculate_min_sample_size(bcr, mde, power = 0.8, sig_level = 0.05)
np_calculate_z_val(sig_level = 0.05, two_tailed = True)
pd_generate_ctr_data(N_A, N_B, p_A, p_B, days = None, control_label = 'A', test_label = 'B', seed = None)
plot_ab(ax, N_A, N_B, bcr, d_hat, sig_level = 0.05, show_power = False, show_alpha = False, show_beta = False, show_p_value = False, show_legend = True)
plot_alternate_hypothesis_dist(ax, stderr, d_hat)
plot_binom_dist(ax, A_converted, A_cr, A_total, B_converted, B_cr, B_total)
plot_confidence_interval(ax, mu, s, sig_level = 0.05, color = 'grey')
plot_norm_dist(ax, mu, std, with_CI = False, sig_level = 0.05, label = None)
plot_null_hypothesis_dist(ax, stderr)
show_area(ax, d_hat, stderr, sig_level, area_type = 'power')
test_ab_getstat()
test_all()
test_np_calculate_ab_dist()
test_np_calculate_confidence_interval()
test_np_calculate_min_sample_size()
test_np_calculate_z_val()
test_pd_generate_ctr_data()
test_plot_ab()
test_plot_binom_dist()
test_zplot()
zplot(ax, area = 0.95, two_tailed = True, align_right = False)



utilmy/recsys/bandits/__init__.py


utilmy/recsys/bandits/banditml/__init__.py


utilmy/recsys/bandits/banditml/banditml/__init__.py


utilmy/recsys/bandits/banditml/scripts/create_bq_tables.py
-------------------------functions----------------------
create_dataset(client: bigquery.Client, dataset_id: str, description: str, location: str)
create_table(client: bigquery.Client, dataset_id: str, table_id: str, fields: List[Dict])
main(args)



utilmy/recsys/bandits/banditml/setup.py


utilmy/recsys/bandits/banditml/tests/__init__.py


utilmy/recsys/bandits/banditml/tests/fixtures.py


utilmy/recsys/bandits/banditml/tests/test_models.py
-------------------------methods----------------------
TestFeedbackMappers.assert_match_bq_record(self, r: LegacyBase, f: Feedback, delayed: bool  =  False)
TestFeedbackMappers.assert_metrics(self, metrics: Dict, feedbacks: List[Feedback])
TestFeedbackMappers.make_reward(metrics: Dict, delayed: bool  =  False)
TestFeedbackMappers.setUp(self)
TestFeedbackMappers.test_from_decision(self)
TestFeedbackMappers.test_from_delayed_reward(self)
TestFeedbackMappers.test_from_immediate_reward(self)
TestFeedbackMappers.test_to_from_decision(self)


utilmy/recsys/bandits/banditml_eval/__init__.py


utilmy/recsys/bandits/banditml_eval/ope/__init__.py


utilmy/recsys/bandits/banditml_eval/setup.py


utilmy/recsys/bandits/eval_replay/bandits/epsilon_greedy.py
-------------------------functions----------------------
epsilon_greedy_policy(df, arms, epsilon = 0.15, slate_size = 5, batch_size = 50)



utilmy/recsys/bandits/eval_replay/bandits/exp3.py
-------------------------functions----------------------
distr(weights, gamma = 0.0)
draw(probability_distribution, n_recs = 1)
exp3_policy(df, history, t, weights, movieId_weight_mapping, gamma, n_recs, batch_size)
update_weights(weights, gamma, movieId_weight_mapping, probability_distribution, actions)



utilmy/recsys/bandits/eval_replay/bandits/ucb.py
-------------------------functions----------------------
ucb1_policy(df, t, ucb_scale = 2.0)



utilmy/recsys/bandits/eval_replay/bandits/utils.py
-------------------------functions----------------------
score(history, df, t, batch_size, recs)
summarise()



utilmy/recsys/bandits/offline_replayer_eval_amzon.py
-------------------------functions----------------------
export_to_json(dictionary, file_name)
log(*s)

-------------------------methods----------------------
ABTestReplayer.__init__(self, n_visits, n_test_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
ABTestReplayer.record_result(self, visit, item_idx, reward)
ABTestReplayer.reset(self)
ABTestReplayer.select_item(self)
ABTestReplayer.simulator(self)
EpsilonGreedyReplayer.__init__(self, epsilon, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
EpsilonGreedyReplayer.record_result(self, visit, item_idx, reward)
EpsilonGreedyReplayer.reset(self)
EpsilonGreedyReplayer.select_item(self)
EpsilonGreedyReplayer.simulator(self)
ReplaySimulator.__init__(self, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1, random_seed = 1)
ReplaySimulator.record_result(self, visit, item_idx, reward)
ReplaySimulator.replay(self)
ReplaySimulator.reset(self)
ReplaySimulator.select_item(self)
ThompsonSamplingReplayer.__init__(self, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
ThompsonSamplingReplayer.record_result(self, visit, item_idx, reward)
ThompsonSamplingReplayer.reset(self)
ThompsonSamplingReplayer.select_item(self)
ThompsonSamplingReplayer.simulator(self)
UCBSamplingReplayer.__init__(self, ucb_c, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
UCBSamplingReplayer.record_result(self, visit, item_idx, reward)
UCBSamplingReplayer.reset(self)
UCBSamplingReplayer.select_item(self)
UCBSamplingReplayer.simulator(self)


utilmy/recsys/bandits/readme.py


utilmy/recsys/bandits/recostep_offline_replayer_eval_movielens.py
-------------------------methods----------------------
ABTestReplayer.__init__(self, n_visits, n_test_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
ABTestReplayer.record_result(self, visit, item_idx, reward)
ABTestReplayer.reset(self)
ABTestReplayer.select_item(self)
EpsilonGreedyReplayer.__init__(self, epsilon, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1)
EpsilonGreedyReplayer.select_item(self)
ReplaySimulator.__init__(self, n_visits, reward_history, item_col_name, visitor_col_name, reward_col_name, n_iterations = 1, random_seed = 1)
ReplaySimulator.record_result(self, visit, item_idx, reward)
ReplaySimulator.replay(self)
ReplaySimulator.reset(self)
ReplaySimulator.select_item(self)
ThompsonSamplingReplayer.record_result(self, visit, item_idx, reward)
ThompsonSamplingReplayer.reset(self)
ThompsonSamplingReplayer.select_item(self)


utilmy/recsys/metric.py
-------------------------functions----------------------
_mean_ranking_metric(y, labels, metric)
_require_positive_k(k)
_single_list_similarity(y_preds: list, feature_df: pd.DataFrame, u: int)
_warn_for_empty_labels()
catalog_coverage(y_preds: List[list], catalog: list)
coverage_at_k(y_preds, product_data, k = 3)
help()
hit_rate_at_k(y_preds, y_true, k = 3)
hit_rate_at_k_nep(y_preds, y_true, k = 3)
intra_list_similarity(y_preds: List[list], feature_df: pd.DataFrame)
mean_average_precision(y, labels, assume_unique = True)
metrics_calc(dirin:Union[str, pd.DataFrame], dirout:str = None, colid = 'userid', colrec = 'reclist', coltrue = 'purchaselist', colinfo = 'genrelist', colts = 'datetime', methods = [''], nsample = -1, nfile = 1, featuredf:pd.DataFrame = None, popdict:dict = None, topk = 5, **kw)
metrics_calc_batch(dirin:Union[str, pd.DataFrame], dirout:str = None, colid = 'userid', colrec = 'reclist', coltrue = 'purchaselist', colinfo = 'genrelist', colts = 'datetime', method = [''], nsample = -1, nfile = 1, **kw)
mrr_at_k(y_preds, y_true, k = 3)
mrr_at_k_nep(y_preds, y_true, k = 3)
ndcg_at_k(y, labels, k = 10, assume_unique = True)
novelty(y_preds: List[list], pop: dict, u: int, n: int)
personalization(y_preds: List[list])
popularity_bias_at_k(y_preds, x_train, k = 3)
precision_at(y, labels, k = 10, assume_unique = True)
precision_at_k(y_preds, y_true, k = 3)
recall_at_k(y_preds, y_true, k = 3)
recall_average_at_k_mean(actual: List[list], y_preds: List[list], k = 10)
recall_avg_at_k(actual: list, y_preds: list, k = 10)
recommender_precision(y_preds: List[list], actual: List[list])
recommender_recall(y_preds: List[list], actual: List[list])
sample_hits_at_k(y_preds, y_true, x_test = None, k = 3, size = 3)
sample_misses_at_k(y_preds, y_true, x_test = None, k = 3, size = 3)
statistics(x_train, y_train, x_test, y_true, y_pred)
test_all()
test_get_testdata()
test_metrics()



utilmy/recsys/metrics/__Init__.py


utilmy/recsys/metrics/distance_metrics.py