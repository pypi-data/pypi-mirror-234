from .base import Environment, TimeStep
from .conversation import Conversation, ModeratedConversation
from .chameleon_competition import Chameleon_Competition
from .chameleon_competition_pgm import Chameleon_Competition_PGM

from .chameleon import Chameleon
from .chameleon_inter import Chameleon_Inter
from .chameleon_iter import Chameleon_Iter
from .chameleon_pgm_cal import Chameleon_PGM_Cal
from .chameleon_pgm_cal_active import Chameleon_PGM_Cal_Active
from .chameleon_pgm_cal_active_fewshot import Chameleon_PGM_Cal_Active_Fewshot
from .chameleon_pgm import Chameleon_PGM
from .pettingzoo_chess import PettingzooChess
from .pettingzoo_tictactoe import PettingzooTicTacToe
from .undercover_competition import Undercover_Competition
from .undercover_competition_pgm import Undercover_Competition_PGM

from ..config import EnvironmentConfig

ALL_ENVIRONMENTS = [
    Conversation,
    ModeratedConversation,
    Chameleon,
    Chameleon_Inter,
    Chameleon_Iter,
    Chameleon_PGM_Cal,
    Chameleon_PGM,
    PettingzooChess,
    PettingzooTicTacToe,
    Chameleon_PGM_Cal_Active,
    Chameleon_PGM_Cal_Active_Fewshot,
    Chameleon_Competition,
    Chameleon_Competition_PGM,
    Undercover_Competition,
    Undercover_Competition_PGM
]

ENV_REGISTRY = {env.type_name: env for env in ALL_ENVIRONMENTS}

print(ENV_REGISTRY)
# Load an environment from a config dictionary
def load_environment(config: EnvironmentConfig):
    try:
        env_cls = ENV_REGISTRY[config["env_type"]]
    except KeyError:
        raise ValueError(f"Unknown environment type: {config['env_type']}")
    print(config)
    env = env_cls.from_config(config)
    return env
