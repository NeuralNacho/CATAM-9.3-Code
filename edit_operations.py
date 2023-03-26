class edit_operations:
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2
    
    def optimal_transcript(self):
        # Will reduce matrix to a vector to have 
        # O(n) space complexity

        distance_row = [None] * (len(self.string2) + 1)
        transcript_row = [None] * (len(self.string2) + 1)
        # Would be a row in matrix of edit_distance algorithm
        # Variables above have 'matching' entries

        for j in range(len(self.string2) + 1):
            distance_row[j] = j
            transcript_row[j] = 'I' * j 
            # Boundary case have to insert entire second 
            # string

        for i in range(len(self.string1)):
            # Store D(i-1, j-1) entries
            dist_temp1 = distance_row[0]
            tran_temp1 = transcript_row[0]

            # Update to next row B.C
            distance_row[0] = i + 1
            transcript_row[0] = 'D' * (i + 1)

            for j in range(len(self.string2)):
                # Store D(i-1, j-1) for next iteration
                # Need second variable since can't store
                # and update simultaneously
                dist_temp2 = distance_row[j + 1]
                tran_temp2 = transcript_row[j + 1]

                char_match = 1
                if self.string1[i] == self.string2[j]:
                    char_match = 0
                
                distance_row[j + 1] = min(distance_row[j] + 1, 
                                    distance_row[j + 1] + 1, 
                                    dist_temp1 + char_match)

                # Update transcript row
                # First find the operation used 
                # for minimal edit distance
                operation = self.find_operation(
                                    distance_row[j] + 1,
                                    distance_row[j + 1] + 1, 
                                    dist_temp1 + char_match, 
                                    char_match)
                transcript_row[j + 1] = \
                    self.update_transcript(transcript_row, 
                                operation, tran_temp1, j)

                dist_temp1 = dist_temp2
                tran_temp1 = tran_temp2

        return distance_row[len(self.string2)], \
                transcript_row[len(self.string2)][:50]

    def find_operation(self, dist1, dist2, dist3, char_match):
        # helper function for optimal_transcript
        min_dist = min(dist1, dist2, dist3)

        if dist1 == min_dist:
            return 'I'
        elif dist2 == min_dist:
            return 'D'
        elif char_match == 0:
            return 'M'
        else:
            return 'R'

    def update_transcript(self, transcript_row, operation, 
                                                temp, index):
        # helper function for optimal_transcript
        if operation == 'I':
            return transcript_row[index] + 'I'
        elif operation == 'D':
            return transcript_row[index + 1] + 'D'
        elif operation == 'M':
            return temp + 'M'
        else:
            return temp + 'R'

    def optimal_alignment(self, transcript):
        # Can decipher alignment from transcript
        index1 = 0  # index along string 1
        index2 = 0  # index along string 2
        line1 = ''  # first line of output
        line2 = ''

        for char in transcript:
            if char == 'M':
                line1 += self.string1[index1]
                line2 += self.string2[index2]

                index1 += 1
                index2 += 1
            
            if char == 'R':
                line1 += self.string1[index1]
                line2 += self.string2[index2]

                index1 += 1
                index2 += 1

            if char == 'I':
                line1 += ' '  # adding a space
                line2 += self.string2[index2]

                index2 += 1
            
            if char == 'D':
                line1 += self.string1[index1]
                line2 += ' '

                index1 += 1

        return line1, line2


if __name__ == "__main__":
    protein_A = 'MGLSDGEWQLVLKVWGKVEGDLPGHGQEVLIRLFKTHPETLEK\
FDKFKGLKTEDEMKASADLKKHGGTVLTALGNILKKKGQHEAELKPLAQSHATKHKISIK\
FLEYISEAIIHVLQSKHSADFGADAQAAMGKALELFRNDMAAKYKEFGFQG'
    protein_B = 'MADFDAVLKCWGPVEADYTTMGGLVLTRLFKEHPETQKLFPKF\
AGIAQADIAGNAAISAHGATVLKKLGELLKAKGSHAAILKPLANSHATKHKIPINNFKLI\
SEVLVKVMHEKAGLDAGGQTALRNVMGIIIADLEANYKELGFSG'

    output = edit_operations(protein_A, protein_B)
    transcript = output.optimal_transcript()
    print(transcript[0])
    print(transcript[1])
    print( output.optimal_alignment(transcript[1])[0] )
    print( output.optimal_alignment(transcript[1])[1] )
