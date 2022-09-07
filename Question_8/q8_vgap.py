class q8_vgap:
    # Methods very similar to v_gap.py
    def __init__(self, string1, string2, u):
        self.string1 = string1
        self.string2 = string2
        self.u = u

        self.V_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        self.row_max_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        self.col_max_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]

        self.update_grids()


    def update_bcs(self):
        for i in range(len(self.string1) + 1):
            self.V_matrix[i][0] = self.u
            self.row_max_matrix[i][0] = self.u
        
        for j in range(len(self.string2) + 1):
            self.V_matrix[0][j] = self.u
            self.col_max_matrix[0][j] = self.u

        self.V_matrix[0][0] = 0
        self.row_max_matrix[0][0] = 0
        self.col_max_matrix[0][0] = 0


    def find_s(self, char1, char2):
        if char1 == char2:
            return 1
        else:
            return -1


    def update_grids(self):
        self.update_bcs()
        for i in range(len(self.string1)):
            for j in range(len(self.string2)):
                s = self.find_s(self.string1[i], 
                                self.string2[j])

                G = self.V_matrix[i][j] + s

                self.V_matrix[i + 1][j + 1] = \
                    max(self.row_max_matrix[i + 1][j] + 
                        self.u, self.col_max_matrix[i][j + 1]
                        + self.u, G)

                self.row_max_matrix[i + 1][j + 1] = \
                    max(self.row_max_matrix[i + 1][j], 
                            self.V_matrix[i + 1][j + 1])
                self.col_max_matrix[i + 1][j + 1] = \
                    max(self.col_max_matrix[i][j + 1], 
                            self.V_matrix[i + 1][j + 1])


    def get_score(self):
        return self.V_matrix\
            [len(self.string1)][len(self.string2)]


if __name__ == '__main__':
    # for testing purposes
    string1 = 'aabbaaabab'
    string2 = 'babbbbabab'
    test = q8_vgap(string1, string2, -3)
    print(test.get_score())
    for i in range(len(string1) + 1):
        print(test.V_matrix[i])