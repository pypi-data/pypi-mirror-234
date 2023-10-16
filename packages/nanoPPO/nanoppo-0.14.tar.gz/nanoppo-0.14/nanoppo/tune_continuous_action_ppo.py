from typing import Tuple
from pathlib import Path
from nanoppo.continuous_action_ppo import train
import ray
from ray import tune
import gym
from nanoppo.continuous_action_ppo import update_config
from nanoppo.random_utils import set_seed
from nanoppo.envs.point_mass2d import PointMass2DEnv

gym.envs.register("PointMass2D-v0", entry_point=PointMass2DEnv)

# set_seed(SEED)

# Define the hyperparameter search space
mountaincar_search_space = {
    "project": "tune_continuous_action_ppo",
    "env_name": "MountainCarContinuous-v0",
    "policy_lr": tune.loguniform(1e-6, 1e-3),
    "value_lr": tune.loguniform(1e-6, 1e-3),
    "weight_decay": tune.loguniform(1e-6, 1e-3),
    "scheduler": tune.choice([None, "exponential", "cosine"]),
    # "cosine_T_max": tune.choice([50, 100, 200, 500]),
    "sgd_iters": tune.choice([2, 5, 10, 20, 30]),
    # "scale_states": tune.choice(["standard", "minmax"]),
    #    "rescaling_rewards": True,
    #   "scale_states": tune.choice(["by_sample", "by_env", None]),
    #    "init_type": tune.choice(['he', 'xavier']),
    "batch_size": tune.choice([64, 128, 256, 512]),
    # "l1_loss": tune.choice([True, False]),
    "clip_param": tune.uniform(0.1, 0.3),
    "max_grad_norm": tune.uniform(0.5, 1.0),
    "vf_coef": tune.uniform(0.5, 1.0),
    "entropy_coef": tune.loguniform(1e-6, 1e-3),
    "tau": tune.loguniform(0.9, 1),
}

pendulum_search_space = {
    "project": "tune_continuous_action_ppo",
    "seed": tune.choice(range(1000)),
    "env_name": "Pendulum-v1",
    "policy_lr": tune.loguniform(1e-5, 1e-2),
    "value_lr": tune.loguniform(1e-5, 1e-2),
    "weight_decay": tune.loguniform(1e-4, 1e-2),
    # "cosine_T_max": tune.choice([ 200, 500]),
    "sgd_iters": tune.choice([2, 3, 5, 10]),
    # "scheduler": tune.choice([None, "exponential", "cosine"]),
    "scale_states": tune.choice(["standard", "minmax", "robust", "quantile"]),
    # "scheduler": None,
    # "scale_states": "robust",
    "use_gae": tune.choice([True, False]),
    "init_type": tune.choice(["he", "xavier"]),
    # "init_type": "xavier",
    # "batch_size": tune.choice([64, 128, 256, 512]),
    "batch_size": tune.choice([64, 128, 256, 512]),
    # "l1_loss": False,
    "clip_param": tune.loguniform(0.2, 0.5),
    "max_grad_norm": tune.uniform(0.5, 1),
    "vf_coef": tune.uniform(0.1, 2),
    "entropy_coef": tune.loguniform(1e-7, 1e-3),
    "tau": tune.loguniform(0.9, 1),
}

pointmass2d_search_space = {
    "project": "tune_continuous_action_ppo",
    # "seed": tune.choice(range(1000)),
    "env_name": "PointMass2D-v0",
    "policy_lr": tune.loguniform(1e-5, 1e-3),
    "value_lr": tune.loguniform(1e-5, 1e-3),
    "weight_decay": tune.loguniform(1e-4, 1e-2),
    # "cosine_T_max": tune.choice([ 200, 500]),
    "sgd_iters": tune.choice([2, 3, 5, 10]),
    # "scheduler": tune.choice([None, "exponential", "cosine"]),
    # "scale_states": tune.choice(["standard", "minmax", "robust", "quantile"]),
    # "scheduler": None,
    # "scale_states": "robust",
    # "use_gae": tune.choice([True, False]),
    "use_gae": True,
    # "init_type": tune.choice(["default", "he", "xavier"]),
    # "init_type": "xavier",
    # "batch_size": tune.choice([64, 128, 256, 512]),
    "batch_size": tune.choice([64, 128, 256, 512]),
    # "l1_loss": False,
    # "clip_param": tune.uniform(0.2, 0.4),
    # "max_grad_norm": tune.uniform(0.5, 0.7),
    "vf_coef": tune.uniform(0.1, 1),
    "entropy_coef": tune.loguniform(1e-7, 1e-3),
    # "tau": tune.loguniform(0.9, 1),
}


def training_function(search_config):
    # set_seed(search_config.pop("seed"))
    tune_config = update_config(search_config)
    tune_config.update({"verbose": False, "wandb_log": False})
    tune_config.update({"report_func": lambda **kwargs: tune.report(**kwargs)})

    policy, value, average_reward, total_iters = train(**tune_config)
    print("train", "average reward", average_reward, "total iter", total_iters)


stop_criteria = {"training_iteration": 50, "mean_reward": 90}

if __name__ == "__main__":
    ray.init(num_cpus=10, num_gpus=0, local_mode=False)
    # search_space = pendulum_search_space
    # search_space =  mountaincar_search_space
    # search_space = weight_search_space
    search_space = pointmass2d_search_space
    # Run the hyperparameter search with Tune
    analysis = tune.run(
        training_function,
        config=search_space,
        num_samples=50,  # Number of different configurations to try
        stop=stop_criteria,  # Stop after 10 iterations,
        metric="mean_reward",  # Compare trials by their mean reward
        progress_reporter=tune.CLIReporter(
            max_progress_rows=10,
            max_error_rows=10,
            metric_columns=["mean_reward", "training_iteration"],
        ),
        verbose=1,
        fail_fast=False,
    )

    # Print the best configuration and its performance
    # best_config = analysis.get_best_config(metric="mean_reward", mode="max", scope="last-10-avg")
    # print(f"Best config: {best_config}")
    # print(f"Best performance: {analysis.get_best_trial(metric='mean_reward', mode='max', scope='last-10-avg')}")

    # Sort trials based on their performance
    sorted_trials = sorted(
        analysis.trials,
        key=lambda trial: trial.last_result.get("mean_reward", 0),
        reverse=True,
    )

    # Print the top 5 configurations and their performances
    for idx, trial in enumerate(sorted_trials[:5]):
        print(f"Rank {idx + 1}:")
        print(f"Config: {trial.config}")
        print(f"Mean Reward: {trial.last_result['mean_reward']}\n")
