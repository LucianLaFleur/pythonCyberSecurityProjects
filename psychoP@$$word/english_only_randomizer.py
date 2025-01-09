import random

#  verbs from :aaronbassett
# noun + adj from : taikuukaits
# bukowa, common other languages


# NYI: encapsulate this logic to make a much longer possible word
# Function to make X words long...
# first_word_arr = random.choice(wordlists)
# second_word_arr = random.choice(wordlists)
# third_word_arr = random.choice(wordlists)
# randomized_word_arrs = [first_word_arr, second_word_arr, third_word_arr]

# NYI: using names of characters, painters, brands, and cities would be a good mix-up

# ------------------------------

# The possible nums/chars to add to the end of each word
addetives = "!@#$%^&*()-_=+[]|;:,.<>?269"

#  ---- ENGLISH-ONLY activated by default ----- 
# Comment out below section and then activate next wordlist set with the bigger array 
#  for multi-lingual version ---------------------------------------------------

wordlist1 = "nouns1.txt"
wordlist2 = "adjectives1.txt"
wordlist3 = "verbs1.txt"

wordlists = [wordlist1, wordlist2, wordlist3]
#  / English version ---------------------------------------

# ---- ENGLISH ONLY ABOVE, comment out the 3 above, and activate the details below
# in order to activate the multi-lingual version --------------------------
# ----------------------------------------------
# wordlist1 = "nouns1.txt"
# wordlist2 = "adjectives1.txt"
# wordlist3 = "verbs1.txt"
# wordlist4 = "afrikaansNouns.txt"
# wordlist5 = "spanishNouns.txt"
# wordlist6 = "frenchNouns.txt"

# wordlists = [wordlist1, wordlist2, wordlist3, wordlist4, wordlist5, wordlist6]
# /multi-lingual version ----------------------------------------------

# Generates a random number between 1 and the given input number X (inclusive).
def rand_num_w_max(x):
    if x < 1:
        raise ValueError("Input number must be greater than or equal to 1")
    return random.randint(1, x)

# Example usage:
# random_number = randNumWithMaxOf(20)
# will be a random num between 1 and 20, like a d20 dice roll

# Function to randomly select words from the file
def select_random_word(filename):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file]
    return random.choice(words)

# Function to add random a random symbol 1-3 times
def add_random_symbols(word):
    chance = rand_num_w_max(100)
    if chance < 20:
        # 20% chance to add 1 character
        return word + random.choice(addetives)
    elif chance < 40:
        # 20% to add 2 characters
        return word + f"{random.choice(addetives) * 2}"
    elif chance < 60:
        # 20% 3 characters
        return word + f"{random.choice(addetives) * 3}"
    elif chance < 80:
        # 20% 4 characters
        return word + f"{random.choice(addetives) * 4}"
    else:
        # 20% for no chars between
        return word

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
                modified_word.append('$')
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
                modified_word.append(char.upper())
            else:
                modified_word.append(char)
    
    return ''.join(modified_word)

# Main function to generate the string
def generate_string_with_symbols():
    # randomly choose a source wordlist for each word
    first_word_arr = random.choice(wordlists)
    second_word_arr = random.choice(wordlists)
    third_word_arr = random.choice(wordlists)
    randomized_word_arrs = [first_word_arr, second_word_arr, third_word_arr]
    output_string = []
    for sub_arr in randomized_word_arrs:
        selected_word = select_random_word(sub_arr)
        modded_word = leet_letters(selected_word)
        symbol_appended_word = add_random_symbols(modded_word)
        output_string.append(symbol_appended_word)
    
    final_string = ''.join(output_string)
    print(final_string)

def generate_simple_string():
    # randomly choose a source wordlist for each word
    first_word_arr = random.choice(wordlists)
    second_word_arr = random.choice(wordlists)
    third_word_arr = random.choice(wordlists)
    randomized_word_arrs = [first_word_arr, second_word_arr, third_word_arr]
    output_string = []
    for sub_arr in randomized_word_arrs:
        selected_word = select_random_word(sub_arr)
        output_string.append(selected_word)
    final_string = '_'.join(output_string)
    print(final_string)

# Call the main function with the input file
print("your psycho-P@$$word is ---------------")
generate_string_with_symbols()
print("--- and a simple string ---------------")
generate_simple_string()

# NOTE:
#   Remember you can activate the multi-lingual word list in the comment area at the top with the French and Afrikaans samples present!
