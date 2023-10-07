from typing import List, Union
import re
from tenacity import RetryError
import logging
import uuid
from abc import abstractmethod
import asyncio
import json

from .backends import IntelligenceBackend, load_backend
from .message import Message, SYSTEM_NAME
from .config import AgentConfig, Configurable, BackendConfig
from ..prompts.chameleon_pgm import clue_demo, view_demo

# A special signal sent by the player to indicate that it is not possible to continue the conversation, and it requests to end the conversation.
# It contains a random UUID string to avoid being exploited by any of the players.
SIGNAL_END_OF_CONVERSATION = f"<<<<<<END_OF_CONVERSATION>>>>>>{uuid.uuid4()}"


class Agent(Configurable):

    @abstractmethod
    def __init__(self, name: str, role_desc: str, global_prompt: str = None, *args, **kwargs):
        super().__init__(name=name, role_desc=role_desc, global_prompt=global_prompt, **kwargs)
        self.name = name

        self.role_desc = role_desc
        self.global_prompt = global_prompt



class Player(Agent):
    """
    Player of the game. It can takes the observation from the environment and return an action
    """

    def __init__(self, name: str, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend],
                 global_prompt: str = None, **kwargs):

        if isinstance(backend, BackendConfig):
            backend_config = backend
            backend = load_backend(backend_config)
        elif isinstance(backend, IntelligenceBackend):
            backend_config = backend.to_config()
        else:
            raise ValueError(f"backend must be a BackendConfig or an IntelligenceBackend, but got {type(backend)}")

        assert name != SYSTEM_NAME, f"Player name cannot be {SYSTEM_NAME}, which is reserved for the system."

        # Register the fields in the _config
        super().__init__(name=name, role_desc=role_desc, backend=backend_config,
                         global_prompt=global_prompt, **kwargs)
        

        self.backend = backend

    def to_config(self) -> AgentConfig:
        return AgentConfig(
            name=self.name,
            role_desc=self.role_desc,
            backend=self.backend.to_config(),
            global_prompt=self.global_prompt,
        )

    def act(self, observation: List[Message], request_msg=None, single_history=False) -> str:
        """
        Call the agents to generate a response (equivalent to taking an action).
        """
        try:
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc,
                                          history_messages=observation, global_prompt=self.global_prompt,
                                          request_msg=request_msg, single_history=single_history)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def __call__(self, observation: List[Message],request_msg=None, single_history=False) -> str:
        return self.act(observation, request_msg=request_msg, single_history=single_history)

    async def async_act(self, observation: List[Message], request_msg=None) -> str:
        """
        Async call the agents to generate a response (equivalent to taking an action).
        """
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=self.global_prompt,
                                                request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def reset(self):
        self.backend.reset()




class ChameleonPlayer(Player):
    """
    Player of the game. It can takes the observation from the environment and return an action
    """

    def __init__(self, name: str, role: str, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend],
                 global_prompt: str = None, **kwargs):

        super().__init__(name=name, role_desc=role_desc, backend=backend,
                         global_prompt=global_prompt, **kwargs)
        self.role = role
        
        


    def act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Call the agents to generate a response (equivalent to taking an action).
        """
        if stage == "give clues":
            cur_global_clue = self.global_prompt + clue_demo[self.role]
        elif stage == "pgm":
            cur_global_clue = self.global_prompt + view_demo[self.role]
        else:
            cur_global_clue=self.global_prompt
        
        try:
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc,
                                          history_messages=observation, global_prompt=cur_global_clue,
                                          request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def __call__(self, observation: List[Message],request_msg=None, stage=None) -> str:
        return self.act(observation, request_msg=request_msg, stage=stage)

    async def async_act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Async call the agents to generate a response (equivalent to taking an action).
        """
        if stage == "give clues":
            cur_global_clue = self.global_prompt + clue_demo[self.role]
        elif stage == "pgm":
            cur_global_clue = self.global_prompt + view_demo[self.role]
        else:
            cur_global_clue=self.global_prompt
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=cur_global_clue,
                                                request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def reset(self):
        self.backend.reset()





class PGMPlayer(Player):
    """
    Player of the game. It can takes the observation from the environment and return an action
    """

    def __init__(self, name: str, role: str, clue_demo, view_demo, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend],
                 global_prompt: str = None, **kwargs):

        super().__init__(name=name, role_desc=role_desc, backend=backend,
                         global_prompt=global_prompt, **kwargs)
        self.role = role
        self.clue_demo = clue_demo
        self.view_demo = view_demo
        
    
    def act(self, observation: List[Message], request_msg=None, stage=None, single_history=False) -> str:
        """
        Call the agents to generate a response (equivalent to taking an action).
        """
        if stage == "give clues":
            cur_global_clue = self.global_prompt + self.clue_demo[self.role]
        elif stage == "pgm":
            cur_global_clue = self.global_prompt + self.view_demo[self.role]
        else:
            cur_global_clue=self.global_prompt
        
        try:
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc,
                                          history_messages=observation, global_prompt=cur_global_clue,
                                          request_msg=request_msg, single_history=single_history)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def __call__(self, observation: List[Message],request_msg=None, stage=None, single_history=False) -> str:
        return self.act(observation, request_msg=request_msg, stage=stage, single_history=single_history)

    async def async_act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Async call the agents to generate a response (equivalent to taking an action).
        """
        if stage == "give clues":
            cur_global_clue = self.global_prompt + self.clue_demo[self.role]
        elif stage == "pgm":
            cur_global_clue = self.global_prompt + self.view_demo[self.role]
        else:
            cur_global_clue=self.global_prompt
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=cur_global_clue,
                                                request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    def reset(self):
        self.backend.reset()


class FixUndercoverPlayer(Player):
    """
    Player of the game. It can takes the observation from the environment and return an action
    """
    def __init__(self, name: str, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend], game_path: str,
                 global_prompt: str = None, **kwargs):
        super().__init__(name=name, role_desc=role_desc, backend=backend,
                         global_prompt=global_prompt, **kwargs)
        
        with open(game_path) as f:
            hist = json.load(f)["history"]
        self.clues = []
        for msg in hist:
            if msg["agent_name"] == name and msg["visible_to"] == "all":
                self.clues.append(msg["content"])
        
        print(f"Init FixPlayer for {name}, My clue is {self.clues}")

    def act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Call the agents to generate a response (equivalent to taking an action).
        """
        print(stage)
        if stage == "give clues":
            print(f"{self.name}============>using fix clue {self.clues[0]}")
            response = self.clues[0]
            self.clues.pop(0)
            return response
        try: 
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc,
                                          history_messages=observation, global_prompt=self.global_prompt,
                                          request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    async def async_act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Async call the agents to generate a response (equivalent to taking an action).
        """
        print("aynsc: ", stage)
        if stage == "give clues":
            print(f"{self.name}============>using fix clue {self.clue}")
            response = self.clue
            return response
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=self.global_prompt,
                                                request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response


    def __call__(self, observation: List[Message],request_msg=None, stage=None) -> str:
        return self.act(observation, request_msg=request_msg, stage=stage)






class Moderator(Player):
    """
    A special type of player that moderates the conversation (usually used as a component of environment).
    """

    def __init__(self, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend],
                 terminal_condition: str, global_prompt: str = None, **kwargs):
        name = "Moderator"
        super().__init__(name=name, role_desc=role_desc, backend=backend, global_prompt=global_prompt, **kwargs)

        self.terminal_condition = terminal_condition

    def to_config(self) -> AgentConfig:
        return AgentConfig(
            name=self.name,
            role_desc=self.role_desc,
            backend=self.backend.to_config(),
            terminal_condition=self.terminal_condition,
            global_prompt=self.global_prompt,
        )

    def is_terminal(self, history: List[Message], *args, **kwargs) -> bool:
        """
        check whether the conversation is over
        """
        # If the last message is the signal, then the conversation is over
        if history[-1].content == SIGNAL_END_OF_CONVERSATION:
            return True

        try:
            request_msg = Message(agent_name=self.name, content=self.terminal_condition, turn=-1)
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc, history_messages=history,
                                          global_prompt=self.global_prompt, request_msg=request_msg, *args, **kwargs)
        except RetryError as e:
            logging.warning(f"Agent {self.name} failed to generate a response. "
                            f"Error: {e.last_attempt.exception()}.")
            return True

        if re.match(r"yes|y|yea|yeah|yep|yup|sure|ok|okay|alright", response, re.IGNORECASE):
            # print(f"Decision: {response}. Conversation is ended by moderator.")
            return True
        else:
            return False


class FixChameleonPlayer(Player):
    """
    Player of the game. It can takes the observation from the environment and return an action
    """
    def __init__(self, name: str, role_desc: str, backend: Union[BackendConfig, IntelligenceBackend], game_path: str,
                 global_prompt: str = None, **kwargs):
        super().__init__(name=name, role_desc=role_desc, backend=backend,
                         global_prompt=global_prompt, **kwargs)
        game_path = 'llm_agent/' + game_path
        with open(game_path) as f:
            hist = json.load(f)["history"]
        for msg in hist:
            if msg["agent_name"] == name:
                self.clue = msg["content"]
                break
        print(f"Init FixChameleonPlayer for {name}, My clue is {self.clue}")

    def act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Call the agents to generate a response (equivalent to taking an action).
        """
        print(stage)
        if stage == "give clues":
            print(f"{self.name}============>using fix clue {self.clue}")
            response = self.clue
            return response
        try: 
            response = self.backend.query(agent_name=self.name, role_desc=self.role_desc,
                                          history_messages=observation, global_prompt=self.global_prompt,
                                          request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response

    async def async_act(self, observation: List[Message], request_msg=None, stage=None) -> str:
        """
        Async call the agents to generate a response (equivalent to taking an action).
        """
        print("aynsc: ", stage)
        if stage == "give clues":
            print(f"{self.name}============>using fix clue {self.clue}")
            response = self.clue
            return response
        try:
            response = self.backend.async_query(agent_name=self.name, role_desc=self.role_desc,
                                                history_messages=observation, global_prompt=self.global_prompt,
                                                request_msg=request_msg)
        except RetryError as e:
            err_msg = f"Agent {self.name} failed to generate a response. Error: {e.last_attempt.exception()}. Sending signal to end the conversation."
            logging.warning(err_msg)
            response = SIGNAL_END_OF_CONVERSATION + err_msg

        return response


    def __call__(self, observation: List[Message],request_msg=None, stage=None) -> str:
        return self.act(observation, request_msg=request_msg, stage=stage)