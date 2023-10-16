from typing import List, Dict, Union
import random
import re
import numpy as np

from .base import Environment, TimeStep
from ..message import Message, MessagePool
from ..agent import SIGNAL_END_OF_CONVERSATION
from ..config import EnvironmentConfig

from chatarena.pgm import PGM_List

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


class Chameleon_PGM_Noiter(Environment):
    type_name = "chameleon_pgm_noiter"

    def __init__(self, player_names: List[str], topic_codes: Dict[str, List[str]] = None, **kwargs):
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
        self._num_players = len(self.player_names)

        self.reset()  # To initialize the game (select topic, code, chameleon)

    def get_next_player(self) -> str:
        """
        get the next player
        """
        if self._current_phase != "guess":
            return self.player_names[self._next_player_idx]
        else:
            return self.chameleon_name

    def reset(self):
        """
        sample topic, code and chameleon code
        """
        self.topic = random.choice(list(self.topic_codes.keys()))
        self.code = random.choice(self.topic_codes[self.topic])
        self.chameleon_name = random.choice(self.player_names)
        # self.topic = "Fruits"
        # self.code = "Banana"
        # self.chameleon_name = "Player 2"
        self.non_chameleon_names = [name for name in self.player_names if name != self.chameleon_name]



        self._current_turn = 0
        self._next_player_idx = 0
        # self._current_phase = "give clues"

        self.message_pool.reset()
        with open("results/human_pgm_1.txt") as f:
            self._human_pgm_demo = f.read()
        self._moderator_speak(f"")

        # self._moderator_speak(f"To help you better undertstand how to play the game, I will give you one example:\n{self._human_pgm_demo}")
 
        self._moderator_speak(f"Now the game starts! The topic is: {self.topic}")
        self._moderator_speak(f"You are not chameleon. The word is: {self.code}",
                              visible_to=self.non_chameleon_names)
        self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
        
        # self._moderator_speak("Each player need maintain a probabilistic graph model(PGM) to reason the probability of each player being chameleon.\n"
        #     "The PGM should consider different perspectives. Your own perspective and the perspectives you think other players would have.\n"
        #     # "The format of your maintained PGM should be Player xx: [xx,xx,xx]. If 'Player xx' is yourself, remember to add '(myself)' behind.\n"
        #     "Suppose there are three players, the following is an json PGM example maintained by Player 1.\n"
        #     "{'Player 1': [xx,xx,xx], 'Player 2': [xx,xx,xx],'Player 3': [xx,xx,xx]}\n"
        #     "Specifically, the first item 'Player 1': [xx,xx,xx] are the three probabilities that player 1 think Player 1,2,3 as chameleon.\n"
        #     "The second item 'Player 2': [xx,xx,xx] are probabilities of Player 1,2,3 being chameleon that Player 1 think Player 2 would have. \n"
        #     "Similarly, the third item 'Player 3': [xx,xx,xx] are probabilities of Player 1,2,3 being chameleon that Player 1 think Player 3 would have.\n"
        #     "With this PGM, each player can better deduce who is chameleon by choosing the player with the highest probability from their own perspective."
        #     "In addition, a player can also give clue that lowers the probability of him/her from the pespective the player think other players would have."
        #     "The probabilities should be sum to 1 and the most suspicious Player should have the highest probability."
        # )
        self._moderator_speak("Next you give your clues one by one but never include the secret word in the clue.\n"
                              "Each time after a player giving a clue, every player need to analyze the possibilities of each player being chameleon.\n"
                              "-If you are chameleon, try to guess the secret word and try to  "
                              "-If you are not chameleon, try to indicate how would you like to raise of lower the possibilities you think other players are chameleons.")
                            #   "The criteria to update the PGM:\n"
                            #   "If you think one player is more suspicious to be an chameleon according to their clue, you need to increase his or her probability.\n"
                            #   "Your PGM is only visible to yourselves.")
        self._current_phase = "give clues" 
        self._moderator_speak(f"Now {self.player_names[0]}, we can start from you to give the clue.")
        # self._moderator_speak("Each player need maintain a probabilistic graph model(PGM) to reason the probability of each player being chameleon.\n"
        #     "The PGM should consider different perspectives. Your own perspective and the perspectives you think other players would have.\n"
        #     "The format of your maintained PGM should be Player xx -> [xx,xx,xx]. If 'Player xx' is yourself, remember to add '(myself)' behind.\n"
        #     "The probabilities should be sum to 1 and the most suspicious Player should have the highest probability. \n"
        #     "The following is an example of PGM.\n"
        #     "'PGM:\n"
        #     "Player xx(myself) -> [0.3,0.2,0.5]\n"
        #     "Player xx -> [0.2,0.5,0.2]\n"
        #     "Player xx -> [0.4,0.1,0.5]'\n"
        #     f"Now {self.player_names[1]}, start giving your PGM from each player's perspective. Please end PGM with <EOS> "
        # )
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._player_pgm_dict = PGM_List(self.player_names, self.chameleon_name)
        # one_player_pgm = {name: 1/len(self.player_names)*np.ones((len(self.player_names))) for name in self.player_names}
        
        # self._player_pgm_dict = {name: , }# reset the probability of chameleon.
        # self._chameleon_idx = self.player_names.index(self.chameleon_name)
        # print(self._player_pgm_dict)
        # self._player_pgm_dict[self.chameleon_name][self._chameleon_idx] = np.zeros((len(self.player_names)))
        # self._player_pgm_dict[self.chameleon_name][self._chameleon_idx][self._chameleon_idx] = 1
        self._finish_clue = False
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
    # def get_pgm_conditions(self, player_name):
    #     pgm = self.PGM_List[player_name]
    #     self.clues[-1]



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


    def text_to_pgm(self, text):
        pattern = r"<pgm>(.*?)<\/pgm>"
        matches = re.findall(pattern, text, re.DOTALL)
        print(text, matches)
        try:
            pgm = json.loads(matches[0])
        except:
            print("cannot recognize the json")
            pgm = None
        for player_name in self.player_names:
            if player_name not in pgm:
                print("PGM is not valid")
                pgm = None
        return pgm
        

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
            message = Message(agent_name=player_name, content=action, turn=self._current_turn)
            self.message_pool.append_message(message)
            # Update the counters
            
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_clue_player_idx = self._next_player_idx + 1
            else:
                self._finish_clue = True
            self._current_phase = "pgm"
            self._next_player_idx = 0
            self._moderator_speak(f"Now {self.player_names[self._next_player_idx]}, deduce your new PGM based on the newly given clue and your previous PGM."
                "You should use the json form. Please give PGM in the format: My PGM is:... ", visible_to=[self.player_names[self._next_player_idx]])
          
            # self._moderator_speak(f"Now {self.player_names[self._next_player_idx]}, deduce your new PGM based on the newly given clue."
            #     "You should use the json form. Please give PGM in the format: My PGM is:... ", visible_to=[self.player_names[self._next_player_idx]])
            # # print("after giving the messgae ")
            self._current_turn += 1

            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages

        elif self._current_phase == "accuse":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            vote = self._text2vote(action)
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
                if max_vote_player != self.chameleon_name:
                    accuse_correct = False

                if not accuse_correct:
                    if even_vote:
                        self._moderator_speak(f"There are even votes. The accusation does not stand. "
                                              f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                    else:
                        self._moderator_speak(
                            f"The most-voted player is {max_vote_player}. The accusation is incorrect. "
                            f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!"
                        )
                    rewards = self.get_rewards(chameleon_win=True)
                    terminal = True
                else:
                    self._moderator_speak(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
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
                rewards = self.get_rewards(chameleon_win=True)
            else:
                self._moderator_speak(f"{player_name} guessed the code wrong! The secret word is {self.code}. "
                                      f"{self.non_chameleon_names} won!")
                rewards = self.get_rewards(chameleon_win=False)
            timestep = TimeStep(observation=self.get_observation(),
                                reward=rewards,
                                terminal=True)
        elif self._current_phase == "pgm":
            # generate PGM
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            # update PGM dict
            # pgm = self.text_to_pgm(action)
            # self._player_pgm_dict.update(player_name, pgm)
            
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
                self._current_phase = "pgm"
                # self._moderator_speak(f"Now {self.player_names[self._next_player_idx]}, deduce your new PGM based on the newly given clue."
                # "You should use the json form. Please give PGM in the format: My PGM is:... ", visible_to=[self.player_names[self._next_player_idx]])
                self._moderator_speak(f"Now {self.player_names[self._next_player_idx]}, deduce your new PGM based on the newly given clue and your previous PGM."
                "You should use the json form. Please give PGM in the format: My PGM is:... ", visible_to=[self.player_names[self._next_player_idx]])
          
            else:
                self._next_player_idx = self._next_clue_player_idx
                if self._finish_clue:
                    self._current_phase = "accuse"
                    self._next_player_idx = 0
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                         "You cannot vote for yourself.\n"
                                         "Remember your vote should be consistent with your PGM, that is, vote the player you think who has the highest probability to be the chameleon.")
                else:
                    self._current_phase = "give clues"
                    self._moderator_speak(f"Now {self.player_names[self._next_clue_player_idx]}, please give your text clue. Try to lower your probability of being chameleon from other players' perspectives. Don't mistakenly give the PGM.", visible_to=[self.player_names[self._next_clue_player_idx]])
            
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages

            

            # if self._finish_clue: # if finish clue, then each player update their pgm again.
            #     if self._next_player_idx < len(self.player_names) - 1:
            #         self._next_player_idx += 1
            #         self._current_phase = "pgm"
            #     else:
            #         self._next_player_idx = self._player_start_idx
            #         self._current_phase = "accuse"
            #         self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
            #                           "You cannot vote for yourself.")
            # else: # pgm then give clues
            #     self._current_phase = "give clues"
            #     self._moderator_speak(f"Now {player_name}, give your clue and try to iteratively refine the clues with the help of Critic.\n"
            #                            "Each of your clue should be based on your PGM but never give your PGM as clue. Just give a clue descirbing the secret word."
            #                            "If you are the chameleon, try to pretend to describing the same secret word.", visible_to=[player_name])


            # self._current_turn += 1
            # timestep = TimeStep(observation=self.get_observation(),
            #                     reward=self.get_zero_rewards(),
            #                     terminal=False)  # Return all the messages
            
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True

        return timestep
