
templ_0 = '''Now <PLAYER>, Based on the above clues, analyze who is more suspicious of the chameleon from your perspective and the perspective of other players you think."
                                "You must give an evaluation for each player by choosing one from [\"no change\",\"more suspicious\",\"less suspicious\"]\n"
                                  f"You must follow the format below to give the evaluation. As <PLAYER>, in my opinion: \n"
                                  "What Player 2 is thinking now:\n"
                                  "Player 1 is xxx\n"
                                  "Player 2 is xxx\n"
                                  "Player 3 is xxx\n"
                                  "Because....\n\n"
                                  "What Player 2 is thinking now:\n"
                                  "Player 1 is xxx\n"
                                  "Player 2 is xxx\n"
                                  "Player 3 is xxx\n"
                                  "Because....\n\n"
                                  "What Player 3 is thinking now:\n"
                                  "Player 1 is xxx\n"
                                  "Player 2 is xxx\n"
                                  "Player 3 is xxx\n"
                                  "Because....\n'''

templ_1 = '''Now <PLAYER>, Based on the above clues, analyze who is more suspicious of the chameleon from your perspective and the perspective of other players you think.
You must give an evaluation for each player by choosing one from [\"no change\",\"more suspicious\",\"less suspicious\"]
You must fill the following template below to give the evaluation, never miss a line:
"
As <PLAYER>, in my opinion: 
Player 1 thinks Player 1 is xxx
Player 1 thinks Player 2 is xxx
Player 1 thinks Player 3 is xxx
Because....\n
Player 2 thinks Player 1 is xxx
Player 2 thinks Player 2 is xxxa
Player 2 thinks Player 3 is xxx
Because....\n
Player 3 thinks Player 1 is xxx
Player 3 thinks Player 2 is xxx
Player 3 thinks Player 3 is xxx
Because....
"
'''

view_templ_active_non_chameleon = '''Now <PLAYER>, based on the clue given by <PRE_PLAYER>, analyze who is more suspicious as the chameleon from your perspective and the perspective of other players you think.
You can evaluate in the following format. 
As <PLAYER>, in my own perspective, I am a non-chameleon. I first evaluate from my own perspective:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because...
As for other players' perspectives:
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
'''
view_templ_active_chameleon = '''Now <PLAYER>, based on the clue given by <PRE_PLAYER>, analyze who is more suspicious as the chameleon from the perspectives of other players.
You must evaluate in the following format. 
As <PLAYER>, in my own perspective, I am the chameleon, so I just analyze other players' views:
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
'''

view_templ_active_chameleon_wcode = '''Now <PLAYER>, based on the clue given by <PRE_PLAYER>, try to guess the secret word and analyze who is more suspicious as the chameleon from the perspectives of other players.
You must evaluate in the following format. 
Now I guess the secret word is "...".
As <PLAYER>, in my own perspective, I am the chameleon, so I only analyze other players' views:
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
'''

view_templ_active_chameleon_wcode_v1 = '''Now <PLAYER>, analyze the clues from other players, don't consider your own clue, guess the secret word and analyze who is more suspicious as the chameleon from the perspectives of other players.
You must evaluate in the following format. 
Now I guess the secret word is "...", because....
As <PLAYER>, in my own perspective, I am the chameleon, so I only analyze other players' views:
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
I think now Player xx think:
Player xx is more suspicious
Player xx is less suspicious
Player xx is no change
...
Because... 
'''



clue_templ_v1="Now <PLAYER> is suspecting you, try to deceive <PLAYER> in your clue and reduce your suspiciousness."

clue_templ="Now <PLAYER> is suspecting you, try to reduce your suspiciousness in your clue."

clue_templ_active="Now <PLAYER>, as a non-chameleon, you should give more specifc clue while not reveal the secret word. "
clue_templ_active_chameleon="Now <PLAYER>, you are the chameleon. Try to guess the secret word by yourself and give your clue related to your thinking secret code. <TARGET_PLAYER> is suspecting you,  try to make you clue close to <TARGET_PLAYER>'s."


clue_templ_active_1="<PLAYER>, you are non-chameleon, your target is to increase the suspiciousness of the <TARGET_PLAYER>. For example, by giving more specific clues than the <TARGET_PLAYER>. Remember don't reveal the secret code; "
clue_templ_active_chameleon_1="<PLAYER>, you are chameleon, your target is to blend in and defraud trust from the <TARGET_PLAYER>. If any player's clue is specific and you have guessed the secret code, try to be more specific; If other players' clue are general, try to be close to the <TARGET_PLAYER>."


# clue_templ_active_chameleon_1="<PLAYER>, you are chameleon, your target is to blend in and defraud trust from the <TARGET_PLAYER>. If you If any player's clue is specific and you have guessed the secret code, try to be more specific; If other players' clue are general, try to be close to the <TARGET_PLAYER>."