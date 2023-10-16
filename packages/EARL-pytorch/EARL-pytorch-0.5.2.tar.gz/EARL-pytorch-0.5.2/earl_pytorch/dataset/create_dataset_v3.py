import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import ballchasing as bc
import numpy as np
import pandas as pd

# from earl_pytorch import EARL
from tqdm import tqdm

command = r'carball.exe -i "{}" -o "{}" parquet'

ENV = os.environ.copy()
ENV["NO_COLOR"] = "1"


class CarballAnalysis:
    METADATA_FNAME = "metadata.json"
    ANALYZER_FNAME = "analyzer.json"
    BALL_FNAME = "__ball.parquet"
    GAME_FNAME = "__game.parquet"
    PLAYER_FNAME = "player_{}.parquet"

    def __init__(self, processed_folder: str):
        # print(processed_folder, self.METADATA_FNAME)
        self.metadata = json.load(open(os.path.join(processed_folder, self.METADATA_FNAME)))
        self.analyzer = json.load(open(os.path.join(processed_folder, self.ANALYZER_FNAME)))

        self.ball = pd.read_parquet(os.path.join(processed_folder, self.BALL_FNAME))
        self.game = pd.read_parquet(os.path.join(processed_folder, self.GAME_FNAME))
        self.players = {}
        for player in self.metadata["players"]:
            uid = player["unique_id"]
            player_path = os.path.join(processed_folder, self.PLAYER_FNAME.format(uid))
            if os.path.exists(player_path):
                self.players[uid] = pd.read_parquet(player_path)


def download_replays(n=1_000):
    for gamemode in bc.Playlist.RANKED:
        gm_folder = os.path.join(working_dir, "replays", gamemode)
        os.makedirs(gm_folder, exist_ok=True)
        replay_iter = api.get_replays(
            min_rank=bc.Rank.SUPERSONIC_LEGEND,
            max_rank=bc.Rank.SUPERSONIC_LEGEND,
            season=bc.Season.SEASON_5_FTP,
            count=n
        )
        for replay in replay_iter:
            if not os.path.exists(os.path.join(gm_folder, replay["id"])):
                api.download_replay(replay["id"], gm_folder)
                print(replay["id"], "downloaded")


def process_replay(replay_path, output_folder, skip_existing=True):
    folder, fn = os.path.split(replay_path)
    replay_name = fn.replace(".replay", "")
    processed_folder = os.path.join(output_folder, replay_name)
    if skip_existing and os.path.isdir(processed_folder) and len(os.listdir(processed_folder)) > 0:
        return
    os.makedirs(processed_folder, exist_ok=True)

    with open(os.path.join(processed_folder, "carball.o.log"), "w", encoding="utf8") as stdout_f:
        with open(os.path.join(processed_folder, "carball.e.log"), "w", encoding="utf8") as stderr_f:
            return subprocess.run(
                command.format(replay_path, processed_folder),
                stdout=stdout_f,
                stderr=stderr_f,
                env=ENV
            )


def foo(replay_path):
    parsed_folder = os.path.split(replay_path.replace("replays", "parsed", 1))[0]
    process_replay(replay_path, parsed_folder)
    return os.path.split(replay_path)[-1].replace(".replay", "")


def parse_replays():
    # for gamemode in bc.Playlist.RANKED:
    #     replay_folder = os.path.join(working_dir, "replays", gamemode)
    #     parsed_folder = os.path.join(working_dir, "parsed", gamemode)
    #     for replay in os.listdir(replay_folder):
    #         process_replay(os.path.join(replay_folder, replay), parsed_folder)
    #         print(replay, "processed")

    base_path = r"E:\rokutleg"
    for group in (r"RLCS\RLCS 2021-22", "RLCS"):  # "2021-ssl-replays", "2021-ranked-replays", "2021-electrum-replays"
        replay_folder = os.path.join(base_path, "replays", group)
        replay_paths = [os.path.join(dp, f)
                        for dp, dn, fn in os.walk(replay_folder)
                        for f in fn
                        if f.endswith(".replay")]

        with ProcessPoolExecutor() as ex:
            it = tqdm(map(foo, replay_paths), total=len(replay_paths))
            for r_id in it:
                it.set_postfix_str(r_id)

        # for replay_path in replay_paths:
        #     foo(replay_path)
        # parsed_folder = os.path.split(replay_path.replace("replays", "parsed", 1))[0]
        # process_replay(replay_path, parsed_folder)
        # print(os.path.split(replay_path)[-1].replace(".replay", ""), "processed")


def train_model():
    model = EARL()

    shard_size = 1_000_000
    for epoch in range(100):
        data = np.zeros((shard_size, 41, 24))

    analysis = CarballAnalysis()


def main():
    # download_replays()
    parse_replays()


if __name__ == '__main__':
    working_dir = sys.argv[1]
    api = bc.Api(sys.argv[2])
    main()
