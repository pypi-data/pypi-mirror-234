

from typing import List, Dict, Union
import random
import re

from .base import Environment, TimeStep
from ..message import Message, MessagePool
from ..agent import SIGNAL_END_OF_CONVERSATION
from ..config import EnvironmentConfig

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


class Chameleon_Iter(Environment):
    type_name = "chameleon_iter"

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
        self._player_start_idx = 1
        self._next_player_idx = self._player_start_idx # start with player 1, 0 is critic
        self._current_player_idx = self._player_start_idx
        self._current_clue = None
        self._critic_turns = 0
        self._current_phase = "give clues"  # "give clues", "accuse", "guess"
        self._players_votes = None
        self._initialized = False
        self._critic_idx = 0

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
        self.chameleon_name = random.choice(self.player_names[1:])
        self.non_chameleon_names = [name for name in self.player_names[1:] if name != self.chameleon_name]
        

        self._current_turn = 0
        self._next_player_idx = self._player_start_idx  # start with player 1, 0 is critic
        self._critic_turns = 0
        self._current_critic_player = self._player_start_idx
        self._current_phase = "give clues"
        self._critic_name= self.player_names[0]
        

        self.message_pool.reset()

        self._moderator_speak(f"Now the game starts! The topic is: {self.topic}")
        self._moderator_speak(f"You are not chameleon. The word is: {self.code}",
                              visible_to=self.non_chameleon_names)
        self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
        self._moderator_speak(f"You are the critic, in this game, {self.non_chameleon_names} are not chameleon and {self.chameleon_name} is the chameleon. Later you need to critic their clues, do not give away the other player's role to the player you are evaluate.", visible_to=[self._critic_name])
        self._moderator_speak(
            f"Now every player except the Critic gives one clue (but never include the secret word in the clue). "
            f"You cannot repeat what others has said. We will start with {self.player_names[1]}.")
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        

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

    def is_good_enough(self, msg) -> bool:
        """
        check if the critic is good enough
        """
        
        critic_text = msg.content.lower()
        if "good clue" in critic_text:
            return True
        return False


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
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, visible_to=[self._critic_name])

            msg_pos = self.message_pool.append_message(message)
            self._current_clue = action
            self._current_clue_pos = msg_pos
            self._current_player_idx = self._next_player_idx # record the current player
            self._current_player = self.player_names[self._current_player_idx]
            print("Current player: ", self.player_names[self._next_player_idx])
            self._current_turn += 1

            self._current_phase = "critic"
            #
            if self._critic_turns == 0:
                self._moderator_speak(f"Now Critic, forget last player and focus on the {player_name}'s clue. The evaluation should be based on the players role.\n"
                                   "If a player is not a chameleon, his/her clue should be relevant to secret word but never include the secret word.\n"
                                   "If a player is chameleon, his/her clues should be similar to what other player is decribing but not repeat other players' clues too much."
                                   "Typically, a chameleon tries to guess the secret word from other players' clues and then give the description about his or her guessed secret word.\n"
                                   "You can evaluate like this: "
                                   f"{player_name}: Your clue ..."
                                   "If you think the clue is good enough, you can give evaluation 'good clue'.",
                                  visible_to=[self._critic_name] )
            else:
                self._moderator_speak(f"Give the evaluation to {player_name}'s new clue.", visible_to=[self._critic_name] )
            self._next_player_idx = self._critic_idx # now critic start to eval
            
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages
            

            
            # self.message_pool.append_message(message)

            # if not self.iter_end(message):
            #     self._current_phase == "re"


            # # Update the counters
            # self._current_turn += 1
            # if self._next_player_idx < len(self.player_names) - 1:
            #     self._next_player_idx += 1
            # else:
            #     self._next_player_idx = 0
            #     self._current_phase = "accuse"
            #     self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon. "
            #                           "You cannot vote for yourself.")
            #     self._current_turn += 1


            
            # timestep = TimeStep(observation=self.get_observation(),
            #                     reward=self.get_zero_rewards(),
            #                     terminal=False)  # Return all the messages


        elif self._current_phase == "critic":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn, visible_to=[self.player_names[self._current_player_idx]])
            is_good_enough = self.is_good_enough(message)
            self.message_pool.append_message(message) 
            # print("is_good_enough: ", is_good_enough)
            
            self._critic_turns += 1

            if is_good_enough or self._critic_turns == 3: # if good enough or repeat for more than 3 turns, show the clue to all and move to next player
                if is_good_enough: 
                    self._moderator_speak("The clue is good enough, now I will show your clue to other players", visible_to=[self._current_player])
                else:
                    self._moderator_speak("Already refine for 3 turns, run out of patience, now I will show your clue to other players", visible_to=[self._current_player])
    
                # add one player's message to all other players
                message = Message(agent_name=self._current_player, content=self._current_clue, turn=self._current_turn, visible_to="all")
                self.message_pool.append_message(message) 
                self._critic_turns = 0
                # move to next player to give clue, if run out of player, then accuse
                self._next_player_idx = self._current_player_idx
                if self._next_player_idx < len(self.player_names) - 1:
                    self._next_player_idx += 1
                    self._current_phase = "give clues"
                else:
                    self._next_player_idx = self._player_start_idx
                    self._current_phase = "accuse"
                    # print("Show all the messages now")
                    # self.message_pool.print()
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                      "You cannot vote for yourself.")
            else: # let the critic give comments.
                self._next_player_idx = self._current_player_idx
                self._moderator_speak(f"Refine your last clue according to the Critic's comment. Don't apologize and only give the clue. Never inclue the secret word in the clue.", visible_to=[self.player_names[self._next_player_idx]])
                self._current_phase = "give clues"
            # self.message_pool.append_message(message)            
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
                    terminal = False
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
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True

        return timestep
