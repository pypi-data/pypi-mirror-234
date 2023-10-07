
"""
PGM only when PGM player start to act
"""
from typing import List, Dict, Union
import random
import re
import json
import time
import os
from .base import Environment, TimeStep
from ..message import Message, MessagePool
from ..agent import SIGNAL_END_OF_CONVERSATION
from ..config import EnvironmentConfig


from chatarena.pgm import PGM_List
from utils.view_template import *
from utils.pgm_calculator import PGM
from utils.clue import Clue
import numpy as np
import copy

DEFAULT_TOPIC_CODES = {
    "Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Grape",
        "Strawberry",
        "Pineapple",
        "Mango",
        "Watermelon",
    ],
    "Animals": [
        "Lion",
        "Elephant",
        "Giraffe",
        "Monkey",
        "Zebra",
        "Tiger",
        "Bear",
        "Kangaroo",
    ],
    "Sports": [
        "Soccer",
        "Basketball",
        "Tennis",
        "Baseball",
        "Swimming",
        "Cycling",
        "Volleyball",
        "Golf",
    ],
    "Countries": [
        "United States",
        "Canada",
        "Brazil",
        "United Kingdom",
        "France",
        "Germany",
        "Japan",
        "Australia",
    ],
}


class Chameleon_Competition_PGM(Environment):
    type_name = "chameleon_competition_pgm"

    def __init__(self, player_names: List[str], topic_codes: Dict[str, List[str]] = None, competition=None, **kwargs):
        super().__init__(player_names=player_names, topic_codes=topic_codes, **kwargs)

        if topic_codes is None:
            topic_codes = DEFAULT_TOPIC_CODES
        self.topic_codes = topic_codes

        # The "state" of the environment is maintained by the message pool
        self.message_pool = MessagePool()

        # Randomly sample a topic, code and chameleon player
        self.topic = None
        self.code = None
        self.chameleon_name = None
        self.non_chameleon_names = None

        # Game states
        self._current_turn = 0
        self._next_player_idx = 0
        self._current_phase = "give clues"  # "give clues", "accuse", "guess"
        self._players_votes = None
        self._initialized = False
        self._win_group = -1
        self.player_backends = {}
        self.game_setting = None
        self.competition = competition

        self._num_players = len(self.player_names)
        self._view_templ = templ_1
        self._view_non_chameleon_templ = view_templ_active_non_chameleon
        self._view_chameleon_templ = view_templ_active_chameleon_wcode_v2
        self._clue_templ = clue_templ_v1
        # self._clue_templ_non_chameleon = clue_templ_active
        # self._clue_templ_chameleon = clue_templ_active_chameleon
        self._clue_templ_non_chameleon = clue_templ_active_1
        self._clue_templ_chameleon = clue_templ_active_chameleon_1
        with open("results/analysis_demo_two_role_simple.txt") as f:
           self._analysis_demo = f.read()


        self.reset()  # To initialize the game (select topic, code, chameleon)

    def get_next_player(self) -> str:
        """
        get the next player
        """
        if self._current_phase != "guess":
            print(self._next_player_idx)
            return self.player_names[self._next_player_idx]
        else:
            return self.chameleon_name
    
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
                "is_pgm": message.is_pgm,
                "is_good_pgm": message.is_good_pgm,
                "is_clue": message.is_clue,
                "is_good_clue": message.is_good_clue,
            }
            message_rows.append(message_row)
        assert self._win_group >= 0
        result = "non-chameleon" if self._win_group == 0 else "chameleon"

        with open(path, "w") as f:
            json.dump({
                "chameleon": self.chameleon_name, 
                "game_setting": self.game_setting,
                "player_backends": self.player_backends, 
                "history": message_rows,
                "win_flag": self._win_group,
                "player_votes": self._vote_for_each_player,
                "result": result,
                }, 
                f, indent=4)

    def get_win_group(self):
        assert self._win_group >= 0
        return "non-chameleon" if self._win_group == 0 else "chameleon"

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
        sample topic, code and chameleon code
        """
        self.game_path = None 
        print(self.competition["random"])
        if self.competition["random"]:
            self.topic = random.choice(list(self.topic_codes.keys()))
            self.code = random.choice(self.topic_codes[self.topic])
            self.chameleon_name = random.choice(self.player_names)
        else:
            self.topic = self.competition["topic"]
            self.code = self.competition["code"]
            self.chameleon_name = self.competition["chameleon_name"]
        self.game_setting = {"topic": self.topic, "code": self.code, "chameleon_name": self.chameleon_name}

        self.chameleon_idx = self.player_names.index(self.chameleon_name)
        self.non_chameleon_names = [name for name in self.player_names if name != self.chameleon_name]

        # reset the players' backends depends on their roles
        self.player_backends = {}
        if self.competition:
            for player_name in self.player_names:
                if player_name == self.chameleon_name:
                    self.player_backends[player_name] = self.competition["chameleon"]
                else:
                    self.player_backends[player_name] = self.competition["non-chameleon"]



        self._player_pgm_dict = PGM_List(self.player_names, self.chameleon_name)
        self._finish_clue = False
        self._initialized = True
        self._pgm_list = []
        for pi in range(self._num_players):
            is_chameleon = (pi==self.chameleon_idx)
            self._pgm_list.append(PGM(is_chameleon, self._num_players, pi))
        
        self._clue_list = []
        self.target_player_tuples = [] #(a,b,c)
        self._clue_turn = 0
        self.all_player_views  = []
        now = time.strftime("%m%d%H%M%S", time.localtime(time.time()))
        self.clue_fname=f"results/clues/{now}"
        self.is_leak = False
        self.target_player_tuples = [(pi, 0, -1) for pi in range(self._num_players) if pi != 0]


        self._current_turn = 0
        self._next_player_idx = 0
        self._current_phase = "give clues"

        self.message_pool.reset()
        
        
        self.pgm_players = [pn for pn in self.player_names if self.player_backends[pn]["model"].endswith("pgm")]
        self.pgm_player_ids = [self.player_names.index(pn) for pn in self.pgm_players]
        # import pdb;pdb.set_trace()

        self._moderator_speak(f"To help you know how to analyze the roles of players, I will give you some examples:\n{self._analysis_demo}", visible_to=self.pgm_players)

        self._moderator_speak(f"Now the game starts! This is a totally new game. Don't take content from the above exmaples into the current game. The topic is: {self.topic}")
        self._moderator_speak(f"You are not chameleon. The word is: {self.code}",
                              visible_to=self.non_chameleon_names)
        self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
        self._moderator_speak(
            f"Now everyone gives one clue (but never include the secret word). "
            f"You cannot repeat what others has said. We will start with {self.player_names[0]}.")
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._vote_for_each_player = {name: None for name in self.player_names}
        self._text_votes = {}
        self._pgm_votes = {}


        self._win_group = -1 # 0, none chameleon; 1(right vote, guessed right),2(wrong vote),3(even vote)

        self._initialized = True
        init_timestep = TimeStep(observation=self.get_observation(),
                                 reward=self.get_zero_rewards(),
                                 terminal=False)

        return init_timestep

    def print(self):
        self.message_pool.print()

    def get_observation(self, player_name=None, drop_not_show=False) -> List[Message]:
        """
        get observation for the player
        """
        if player_name is None:
            return self.message_pool.get_all_messages()
        else:
            return self.message_pool.get_visible_messages(player_name, turn=self._current_turn)

    
    def _text2change(self, text):
        """
        convert text to change on chameleon.
        """
        pattern = r'Player \d+'
        lines = text.split("\n")
        factor = np.zeros((self._num_players, self._num_players))
        changes = {"no change":0, "more suspicious":1, "less suspicious":-1}
        cur_player = self.player_names[self._next_player_idx]
        for line in lines:
            if line.startswith("Now I guess the secret word is "):
                guess_code = re.findall(r'"([^"]*)"', line)[0]
                if guess_code.lower() == self.code.lower():
                    self.is_leak = True
            
            if line.startswith("As Player"):
                cur_player = re.search(pattern, line).group(0)
            if line.startswith("I think now Player"):
                cur_player = re.search(pattern, line).group(0)
            if line.startswith("Player"):
                try:
                    cur_to_eval_player = re.search(pattern, line).group(0)
                    cur_eval = 0
                    for c in changes:
                        if c in line:
                            cur_eval = changes[c]
                except:
                    print("no change text detected")
                cur_player_idx = self.player_names.index(cur_player)
                # print(cur_player, cur_to_eval_player, cur_eval)
                cur_to_eval_player_idx = self.player_names.index(cur_to_eval_player)
                factor[cur_player_idx][cur_to_eval_player_idx] = cur_eval
        return factor


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


    def _cal_vote(self, text_votes):
        print(text_votes)
        pgm_votes = copy.deepcopy(text_votes)
        for pn in self.pgm_players:
            
            v = self._pgm_list[self.player_names.index(pn)]._to_vote()
            # print(pn, v)
            pgm_votes[pn] = self._pgm_list[self.player_names.index(pn)]._to_vote()
        
        vote_dict = {}
        even_note = False
        print("According to PGM:")
        for pn,v in pgm_votes.items():
            print(f"{pn} vote {self.player_names[v]}.")
            if v not in vote_dict:
                vote_dict[v] = 0
            vote_dict[v] += 1
        max_vote_idx = max(vote_dict, key=vote_dict.get)
        for v, n in vote_dict.items():
            if v != max_vote_idx and n == vote_dict[max_vote_idx]:
                even_note = True
        accuse_correct  = False
        if max_vote_idx == self.chameleon_idx and not even_note:
            accuse_correct = True
        return max_vote_idx, accuse_correct, even_note, vote_dict, pgm_votes

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

    def _moderator_speak(self, text: str, visible_to: Union[str, List[str]] = "all", is_show=True):
        """
        moderator say something
        """
        message = Message(agent_name="Moderator", content=text, turn=self._current_turn, visible_to=visible_to, is_show=is_show)
        self.message_pool.append_message(message)

    def get_rewards(self, chameleon_win: bool) -> Dict[str, float]:
        """
        get rewards for each player
        """
        rewards = {}
        for name in self.player_names:
            # The winner gets 1, the loser gets 0
            rewards[name] = float((name == self.chameleon_name) == chameleon_win)

        return rewards

    def is_terminal(self) -> bool:
        """
        check if the conversation is over
        """
        # If the last message is the signal, then the conversation is over
        if self.message_pool.last_message.content.startswith(SIGNAL_END_OF_CONVERSATION):
            return True
        
    def is_pgm_player(self, player_idx):
        return self.player_backends[self.player_names[player_idx]]["model"].endswith("pgm")
    

    def find_next_pgm_player(self, start_player_idx):
        # If already the last player, return None
        if not start_player_idx < len(self.player_names): 
            
            return None
        # Iterate and find the next PGM, if no, return None.
        for idx in range(start_player_idx, len(self.player_names)):
            if self.is_pgm_player(idx):
                return idx
        return None
        

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
        # print(f"Chameleon: {self.chameleon_name}, Code: {self.code}, Topic: {self.topic}")
        assert player_name == self.get_next_player(), f"Wrong player! It is {self.get_next_player()} turn."
        if self._current_phase == "give clues":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, is_clue=True)
            self.message_pool.append_message(message) # insert msg into pool
            self._current_clue_player_idx = self._next_player_idx  # record the current clue giver

            if self._next_player_idx < len(self.player_names) - 1:  # Update counter for next clue giver, record next clue giver
                self._next_clue_player_idx = self._next_player_idx + 1
                
            else:
                self._finish_clue = True

            
            if self._finish_clue: # After every player gives the clue, PGM player need to analyze again
                self._next_player_idx = self.find_next_pgm_player(0) # find the next pgm player from start
                print("pgm player: ", self._next_player_idx)
                if self._next_player_idx is not None:
                    self._current_phase = "pgm"
                    if self.chameleon_idx  == self._next_player_idx:
                        mod_text = self._view_chameleon_templ
                    else:
                        mod_text = self._view_non_chameleon_templ
                    mod_text = mod_text.replace("<PLAYER>", self.player_names[self._next_player_idx])
                    mod_text = mod_text.replace("<PRE_PLAYER>", self.player_names[self._current_clue_player_idx])
                    self._moderator_speak(mod_text, visible_to=[self.player_names[self._next_player_idx]], is_show=False)
                else:
                    self._current_phase = "accuse"
                    self._next_player_idx = 0 # vote from the first player
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                            "You cannot vote for yourself.\n")
                

            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages

        
        elif self._current_phase == "accuse":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            
            self.message_pool.append_message(message)
            vote = self._text2vote(action)
            self._text_votes[player_name] = self.player_names.index(vote)
            
            if vote in self.player_names:
                self._players_votes[vote] += 1
            
            if self._next_player_idx < len(self.player_names)-1:
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
                if max_vote_player != self.chameleon_name:
                    accuse_correct = False

                # if not accuse_correct:
                #     if even_vote:
                #         self._moderator_speak(f"There are even votes. The accusation does not stand. "
                #                               f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                #         self._win_group = 3
                #     else:
                #         self._moderator_speak(
                #             f"The most-voted player is {max_vote_player}. The accusation is incorrect. "
                #             f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!"
                #         )
                #         self._win_group = 2
                #     rewards = self.get_rewards(chameleon_win=True)
                #     terminal = True
                # else:
                    
                #     self._moderator_speak(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                #                           f"Now {self.chameleon_name} can guess the secret code. "
                #                           "You should say: I guess the code is \"...\"")
                    
                    # self._current_phase = "guess"
                    # rewards = self.get_zero_rewards()
                    # terminal = False
                print(self._text_votes)
                # show result of PGM, record PGM result in file
                cal_max_vote, cal_accuse_correct, cal_even_note, _ , self._pgm_votes = self._cal_vote(self._text_votes)
                print(self._pgm_votes)
                for pl in self._pgm_votes:

                    self._vote_for_each_player[pl]= self.player_names[self._pgm_votes[pl]]
                if not cal_accuse_correct:
                    if cal_even_note:
                        self._moderator_speak(f"There are even notes. The chameleon {self.chameleon_name} wins.")
                        print(f"There are even notes. The chameleon {self.chameleon_name} wins.")
                        self._win_group = 3
                        
                    else:
                        self._moderator_speak(f"The most-voted player is {self.player_names[cal_max_vote]}. The accusation is incorrect. "
                              f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                        print(f"The most-voted player is {self.player_names[cal_max_vote]}. The accusation is incorrect. "
                              f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                        self._win_group = 2
                    rewards = self.get_rewards(chameleon_win=True)
                    terminal = True
                else:
                    self._moderator_speak(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                                          f"Now {self.chameleon_name} can guess the secret code. "
                                          "You should say: I guess the code is \"...\"")
                    print(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                                          f"Now {self.chameleon_name} can guess the secret code. "
                                          "You should say: I guess the code is \"...\"")
                    self._current_phase = "guess"
                    rewards = self.get_zero_rewards()
                    terminal = False
                    
                    
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(), reward=rewards, terminal=terminal)

        elif self._current_phase == "guess":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=player_name)
            self.message_pool.append_message(message)
            if self._is_true_code(action):
                self._moderator_speak(f"{player_name} guessed the code correctly! The secret word is {self.code}. "
                                      f"{self.chameleon_name} won!")
                self._win_group = 1
                rewards = self.get_rewards(chameleon_win=True)
            else:
                self._moderator_speak(f"{player_name} guessed the code wrong! The secret word is {self.code}. "
                                      f"{self.non_chameleon_names} won!")
                self._win_group = 0
                rewards = self.get_rewards(chameleon_win=False)

            timestep = TimeStep(observation=self.get_observation(),
                                reward=rewards,
                                terminal=True)
        elif self._current_phase == "pgm":

            print("Before")
            cur_pgm = self._pgm_list[self.player_names.index(player_name)]
            cur_pgm.print() # print existing PGM
            factor = self._text2change(action)
            self.all_player_views.append(factor[self._next_player_idx])
            cur_pgm.update(factor)
            print(player_name, factor)
            print("After")
            cur_pgm.print()
            is_good_pgm = False
            if player_name != self.chameleon_name:
                is_good_pgm = cur_pgm.get_target() == self.chameleon_idx
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, is_pgm=True, is_good_pgm=is_good_pgm,
                              visible_to=[player_name])
            self.message_pool.append_message(message)            
            self._next_player_idx += 1 # find next pgm player
            self._next_player_idx = self.find_next_pgm_player(self._next_player_idx)
            print("pgm player: ", self._next_player_idx)

            if self._next_player_idx is not None:
                self._current_phase = "pgm" 
                if self.chameleon_idx  == self._next_player_idx:
                    mod_text = self._view_chameleon_templ
                else:
                    mod_text = self._view_non_chameleon_templ
                mod_text = mod_text.replace("<PLAYER>", self.player_names[self._next_player_idx])
                mod_text = mod_text.replace("<PRE_PLAYER>", self.player_names[self._current_clue_player_idx])
                self._moderator_speak(mod_text, visible_to=[self.player_names[self._next_player_idx]], is_show=False)  
            else:
                self._next_player_idx = self._next_clue_player_idx  # Cannot find next pgm player, go to the clue phase
                if self._finish_clue:
                    self._current_phase = "accuse"
                    self._next_player_idx = 0
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                        "You cannot vote for yourself.\n")
                else:
                    # if all player finish giving the pgm to 
                    self._current_phase = "give clues"
                    is_pgm = self.is_pgm_player(self._next_player_idx)
                    # If PGM player, the moderator will give the target for the player.
                    if is_pgm:
                        self._target_player_idx = self._pgm_list[self._next_clue_player_idx].get_target()
                        if self.chameleon_idx == self._next_clue_player_idx: 
                            mod_text = self._clue_templ_chameleon
                            self.target_player_tuples=[(self._target_player_idx, self._next_clue_player_idx, -1)]
                        else:
                            mod_text = self._clue_templ_non_chameleon
                            self.target_player_tuples = [(i, self._target_player_idx, 1) for i in range(self._num_players) if i not in [self._target_player_idx, self._next_player_idx]]
                        mod_text = mod_text.replace("<PLAYER>",self.player_names[self._next_clue_player_idx])
                        mod_text = mod_text.replace("<TARGET_PLAYER>",self.player_names[self._target_player_idx])
                        self._moderator_speak(mod_text, visible_to=[self.player_names[self._next_clue_player_idx]])
                    self._moderator_speak(f"Now {self.player_names[self._next_clue_player_idx]}, please give your text clue. Never include the secret word.", visible_to=[self.player_names[self._next_clue_player_idx]])

                
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")
        
        print(self._win_group)


        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True
        

        return timestep
