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
from ...utils.pgm_calculator import UndercoverPGM
from ...prompts.under_cover_pgm import *
import copy


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


class Undercover_Competition_PGM(Environment):
    type_name = "undercover_competition_pgm"
 
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
        self._num_players = len(player_names)
     
        self._clue_unclear = clue_templ_active_unclear_v2
        self._clue_undercover = clue_templ_active_undercover_v2
        self._clue_non_undercover = clue_templ_active_non_undercover_v2

        self.pgm_template = pgm_template_v5
        self.pgm_template_questions = pgm_template_questions

        self._view_template = pgm_template_v4
        self._view_template_question = pgm_template_question_v4
        self._view_unclear = pgm_unclear
        self._view_undercover = pgm_undercover
        self._view_non_undercover = pgm_non_undercover
        self._single_history = False

        self._analysis_demo = analysis_demo_v1

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

        self.undercover_idx = self.player_names.index(self.undercover_name)
        
        # reset the players' backends depends on their roles
        self.player_backends = {}
        if self.competition:
            for player_name in self.player_names:
                if player_name == self.undercover_name:
                    self.player_backends[player_name] = self.competition["undercover"]
                else:
                    self.player_backends[player_name] = self.competition["non-undercover"]
        self.pgm_players = [pn for pn in self.player_names if self.player_backends[pn]["model"].endswith("pgm")]
        self.threshold=0.009
        self._current_turn = 0
        self._next_player_idx = 0
        self._remain_clue_round = self._clue_round
        self._pgm_list = []
        self._undercover_self_diagnoses = {p:"not sure" for p in self.player_names}
        self._pgm_step = "is_undercover"
        self._pgm_before_clue = True
        
        for pi in range(self._num_players):
            self._pgm_list.append(UndercoverPGM(self._num_players, pi))


        self._current_phase = "give clues"

        self.message_pool.reset()
        # self._moderator_speak(f"To help you know how to analyze who is undercover, I will give you an example:\n{self._analysis_demo}", visible_to=self.pgm_players)


        self._moderator_speak(f"Now the game starts!")
        self._moderator_speak(f"Your word is: {self.undercover_code}",
                              visible_to=self.undercover_name)
        for player_name in self.non_undercover_names:
            self._moderator_speak(f"Your word is: {self.non_undercover_code}",
                              visible_to=player_name)
        self._moderator_speak(
            f"Now everyone gives one clue (but never include the secret word). "
            f"You cannot repeat what others has said. We will start with {self.player_names[0]}.")
        
        if self.is_pgm_player(0): 
            self._moderator_speak(self._clue_unclear.format(player=self.player_names[0]), visible_to=[self.player_names[0]])
        
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._vote_of_each_player= {name: None for name in self.player_names}
        self._win_group = -1 # 0, none undercover; 1(right vote, guessed right),2(wrong vote),3(even vote)
        self._text_votes = {name: -1 for name in self.player_names}
        self.pgm_players = [pn for pn in self.player_names if self.player_backends[pn]["model"].endswith("pgm")]
        self.pgm_player_ids = [self.player_names.index(pn) for pn in self.pgm_players]

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
    def _text2pgm(self, text):

        pass
    def _text2change(self, text):
        """
        convert text to change on undercover.
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
                cur_to_eval_player = re.search(pattern, line).group(0)
                cur_eval = 0
                for c in changes:
                    if c in line:
                        cur_eval = changes[c]
                cur_player_idx = self.player_names.index(cur_player)
                # print(cur_player, cur_to_eval_player, cur_eval)
                cur_to_eval_player_idx = self.player_names.index(cur_to_eval_player)
                factor[cur_player_idx][cur_to_eval_player_idx] = cur_eval
        return factor
    
    def _text2changev3(self, text):
        """
        convert text to change on undercover.
        """
        pattern = r"Player \d+"
        pattern1 = r'I think Player \d+ is *[undercover|the undercover]'
        pattern2 = r'I think Player \d+ thinks Player \d+ is *[undercover|the undercover]'

        lines = text.split("\n")
        factor = np.zeros((self._num_players, self._num_players))
        changes = {"no change":0, "more suspicious":1, "less suspicious":-1}
        cur_player = self.player_names[self._next_player_idx]
        for line in lines:
            if line == "\n" :
                continue
            
            if re.search(pattern1, line):
                cur_view_player_idx = self.player_names.index(cur_player)
                cur_to_eval_player_idx = self.player_names.index(re.findall(pattern, re.search(pattern1, line).group(0))[0])
                factor[cur_view_player_idx][cur_to_eval_player_idx] = changes["more suspicious"]

            elif re.search(pattern2, line):
                players = re.findall(pattern, re.search(pattern2, line).group(0))
                assert len(players) == 2
                cur_view_player_idx = self.player_names.index(players[0])
                cur_to_eval_player_idx = self.player_names.index(players[1])
                factor[cur_view_player_idx][cur_to_eval_player_idx] = changes["more suspicious"]
            else:
                print("cannot parse the line: ", line)
        print(factor)
        return factor

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
    
    def _cal_vote(self, text_votes):
        print(text_votes)
        pgm_votes = copy.deepcopy(text_votes)
        for pn in self.pgm_players:
            v = self._pgm_list[self.player_names.index(pn)]._to_vote()
            print(pn, v)
            pgm_votes[pn] = v
        
        vote_dict = {}
        even_note = False
        print("According to PGM:")
        for pn,v in pgm_votes.items():
            if v is None: 
                print(f"{pn} vote None in PGM, use the vote from text,", self.player_names[text_votes[pn]] )
                v = text_votes[pn] 
                pgm_votes[pn] = v
            else:
                print(f"{pn} vote {self.player_names[v]}.")
            if v not in vote_dict:
                vote_dict[v] = 0
            vote_dict[v] += 1
        max_vote_idx = max(vote_dict, key=vote_dict.get)
        for v, n in vote_dict.items():
            if v != max_vote_idx and n == vote_dict[max_vote_idx]:
                even_note = True
        accuse_correct  = False
        if max_vote_idx == self.undercover_idx and not even_note:
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

    def _get_current_clues(self):
        msgs = self.get_observation()
        cur_clues = []
        for msg in msgs:
            if msg.agent_name.startswith("Player") and msg.is_clue and msg.visible_to == "all":
                cur_clues.append(msg.agent_name+": "+msg.content)
        return cur_clues

    def _get_current_clue_text(self, player_name=None):
        cur_clues = self._get_current_clues()
        cur_clue_text = ""
        round_num = int(len(cur_clues)/len(self.player_names))
        player_num = int(len(self.player_names))
        clue_text_list= []
        for ci, clue in enumerate(cur_clues):
            if ci % player_num == 0:
                ri = ci // player_num
                clue_text_list.append(f"Round {ri}")
            clue_text_list.append(clue)
        cur_clue_text = "\n".join(clue_text_list)
        return cur_clue_text 
            
    def parse_undercover(self, output_text):
        ans = output_text.split(",")[0].strip().lower()
        
        if ans in ["yes","no","not sure"]:
            return ans
        else:
            print("cannot parse the answer,", output_text)
            return "not sure"

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
        request_msg = None
        self._single_history = False

        assert player_name == self.get_next_player(), f"Wrong player! It is {self.get_next_player()} turn."
        if self._current_phase == "give clues":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, is_clue=True)
            self.message_pool.append_message(message)
            print("GIVING CLUE, ",  player_name)
            # print(self._get_current_clue_text())

            if self._next_player_idx < len(self.player_names) - 1: # enumerate all player to give clues
                self._next_player_idx += 1
                next_player = self.player_names[self._next_player_idx]
                if self.is_pgm_player(self._next_player_idx):
                    self._current_phase = "pgm"
                    self._single_history = True
                    clues = self._get_current_clue_text()
                    clue_text = self.pgm_template.format(clues=clues)
                    code = self.undercover_code if next_player == self.undercover_name else self.non_undercover_code
                    user_text = clue_text + self.pgm_template_questions["is_undercover"].format(player=next_player, code=code)
                    request_msg = user_text
                else:
                    self._current_phase = "give clues"
                    self._moderator_speak(f"Now {next_player}, please give your text clue. Never include the secret word.", visible_to=[next_player])
                    


                # if self.is_pgm_player(self._next_player_idx):                    
                #     self_diag = self._undercover_self_diagnoses[next_player]
                #     _, _target_player_idx = self._pgm_list[self._next_player_idx].get_target()
                #     target_player = self.player_names[_target_player_idx]
                #     if self_diag == "not sure":
                #         mod_text = self._clue_unclear
                #     elif self_diag == "yes":
                #         mod_text = self._clue_undercover
                #     elif self_diag == "no":
                #         mod_text = self._clue_non_undercover
                #     else:
                #         print("Do not support this undercover status, ", self_diags)
                #     mod_text = mod_text.format(player=next_player, target_player=target_player)
                #     request_msg = mod_text
                # self._moderator_speak(f"Now {next_player}, please give your text clue. Never include the secret word.", visible_to=[next_player])
                
            else: 
                # pgm start at end of each round.
                print("start pgm after end of round")
                self._next_player_idx = self.find_next_pgm_player(0)
                if self._next_player_idx is not None:
                    next_player = self.player_names[self._next_player_idx]
                    self._current_phase = "pgm"
                    self._single_history = True
                    self._pgm_step = "is_undercover"
                    clues = self._get_current_clue_text()
                    clue_text = self.pgm_template.format(clues=clues)
                    code = self.undercover_code if next_player == self.undercover_name else self.non_undercover_code
                    user_text = clue_text + self.pgm_template_questions["is_undercover"].format(player=next_player, code=code)
                    request_msg = user_text
                else:
                    # this branch indicates there is no pgm player in the game.
                    self._remain_clue_round -= 1 
                    if self._remain_clue_round == 0:
                        self._next_player_idx = 0
                        self._current_phase = "accuse"
                        self._moderator_speak("Now vote which of the other players (excluding yourself) is the undercover. "
                                      "You cannot vote for yourself.")
                    else:
                        self._next_player_idx = 0
                        self._current_phase = "give clues"
                        self._moderator_speak(f"Now we starting {self._clue_round+1-self._remain_clue_round} round of giving clue, we still start from {self.player_names[0]}")
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                request_msg=request_msg,
                                terminal=False)  # Return all the messages
        elif self._current_phase == "accuse":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            vote = self._text2vote(action)
            self._text_votes[player_name] = self.player_names.index(vote)
            if vote in self.player_names:
                self._players_votes[vote] += 1
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
                rewards = self.get_zero_rewards()
                terminal = False
            else:
                print(self._text_votes)
                # show result of PGM, record PGM result in file
                cal_max_vote, cal_accuse_correct, cal_even_note, _ , self._pgm_votes = self._cal_vote(self._text_votes)
                print(self._pgm_votes)
                for pl in self._pgm_votes:
                    self._vote_of_each_player[pl]= self.player_names[self._pgm_votes[pl]]
                if not cal_accuse_correct:
                    if cal_even_note:
                        self._moderator_speak(f"There are even notes. The undercover {self.undercover_name} wins.")
                        self._win_group = 2
                    else:
                        self._moderator_speak(f"The most-voted player is {self.player_names[cal_max_vote]}. The accusation is incorrect. "
                              f"{self.undercover_name} is the undercover. {self.undercover_name} won the game!")
                        self._win_group = 1
                    rewards = self.get_rewards(undercover_win=True)
                else:
                    self._moderator_speak(f"The accusation is correct! {self.undercover_name} is the undercover! {self.non_undercover_names} won!")
                    self._win_group = 0
                    rewards = self.get_rewards(undercover_win=False)
               
                terminal = True
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(), reward=rewards, request_msg=request_msg, terminal=terminal)

        elif self._current_phase == "pgm":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, is_pgm=True, is_show=False)
            self.message_pool.append_message(message)
            # two steps for pgm, "is undercover, analyze pgm"
            clues = self._get_current_clue_text()
            code = self.undercover_code if player_name == self.undercover_name else self.non_undercover_code
            if self._pgm_step == "is_undercover":
                self._pgm_step = "analyze_pgm"
                self._current_phase = "pgm"
                self._single_history = True
                ans = self.parse_undercover(action)
                self._undercover_self_diagnoses[player_name] = ans
                clue_text = self.pgm_template.format(clues=clues)
                start_idx = 2
                user_text = clue_text
                if ans == "yes":
                    for othp in [p for p in self.player_names if p != player_name]:
                        user_text +=  self.pgm_template_questions["other_pgm_under"].format(idx=start_idx, code=code, player=player_name, other_player=othp)
                        start_idx +=1
                else:
                    user_text += self.pgm_template_questions["self_pgm_non_under"].format(idx=start_idx, code=code, player=player_name)
                    start_idx += 1
                    for othp in [p for p in self.player_names if p != player_name]:
                        user_text +=  self.pgm_template_questions["other_pgm_non_under"].format(idx=start_idx, code=code, player=player_name, other_player=othp)
                        start_idx +=1
                request_msg = user_text
                
            elif self._pgm_step == "analyze_pgm":
                cur_pgm = self._pgm_list[self.player_names.index(player_name)]
                cur_pgm.update(self._text2changev3(action))
                self._pgm_step = "is_undercover" # reset pgm_step to is_undercover   
                clues = self._get_current_clue_text()   
                if len(self._get_current_clues()) % len(self.player_names) == 0: # normal pgm at the end of one round, continue to search for next pgm
                    print("Current Player: ", self.player_names[self._next_player_idx])
                    self._next_player_idx += 1
                    self._next_player_idx = self.find_next_pgm_player(self._next_player_idx)
                    print("PGM: ", self._next_player_idx)
                    if self._next_player_idx is not None: # there is still more pgm players
                        next_player = self.player_names[self._next_player_idx]
                        self._current_phase = "pgm"
                        self._single_history = True
                        clue_text = self.pgm_template.format(clues=clues)
                        code = self.undercover_code if next_player == self.undercover_name else self.non_undercover_code
                        user_text = clue_text + self.pgm_template_questions["is_undercover"].format(player=next_player, code=code)
                        request_msg = user_text
                    else: # iterate over all pgm players
                        self._remain_clue_round -= 1 
                        if self._remain_clue_round == 0: 
                            self._next_player_idx = 0
                            self._current_phase = "accuse"
                            self._moderator_speak("Now vote which of the other players (excluding yourself) is the undercover."
                                            "You cannot vote for yourself.")
                        else:
                            print("==========> start new round of clue giving, start from ")
                            self._next_player_idx = 0
                            self._current_phase = "give clues"
                            self._moderator_speak(f"Now we starting {self._clue_round+1-self._remain_clue_round} round of giving clue, we still start from {self.player_names[0]}")
                            next_player = self.player_names[self._next_player_idx]
                            if self.is_pgm_player(self._next_player_idx):
                                _, _target_player_idx = self._pgm_list[self._next_player_idx].get_target()
                                target_player = self.player_names[_target_player_idx]
                                self_diag = self._undercover_self_diagnoses[next_player]
                                if self_diag == "not sure":
                                    mod_text = self._clue_unclear
                                elif self_diag == "yes":
                                    mod_text = self._clue_undercover
                                elif self_diag == "no":
                                    mod_text = self._clue_non_undercover
                                else:
                                    print("Do not support this undercover status, ", self_diag)
                                
                                mod_text = mod_text.format(player=next_player, target_player=target_player)
                                request_msg = mod_text
                            self._moderator_speak(f"Now {next_player}, please give your text clue. Never include the secret word.", visible_to=[next_player])
                else:
                    # if pgm is before clue, go back to give clues
                    self._current_phase = "give clues"
                    print("give clue after pgm")
                    next_player = self.player_names[self._next_player_idx]
                    _, _target_player_idx = self._pgm_list[self._next_player_idx].get_target()
                    target_player = self.player_names[_target_player_idx]
                    self_diag = self._undercover_self_diagnoses[next_player]
                    if self_diag == "not sure":
                        mod_text = self._clue_unclear
                    elif self_diag == "yes":
                        mod_text = self._clue_undercover
                    elif self_diag == "no":
                        mod_text = self._clue_non_undercover
                    else:
                        print("Do not support this undercover status, ", self_diag)
                    
                    mod_text = mod_text.format(player=next_player, target_player=target_player)
                    request_msg = mod_text
                    self._moderator_speak(f"Now {next_player}, please give your text clue. Never include the secret word.", visible_to=[next_player])
            else:
                print("Do not suport pgm step, ", self._pgm_step)
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(), reward=self.get_zero_rewards(), request_msg=request_msg, terminal=False)
        
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")
        
        print(self._win_group)

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True
        

        return timestep
