#!/usr/bin/env python3
import random
from discord.ext import commands
from Users import Users

# open with file read for hangman at the top.
# this way, we won't have to re-open the file every hangman, and we can just call pick_word()
# make sure there is no carriage return after last word in text file
# words_file = open("/usr/local/words.txt","r") # unix dedicated server version
words_file = open("words.txt", "r")  # windows version
all_words = words_file.readlines()
words_file.close()

hangmen = [
    ' -----------    \n|          |    \n|             \n|          \n|          \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|         \n|          \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|          |  \n|          \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|        /|  \n|          \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|        /|\\  \n|          \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|        /|\\  \n|        /   \n|              \n|              \n',
    ' -----------    \n|          |    \n|         O    \n|        /|\\  \n|        / \\  \n|              \n|              \n']

hm_categories_help = '```fix\n1. Country name\n2. Farm\n3. Camping\n4. Household items/devices\n' \
                     '5. Beach\n6. Holidays\n7. US States\n8. Sports & Hobbies```'

cancel_strings = ['STOP', 'CANCEL']


class Games:
    def __init__(self, client):
        self.client = client

    '''ROB FUNCTION'''
    @commands.command(name='rob', description='Steal money from others', brief='can use %steal',
                      aliases=['thief', 'thieve', 'ROB', 'steal', 'mug'], pass_context=True)
    async def rob(self, context):
        # create instance of the user starting the robbery
        robber = Users(context.message.author.id)

        # make sure the robber has an account
        if robber.find_user() == 0:
            await self.client.say(context.message.author.mention + " You don't have an account.\n"
                                                                   "Use **%create** to make one.")
            return

        # pick a random user in the server to rob
        # user_to_rob variable will function as the victim user's "english" name
        user_to_rob = random.choice(list(context.message.server.members))
        # make an instance of the target
        victim = Users(user_to_rob.id)
        counter = 1

        # while the user to rob is yourself, re-roll the target
        # while the user to rob does not have an account in the database, re-roll the target
        while user_to_rob == context.message.author or victim.find_user() == 0:
            # only try 30 different members... don't want an infinite while loop
            # this part is inefficient, but only way I can think of right now with discord's functionality
            if counter == 30:
                await self.client.say('No users found to rob...')
                return
            user_to_rob = random.choice(list(context.message.server.members))
            # create a new instance of victim each loop
            # in order to check if the reroll has an account in database
            victim = Users(user_to_rob.id)
            counter += 1

        # 40% chance to fail rob
        if 4 >= random.randint(1, 10) >= 1:
            # take 5% of robber's money for bail funds
            bail = int(robber.get_user_money(0) * .05)
            robber.update_user_money(bail * -1)
            await self.client.say('<a:policesiren2:490326123549556746> :oncoming_police_car: '
                                  '<a:policesiren2:490326123549556746>\n'
                                  '<a:monkacop:490323719063863306>'
                                  '         <a:monkacop:490323719063863306>\n**'
                                  '' + str(user_to_rob) + '** dodged and the '
                                  'police shot you in the process.\n'
                                  'You spent **$' + str(bail) + '** to bail out of jail.')
            return

        # we passed the dodge check, so reward thief with 10% of victim's total money
        prize = int(victim.get_user_money(0) * .10)
        victim.update_user_money(prize * -1)
        robber.update_user_money(prize)
        await self.client.say('**Success!** <:poggers:490322361891946496>\n'
                              'You robbed **$'
                              '' + str(prize) + '** from **' + str(user_to_rob) + '**')

    '''FLIP COIN FUNCTION'''
    @commands.command(name='flip', description='Flip a coin to earn social status.',
                      brief='can use "%flip" or "%flip X", with X being heads or tails',
                      aliases=['f', 'flpi', 'FLIP', 'F'], pass_context=True)
    async def flip_coin(self, context, *args):
        result = random.randint(0, 1)  # flipping in "binary"
        win = 0

        # first, check if they specified a bet and they have enough money for it
        try:
            user = Users(context.message.author.id)
            bet = int(args[1])
            # pass 0 to return integer version of money, see USERS.PY function
            if bet > user.get_user_money(0):
                await self.client.say("You don't have enough money for that bet..."
                                      " <a:pepehands:485869482602922021> " + context.message.author.mention)
                return
        except:
            pass

        # check if they specified a guess of heads or tails
        # process if they won or not
        try:
            if args[0] == 'heads':
                if result == 1:
                    msg = '<:heads:486705167643967508> Result is **Heads**! You win! <a:worryHype:487059927731273739>'
                    win = 1
                else:
                    msg = '<:heads:486705184370589718> Result is **Tails**! You lost. <a:pepehands:485869482602922021>'
            else:
                if result == 1:
                    msg = '<:heads:486705167643967508> Result is **Heads**! You lost. <a:pepehands:485869482602922021>'
                else:
                    msg = '<:heads:486705184370589718> Result is **Tails**! You win! <a:worryHype:487059927731273739>'
                    win = 1
        except:
            #no arguments provided at all. so just give a result
            print("No argument specified for betting on the coin side.")
            if result == 1:
                msg = '<:heads:486705167643967508> Result is **Heads**!'
            else:
                msg = '<:heads:486705184370589718> Result is **Tails**!'
        await self.client.say(msg + ' ' + context.message.author.mention)

        # if they specified a "guess" and "bet" that was valid, check if they won
        # note this will only pass through if "bet" was assigned through the earlier try/catch
        try:
            if win == 1:
                # triple user's bet if they win, add to account
                msg = user.update_user_money(bet * 2)
            else:
                # remove user's bet from their account if they lose
                msg = user.update_user_money(bet * -1)
                # if they have $0 after that flip, give a donation dollar to discourage account re-creation
                # pass in 0 for get_user_money to return the money as integer, SEE USERS.PY
                if user.get_user_money(0) == 0:
                    msg += "\n** **\n_The gambling gods have shown mercy on your bankrupt existence, and given you **$1**_"
                    msg += "\n" + user.update_user_money(1)
            await self.client.say(msg)
        except:
            print("No bet specified")

    '''HANGMAN main function'''
    @commands.command(name='hangman', description='Guess the word in order to survive.',
                      brief='can use "%hangman", type "stop" or "cancel" to end game',
                      aliases=['hm', 'hang', 'HM', 'HANGMAN'], pass_context=True)
    async def hangman(self, context, *args):
        wrong_guesses = 0  # global running count of incorrect guesses
        guessed_letters = ['']  # string of letters

        # pick starting word with a category, also make the string of underscores to replace later
        # check if they want to list the categories
        try:
            if args[0] in ('help', 'HELP', 'categories', 'cats', 'h'):
                await self.client.say(context.message.author.mention + ' Categories:\n' + hm_categories_help)
                return
            correct_word, category, underscore_sequence = pick_word(int(args[0]))

        # if no category was specified in argument by user...
        except:
            # pick random category 1-8
            rand_category = random.randint(1, 8)
            correct_word, category, underscore_sequence = pick_word(rand_category)

        await self.client.say(context.message.author.mention + ' Word category is: **```fix\n' + category + '```**')
        await self.client.say('** **')
        # print the hangman ascii setup
        await self.client.say(hangmen[0])
        await self.client.say('** **\n' + "".join(underscore_sequence))
        # use ** ** for empty line, discord doesn't allow empty messages.
        # also, using "".join because discord api can't  print lists.
        # we could cast, but the format would be unfriendly for the game.

        while True:  # main game loop
            await self.client.say('*Guess a letter or the entire word now...*')
            guess = await self.client.wait_for_message(author=context.message.author,
                                                       timeout=60)  # wait for user's guess
            already_guessed = 1
            while already_guessed == 1:  # loop that will exit immediately if letter guess isn't a repeat
                if guess.clean_content.upper() in str("".join(guessed_letters)):
                    await self.client.purge_from(context.message.channel, limit=1)
                    await self.client.say('\n*You already tried that. Guess a different letter now...*')
                    # wait for user's guess now
                    guess = await self.client.wait_for_message(author=context.message.author, timeout=30)
                    # account for that extra message, so delete last one
                    await self.client.purge_from(context.message.channel, limit=1)
                else:
                    already_guessed = 0

            '''RUN WIN CHECKS AND CANCEL CHECKS NOW'''
            # run conditionals to check if they guessed entire word or they used a cancel keyword
            print(guess.clean_content.upper() + ' and correct word: ' + correct_word)  # console print
            if guess.clean_content.upper() == correct_word:
                await self.client.purge_from(context.message.channel, limit=6)
                await self.client.say(hangmen[wrong_guesses])
                await self.client.say('**Correct word pick** <a:worryHype:487059927731273739>')
                await self.client.say('You **won** the game!! <a:worryHype:487059927731273739> Correct word was:'
                                      ' **' + correct_word.upper() + '** ' + context.message.author.mention)
                # add $200 to user's bank account now
                user = Users(context.message.author.id)
                await self.client.say(user.update_user_money(200))
                return

            if guess.clean_content.upper() in cancel_strings:
                await self.client.purge_from(context.message.channel, limit=6)
                await self.client.say('**Cancelled** the game!! <a:pepehands:485869482602922021> Correct word was: '
                                      '**' + correct_word.upper() + '** ' + context.message.author.mention)
                return

            # quick win check, check for any underscores left to fill.
            # if unknown_letters ends up as 0 for this iteration, then there are no letters left to guess.
            num_matches, underscore_sequence = find_matches(guess, correct_word, underscore_sequence)
            unknown_letters = 0
            for x in underscore_sequence:
                if x == '\u2581':  # if it's an underscore still, the letter is still unknown to the user
                    unknown_letters += 1
            if unknown_letters == 0:
                await self.client.purge_from(context.message.channel, limit=6)
                await self.client.say(hangmen[wrong_guesses])
                await self.client.say('You **won** the game!! <a:worryHype:487059927731273739> Correct word was: '
                                      '**' + correct_word.upper() + '** ' + context.message.author.mention)
                # add $200 to user's bank account now
                user = Users(context.message.author.id)
                await self.client.say(user.update_user_money(200))
                return

            # clear up last 6 messages, only 5 if first round, to reduce bot spam
            if len(guessed_letters) == 1:
                await self.client.purge_from(context.message.channel, limit=5)
            else:
                await self.client.purge_from(context.message.channel, limit=6)

            # print whether they guessed a correct letter or not
            if num_matches == 0:
                wrong_guesses += 1  # no letters matched, so they guessed a wrong letter
                if len(guess.clean_content) == 1:
                    await self.client.say('**Wrong letter pick** <a:pepehands:485869482602922021>')
                else:
                    await self.client.say('**Wrong word pick** <a:pepehands:485869482602922021>')
            else:
                await self.client.say('**Correct letter pick** <a:worryHype:487059927731273739>')
                # don't need "correct word pick" next because that would trigger
                # in the conditional right after the guess is taken

            # print the ascii art corresponding to wrong guesses
            if wrong_guesses < 6:
                await self.client.say(hangmen[wrong_guesses])
            elif wrong_guesses == 6:
                await self.client.say(hangmen[6])
                await self.client.say('\nYou were **hanged**! <a:pepehands:485869482602922021> The word was: '
                                      '**' + correct_word + '**\n' + context.message.author.mention)
                return

            # print underscores/letters, our main interface
            await self.client.say('** **\n**' + "".join(underscore_sequence) + '**')
            # add last guessed letter to our guessed-so-far list
            guessed_letters, all_guessed = add_guess_to_list(guess, guessed_letters)
            # print all letters guessed so far
            # all_guessed is just the string version of guessed_letters (a list version)
            await self.client.say('** ```fix\nGuessed so far: ' + all_guessed + '``` **')


def setup(client):
    client.add_cog(Games(client))


def pick_word(cat):
    if cat == 1:
        random_word = random.choice(all_words[0:180])
        category = 'Country name'
    elif cat == 2:
        random_word = random.choice(all_words[181:319])
        category = 'Farm'
    elif cat == 3:
        random_word = random.choice(all_words[320:389])
        category = 'Camping'
    elif cat == 4:
        random_word = random.choice(all_words[390:490])
        category = 'Household items/devices'
    elif cat == 5:
        random_word = random.choice(all_words[491:603])
        category = 'Beach'
    elif cat == 6:
        random_word = random.choice(all_words[604:648])
        category = 'Holidays'
    elif cat == 7:
        random_word = random.choice(all_words[649:699])
        category = 'US States'
    elif cat == 8:
        random_word = random.choice(all_words[700:998])
        category = 'Sports & Hobbies'
    else:
        random_word = random.choice(all_words[649:699])
        category = 'US States'

    # quick band-aid fix to truncate CR in text file, COMING BACK LATER TO FIX
    length = len(random_word) - 1  # to remove carriage return, I'm not using unix format to make the list
    random_word = random_word[:length]  # truncate word with [:length] cause of carriage return in text file...

    underscore_sequence = list('')  # this will be our list of underscores
    # it will be consistently replaced by guesses

    # fill the underscore_sequence list with underscore underscore_sequencelate of the correct word
    for x in random_word:
        if x == ' ':
            underscore_sequence += '      '  # in the case of 2-word phrases, need to move everything over
        elif x == '\'':
            underscore_sequence += ' \''
        else:
            underscore_sequence += ' \u2581'  # if not a space, add: \u2581, a special underscore character.
            # using to replace by correctly guessed letters

    return random_word.upper(), category, underscore_sequence


def add_guess_to_list(guess, guessed):  # accepts guess and list of all guesses
    if len(guess.clean_content) > 1:  # don't want to add whole word to guess list
        all_guessed = ''.join(map(str, guessed))
        return guessed, all_guessed
    guessed.extend(guess.clean_content.upper())  # add last guess to the list of guessed words
    guessed.extend(' ')  # add space to guessed list
    all_guessed = ''.join(map(str, guessed))  # messy syntax, convert the list into a string so bot can print it
    return guessed, all_guessed


def find_matches(guess, correct_word, underscore_sequence):
    index = 0
    num_matches = 0
    for x in correct_word:
        index += 1
        if x == ' ':
            index += 2
        # if any matches, we need to replace underscore(s) in the sequence
        # and increase the number of matches for the loop
        if guess.clean_content.upper() == x:
            # convulted index scheme due to underscore_sequence format
            underscore_sequence[index * 2 - 1] = guess.clean_content.upper()
            num_matches += 1
    return num_matches, underscore_sequence
