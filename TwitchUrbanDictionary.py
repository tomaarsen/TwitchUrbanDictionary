from TwitchWebsocket import TwitchWebsocket
import json, requests, random, logging, time

from itertools import accumulate
from enum import Enum, auto
from Log import Log
Log(__file__)

from Settings import Settings
from Database import Database

class ResultCode(Enum):
    SUCCESS = auto()
    ERROR = auto()

class CommandType(Enum):
    DEFINITION = 0
    EXAMPLE = 1

class TwitchUrbanDictionary:
    def __init__(self):
        # Initialize variables
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.max_chars = None
        self.cooldown = None

        self.last_message_t = 0

        # Fill uninitialized variables using settings.txt
        self.update_settings()

        # Set up Database
        self.db = Database(self.chan)

    def start(self):
        # Instantiate TwitchWebsocket instance with correct params
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=None,
                                  live=True)
        
        # Start the websocket connection
        self.ws.start_bot()
        
    def update_settings(self):
        # Fill previously initialised variables with data from the settings.txt file
        self.host, self.port, self.chan, self.nick, self.auth, self.max_chars, self.cooldown = Settings().get_settings()

    def message_handler(self, m):
        try:
            if m.type == "366":
                logging.info(f"Successfully joined channel: #{m.channel}")
            
            elif m.type == "PRIVMSG":

                    # Listen for command. Send along the correct CommandType so handle_command knows what information it should grab
                    if m.message.startswith("!urban"):
                        self.handle_command(m, CommandType.DEFINITION)

                    elif m.message.startswith("!example"):
                        self.handle_command(m, CommandType.EXAMPLE)

            elif m.type == "WHISPER":
                # Allow people to whisper the bot to disable or enable whispers.
                if m.message == "!nopm":
                    logging.debug(f"Adding {m.user} to Do Not Whisper.")
                    self.db.add_whisper_ignore(m.user)
                    self.ws.send_whisper(m.user, "You will no longer be sent whispers. Type !yespm to reenable. ")

                elif m.message == "!yespm":
                    logging.debug(f"Removing {m.user} from Do Not Whisper.")
                    self.db.remove_whisper_ignore(m.user)
                    self.ws.send_whisper(m.user, "You will again be sent whispers. Type !nopm to disable again. ")

        except Exception as e:
            logging.exception(e)

    def check_if_streamer(self, m):
        # True if the user is the streamer
        return m.user == m.channel

    def handle_command(self, m, command_type):
        # Check for cooldown
        if self.last_message_t + self.cooldown < time.time() or self.check_if_streamer(m):

            split_message = m.message.split()

            # If a term(s) is/are passed
            if len(split_message) > 1:
                term = " ".join(split_message[1:])

                # Get the output as well as the return code
                out, code = self.fetch_urban(term, command_type)
                
                # Send messages to Twitch chat
                # Because in all cases, error or success, 
                # we want to output `out` to chat, we ignore `code` for now.
                self.ws.send_message(out)
                logging.info(f"{term}'s {['definition', 'example'][command_type.value]} -> {out}")

                if code == ResultCode.SUCCESS:
                    self.last_message_t = time.time()
            else:
                self.ws.send_message(f"Please add term(s) like: {['!urban', '!example'][command_type.value]} bot")
        else:
            # Let the user know the cooldown check failed
            if not self.db.check_whisper_ignore(m.user):
                self.ws.send_whisper(m.user, f"Cooldown hit: {self.last_message_t + self.cooldown - time.time():0.2f} out of {self.cooldown:.0f}s remaining. !nopm to stop these cooldown pm's.")
            logging.info(f"Cooldown hit with {self.last_message_t + self.cooldown - time.time():0.2f}s remaining")

    def fetch_urban(self, term, command_type):
        # Construct URL and get result
        url = f"http://api.urbandictionary.com/v0/define?term={term}"
        data = requests.get(url).json()
        
        if "list" not in data:
            print(data)
            return "Unknown error encountered, likely related to a rate limit.", ResultCode.ERROR

        # Get the list of definitions
        definition_list = data["list"]

        # If there are no definitions
        if len(definition_list) == 0:
            return "No definition exists for that term.", ResultCode.ERROR

        # Get the dict of the "best" definition
        definition_dict = data["list"][0]

        # Get the actual definition/example using the value of the CommandType enum
        definition = definition_dict[["definition", "example"][command_type.value]]
        word = definition_dict["word"].capitalize()

        # Clean the definition by removing hyperlink notations, (eg the brackets)
        definition = self.clean(definition)
        # Truncase the definition
        definition = self.truncate(definition)

        # If we are dealing with a definition, we include the term the definition is for
        if command_type == CommandType.DEFINITION:
            definition = f"{word}: {definition}"

        # Return our modified definition
        return definition, ResultCode.SUCCESS
    
    def clean(self, definition):
        # Creates a dict from the ord of all "to delete" characters, mapped to None. 
        # Also creates a dict from the ord of all "to replace with space", mapped to " ".
        # The translation table made up of these dicts added together will return a string with all characters properly changed.
        return definition.translate({**{ord(v): " " for v in "\r\n\t"}, **{ord(v): None for v in "[]"}})

    def truncate(self, definition):
        # Variable to potentially add a suffix to indicate that the definition or example has been truncated. True by default.
        is_truncated = True

        # Strip the definition into seperate sentences. Add a dot if it seems necessary
        sentences = [sentence.strip() + ("." if sentence.strip()[-1] != '"' else "") for sentence in definition.split(".") if len(sentence.strip()) > 0]

        # Get a generator of the length of each sentence
        sentence_length_gen = (len(sentence) for sentence in sentences)

        # Generate the sentence count. We can use the index from enumerate for this
        for count, length in enumerate(accumulate(sentence_length_gen)):
            # There must always be at least 1 sentence
            # And if the accumulated sentence length so far is over 150 characters, break.
            if count > 0 and length > self.max_chars:
                break
        # This else is only called if the break is not reached
        else:
            # Increment the count by 1, which will cause all sentences to be returned.
            count += 1
            is_truncated = False

        # Return a string of the first `count` sentences
        return " ".join(sentences[:count]) + (" [...]" if is_truncated else "")

if __name__ == "__main__":
    TwitchUrbanDictionary().start()
