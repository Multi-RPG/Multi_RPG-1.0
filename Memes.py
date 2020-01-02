#!/usr/bin/env python3
import requests
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path
import urllib.request
import textwrap
import configparser
import sys

# prepare data for IMGFLIP public API: https://api.imgflip.com/
# set URL that we will direct our non-custom memes requests to
URL = "https://api.imgflip.com/caption_image"
# set up parser to config through our .ini file with our imgflip account details
config = configparser.ConfigParser()
imgflip_token_path = Path(
    "tokens/tokenimgflip.ini"
)  # use forward slash "/" for path directories
# confirm the token is located in the above path
if imgflip_token_path.is_file():
    config.read(imgflip_token_path)
    username = config.get("USER1", "username")
    password = config.get("USER1", "password")
else:
    print(
        "\n",
        "IMGFLIP account token not found at: ",
        imgflip_token_path,
        "... Please correct file path in Memes.py file.",
    )
    sys.exit()


class Memes:
    def __init__(self, client):
        self.client = client

    # Not using IMGFLIP API for custom memes. Instead, using Python Imaging Library for image processing
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(
        name="custom",
        description="generate your own twitter style meme",
        brief="can use =memegen",
        aliases=["memegen", "CUSTOM", "meme"],
        pass_context=True,
    )
    async def custom_meme(self, context, *args):
        # made this check function with the help of discord API documentation
        # it will be called below when purging, to only purge messages from itself and user who called this command
        def purge_check(msg):
            return (
                msg.author == context.message.author or msg.author == self.client.user
            )

        # first, get the inputs from user. this command needs the meme text and the meme image
        await self.client.say(
            "<:wthumbs:493806177894006786> First, type the text for your"
            " custom twitter-styled meme..."
        )
        user_text = await self.client.wait_for_message(
            author=context.message.author, timeout=60
        )
        await self.client.say(
            "<:wthumbs:493806177894006786> Now, send an image URL for your"
            " custom twitter-styled meme..."
        )
        user_image = await self.client.wait_for_message(
            author=context.message.author, timeout=60
        )
        await self.client.purge_from(
            context.message.channel, limit=5, check=purge_check
        )

        # set header uger-agent as Mozilla Firefox so our image requests (for custom memes) won't be denied
        opener = urllib.request.build_opener()
        opener.addheaders = [
            (
                "User-agent",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/36.0.1941.0 Safari/537.36",
            )
        ]
        urllib.request.install_opener(opener)

        # try to start the request to get the image specified by user
        try:
            # download the image as "UserImage.png"
            urllib.request.urlretrieve(
                user_image.clean_content, "custom_memes\\UserImage.png"
            )
        except:
            # the bot failed to retrieve image at that URL
            await self.client.say(
                context.message.author.mention
                + " The link you provided seems to be faulty..."
                " <a:pepehands:485869482602922021>"
            )
            return

        # SETUP WHITE BACKGROUND CANVAS
        background = Image.open("custom_memes\memebackground.png")
        draw = ImageDraw.Draw(background)
        # set custom true type font from our directory, helvetica neue
        font = ImageFont.truetype("custom_memes\helv.ttf", 25)
        smallfont = ImageFont.truetype("custom_memes\helv.ttf", 21)

        # PASTE USER'S PROFILE PICTURE AND USERNAME ON TOP OF BACKGROUND CANVAS
        # retrieve the URL for this user's avatar to embed above the text
        urllib.request.urlretrieve(
            context.message.author.avatar_url, "custom_memes\\UserAvatar.webp"
        )
        # read the avatar image that we downloaded, convert to RGB so we can process it
        img = Image.open("custom_memes\\UserAvatar.webp", "r").convert("RGB")
        # resize avatar to to be thumbnail size
        # using ANTIALIAS as good practice for using PIL library
        img = img.resize((45, 45), Image.ANTIALIAS)
        # paste the image onto background at the top
        background.paste(img, (10, 5))
        # draw the user's username next to their profile picture
        draw.text(
            (63, 1), ("@" + str(context.message.author)), (65, 65, 65), font=smallfont
        )

        # PASTE THE MEME TEXT IN MIDDLE OF BACKGROUND CANVAS
        # draw their specified text on the white background, with word wrapping
        offset = 60
        for line in textwrap.wrap(user_text.clean_content, width=40):
            draw.text((10, offset), line, (1, 1, 1), font=font)
            offset += font.getsize(line)[1]

        # PASTE THE MEME PICTURE ON BOTTOM OF BACKGROUND CANVAS
        # read the image that we downloaded earlier
        try:
            img = Image.open("custom_memes\\UserImage.png", "r").convert("RGB")
        except:
            # if we can't read the image downloaded, it's in the wrong format...
            await self.client.say(
                "PNG/JPG/WebP links only please! <a:pepehands:485869482602922021>"
            )
            return
        # resize image to fit background
        # using ANTIALIAS as good practice for using PIL library
        img = img.resize((468, 277), Image.ANTIALIAS)
        # get the offset to center the pic at bottom
        img_w, img_h = img.size
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, 191)
        # paste the image onto background now at the position specified
        background.paste(img, offset)
        background.save("custom_memes\memegenresult.png")

        await self.client.send_file(
            context.message.channel, "custom_memes\memegenresult.png"
        )

    @commands.command(
        name="trumporder",
        description="executive order from trump",
        brief='can use =trumporder "order"',
        aliases=[
            "trump",
            "order",
            "executiveorder" "TRUMP",
            "EXECUTIVE",
            "executive",
            "ORDER",
        ],
        pass_context=True,
    )
    async def trump_order(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 91545132
        font = "arial"

        try:
            order = ""
            # if the command was processed with mobile quotes “ ”, compile all arguments given
            if "“" in args[0]:
                for argument in args:
                    order = order + " " + argument

                # strip mobile's weird double quotes from the arguments
                order = order.replace("“", "").replace("”", "")
            else:
                order = str(args[0])
            print("trump order meme arguments: " + order)
        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =trumporder like so: =trumporder "order"```'
            )
            return

        DATA = {
            "template_id": template_id,
            "username": username,
            "password": password,
            "boxes[1][text]": order,
            "boxes[1][color]": "#000000",
            "boxes[1][outline_color]": "#bccfd3",
            "boxes[1][x]": 1271,
            "boxes[1][y]": 563,
            "boxes[1][width]": 441,
            "boxes[1][height]": 456,
            "max_font_size": 70,
            "font": font,
            "api_paste_format": "python",
        }

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="2buttons",
        description="2 buttons meme",
        brief='can use =2buttons "option1" "option2"',
        aliases=["buttons", "2 buttons", "twobuttons"],
        pass_context=True,
    )
    async def two_buttons(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 87743020
        font = "arial"
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            button1 = str(args[0])
            button2 = str(args[1])
            print("2 buttons meme arguments: " + button1 + " " + button2)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =twobuttons like so: =twobuttons "option1" "option2"```'
            )
            return

        DATA = {
            "template_id": template_id,
            "username": username,
            "password": password,
            "boxes[0][text]": button1,
            "boxes[0][color]": "#000000",
            "boxes[0][outline_color]": "#ffffff",
            "boxes[1][text]": button2,
            "boxes[1][color]": "#000000",
            "boxes[1][outline_color]": "#ffffff",
            "max_font_size": 45,
            "font": "arial",
        }

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="reasonstolive",
        description="book of reasons to live",
        brief='can use =reasonstolive "reasons"',
        aliases=["pepelive", "reasons", "hope", "pepebook"],
        pass_context=True,
    )
    async def reasons_to_live(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 49740399
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            reasons = ""
            # if the command was processed with mobile quotes “ ”, compile all arguments given
            if "“" in args[0]:
                for argument in args:
                    reasons = reasons + " " + argument

                # strip mobile's weird double quotes from the arguments
                reasons = reasons.replace("“", "").replace("”", "")
            else:
                reasons = str(args[0])
            print("reasons to live meme arguments: " + reasons)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =reasonstolive like so: =reasonstolive "reasons"```'
            )
            return

        DATA = {
            "template_id": template_id,
            "username": username,
            "password": password,
            "boxes[1][text]": reasons,
            "boxes[1][color]": "#000000",
            "boxes[1][outline_color]": "#ffffff",
            "boxes[1][x]": 50,
            "boxes[1][y]": 500,
            "boxes[1][width]": 170,
            "boxes[1][height]": 200,
            "max_font_size": 24,
            "font": font,
        }

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="bookfacts",
        description="book of facts meme",
        brief='can use =bookfacts "facts"',
        aliases=[
            "book",
            "facts",
            "BOOK",
            "FACTS",
            "bookoffacts",
            "BOOKOFFACTS",
            "factsbook",
            "FACTSBOOK",
        ],
        pass_context=True,
    )
    async def book_of_facts(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 117573930
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            facts = ""
            # if the command was processed with mobile quotes “ ”, compile all arguments given
            if "“" in args[0]:
                for argument in args:
                    facts = facts + " " + argument

                # strip mobile's weird double quotes from the arguments
                facts = facts.replace("“", "").replace("”", "")
            else:
                facts = str(args[0])
            print("book of facts meme arguments: " + facts)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =bookfacts like so: =bookfacts "facts"```'
            )
            return

        DATA = {
            "template_id": template_id,
            "username": username,
            "password": password,
            "boxes[1][text]": facts,
            "boxes[1][color]": "#000000",
            "boxes[1][outline_color]": "#e9f5e1",
            "boxes[1][x]": 0,
            "boxes[1][y]": 330,
            "boxes[1][width]": 200,
            "boxes[1][height]": 200,
            "boxes[1][outline_width]": 1,
            "boxes[1][font_shadow]": 0,
            "max_font_size": 26,
            "font": font,
            "api_paste_format": "python",
        }

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="changemymind",
        description="change my mind meme",
        brief='can use =changemymind "statement"',
        aliases=["debate", "CHANGEMYMIND", "changemind", "change"],
        pass_context=True,
    )
    async def change_my_mind(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 129242436
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            facts = ""
            # if the command was processed with mobile quotes “ ”, compile all arguments given
            if "“" in args[0]:
                for argument in args:
                    facts = facts + " " + argument

                # strip mobile's weird double quotes from the arguments
                facts = facts.replace("“", "").replace("”", "")
            else:
                facts = str(args[0])
            print("change my mind meme arguments: " + facts)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =changemymind like so: =changemymind "statement"```'
            )
            return

        DATA = {
            "template_id": template_id,
            "username": username,
            "password": password,
            # 'boxes[0][text_align]': 'left',
            "boxes[1][text_align]": "left",
            "boxes[1][text]": facts,
            "boxes[1][color]": "#000000",
            "boxes[1][outline_color]": "#d6d4e1",
            "max_font_size": 22,
            "font": font,
            "api_paste_format": "python",
        }

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    """start using key value pairs instead of dictionaries for (DATA) when order matters
    (' ',' ') vs (' ':' ')
    """

    @commands.command(
        name="slapbutton",
        description="blue button karate chop meme",
        brief='can use =slapbutton "cause" "reaction"',
        aliases=["chopbutton", "bluebutton", "SLAPBUTTON", "buttonslam", "smashbutton"],
        pass_context=True,
    )
    async def slap_button(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 119139145
        font = "arial"

        # try-catch block, because of *args array. if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            cause = str(args[0])
            reaction = str(args[1])
            print("slap button meme arguments: " + cause + " " + reaction)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =slapbutton like so: =slapbutton "cause" "reaction"```'
            )
            return

        DATA = (
            ("template_id", template_id),
            ("username", username),
            ("password", password),
            ("boxes[0][text]", cause),
            ("boxes[1][text]", reaction),
            ("max_font_size", 40),
            ("font", font),
        )

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="brain",
        description="expanding brain meme",
        brief='can use =brain "stage1" "stage2" "stage3" "stage4"',
        aliases=["expand", "brainexpand", "expandbrain", "IQ", "200IQ"],
        pass_context=True,
    )
    async def expanding_brain(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 93895088
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            stage1 = str(args[0])
            stage2 = str(args[1])
            stage3 = str(args[2])
            stage4 = str(args[3])
            print(
                "expanding brain meme arguments: "
                + stage1
                + " "
                + stage2
                + " "
                + stage3
                + " "
                + stage4
            )

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =brain like so: =brain "stage1" "stage2" "stage3" "stage4"```'
            )
            return

        data1 = (
            ("template_id", template_id),
            ("username", username),
            ("password", password),
            ("boxes[0][text]", stage1),
            ("boxes[1][text]", stage2),
            ("boxes[2][text]", stage3),
            ("boxes[3][text]", stage4),
            ("font", font),
            ("boxes[0][color]", "#000000"),
            ("boxes[0][outline_color]", "#ffffff"),
            ("boxes[0][outline_width]", 1),
            ("boxes[0][font_shadow]", 0),
            ("boxes[1][color]", "#000000"),
            ("boxes[1][outline_color]", "#ffffff"),
            ("boxes[1][outline_width]", 1),
            ("boxes[1][font_shadow]", 0),
            ("boxes[2][color]", "#000000"),
            ("boxes[2][outline_color]", "#ffffff"),
            ("boxes[2][outline_width]", 1),
            ("boxes[2][font_shadow]", 0),
            ("boxes[3][color]", "#000000"),
            ("boxes[3][outline_color]", "#ffffff"),
            ("boxes[3][outline_width]", 1),
            ("boxes[3][font_shadow]", 0),
            ("max_font_size", 60),
            ("font", font),
        )

        r = requests.post(url=URL, data=data1)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="pigeon",
        description="Pigeon meme",
        brief='can use =pigeon "boy" "butterfly" "is this a pidgeon?"',
        aliases=["PIDGEON", "pidgeon", "PIGEON"],
        pass_context=True,
    )
    async def pigeon(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 100777631
        font = "arial"
        # try-catch block, because of *args array. if no argument given in discord after "=pidgeon",
        # it will go to the exception
        try:
            whom = str(args[0])
            butterfly = str(args[1])
            # "is this a X" text section of the meme is the most likely to have multiple words,
            # so use join just in case user didn't put that part in strings
            # take all arguments after 2 to make the meme format user friendly,
            # combine into 1 string with spaces between each word
            is_this_a = " ".join(args[2 : len(args)])

            print("Pigeon meme arguments: " + whom + " " + butterfly + " " + is_this_a)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =pigeon like so: =pigeon "boy" "butterfly" "is this a pidgeon?"```'
            )
            return

        DATA = (
            ("template_id", template_id),
            ("font", font),
            ("username", username),
            ("password", password),
            ("boxes[0][text]", whom),
            ("boxes[1][text]", butterfly),
            ("boxes[2][text]", is_this_a),
            ("boxes[0][color]", "#ffffff"),
            ("boxes[0][outline_color]", "#000000"),
            ("boxes[0][outline_width]", 1),
            ("boxes[0][font_shadow]", 0),
            ("boxes[1][color]", "#ffffff"),
            ("boxes[1][outline_color]", "#000000"),
            ("boxes[1][outline_width]", 1),
            ("boxes[1][font_shadow]", 0),
            ("boxes[2][color]", "#ffffff"),
            ("boxes[2][outline_color]", "#000000"),
            ("boxes[2][outline_width]", 1),
            ("boxes[2][font_shadow]", 0),
            ("max_font_size", 100),
            ("api_paste_format", "python"),
        )

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="leftexit",
        description="Swerve left exit meme",
        brief='can use =leftexit "left" "right" "car"',
        aliases=["carswerve", "LEFTEXIT", "swerve"],
        pass_context=True,
    )
    async def left_exit(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 124822590
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            left = str(args[0])
            right = str(args[1])
            car = " ".join(args[2 : len(args)])

            print("Left exit meme arguments " + left + " " + right + " " + car)

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =leftexit like so: =leftexit "left" "right" "car"```'
            )
            return

        DATA = (
            ("template_id", template_id),
            ("username", username),
            ("password", password),
            ("boxes[0][text]", left),
            ("boxes[1][text]", right),
            ("boxes[2][text]", car),
            ("font", font),
            ("boxes[0][color]", "#ffffff"),
            ("boxes[0][outline_color]", "#000000"),
            ("boxes[0][outline_width]", 1),
            ("boxes[0][font_shadow]", 0),
            ("boxes[1][color]", "#ffffff"),
            ("boxes[1][outline_color]", "#000000"),
            ("boxes[1][outline_width]", 1),
            ("boxes[1][font_shadow]", 0),
            ("boxes[2][color]", "#ffffff"),
            ("boxes[2][outline_color]", "#000000"),
            ("max_font_size", 75),
            ("api_paste_format", "python"),
        )

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])

    @commands.command(
        name="boyfriend",
        description="boyfriend checking out girl meme",
        brief='can use =boyfriend "new girl" "distracted boyfriend" "girlfriend"',
        aliases=["BOYFRIEND", "bf", "BF", "checkout", "CHECKOUT"],
        pass_context=True,
    )
    async def boyfriend(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 112126428
        font = "arial"

        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon" it will go to the exception
        try:
            new_girl = str(args[0])
            distracted_boyfriend = str(args[1])
            girlfriend = " ".join(args[2 : len(args)])

            print(
                "Distracted boyfriend meme arguments "
                + new_girl
                + " "
                + distracted_boyfriend
                + " "
                + girlfriend
            )

        except:
            await self.client.say(
                context.message.author.mention
                + '```ml\nuse =boyfriend like so: "new girl" "distracted boyfriend" "girlfriend"```'
            )
            return

        DATA = (
            ("template_id", template_id),
            ("username", username),
            ("password", password),
            ("boxes[0][text]", new_girl),
            ("boxes[1][text]", distracted_boyfriend),
            ("boxes[2][text]", girlfriend),
            ("font", font),
            ("boxes[0][color]", "#ffffff"),
            ("boxes[0][outline_color]", "#000000"),
            ("boxes[0][outline_width]", 1),
            ("boxes[0][font_shadow]", 0),
            ("boxes[1][color]", "#ffffff"),
            ("boxes[1][outline_color]", "#000000"),
            ("boxes[1][outline_width]", 1),
            ("boxes[1][font_shadow]", 0),
            ("boxes[2][color]", "#ffffff"),
            ("boxes[2][outline_color]", "#000000"),
            ("max_font_size", 75),
            ("api_paste_format", "python"),
        )

        r = requests.post(url=URL, data=DATA)
        text = r.json()
        await self.client.say(text["data"]["url"])


def setup(client):
    client.add_cog(Memes(client))
