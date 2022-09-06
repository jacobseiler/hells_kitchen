import pandas as pd

import numpy as np

class Analysis():

    def __init__(self) -> None:

        self._data = pd.read_csv("./data.csv")

    def compute_risk_ratio(
        self, skip_black_jackets: bool = True, team_to_follow: str = "Red",
    ) -> None:

        table = np.zeros((3, 3))

        # |==============|====================|=====================|===================|
        # |              | Won the Challenge  |  Lost the Challenge |      Total        |
        # |==============|====================|=====================|===================|
        # | Lost Service |          A         |           B         |      A + B        |
        # |--------------|--------------------|---------------------|-------------------|
        # | Won Service  |          C         |           D         |      C + D        |
        # |--------------|--------------------|---------------------|-------------------|
        # | Total        |        A + C       |         B + D       |  A + B + C + D    |
        # |--------------|--------------------|---------------------|-------------------|

        for _, row in self._data.iterrows():
            challenge_winner = row["Challenge Winner"]
            service_loser = row["Service Loser"]
            if not isinstance(challenge_winner, str) and np.isnan(challenge_winner):
                continue

            if not isinstance(service_loser, str) and np.isnan(service_loser):
                continue

            if skip_black_jackets and row["Black Jackets"]:
                continue

            # The service loser will dictate the row.
            if service_loser in {team_to_follow, "Both"}:
                row = 0
            else:
                row = 1

            # Then the challenge winner will dictate the column.
            if challenge_winner in {team_to_follow, "Both"}:
                column = 1
            else:
                column = 0

            table[row][column] += 1

        table[2][0] = table[0][0] + table[1][0]
        table[2][1] = table[0][1] + table[1][1]

        table[0][2] = table[0][0] + table[0][1]
        table[1][2] = table[1][0] + table[1][1]

        table[2][2] = table[2][0] + table[2][1]

        a = table[0][0]
        b = table[0][1]
        c = table[1][0]
        d = table[1][1]

        rr = (a / (a + b)) / (c / (c + d))

        print(rr)
        print(table)
if __name__ == "__main__":

    x = Analysis()
    x.compute_risk_ratio()
    print(x._data)

