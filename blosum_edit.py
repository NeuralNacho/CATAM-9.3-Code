from edit_operations import edit_operations
from blosum_matrix import blosum_matrix


class blosum_edit:
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2
        self.blosum_matrix = blosum_matrix()
        self.operation_obj = \
            edit_operations(self.string1, self.string2)

    def optimal_transcript(self):
        # Code very similar to edit_operations code
        # Space complexity is O(n) grid filled out row by row
        score_row = [None] * (len(self.string2) + 1)
        transcript_row = [None] * (len(self.string2) + 1)
        
        for j in range(len(self.string2) + 1):
            score_row[j] = -8 * j  # score of j insertions
            transcript_row[j] = 'I' * j 

        for i in range(len(self.string1)):
            score_temp1 = score_row[0]
            tran_temp1 = transcript_row[0]

            score_row[0] = -8 * (i + 1)  
            # ^ score of (i +1) deletions
            transcript_row[0] = 'D' * (i + 1)

            for j in range(len(self.string2)):
                score_temp2 = score_row[j + 1]
                tran_temp2 = transcript_row[j + 1]

                char_match = 1
                if self.string1[i] == self.string2[j]:
                    char_match = 0
                
                # Update score for insert and delete
                insert_score = score_row[j] - 8
                delete_score = score_row[j + 1] - 8
                
                # And for replace/match using Blosum
                row = 0
                col = 0
                for counter in range(21):  
                    # 21 rows/ cols in blosum_matrix
                    if self.blosum_matrix.matrix[0][counter]\
                        == self.string1[i]:
                        row = counter

                for counter in range(21):
                    if self.blosum_matrix.matrix[counter][0]\
                        == self.string2[j]:
                        col = counter

                replace_score = score_temp1 + \
                    int(self.blosum_matrix.matrix[row][col])
                score_row[j + 1] = max(insert_score, 
                                        delete_score, 
                                        replace_score)
                                    
                operation = self.find_operation(insert_score, 
                                                delete_score, 
                                               replace_score, 
                                                  char_match)
                transcript_row[j + 1] = \
                    self.operation_obj.update_transcript(
                                transcript_row, operation, 
                                            tran_temp1, j)

                score_temp1 = score_temp2
                tran_temp1 = tran_temp2
        return score_row[len(self.string2)], \
            transcript_row[len(self.string2)][:50]


    def find_operation(self, score1, score2, 
                        score3, char_match):
    # helper function for optimal_transcript
        max_score = max(score1, score2, score3)

        if score1 == max_score:
            return 'I'
        elif score2 == max_score:
            return 'D'
        elif char_match == 0:
            return 'M'
        else:
            return 'R'
    
    def optimal_alignment(self, transcript):
        return self.operation_obj.\
            optimal_alignment(transcript)


if __name__ == '__main__':
    protein_A = 'MGLSDGEWQLVLKVWGKVEGDLPGHGQEVLIRLFKTHPETLEK\
FDKFKGLKTEDEMKASADLKKHGGTVLTALGNILKKKGQHEAELKPLAQSHATKHKISIK\
FLEYISEAIIHVLQSKHSADFGADAQAAMGKALELFRNDMAAKYKEFGFQG' # 'SWAP'
    protein_B = 'MADFDAVLKCWGPVEADYTTMGGLVLTRLFKEHPETQKLFPKF\
AGIAQADIAGNAAISAHGATVLKKLGELLKAKGSHAAILKPLANSHATKHKIPINNFKLI\
SEVLVKVMHEKAGLDAGGQTALRNVMGIIIADLEANYKELGFSG' # 'WPHY'

    output = blosum_edit(protein_A, protein_B)
    transcript = output.optimal_transcript()
    print(transcript[0])
    print(transcript[1])
    print( output.optimal_alignment(transcript[1])[0] )
    print( output.optimal_alignment(transcript[1])[1] )