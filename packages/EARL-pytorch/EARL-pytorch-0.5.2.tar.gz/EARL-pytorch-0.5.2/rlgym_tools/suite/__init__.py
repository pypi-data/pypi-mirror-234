from .air_dribble import air_dribble_config
from .dribble import dribble_config
from rlgym.envs import Match


def match_from_config(config, **additional_kwargs):
    for key, value in config.items():
        if key in additional_kwargs:
            print(f"Overwriting make argument {key}...")
        additional_kwargs[key] = value

    return Match(**additional_kwargs)
