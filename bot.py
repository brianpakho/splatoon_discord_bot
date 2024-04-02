import os
from dotenv import load_dotenv
import discord
import datetime as dt
import requests

# load .env file
load_dotenv()

# access env variable
discord_token = os.getenv('DISCORD_TOKEN')

# enable default intents 
# intents are used to specify which events the bot will receive
intents = discord.Intents.default()
intents.message_content = True # allows the bot to receive events related to message content
client = discord.Client(intents=intents) # initializes a client instance with the specified intents

# let's us know when bot is logged, which client.run() does
@client.event # marks the on_ready() function as an event handler
async def on_ready(): # defines asynchronous function
    print(f'We have logged in as {client.user}') # print msg in terminal

# function for scraping json
def scrape_json_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            
            # Return the JSON data
            return json_data
        else:
            # Print an error message if the request was not successful
            print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Print any exceptions that occur during the process
        print(f"An error occurred: {e}")
        return None

# returns info when a user types stuff
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$mode'):

        json_data = scrape_json_data('https://splatoon3.ink/data/schedules.json')
        
        current_mode = json_data['data']['bankaraSchedules']['nodes'][0]['bankaraMatchSettings'][1]['vsRule']['name']
        next_mode = json_data['data']['bankaraSchedules']['nodes'][1]['bankaraMatchSettings'][1]['vsRule']['name']

        now = dt.datetime.utcnow()

        next_mode_start_time = dt.datetime.strptime(json_data['data']['bankaraSchedules']['nodes'][1]['startTime'], '%Y-%m-%dT%H:%M:%SZ')
        
        minutes_until_next_mode = int((next_mode_start_time - now).total_seconds() / 60)

        msg = 'The current mode is {}. The next mode is {} and starts in {} minutes.'.format(current_mode, next_mode, minutes_until_next_mode)

        await message.channel.send(msg) # i don't really know if await makes a difference but didn't want to change anything

# run bot
client.run(discord_token)