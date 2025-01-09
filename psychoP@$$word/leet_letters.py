import random

def leet_letters(word):
    # output-holder arr for the modified string we're building
    modified_word = []

    # iterate across the letters in the word
    for char in word:
        # Check for "a"'s to be modified ------------------------------ a
        if char == 'a':
            rand_value = random.random()
            if rand_value < 0.3:
                # 30% chance to replace 'a' with '@'
                modified_word.append('@')
            elif rand_value < 0.5:
                # 20% chance to capitalize 'a'
                modified_word.append('A')
            elif rand_value < 0.80:
                # 30% chance to replace 'a' with '4'
                modified_word.append('4')
            else:
                # 20% chance for lower case
                modified_word.append(char)
        elif char == 'b':
            rand_value = random.random()
            if rand_value < 0.35:
                # 35% chance to replace 'b' with '8'
                modified_word.append('8')
            elif rand_value < 0.7:
                # 35% chance to capitalize 'b'
                modified_word.append('B')
            else:
                # 30% chance for lower case b
                modified_word.append(char)
        elif char == 'c':
            rand_value = random.random()
            if rand_value < 0.35:
                # 35% chance to replace 'c' with '('
                modified_word.append('(')
            elif rand_value < 0.7:
                # 35% chance to capitalize 'c'
                modified_word.append('C')
            else:
                # 30% chance for lower case c
                modified_word.append(char)
        elif char == 'e':
            rand_value = random.random()
            if rand_value < 0.35:
                # 35% chance to replace 'e' with '3'
                modified_word.append('3')
            elif rand_value < 0.7:
                # 35% chance to capitalize 'e'
                modified_word.append('E')
            else:
                # 30% chance for lower case c
                modified_word.append(char)
        elif char == 'h':
            rand_value = random.random()
            if rand_value < 0.35:
                # 35% chance to replace 'h' with '#'
                modified_word.append('#')
            elif rand_value < 0.7:
                # 35% chance to capitalize 'h'
                modified_word.append('H')
            else:
                # 30% chance for lower case h
                modified_word.append(char)
        elif char == 'i':
            rand_value = random.random()
            if rand_value < 0.30:
                # 30% chance to replace 'i' with '1'
                modified_word.append('1')
            elif rand_value < 0.50:
                # 20% chance to capitalize 'i'
                modified_word.append('I')
            elif rand_value < 0.80:
                # 30% chance for replacing 'i' with '!'
                modified_word.append('!')
            else:
                # 20% chance for lower case 'i'
                modified_word.append(char) 
        elif char == 'l':
            rand_value = random.random()
            if rand_value < 0.35:
                # 35% chance to replace 'l' with '7'
                modified_word.append('7')
            elif rand_value < 0.7:
                # 35% chance to capitalize 'l'
                modified_word.append('L')
            else:
                # 30% chance for lower case l
                modified_word.append(char)
        elif char == 's':
            rand_value = random.random()
            if rand_value < 0.30:
                # 30% chance to replace 's' with '$'
                modified_word.append('#')
            elif rand_value < 0.50:
                # 20% chance to capitalize 's'
                modified_word.append('S')
            elif rand_value < 0.80:
                # 30% chance for replacing 's' with '5'
                modified_word.append('5')
            else:
                # 20% chance for lower case 's'
                modified_word.append(char) 
        elif char == 't':
            rand_value = random.random()
            if rand_value < 0.40:
                # 40% chance to replace 't' with '+'
                modified_word.append('+')
            elif rand_value < 0.70:
                # 30% chance to capitalize 't'
                modified_word.append('T')
            else:
                # 30% chance for lower case 't'
                modified_word.append(char) 
        elif char == 'v':
            rand_value = random.random()
            if rand_value < 0.40:
                # 40% chance to replace 'v' with '^'
                modified_word.append('^')
            elif rand_value < 0.70:
                # 30% chance to capitalize 'v'
                modified_word.append('V')
            else:
                # 30% chance for lower case 'v'
                modified_word.append(char) 
# otherwise, chance to capitalize letter
        else:
            rand_value = random.random()
            if rand_value < 0.5:
                try:
                    modified_word.append(char.upper())
                except:
                    print(f"couldn't lower-case {char}, appending plainly")
                    modified_word.append(char)
            else:
                modified_word.append(char)
    
    return ''.join(modified_word)

while True:
    input_word = input("Input a string you want in L33t letters, randomized:\t\n>> ")
    modded_word = leet_letters(input_word)
    print(modded_word)
    exit_cue = input("---\n make another word? or [q]uit\n\t>> ")
    if exit_cue == 'q':
        break
print("Program ending. Goodbye")
