from rllte.hub.models import Procgen

if __name__ == "__main__":
    model = Procgen().load_models(
        agent="ppo",
        env_id="bigfish",
        seed=1,
        device="cuda"
    )
    print(model)