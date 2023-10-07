from typing import List, Dict, Union
import random
import re
import json
import time
import os
import numpy as np
from .base import Environment, TimeStep
from ..message import Message, MessagePool
from ..agent import SIGNAL_END_OF_CONVERSATION
from ..config import EnvironmentConfig
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)

# 获取当前文件的目录
current_dir = os.path.dirname(current_file)

# 获取chatarena的父目录
parent_dir = os.path.dirname(current_dir)

parent_dir = os.path.dirname(parent_dir)

#print(parent_dir)

# 获取utils目录的路径
utils_dir = os.path.join(parent_dir, 'utils')

# 获取undercover_words.json文件的完整路径
file_path = os.path.join(utils_dir, 'undercover_words.json')

with open(file_path) as f:
    DEFAULT_TOPIC_CODES = json.load(f)["words"]


class Undercover_Competition(Environment):
    type_name = "undercover_competition"
 
    def __init__(self, player_names: List[str], topic_codes: Dict[str, List[str]] = None, competition=None, **kwargs):
        super().__init__(player_names=player_names, topic_codes=topic_codes, **kwargs)

        if topic_codes is None:
            topic_codes = DEFAULT_TOPIC_CODES
        self.topic_codes = topic_codes

        # The "state" of the environment is maintained by the message pool
        self.message_pool = MessagePool()

        # Randomly sample a topic, code and undercover player
        self.topic = None
        self.code = None
        self.undercover_name = None
        self.non_undercover_names = None

        # Game states
        self._current_turn = 0
        self._next_player_idx = 0
        self._current_phase = "give clues"  # "give clues", "accuse", "guess"
        self._players_votes = None
        self._initialized = False
        self._win_group = -1
        self.player_backends = {}
        self.competition = competition
        self.game_setting = None
        self.rewrite_game_setting = False
        self._clue_round = 2
        self._remain_clue_round = self._clue_round
        self._single_history=False
        

        self.reset()  # To initialize the game (select topic, code, undercover)

    def get_next_player(self) -> str:
        """
        get the next player
        """
        if self._current_phase != "guess":
            return self.player_names[self._next_player_idx]
        else:
            return self.undercover_name
    
    def log_game(self, path):
        """
        save the game history and results:
        game setting, backend setting, game history and result
        """
        
        messages = self.get_observation()
        message_rows = []
        for message in messages:
            message_row = {
                "agent_name": message.agent_name,
                "content": message.content,
                "turn": message.turn,
                "timestamp": str(message.timestamp),
                "visible_to": message.visible_to,
                "msg_type": message.msg_type,
            }
            message_rows.append(message_row)
            
        assert self._win_group >= 0
        result = "non-undercover" if self._win_group == 0 else "undercover"

        with open(path, "w") as f:
            json.dump({
                "undercover": self.undercover_name, 
                "game_setting": self.game_setting,
                "player_backends": self.player_backends, 
                "history": message_rows,
                "win_flag": self._win_group,
                "result": result,
                "player_vote": self._vote_of_each_player,
                }, 
                f, indent=4)

    def get_win_group(self):
        assert self._win_group >= 0
        return "non-undercover" if self._win_group == 0 else "undercover"

    def save_game_setting(self, game_setting):
        now = time.strftime("%m%d%H%M%S", time.localtime(time.time()))
        fname = f"results/game_settings/{now}"
        if os.path.exists(fname):
            k = 1
            while True:
                nfname = f"{fname}-{k}"
                if not os.path.exists(nfname):
                    break
                k += 1
            fname = nfname
            
        with open(fname,"w") as f:
            json.dump(game_setting, f)
    
    def reset(self):
        """
        sample topic, code and undercover code
        """
        if self.competition["random"]:
            topic_group_idx = random.choice(range(len(self.topic_codes))) 
            self.undercover_code, self.non_undercover_code = np.random.choice(self.topic_codes[topic_group_idx], size=2, replace=False)
            self.undercover_name = random.choice(self.player_names)
        else:
            self.undercover_code = self.competition["undercover_code"]
            self.non_undercover_code = self.competition["non_undercover_code"]
            self.undercover_name = self.competition["undercover_name"]
        self.game_setting = {"undercover_code": self.undercover_code, "non_undercover_code": self.non_undercover_code, "undercover_name": self.undercover_name}

        self.non_undercover_names = [name for name in self.player_names if name != self.undercover_name]
        
        # reset the players' backends depends on their roles
        self.player_backends = {}
        if self.competition:
            for player_name in self.player_names:
                if player_name == self.undercover_name:
                    self.player_backends[player_name] = self.competition["undercover"]
                else:
                    self.player_backends[player_name] = self.competition["non-undercover"]

        self._current_turn = 0
        self._next_player_idx = 0
        self._remain_clue_round = self._clue_round
        self._current_phase = "give clues"

        self.message_pool.reset()

        self._moderator_speak(f"Now the game starts!")
        self._moderator_speak(f"Your word is: {self.undercover_code}",
                              visible_to=self.undercover_name)
        for player_name in self.non_undercover_names:
            self._moderator_speak(f"Your word is: {self.non_undercover_code}",
                              visible_to=player_name)
        self._moderator_speak(
            f"Now everyone gives one clue (but never include the secret word). "
            f"You cannot repeat what others has said. We will start with {self.player_names[0]}.")
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._vote_of_each_player= {name: None for name in self.player_names}
        self._win_group = -1 # 0, none undercover; 1(right vote, guessed right),2(wrong vote),3(even vote)

        self._initialized = True
        init_timestep = TimeStep(observation=self.get_observation(),
                                 reward=self.get_zero_rewards(),
                                 terminal=False)

        return init_timestep

    def print(self):
        self.message_pool.print()

    def get_observation(self, player_name=None) -> List[Message]:
        """
        get observation for the player
        """
        if player_name is None:
            return self.message_pool.get_all_messages()
        else:
            return self.message_pool.get_visible_messages(player_name, turn=self._current_turn)

    def _text2vote(self, text) -> str:
        """
        convert text to vote, return a player's name
        """
        # lower = text.lower().replace("[", "").replace("]", "").replace(".", "")
        text = text.lower()
        for name in self.player_names:
            candidates = [name.lower(), name.lower().replace(" ", ""), name.lower().replace(" ", "_")]
            if any([candidate in text for candidate in candidates]):
                return name
        return ""

    def _is_true_code(self, text) -> bool:
        """
        Check whether the text is the true code
        """
        # Get the word enclosed by quote marks with regex
        pattern = r"\"(.+?)\""
        match = re.search(pattern, text)
        if match:
            return match.group(1).lower().replace(" ", "") == self.code.lower().replace(" ", "")
        else:
            # if no quote marks, check whether the last k words match the code
            words = text.split()
            if len(words) >= len(self.code.split()):
                guessed_term = "".join(words[-len(self.code.split()):]).lower().replace(".", "")
                return guessed_term == self.code.lower().replace(" ", "").replace(".", "")
            else:
                return False

    def _moderator_speak(self, text: str, visible_to: Union[str, List[str]] = "all"):
        """
        moderator say something
        """
        message = Message(agent_name="Moderator", content=text, turn=self._current_turn, visible_to=visible_to)
        self.message_pool.append_message(message)

    def get_rewards(self, undercover_win: bool) -> Dict[str, float]:
        """
        get rewards for each player
        """
        rewards = {}
        for name in self.player_names:
            # The winner gets 1, the loser gets 0
            rewards[name] = float((name == self.undercover_name) == undercover_win)

        return rewards

    def is_terminal(self) -> bool:
        """
        check if the conversation is over
        """
        # If the last message is the signal, then the conversation is over
        if self.message_pool.last_message.content.startswith(SIGNAL_END_OF_CONVERSATION):
            return True

    def step(self, player_name: str, action: str) -> TimeStep:
        """
        step function that is called by the arena
        Args:
            player_name: the name of the player that takes the action
            action: the action that the agents wants to take
        """
        # If not initialized, reset the environment
        if not self._initialized:
            self.reset()

        # self.message_pool.print()
        # print(f"undercover: {self.undercover_name}, Code: {self.code}, Topic: {self.topic}")
        assert player_name == self.get_next_player(), f"Wrong player! It is {self.get_next_player()} turn."
        if self._current_phase == "give clues":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn)
            self.message_pool.append_message(message)

            # Update the counters
            self._current_turn += 1
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
            else:
                self._next_player_idx = 0
                self._remain_clue_round -= 1
                if self._remain_clue_round == 0:
                    self._current_phase = "accuse"
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the undercover. "
                                      "You cannot vote for yourself.")
                else:
                    self._current_phase = "give clues"
                    self._moderator_speak(f"Now we starting {self._clue_round+1-self._remain_clue_round} round of giving clue, we still start from {self.player_names[0]}")

                self._current_turn += 1

            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages
        elif self._current_phase == "accuse":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            vote = self._text2vote(action)
            self._vote_of_each_player[player_name] = vote
            if vote in self.player_names:
                self._players_votes[vote] += 1

            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
                rewards = self.get_zero_rewards()
                terminal = False
            else:
                # print(self._players_votes)
                accuse_correct, even_vote = True, False
                max_vote_player = max(self._players_votes, key=self._players_votes.get)
                # detach if other players has the same number of votes
                for name, vote in self._players_votes.items():
                    if name != max_vote_player and vote == self._players_votes[max_vote_player]:
                        accuse_correct, even_vote = False, True
                if max_vote_player != self.undercover_name:
                    accuse_correct = False

                if not accuse_correct:
                    if even_vote:
                        self._moderator_speak(f"There are even votes. The accusation does not stand. "
                                              f"{self.undercover_name} is the undercover. {self.undercover_name} won the game!")
                        self._win_group = 2
                    else:
                        self._moderator_speak(
                            f"The most-voted player is {max_vote_player}. The accusation is incorrect. "
                            f"{self.undercover_name} is the undercover. {self.undercover_name} won the game!"
                        )
                        self._win_group = 1
                    rewards = self.get_rewards(undercover_win=True)
                    
                else:
                    self._moderator_speak(
                            f"The most-voted player is {max_vote_player}. The accusation is correct. "
                            f"{self.undercover_name} is the undercover. {self.undercover_name} won the game!"
                        )
                    self._win_group = 0
                    rewards = self.get_rewards(undercover_win=False)
                terminal = True

            timestep = TimeStep(observation=self.get_observation(), reward=rewards, terminal=terminal)
        
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")
        
        print(self._win_group)

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True
        

        return timestep
