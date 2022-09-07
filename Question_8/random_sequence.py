import random


class random_sequence:
    def __init__(self, p, length):
        self.p = p
        self.length = length
        self.sequence = self.generate_sequence()


    def generate_sequence(self):
        sequence = ''
        for index in range(self.length):
            random_float = random.random()
            if random_float < self.p:
                sequence += 'a'
            else:
                sequence += 'b'
        return sequence

    
    def get_sequence(self):
        return self.sequence


if __name__ == '__main__':
    # For testing purposes
    sequence = random_sequence(1/2, 1000)
    print(sequence.sequence)