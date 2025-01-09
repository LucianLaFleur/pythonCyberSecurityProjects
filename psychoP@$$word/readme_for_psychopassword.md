<h1>What is this?</h1>
Helps make very random strings, loosely based off character-replacement from random source words.

The simplest example is the word selector and most complex is multilingual psycho pass

<h2> leet letters: </h2> </br>
- replaces a portion of characters with l33t character if eligable (like a -> @ or a -> 4)
- randomizes capitalization of letters, even if not a special letter
- Purpose: I saw a lot of leet-speak when doing CTFs, so this tool helps quickly make them
Ex: 
`Input a string you want in L33t letters, randomized:
>> the clock struck twelve and the mouse ran down
+h3 cLOCk stRu(k tw37^e @nd t#3 mOU#3 raN DOWN`

<h2> simple word selector: </h2> </br>
- A randomizer that uses the text files included in this directory to choose random words
- the order of the word-types is random (even if you have  noun, adj., verb as your first 3 lists, the randomizer can choose any order or repeat the same type)
- repeats of words are allowed, and considered extremely rare and random if so (might be improved on to have dliberate repetition for boosting human memory and password entropy)
- words are joined by one single underscore. This spacer can easily be modified by on the [ "_".join(output_string) ] call on line 61.

<h2> multilingual psycho pass: </h2> </br>
- combines leet letters and simple word selector capabilities into a bigger program
- Capabilities from the simple_word_selector are available at the bottom, but the function is commented out. You can also get a random string if you want, so I kept it packaged together because I'm going to use it in a demo recording in the future
- inserts between 0 and 4 of the same special character or number between words. (done to add randomness but make it easier to memorize repeats for a human)
- <b> ! IMPORTANT !</b> uses many language-lists to randomly select a word, which may be in Finnish or Spanish, and then run the leetspeak char-replacement on it before adding.
- Leetspeak replacement will not mess up accented characters -> the weird accent characters are a bit of intended entropy from using random langages.
- Only included roman-alphabet sets to avoid unicode issues with Japanese, Chinese, and Cyrillic. (further expansions with unicode are absolutely possible)

<h2> English only randomizer: </h2> </br>
- Has the other text files commented out, just optimized for an english-word-only setup. 
- No weird ascii characters are involved in this set, like no umlauts or other accents on vowels.

---
Credits for source wordlists --
verbs from :aaronbassett
English nouns and adjectives from : taikuukaits
common nouns for other languages : bukowa 
All the lists can be found at their respective owners' repos.

