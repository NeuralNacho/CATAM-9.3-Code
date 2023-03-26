from blosum_matrix import blosum_matrix


class v_sub:
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2
        self.insertion_score = -2
        self.deletion_score = -2
        self.V_sfx_matrix = \
            [ [None] * (1 + len(self.string2))
            for _ in range(1 + len(self.string1)) ]
        self.blosum_matrix = blosum_matrix()

        self.update_bcs()
        self.calculate_V_sfx()


    def find_s(self, char1, char2):
        # Calculates score from blosum matrix when 
        # replacement is made
        row = 0
        col = 0
        for counter in range(21):  
            # 21 rows/ cols in blosum_matrix
            if self.blosum_matrix.matrix[0][counter]\
                == char1:
                row = counter

        for counter in range(21):
            if self.blosum_matrix.matrix[counter][0]\
                == char2:
                col = counter
        return int(self.blosum_matrix.matrix[row][col])
        

    def update_bcs(self):
        for i in range(len(self.string1) + 1):
            self.V_sfx_matrix[i][0] = 0
        for j in range(len(self.string2) + 1):
            self.V_sfx_matrix[0][j] = 0
    
    
    def calculate_V_sfx(self):
        for i in range(len(self.string1)):
            for j in range(len(self.string2)):

                replacement = self.V_sfx_matrix[i][j] + \
                    self.find_s(self.string1[i], 
                                self.string2[j])                
                insertion = self.V_sfx_matrix[i][j + 1] + \
                    self.insertion_score
                deletion = self.V_sfx_matrix[i + 1][j] + \
                    self.deletion_score
                
                self.V_sfx_matrix[i + 1][j + 1] = max(
                    0,
                    replacement,
                    insertion,
                    deletion
                )

    
    def get_v_sub(self):
        # v_sub is simply the maximum value in 
        # the V_sfx table
        maximum = 0
        for i in range(len(self.string1) + 1):
            for j in range(len(self.string2) + 1):
                maximum = max(maximum, 
                    self.V_sfx_matrix[i][j])

        return maximum


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
    # protein_C = 'MTDSC'
    # protein_D = 'MPYNF' 

    result = v_sub(protein_C, protein_D)
    # for i in range(len(protein_C) + 1):
    #     print(result.V_sfx_matrix[i])
    print(result.get_v_sub())