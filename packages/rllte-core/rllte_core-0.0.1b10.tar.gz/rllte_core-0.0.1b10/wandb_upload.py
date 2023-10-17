import pandas as pd
import argparse
import wandb

parser = argparse.ArgumentParser()
parser.add_argument("--env-id", type=str)
parser.add_argument("--seed", type=int, default=0)

if __name__ == "__main__":
    args = parser.parse_args()
    train_data = pd.read_csv(f"logs/ppo_atari_{args.env_id}_seed_{args.seed}/train.log", sep=",")
    eval_data = pd.read_csv(f"logs/ppo_atari_{args.env_id}_seed_{args.seed}/eval.log", sep=",")

    wandb.init(
        project="rllte-hub",
        group=f"Atari/PPO/{args.env_id}",
        job_type=f"seed={args.seed}",
        name=f"ppo_atari_{args.env_id}_seed_{args.seed}"
    )

    for epoch in range(train_data.shape[0]):
        step = int(train_data.loc[epoch]['step'])
        train_episode_reward = train_data.loc[epoch]['episode_reward']
        train_episode_length = train_data.loc[epoch]['episode_length']
        if eval_data[eval_data['step'] == float(step)].shape[0] > 0:
            eval_episode_reward = eval_data[eval_data['step'] == float(step)]['episode_reward'].values[0]
            eval_episode_length = eval_data[eval_data['step'] == float(step)]['episode_length'].values[0]
            wandb.log({"train/episode_reward": train_episode_reward, 
                       "train/episode_length": train_episode_length,
                       "eval/episode_reward": eval_episode_reward, 
                       "eval/episode_length": eval_episode_length
                       }, step=step)
        else:
            wandb.log({"train/episode_reward": train_episode_reward, 
                       "train/episode_length": train_episode_length,
                       }, step=step)

# if __name__ == "__main__":
#     args = parser.parse_args()
#     train_data = pd.read_csv(f"sac_dmc_{args.env_id}_seed_{args.seed}/train.log", sep=",")
#     eval_data = pd.read_csv(f"sac_dmc_{args.env_id}_seed_{args.seed}/eval.log", sep=",")

#     wandb.init(
#         project="rllte-hub",
#         group=f"DMControl/SAC/{args.env_id}",
#         job_type=f"seed={args.seed}",
#         name=f"sac_dmc_{args.env_id}_seed_{args.seed}"
#     )

#     for epoch in range(train_data.shape[0]):
#         step = int(train_data.loc[epoch]['step'])
#         train_episode_reward = train_data.loc[epoch]['episode_reward']
#         train_episode_length = train_data.loc[epoch]['episode_length']
#         if eval_data[eval_data['step'] == float(step)].shape[0] > 0:
#             eval_episode_reward = eval_data[eval_data['step'] == float(step)]['episode_reward'].values[0]
#             eval_episode_length = eval_data[eval_data['step'] == float(step)]['episode_length'].values[0]
#             wandb.log({"train/episode_reward": train_episode_reward, 
#                        "train/episode_length": train_episode_length,
#                        "eval/episode_reward": eval_episode_reward, 
#                        "eval/episode_length": eval_episode_length
#                        }, step=step)
#         else:
#             wandb.log({"train/episode_reward": train_episode_reward, 
#                        "train/episode_length": train_episode_length,
#                        }, step=step)