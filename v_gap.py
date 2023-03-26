from blosum_matrix import blosum_matrix
from Question_3.edit_operations import edit_operations


class v_gap:
    def __init__(self, string1, string2, u):
        self.string1 = string1
        self.string2 = string2
        self.u = u

        self.V_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        # Following matrix will hae max{V(i,k)} for k <= j-1
        self.row_max_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        self.col_max_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        self.transcript_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        
        self.blosum_matrix = blosum_matrix()
        self.operation_obj = edit_operations(self.string1, 
                                            self.string2)

        self.update_grids()  # actually does the calculations

    def update_bcs(self):  # boundary conditions
        for i in range(len(self.string1) + 1):
            self.V_matrix[i][0] = self.u
            # B.C's of E_matrix to match V_matrix for later 
            # comparison in update_grids
            self.row_max_matrix[i][0] = self.u
            self.transcript_matrix[i][0] = 'D' * i
        
        for j in range(len(self.string2) + 1):
            self.V_matrix[0][j] = self.u
            self.col_max_matrix[0][j] = self.u
            self.transcript_matrix[0][j] = 'I' * j

        self.V_matrix[0][0] = 0  # reset 0,0 index
        self.row_max_matrix[0][0] = 0
        self.col_max_matrix[0][0] = 0

    def find_blosum_val(self, char1, char2):
        # Finds value in the blosum matrix for the 
        # corresponding characters
        for counter in range(21):  
            # 21 rows/ cols in blosum_matrix
            if self.blosum_matrix.\
                matrix[0][counter] == char1:
                row = counter

        for counter in range(21):
            if self.blosum_matrix.\
                matrix[counter][0] == char2:
                col = counter

        return int(self.blosum_matrix.matrix[row][col])
    
    def update_transcript(self, G, row, col):
        tuple = (self.row_max_matrix[row][col - 1] + self.u, 
            self.col_max_matrix[row - 1][col] + self.u, G)
        index = tuple.index(max(tuple))

        if index == 0: # E represents insertion
            self.transcript_matrix[row][col] = \
                self.transcript_matrix[row][col - 1] + 'I'

        elif index == 1: # F represents deletion
            self.transcript_matrix[row][col] = \
                self.transcript_matrix[row - 1][col] + 'D'
        
        else:  # either match or replace
            char_match = ( self.string1[row - 1] == 
                            self.string2[col - 1] )
            if char_match:
                self.transcript_matrix[row][col] = self.\
                    transcript_matrix[row - 1][col - 1] + 'M'
            else:
                self.transcript_matrix[row][col] = self.\
                    transcript_matrix[row - 1][col - 1] + 'R'

    def update_grids(self):
        self.update_bcs()
        for i in range(len(self.string1)):
            for j in range(len(self.string2)):
                s = self.find_blosum_val(self.string1[i], 
                                            self.string2[j])

                G = self.V_matrix[i][j] + s

                self.V_matrix[i + 1][j + 1] = \
                    max(self.row_max_matrix[i + 1][j] + 
                        self.u, self.col_max_matrix[i][j + 1]
                        + self.u, G)
                
                # Only need one comparison since E[i + 1, j] 
                # etc. has considered V[i][k] for 0<=k<=j-1
                # Updating for future use
                self.row_max_matrix[i + 1][j + 1] = \
                    max(self.row_max_matrix[i + 1][j], 
                            self.V_matrix[i + 1][j + 1])
                self.col_max_matrix[i + 1][j + 1] = \
                    max(self.col_max_matrix[i][j + 1], 
                            self.V_matrix[i + 1][j + 1])

                self.update_transcript(G, i + 1, j + 1)

    def get_transcript(self):
        return self.transcript_matrix\
            [len(self.string1)][len(self.string2)]

    def get_alignment(self, transcript):
        return self.operation_obj.\
            optimal_alignment(transcript)

    def get_score(self):
        return self.V_matrix\
            [len(self.string1)][len(self.string2)]


if __name__ == '__main__':
    protein_C = 'MTSDCSSTHCSPESCGTASGCAPASSCSVETACLPGTCATSRC\
QTPSFLSRSRGLTGCLLPCYFTGSCNSPCLVGNCAWCEDGVFTSNEKETMQFLNDRLASY\
LEKVRSLEETNAELESRIQEQCEQDIPMVCPDYQRYFNTIEDLQQKILCTKAENSRLAVQ\
LDNCKLATDDFKSKYESELSLRQLLEADISSLHGILEELTLCKSDLEAHVESLKEDLLCL\
KKNHEEEVNLLREQLGDRLSVELDTAPTLDLNRVLDEMRCQCETVLANNRREAEEWLAVQ\
TEELNQQQLSSAEQLQGCQMEILELKRTASALEIELQAQQSLTESLECTVAETEAQYSSQ\
LAQIQCLIDNLENQLAEIRCDLERQNQEYQVLLDVKARLEGEINTYWGLLDSEDSRLSCS\
PCSTTCTSSNTCEPCSAYVICTVENCCL'
    
    protein_D = 'MPYNFCLPSLSCRTSCSSRPCVPPSCHSCTLPGACNIPANVSN\
CNWFCEGSFNGSEKETMQFLNDRLASYLEKVRQLERDNAELENLIRERSQQQEPLLCPSY\
QSYFKTIEELQQKILCTKSENARLVVQIDNAKLAADDFRTKYQTELSLRQLVESDINGLR\
RILDELTLCKSDLEAQVESLKEELLCLKSNHEQEVNTLRCQLGDRLNVEVDAAPTVDLNR\
VLNETRSQYEALVETNRREVEQWFTTQTEELNKQVVSSSEQLQSYQAEIIELRRTVNALE\
IELQAQHNLRDSLENTLTESEARYSSQLSQVQSLITNVESQLAEIRSDLERQNQEYQVLL\
DVRARLECEINTYRSLLESEDCNLPSNPCATTNACSKPIGPCLSNPCTSCVPPAPCTPCA\
PRPRCGPCNSFVR'

    output = v_gap(protein_C, protein_D, -12)
    transcript = output.get_transcript()[:50]
    print(output.get_score())
    print(transcript)
    print( output.get_alignment(transcript)[0] )
    print( output.get_alignment(transcript)[1] )



