Co-authors: 
- Peter Roescher: https://github.com/peterroescher
- Judith Kaptein: https://github.com/judithrk

## How to use Poppy
1. Make sure you have python 3.4 installed (might work with later versions)
2. Make sure you've installed all the required libraries listed in requirements.txt. Install these using `pip3 install -r requirements.txt`
3. Create the NLP config using `cp nlp.config.example nlp.config`
4. Fill in the NLP Api key you can acquire via Wit.AI
5. Create the Weather config file using `cp weather.config.example weather.config`
6. run conversation_start.py using `python3 conversation_start.py`

## How Poppy works

### Basic structure
Poppy uses conversations and commands to communicate with the user.
When you first start Poppy Poppy will ask you a couple of questions to save some basic user information
After Poppy is ready for use it will listen for your command. Currently this is "Hello Poppy"  
After which you can enter a command. At the time there are 2 commands.

"What day is it today?"  
"Whats the weather in [location]"


### Locale
Currently Poppy fully supports two languages and one in a basic stage
Dutch (Full support)
English (Full support)
Turkish (Basic support)

Setting the locale is a 3 step process. Poppy has a language setting, the NLP module has its own language setting and the TTS has its language setting.
All these aspects need to have their translations and settings set to the language in order to work.

### Commands
The commands are executed whenever an intent is linked with this command. A command can be a simple task or it can spark a conversation. 
Commands are defined in `CommandCentre/commands.py` and need to implement the `Command` class. 
The `execute()` method is called whenever the `CommandCentre` gets an intent that is linked with this command.  
Implement the `RequiresResponse` to pass the response the `IntentHandler` generated along to the command.  
It can then be accessed via the `self.response` property. 
Commands are free to do whatever and can be used to start other conversations, generate data, speak to the user or whatever you desire.  

### Conversations
Conversations are basic question-answer structures that are developed to get information  
from the user and lay information back to the user depending on the answers they provided.
A conversation therefor requires information and uses questions to get this information. Required information can be defined in the `self.required_properties` property.
A required property can be coupled to a question, there's an example below:

A conversation must extend the `Conversation` class. 
The `start` method is used to get the first question from the conversation. It returns a `Question` class or a `EndOfConversation` class

#### Required properties
```python
required_properties = {
    'name': AskForName
}
```
Poppy will use the AskForName class to get the name property filled.

#### Intents and contextual responses
Poppy will ask the question and listen to the users response. It will try and get an Intent back from the Natural Language Processing engine. 
Once it got the intent back it will try and put it back in the conversation to get a contextual response.  
To interpret the intent in the conversation you'll need to create a method with the intent name and prefix it using `intent_`
example:
```python
def intent_give_name(self, response):
    return QuestionContextBuilder.new(
        type=Confirmation, 
        current_question=AskForName, 
        next_question=self.next_question(), 
        intermediate_text=_("From now on, ill address you as %s") % response.name
    )
```
Where `give_name` is the intent name.  
This method will then return a contextual response. In the example above it will ask the user to confirm his or her name and once  
the answer has been confirmed it will use the intermediate_text to confirm the answer back to the user. The `current_question` parameter can be used to repeat the question or do additional logic.
The `next_question` property will be used to start the next question in the conversation.   
A contextual response can be one of many things but as of now there are only a few namely:
`Confirm`
`Success`
`AskForRepeat`

`Confirm` will ask the user to confirm an answer provided, this is handy when personal information needs to be correct.  
`Success` will just continue the conversation  
`AskForRepeat` will prompt the question to get asked again  
  
All these contextual responses are handled and managed by the `ConversationHandler` class and the contextual responses are created by the conversation class using the `QuestionContextBuilder`
  
### Questions
A question is used to fetch information from the user. It is a very simple class that implements the `Question` class.
The `ask_question` method is called and it returns a string. 

The `FreeAnswer` class may also be extended when the question doesn't require an intent but the answer may just be the full answer given by the user.
Keep in mind, an answer with an intent is always preferred.


### TTS
The TTS module is very simple to use. It uses Google's Text To Speech SDK but can be changed because the TTS module uses a strategy pattern.  
To use the TTS module you'll import tts from the TTS package and use the `say()` method with the string as first and only parameter
Here's an example
```python
from TTS import tts
tts.say("Hello world")
```

Above example will say Hello world.

The TTS creates an mp3 file and stores it in `/resources/audio/tts_result.mp3` it'll overwrite everytime you use it. 

To set the language you need to change the `USE_TTS_LANGUAGE` in `config.py`

### NLP
The NLP module handles the communication with the Natural Language Processing engine. It too uses a strategy pattern. And can be replaced. 
Though the NLP is a vital part to get input it isn't used that much as a module since the data it provides is useless without context.
The `IntentHandler` is the class that provides this context. It will listen for microphone input and store it in `/resources/audio/microphone-results.wav`
It will upload the audio using the NLP package and get a formatted response back. The WitAIResponse class is responsible for doing this.

