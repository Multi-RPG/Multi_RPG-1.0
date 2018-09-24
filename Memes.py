#!/usr/bin/env python3
import requests
from discord.ext import commands

# prepare data for IMGFLIP public API: https://api.imgflip.com/
username = 'hangman39'
# read our IMGFLIP account password from text file
# pass_file = open("/usr/DiscordBot/config2.txt","r") # unix version
pass_file = open("config2.txt","r") # windows version
password = pass_file.read()
pass_file.close()
# set URL that we will direct our requests to
URL = "https://api.imgflip.com/caption_image"

class Memes:
    def __init__(self, client):
        self.client = client
    @commands.command(name='trumporder', description='executive order from trump', brief='can use =trumporder "order"',
                      aliases=['trump', 'order', 'executiveorder' 'TRUMP', 'EXECUTIVE', 'executive', 'ORDER'], pass_context=True)
    async def trump_order(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 91545132
        font = 'arial'
        
        try:
            order = str(args[0]) # the argument is passed as message object, gotta cast
            print('trump order meme arguments: ' + order)  
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =trumporder like so: =trumporder "order"```')
            return
        
        DATA = {'template_id':template_id,
                'username':username,
                'password':password,
                'boxes[1][text]':order,
                'boxes[1][color]':"# 000000",
                'boxes[1][x]':1271,
                'boxes[1][y]':563,
                'boxes[1][width]':441,
                'boxes[1][height]':456,   
                'max_font_size':70,
                'font':font,
                'api_paste_format':'python'}
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
        
    @commands.command(name='2buttons', description='2 buttons meme', brief='can use =2buttons "option1" "option2"',
                      aliases=['buttons', '2 buttons', 'twobuttons'], pass_context=True)
    async def two_buttons(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 87743020
        
                
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            button1 = str(args[0]) # the argument is passed as message object, gotta cast
            button2 = str(args[1]) 
            print('2 buttons meme arguments: ' + button1 + ' ' + button2)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =twobuttons like so: =twobuttons "option1" "option2"```')
            return
        
        DATA = {'template_id':template_id,
                'username':username,
                'password':password,
                'boxes[0][text]':button1,
                'boxes[1][text]':button2,
                'max_font_size':45,
                'font':'impact'}
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])    
        
    @commands.command(name='reasonstolive', description='book of reasons to live', brief='can use =reasonstolive "reasons"',
                      aliases=['pepelive', 'reasons', 'hope', 'pepebook'], pass_context=True)
    async def reasons_to_live(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 49740399
        font = 'arial'
        
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            reasons = str(args[0]) # the argument is passed as message object, gotta cast
            print('reasons to live meme arguments: ' + reasons)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =reasonstolive like so: =reasonstolive "reasons"```')
            return
        
        DATA = {'template_id':template_id,
                'username':username,
                'password':password,
                'boxes[1][text]':reasons,
                'boxes[1][color]':"# ffffff",
                'boxes[1][outline_color]': "# 000000",
                'boxes[1][x]':50,
                'boxes[1][y]':500,
                'boxes[1][width]':200,
                'boxes[1][height]':200,                
                'max_font_size':24,
                'font':font}
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
        
    @commands.command(name='bookfacts', description='book of facts meme', brief='can use =bookfacts "facts"',
                      aliases=['book', 'facts', 'BOOK', 'FACTS', 'bookoffacts', 'BOOKOFFACTS', 'factsbook', 'FACTSBOOK'],
                      pass_context=True)
    async def book_of_facts(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 117573930
        font = 'arial'
        
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            facts = str(args[0]) # the argument is passed as message object, gotta cast
            print('book of facts meme arguments: ' + facts)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =bookfacts like so: =bookfacts "facts"```')
            return
        
        DATA = {'template_id':template_id,
                'username':username,
                'password':password,
                'boxes[1][text]':facts,
                'boxes[1][color]':"# ffffff",
                'boxes[1][outline_color]': "# 000000",
                'boxes[1][x]':0,
                'boxes[1][y]':330,
                'boxes[1][width]':200,
                'boxes[1][height]':200,
                'boxes[1][outline_width]': 1,
                'boxes[1][font_shadow]':0,
                'max_font_size':26,
                'font':font,
                'api_paste_format':'python'}
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])    
    
    
    
    '''start using key value pairs instead of dictionaries for (DATA) when order matters
    (' ',' ') vs (' ':' ')
    '''
    @commands.command(name='slapbutton', description='blue button karate chop meme', brief='can use =slapbutton "cause" "reaction"',
                      aliases=['chopbutton', 'bluebutton', 'SLAPBUTTON' ,'buttonslam', 'smashbutton'], pass_context=True)
    async def slap_button(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 119139145
        font = 'arial'
        
        # try-catch block, because of *args array. if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            cause = str(args[0]) # the argument is passed as message object, gotta cast
            reaction = str(args[1]) 
            print('slap button meme arguments: ' + cause + ' ' + reaction)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =slapbutton like so: =slapbutton "cause" "reaction"```')
            return
        
        DATA = (
                ('template_id',template_id),
                ('username',username),
                ('password',password),
                ('boxes[0][text]',cause),
                ('boxes[1][text]',reaction),
                ('max_font_size',40),
                ('font',font),
                )
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
        
    @commands.command(name='brain', description='expanding brain meme', brief='can use =brain "stage1" "stage2" "stage3" "stage4"',
                      aliases=['expand', 'brainexpand', 'expandbrain', 'IQ', '200IQ'], pass_context=True)
    async def expanding_brain(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 93895088
        font = 'arial'
        
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            stage1 = str(args[0]) # the argument is passed as message object, gotta cast
            stage2 = str(args[1]) # the argument is passed as message object, gotta cast
            stage3 = str(args[2]) # the argument is passed as message object, gotta cast
            stage4 = str(args[3]) # the argument is passed as message object, gotta cast
            print('expanding brain meme arguments: ' + stage1 + ' ' + stage2 + ' ' + stage3 + ' ' + stage4)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =brain like so: =brain "stage1" "stage2" "stage3" "stage4"```')
            return
        
        data1 = (
                ('template_id', template_id),
                ('username', username),
                ('password', password),
                ('boxes[0][text]', stage1),
                ('boxes[1][text]', stage2),
                ('boxes[2][text]', stage3),
                ('boxes[3][text]', stage4),
                ('font', font),
                ('boxes[0][color]', "# 000000"),
                ('boxes[0][outline_color]', "# 000000"),
                ('boxes[0][outline_width]', 1),
                ('boxes[0][font_shadow]', 0),
                ('boxes[1][color]',"# 000000"),
                ('boxes[1][outline_color]', "# 000000"),
                ('boxes[1][outline_width]', 1),
                ('boxes[1][font_shadow]',0),
                ('boxes[2][color]',"# 000000"),
                ('boxes[2][outline_color]', "# 000000"),
                ('boxes[2][outline_width]', 1),
                ('boxes[2][font_shadow]',0),             
                ('boxes[3][color]',"# 000000"),
                ('boxes[3][outline_color]', "# 000000"),
                ('boxes[3][outline_width]', 1),
                ('boxes[3][font_shadow]',0),
                ('max_font_size',60),
                ('font', font),
                )
        
        r = requests.post(url = URL, data = data1)
        text = r.json()
        await self.client.say(text['data']['url'])    
    
    @commands.command(name='pigeon', description='Pigeon meme', brief='can use =pigeon "boy" "butterfly" "is this a pidgeon?"',
                      aliases=['PIDGEON', 'pidgeon', 'PIGEON'], pass_context=True)
    async def pigeon(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 100777631
                        
        # try-catch block, because of *args array. if no argument given in discord after "=pidgeon",
        # it will go to the exception
        try:
            whom = str(args[0]) # the argument is passed as message object, gotta cast
            butterfly = str(args[1]) 
            # "is this a X" text section of the meme is the most likely to have multiple words,
            # so use join just in case user didn't put that part in strings
            # take all arguments after 2 to make the meme format user friendly,
            # combine into 1 string with spaces between each word
            is_this_a = " ".join(args[2:len(args)])
            
            print('Pigeon meme arguments: ' + whom + ' ' + butterfly + ' ' + is_this_a)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =pigeon like so: =pigeon "boy" "butterfly" "is this a pidgeon?"```')
            return
        
        DATA = (
                ('template_id',template_id),
                ('username',username),
                ('password',password),
                ('boxes[0][text]',whom),
                ('boxes[1][text]',butterfly),
                ('boxes[2][text]',is_this_a),
                ('max_font_size',100),
                ('api_paste_format','python'),
                )
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
        
    @commands.command(name='leftexit', description='Swerve left exit meme', brief='can use =leftexit "left" "right" "car"',
                      aliases=['carswerve', 'LEFTEXIT', 'swerve'], pass_context=True)
    async def left_exit(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 124822590
                        
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon", it will go to the exception
        try:
            left = str(args[0]) # the argument is passed as message object, gotta cast
            right = str(args[1])
            car = " ".join(args[2:len(args)])
            
            print('Left exit meme arguments ' + left + ' ' + right + ' ' + car)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =leftexit like so: =leftexit "left" "right" "car"```')
            return
        
        DATA = (
                ('template_id',template_id),
                ('username',username),
                ('password',password),
                ('boxes[0][text]',left),
                ('boxes[1][text]',right),
                ('boxes[2][text]',car),
                ('max_font_size',75),
                ('api_paste_format','python'),
                )
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
    

    @commands.command(name='boyfriend', description='boyfriend checking out girl meme',
                      brief='can use =boyfriend "new girl" "distracted boyfriend" "girlfriend"',
                      aliases=['BOYFRIEND', 'bf', 'BF', 'checkout', 'CHECKOUT'], pass_context=True)
    async def boyfriend(self, context, *args):
        # using IMGFLIP public API: https://api.imgflip.com/
        template_id = 112126428
                        
        # try-catch block, because of *args array.
        # if no argument given in discord after "=pidgeon" it will go to the exception
        try:
            new_girl = str(args[0]) # the argument is passed as message object, gotta cast
            distracted_boyfriend = str(args[1])
            girlfriend = " ".join(args[2:len(args)])
            
            print('Distracted boyfriend meme arguments ' + new_girl + ' ' + distracted_boyfriend + ' ' + girlfriend)
            
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =boyfriend like so: "new girl" "distracted boyfriend" "girlfriend"```')
            return
        
        DATA = (
                ('template_id',template_id),
                ('username',username),
                ('password',password),
                ('boxes[0][text]',new_girl),
                ('boxes[1][text]',distracted_boyfriend),
                ('boxes[2][text]',girlfriend),
                ('max_font_size',75),
                ('api_paste_format','python'),
                )
                
        r = requests.post(url = URL, data = DATA)
        text = r.json()
        await self.client.say(text['data']['url'])
        
def setup(client):
    client.add_cog(Memes(client))
