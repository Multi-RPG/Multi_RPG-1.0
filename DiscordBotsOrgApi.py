import dbl
import configparser
import aiohttp
import asyncio
import logging
import requests
from pathlib import Path


class DiscordBotsOrgAPI:
    """This class handles interactions with the discordbots.org API"""

    def __init__(self, client=None):
        # set up parser to config through our .ini file with our discordbots.org api token
        config = configparser.ConfigParser()
        api_token_path = Path("tokens/token_dbo_api.ini")  # use forward slash "/" for path directories
        # confirm the token is located in the above path, then setup DBL client and execute update_stats
        if api_token_path.is_file():
            config.read(api_token_path)
            # we now have the client's token
            token = config.get('DBL_API', 'token')
            self.token = token  # set this to your DBL token

            # only setup a loop to update server count to API when client is passed in constructor
            if client:
                self.client = client
                self.dblpy = dbl.Client(self.client, self.token, loop=client.loop)
                self.updating = client.loop.create_task(self.update_stats())
        # if the file doesn't exist with the api token, do not attempt to use discordbots.org API
        else:
            print("\nWarning: discordbots.org token not found at: ", api_token_path)
            print("client will continue to run without DiscordBotsOrgApi support.")

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""
        await self.client.wait_until_ready()
        while True:
            logger.info('Attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                logger.info('Posted server count ({})'.format(self.dblpy.guild_count()))
            except Exception as e:
                print("\nWarning: couldn't update server count for discordbots.org. Potential invalid DBO API token.")
                print("client will continue to run without DiscordBots.org API support.")
                logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            # wait 5 hours before updating server count again
            await asyncio.sleep(18000)

    def check_upvote(self, voter_id):
        headers = {'Authorization': self.token}
        api_url = 'https://discordbots.org/api/bots/486349031224639488/check?userId=' + voter_id
        r = requests.get(api_url, headers=headers)
        return r.json()['voted']


def setup(client):
    global logger
    logging.basicConfig(filename='logs/dbo_api_log.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info("Running Multi-RPG")
    logger = logging.getLogger('client')
    client.add_cog(DiscordBotsOrgAPI(client))