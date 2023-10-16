import logging

import coloredlogs


def init():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)s - %(message)s",
    #     datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    # )
    # level_styles={'info': {'color': 'green'}} 不生效
    coloredlogs.install(level=logging.INFO,
                        fmt="%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)s - %(message)s",
                        level_styles={'info': {'color': 'green'}})
