import random
# addetives are the possible nums/chars to add to the end of each word
addetives = "!@#$%^&*()-_=+[]|;:,.<>?269"

wordlist1 = "nouns1.txt"
wordlist2 = "adjectives1.txt"
wordlist3 = "verbs1.txt"
wordlist4 = "afrikaansNouns.txt"
wordlist5 = "spanishNouns.txt"
wordlist6 = "frenchNouns.txt"
wordlist7 = "finnishNouns.txt"
wordlist8 = "irishNouns.txt"
wordlist9 = "germanNouns.txt"

wordlists = [wordlist1, wordlist2, wordlist3, wordlist4, wordlist5, wordlist6, wordlist7, wordlist8, wordlist9]

# Generates a random number between 1 and the given input number X (inclusive).
def rand_num_w_max(x):
    if x < 1:
        raise ValueError("Input number must be greater than or equal to 1")
    return random.randint(1, x)

#ex. >> random_number = randNumWithMaxOf(20)
# will be a random num between 1 and 20, like a d20 dice roll

# Function to randomly select words from the file
def select_random_word(filename):
    with open(filename, 'r') as file:
        words = [line.strip() for line in file]
    return random.choice(words)

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

print("--- your simple string ---------------")
generate_simple_string()
