import flask
import logging
import rcs_chatbot

chatbot = rcs_chatbot.Chatbot(
  "API_URL",
  "BOT_ID",
  "TOKEN",
  None,
  logging.DEBUG
)

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def event():
  try:
    chatbot.processEvent(flask.request.get_json())
    return "ok", 200
  except maap.RequestFailed as ex:
    print("Request failed: " + str(ex))
    return "ok", 200

@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGE)
def messageHandler(event):
  userContact = None
  chatId = None

  if "userContact" in event["messageContact"]:
    userContact = event["messageContact"]["userContact"]
  if "chatId" in event["messageContact"]:
    chatId = event["messageContact"]["chatId"]

  contact = rcs_chatbot.MessageContact(userContact, chatId)

  suggestions = rcs_chatbot.Suggestions()
  suggestions.addReply("reply", "reply")
  suggestions.addUrlAction("url", "url", "http://example.com")

  chatbot.sendMessage(
    contact,
    "You wrote: " + event["RCSMessage"]["textMessage"],
    suggestions
  )

@chatbot.registerEventHandler(rcs_chatbot.EventType.ISTYPING)
def isTypingHandler(event):
  print("isTypingHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGESTATUS)
def messageStatusHandler(event):
  print("messageStatusHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.FILESTATUS)
def fileStatusHandler(event):
  print("fileStatusHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.RESPONSE)
def responseHandler(event):
  print("responseHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.ALIAS)
def aliasHandler(event):
  print("aliasHandler")

@chatbot.registerEventHandler(rcs_chatbot.EventType.NEWUSER)
def newUserHandler(event):
  print("newUserHandler")

if __name__ == '__main__':
    app.run(port=5000, debug=False)
