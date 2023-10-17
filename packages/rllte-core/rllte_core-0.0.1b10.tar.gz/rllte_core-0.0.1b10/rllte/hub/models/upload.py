from huggingface_hub import HfApi, login

login()

api = HfApi()
api.upload_file(
    path_or_fileobj="/export/yuanmingqi/code/rllte/sac_dmc_humanoid_run_seed_0.pth",
    path_in_repo="dmc/sac/sac_dmc_humanoid_run_seed_0.pth",
    repo_id="RLE-Foundation/rllte-hub",
    repo_type="model",
)
