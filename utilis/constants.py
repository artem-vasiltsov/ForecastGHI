import pandas as pd

from settings import CONSTANTS_FILE


def load_constants_y():

    constants = {}
    constants_df = pd.read_excel(CONSTANTS_FILE, "Sheet1")

    for i in range(76):

        constants[i] = {}
        for j in range(1, 13):

            constants[i][j] = constants_df["a" + str(i)][j - 1]

    return constants


if __name__ == '__main__':

    load_constants_y()
