# rcs_chatbot

A Python SDK for [RCS MaaP chatbots](https://www.gsma.com/futurenetworks/wp-content/uploads/2017/11/FNW.11_v1.0.pdf).

## Installation

```bash
pip install rcs_chatbot
```

## Example

See more examples in [the example folder](https://github.com/pvangool/py-rcs-chatbot/tree/master/example).

```python
import flask
import maap

chatbot = maap.Chatbot(
  "API_URL",
  "BOT_ID",
  "TOKEN"
)

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def event():
  try:
    chatbot.processEvent(flask.request.get_json())
    return "ok", 200
  except:
    pass

@chatbot.registerEventHandler(maap.EventType.MESSAGE)
def messageHandler(event):
  contact = maap.MessageContact("+18055551234", None)

  suggestions = maap.Suggestions()
  suggestions.addReply("reply", "reply")
  suggestions.addUrlAction("url", "url", "http://example.com")

  chatbot.sendMessage(contact, "Howdy", suggestions)

if __name__ == '__main__':
    app.run(port=5000, debug=False)
```

