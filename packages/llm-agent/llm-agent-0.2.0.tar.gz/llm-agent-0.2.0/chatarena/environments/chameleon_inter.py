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


class Chameleon_Inter(Environment):
    type_name = "chameleon_inter"

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
        # self.topic = random.choice(list(self.topic_codes.keys()))
        # self.code = random.choice(self.topic_codes[self.topic])
        # self.chameleon_name = random.choice(self.player_names)

        self.topic = "Sports"
        self.code = "Volleyball"
        self.chameleon_name = "Player 2"

        self.non_chameleon_names = [name for name in self.player_names if name != self.chameleon_name]

        self._current_turn = 0
        self._next_player_idx = 0
        self._current_phase = "give clues"

        self.message_pool.reset()
        

        self._moderator_speak(f"Now the game starts! The topic is: {self.topic}")
        self._moderator_speak(f"You are not chameleon. The secret word is: {self.code}",
                              visible_to=self.non_chameleon_names)
        self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
        self._moderator_speak(
            f"Now everyone gives one clue (but don't give away the secret word). Never include the secret word in the clue."
            f"You cannot repeat what others has said. We will start with {self.player_names[0]}.")
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._current_round = 1

        self._initialized = True
        init_timestep = TimeStep(observation=self.get_observation(),
                                 reward=self.get_zero_rewards(),
                                 terminal=False)

        self.INTER_SPEAK="Now forget your roles and try to review the game history. Based on each player's role, evaluate each player's clue and give suggestions to improve the clue.\n"\
        "The following are the evaluation crteria: \n"\
        "If a player is not a chameleon, his/her clue should include some information about the secret word but never give the secret word itself to other players.\n"\
        "If a player is chameleon, his/her clues should be similar to what other player is decribing but not repeat other players' clues too much."\
        "Typically, a chameleon tries to guess the secret word from other players' clues and then give the description about his or her guessed secret word.\n"\
        "You should give evaluations like:\n"\
        "Player x: chameleon, the clue is far away from the secret word; \n"\
        "Player x: not chameleon...., bad clue with the secret code directly in it. \n"\
        "..."

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
            print(text, candidates)
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
            self._current_turn += 1
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
            else:

                self._next_player_idx = 0
                self._current_phase = "accuse"
                self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                      "You cannot vote for yourself."
                                      )
                self._current_turn += 1

            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages
        elif self._current_phase == "interview":
            
            self._current_turn += 1

            message = Message(agent_name=player_name, content=action, turn=self._current_turn)
            self.message_pool.append_message(message)
            # Update the counters
            self._current_turn += 1

            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
            else:
                self._next_player_idx = 0
                self._current_phase = "restart"

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

                    if self._current_round == 2:
                        terminal = True
                    else:
                        terminal = False
                        self._current_round += 1
                        self._next_player_idx = 0
                        self._current_phase = 'interview'
                        self._moderator_speak(self.INTER_SPEAK)
                else:
                    self._moderator_speak(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                                          f"Now {self.chameleon_name} can guess the secret word. "
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

            if self._current_round == 2:
                terminal = True
            else:
                terminal = False
                self._current_phase = 'interview'
                self._moderator_speak(self.INTER_SPEAK)
                self._current_round += 1
                self._next_player_idx = 0
            
            timestep = TimeStep(observation=self.get_observation(),
                                reward=rewards,
                                terminal=terminal)
        elif self._current_phase == "restart":
            self._moderator_speak(f"Second Round! Please forget all the game history in last round but do learn from the evaluations given by each player above.") 
            self._moderator_speak(f"The topic is: {self.topic}")
            self._moderator_speak(f"You are not chameleon. The word is: {self.code}",
                              visible_to=self.non_chameleon_names)
            self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
            self._moderator_speak(f"Now everyone gives one clue (but don't give away the secret word). "
                                  f"You cannot repeat what others has said. We will start with {self.player_names[0]}.")
            self._current_turn += 1
            self._current_phase="give clues"
            self._initialized=True
            self._next_player_idx=0
            rewards = self.get_zero_rewards()
            timestep = TimeStep(observation=self.get_observation(),
                                reward=rewards,
                                terminal=False)

        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True

        return timestep
