from huggingface_hub import HfApi, login

login()

api = HfApi()
api.upload_file(
    path_or_fileobj="/export/yuanmingqi/code/rllte/ppo_atari_Pong-v5_seed_1.pth",
    path_in_repo="atari/ppo/ppo_atari_Pong-v5_seed_1.pth",
    repo_id="RLE-Foundation/rllte-hub",
    repo_type="model"
)
