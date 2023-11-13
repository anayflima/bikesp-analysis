import math
import numpy as np
import pandas as pd
from statsmodels.stats.power import TTestIndPower
import time

def calculate_pooled_estimated_std(std1,std2):
    value = (std1**2 + std2**2)/2
    return math.sqrt(value)

treatment_groups = {0: "T1", 1: "T2", 2: "T3"}
base_group = treatment_groups[1]
receive_nothing_group = treatment_groups[0]
receive_higher_value_group = treatment_groups[2]


############# PARAMETERS ###################

sample_size = {"T1": 150,
               "T2": 150,
               "T3": 150}

probability_zero = {"T1": 0.3,
                    "T2": 0.2,
                    "T3": 0.15}

alpha = 0.05
number_iterations = 10000


# means of the base treatment group. Each set of means will be created around these means
means_base_group = [6, 12, 18, 24, 30]

#############################################


start_time = time.time()

# apply bonferroni correction.
number_comparisons = len(treatment_groups) - 1
alpha_after_correction = alpha/number_comparisons


# generate set of means.
all_means = pd.DataFrame(columns = list(treatment_groups.values()))
count_group = 1
for mean_base_group in means_base_group:
    upper_bound = mean_base_group//2
    for i in range(1, upper_bound):
        all_means.loc['group_' + str(count_group)] = [mean_base_group - i,mean_base_group,mean_base_group + i]
        count_group += 1


number_of_trips_means = pd.DataFrame(columns = treatment_groups.values())
number_of_trips_stds = pd.DataFrame(columns = treatment_groups.values())
number_of_trips_mean_differences = pd.DataFrame(columns = treatment_groups.values())
number_of_trips_percentual_variation_base = pd.DataFrame(columns = treatment_groups.values())
number_of_trips_pooled_estimated_std = pd.DataFrame(columns = treatment_groups.values())

power_df_all_means = pd.DataFrame(columns = treatment_groups.values())
result_dict_of_dfs = {}

power_analysis = TTestIndPower()

for group_count, (mean_group, row_means) in enumerate(all_means.iterrows()):

    power_df = pd.DataFrame(columns = treatment_groups.values())

    means = list(row_means)

    # number of successes will be the mean of the base group
    number_successes = row_means[base_group]

    for iteration in range(number_iterations):
        number_trips_df = pd.DataFrame()

        for i in treatment_groups.keys():
            group = treatment_groups[i]
            mean = means[i]
            p = number_successes/(number_successes + mean)  # probability of success

            # generates a array of 0 and 1. Around {probability_zero}% will be 1.
            is_zero = np.random.binomial(n=1, p = probability_zero[group], size=sample_size[group])

            number_trips = np.where(is_zero == 1, 0, np.random.negative_binomial(n=number_successes, p=p, size=sample_size[group]))
            number_trips_df[group] = number_trips

        mean_base_group = number_trips_df[base_group].mean()
        std_base_group = number_trips_df[base_group].std()

        number_of_trips_means.loc['iteration_' + str(iteration)] = number_trips_df.agg(['mean']).iloc[0].tolist()
        number_of_trips_stds.loc['iteration_' + str(iteration)] = number_trips_df.agg(['std']).iloc[0].tolist()
        number_of_trips_mean_differences.loc['iteration_' + str(iteration)] = number_of_trips_means.loc['iteration_' + str(iteration)] - mean_base_group
        number_of_trips_percentual_variation_base.loc['iteration_' + str(iteration)] = number_of_trips_mean_differences.loc['iteration_' + str(iteration)]/mean_base_group * 100
        number_of_trips_pooled_estimated_std.loc['iteration_' + str(iteration)] = number_of_trips_stds.loc['iteration_' + str(iteration)].apply(calculate_pooled_estimated_std, std2=std_base_group)

        power_iteration_list = []

        for i in treatment_groups.keys():
            group = treatment_groups[i]
            if group != base_group:

                mean_difference = number_of_trips_mean_differences.loc['iteration_' + str(iteration)][group]
                pooled_estimated_std = number_of_trips_pooled_estimated_std.loc['iteration_' + str(iteration)][group]
                effect_size = mean_difference/pooled_estimated_std

                ratio = len(number_trips_df[group])/len(number_trips_df[base_group])

                # one-sized test
                alternative = "smaller" if group == receive_nothing_group else "larger"

                # perform power analysis
                power = power_analysis.solve_power(effect_size=effect_size, nobs1=sample_size[group],
                                            alpha=alpha_after_correction, ratio=ratio, alternative=alternative)
            else:
                power = None

            power_iteration_list.append(power)

        power_iteration_df = pd.DataFrame([power_iteration_list], columns=power_df.columns)
        power_df = pd.concat([power_df, power_iteration_df], ignore_index=True)

    df_group = pd.DataFrame(index = treatment_groups.values())

    df_group['mean'] = number_of_trips_means.mean()
    df_group['std'] = number_of_trips_stds.mean()
    df_group['mean_difference'] = number_of_trips_mean_differences.mean()
    df_group['percentual_variation_base'] = number_of_trips_percentual_variation_base.mean()
    df_group['sample_size'] = list(sample_size.values())
    df_group['pooled_estimated_std'] = number_of_trips_pooled_estimated_std.mean()
    
    df_group['power'] = power_df.mean()

    df_group['iteration'] = group_count

    result_dict_of_dfs[mean_group] = df_group

all_results = pd.concat(result_dict_of_dfs.values())

filename = 'results_power_analysis_alpha_{alpha}_sample_size_{sample_size}_iterations_{number_iterations}_means_base_group_{means_base_group}.csv'.format(alpha = alpha,
                                                                                                                                                          sample_size = sample_size[base_group],
                                                                                                                                                          number_iterations = number_iterations, 
                                                                                                                                                          means_base_group = means_base_group)
all_results.to_csv('results/' + filename)

end_time = time.time()

print('Time to run power analysis for {number_iterations} iterations:'.format(number_iterations = number_iterations), end_time - start_time)