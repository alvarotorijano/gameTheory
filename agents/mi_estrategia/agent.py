from typing import List
from utils.game_core import Agent, COOPERATE, DEFECT


class Pavlov(Agent):
    # empiezo cooperando
    # despues, miro si la ronda anterior me fue bien o mal
    # si me fue bien repito la misma jugada, si me fue mal cambio
    # en la ultima ronda traiciono porque ya no hay consecuencias

    def play(self, own_history: List[str], opponent_history: List[str]) -> str:
        ronda_actual = len(own_history) + 1

        if self.num_rounds is not None and ronda_actual == self.num_rounds:
            return DEFECT

        if not opponent_history:
            return COOPERATE

        mi_ultima = own_history[-1]
        su_ultima = opponent_history[-1]

        # me fue bien si cooperamos los dos, o si traicione y el coopero
        me_fue_bien = (mi_ultima == COOPERATE and su_ultima == COOPERATE) or \
                      (mi_ultima == DEFECT and su_ultima == COOPERATE)

        if me_fue_bien:
            return mi_ultima
        else:
            return DEFECT if mi_ultima == COOPERATE else COOPERATE
