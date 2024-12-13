import argparse
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import mo_gymnasium as mo_gym
import numpy as np
import wandb
import yaml
from mo_gymnasium.utils import MORecordEpisodeStatistics

from morl_baselines.common.evaluation import seed_everything
from morl_baselines.common.experiments import (
    ALGOS,
    ENVS_WITH_KNOWN_PARETO_FRONT,
    StoreDict,
)
from morl_baselines.common.utils import reset_wandb_env
import examples.nile_river_simulation
import examples.susquehanna_river_simulation


@dataclass
class WorkerInitData:
    sweep_id: str
    seed: int
    config: dict
    worker_num: int


@dataclass
class WorkerDoneData:
    hypervolume: float


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", type=str, help="Name of the algorithm to run", choices=ALGOS.keys(), required=True)
    parser.add_argument("--env-id", type=str, help="MO-Gymnasium id of the environment to run", required=True)
    parser.add_argument(
        "--ref-point", type=float, nargs="+", help="Reference point to use for the hypervolume calculation", required=True
    )

    parser.add_argument("--wandb-entity", type=str, help="Wandb entity to use for the sweep", required=False)
    parser.add_argument("--project-name", type=str, help="Project name to use for the sweep", default="MORL-Baselines-sweep")

    parser.add_argument("--sweep-count", type=int, help="Number of trials to do in the sweep worker", default=3)
    parser.add_argument("--num-seeds", type=int, help="Number of seeds to use for the sweep", default=1)

    parser.add_argument(
        "--seed", type=int, help="Random seed to start from, seeds will be in [seed, seed+num-seeds)", default=42
    )

    parser.add_argument(
        "--train-hyperparams",
        type=str,
        nargs="+",
        action=StoreDict,
        help="Override hyperparameters to use for the train method algorithm. Example: --train-hyperparams num_eval_weights_for_front:10 timesteps_per_iter:10000",
        default={},
    )

    parser.add_argument(
        "--config-name",
        type=str,
        help="Name of the config to use for the sweep, defaults to using the same name as the algorithm.",
    )

    args = parser.parse_args()

    if not args.config_name:
        args.config_name = f"{args.algo}.yaml"
    elif not args.config_name.endswith(".yaml"):
        args.config_name += ".yaml"

    return args


def train():
    sweep_run = wandb.init()

    # Reset the wandb environment variables
    config=dict(sweep_run.config)
    args = parse_args()
    print(args)

    seed_everything(args.seed)
    env = mo_gym.make(args.env_id)
    eval_env = mo_gym.make(args.env_id)
    env = MORecordEpisodeStatistics(env, gamma=config["gamma"])


    print(f"Instantiating {args.algo} on {args.env_id}")
    if args.algo == "ols":
        args.init_hyperparams["experiment_name"] = "MultiPolicy MO Q-Learning (OLS)"
    elif args.algo == "gpi-ls":
        args.init_hyperparams["experiment_name"] = "MultiPolicy MO Q-Learning (GPI-LS)"

    algo = ALGOS[args.algo](env=env, wandb_entity=args.wandb_entity, **config, seed=args.seed, group=sweep_id)

    if args.env_id in ENVS_WITH_KNOWN_PARETO_FRONT:
        known_pareto_front = env.unwrapped.pareto_front(gamma=args.gamma)
    else:
        known_pareto_front = None

    print(algo.get_config())

    print("Training starts... Let's roll!")
    algo.train(
        total_timesteps=10000,
        eval_env=eval_env,
        ref_point=np.array(args.ref_point),
        known_pareto_front=known_pareto_front,
        **args.train_hyperparams,
    )

    hypervolume = wandb.run.summary["eval/hypervolume"]
    sweep_run.log(dict(hypervolume=hypervolume))
    wandb.finish()




args = parse_args()

# Create an array of seeds to use for the sweep
seeds = [args.seed + i for i in range(args.num_seeds)]

# Load the sweep config
config_file = os.path.join(os.path.dirname(__file__), "configs", args.config_name)

# Set up the default hyperparameters
with open(config_file) as file:
    sweep_config = yaml.load(file, Loader=yaml.FullLoader)

# Set up the sweep
sweep_id = wandb.sweep(sweep=sweep_config, entity=args.wandb_entity, project=args.project_name)

# Run the sweep agent
wandb.agent(sweep_id, function=train, count=args.sweep_count)
