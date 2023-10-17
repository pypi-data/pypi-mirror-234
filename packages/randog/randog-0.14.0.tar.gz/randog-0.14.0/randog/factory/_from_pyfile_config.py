import random
import typing as t


"""コマンド実行でシード値を固定するために使いまわす Random"""
rnd: t.Optional[random.Random] = None
