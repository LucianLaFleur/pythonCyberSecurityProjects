import random
# takes the input string, breaks along spaces, and re-orders it randomly. 
# Gets your word-salad tossed

input_string = "Mix flour-sugar-eggs and butter into a batter pour into a greased pan and bake in-the oven until golden-brown let-the cake cool frost and-serve"
# Mix flour, sugar, eggs, and butter into a batter, pour into a greased pan, and bake in the oven until golden brown. Let the cake cool, frost, and serve.
def shuffle_string(input_string):
    words = input_string.split()
    random.shuffle(words)
    shuffled_string = ' '.join(words)
    print(shuffled_string)

# Proceess execution
shuffle_string(input_string)
