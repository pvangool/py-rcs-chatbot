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
import rcs_chatbot

chatbot = rcs_chatbot.Chatbot(
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
```

## Usage

### Chatbot Functions

### Suggestions Functions

Suggested Replies consist of a display text and a set of postback data.

Suggested Actions are grouped into seven different categories supporting a total of twelve different suggested actions:

* urlAction:
  * openUrl - Opens a web site or app via deep linking.
* dialerAction:
  * dialPhoneNumber - Calls a phone number via the user's dialer app.
  * dialEnrichedCall - Start an Enriched Call via the user’s dialer app.
  * dialVideoCall - Start a video call via the user’s dialer app.
* mapAction:
  * showLocation - Show location(s) on a map for given coordinates or search query.
  * requestLocationPush - Request for a one-time geo location push.
* calendarAction:
  * createCalendarEvent - Creates a new event on the user's calendar.
* composeAction:
  * composeTextMessage - Compose a draft text message.
  * composeRecordingMessage - Compose a draft message and start recording audio or video.
* deviceAction:
  * requestDeviceSpecifics - Request for a one-time share of device specifics (device model, operating system version, messaging client identifier and version, and remaining battery charge in minutes).
* settingsAction:
  * disableAnonymization - Ask the user to disable the anonymization setting.
  * enableDisplayedNotifications - Ask the user to enable sending displayed notifications.

Most actions allow fallback URLs in case a user does not have any app of the required type installed. Chatbot platforms can use the fallback URL to suggest an appropriate app to the user.

#### constructor()

Returns a new `Suggestions` instance.

#### addReply(displayText, postbackData)

On-the-wire example:

```json
{
  "reply": {
    "displayText": "Yes",
    "postback": {
      "data": "set_by_chatbot_reply_yes"
    }
  }
}
```

#### addUrlAction(displayText, postbackData, url)

On-the-wire example:

```json
{
  "action": {
    "urlAction": {
      "openUrl": {
        "url": "https://www.google.com"
      }
    },
    "displayText": "Open website or deep link",
    "postback": {
      "data": "set_by_chatbot_open_url"
    }
  }
}
```

#### addDialerAction(displayText, postbackData, dialType, phoneNumber, fallbackUrl, subject = None)

On-the-wire example:

```json
{
  "action": {
    "dialerAction": {
      "dialPhoneNumber": {
        "phoneNumber": "+1650253000"
      }
    },
    "displayText": "Call a phone number",
    "postback": {
      "data": "set_by_chatbot_dial_phone_number"
    }
  }
},
{
  "action": {
    "dialerAction": {
      "dialEnrichedCall": {
        "phoneNumber": "+1650253000",
        "subject": "The optional subject for the enriched call"
      }
    },
    "displayText": "Start enriched call",
    "postback": {
      "data": "set_by_chatbot_dial_enriched_call"
    }
  }
},
{
  "action": {
    "dialerAction": {
      "dialVideoCall": {
        "phoneNumber": "+1650253000"
      }
    },
    "displayText": "Start video call",
    "postback": {
      "data": "set_by_chatbot_dial_video_call"
    }
  }
}
```

#### addRequestLocationPushMapAction(displayText, postbackData)

On-the-wire example:

```json
{
  "action": {
    "mapAction": {
      "requestLocationPush": {}
    },
    "displayText": "Request a geo location",
    "postback": {
      "data": "set_by_chatbot_request_location_push"
    }
  }
}
```

#### addShowLocationMapAction(displayText, postbackData, latitude, longitude, label, query, fallbackUrl)

On-the-wire example:

```json
{
  "action": {
    "mapAction": {
      "showLocation": {
        "location": {
          "latitude": 37.4220041,
          "longitude": -122.0862515,
          "label": "Googleplex"
        },
        "fallbackUrl": "https://www.google.com/maps/@37.4219162,-122.078063,15z"
      }
    },
    "displayText": "Show location on a map",
    "postback": {
      "data": "set_by_chatbot_show_location"
    }
  }
},
{
  "action": {
    "mapAction": {
      "showLocation": {
        "location": {
          "query": "restaurants"
        },
        "fallbackUrl": "https://www.google.com/maps/search/restaurants"
      }
    },
    "displayText": "Search location(s) on map",
    "postback": {
      "data": "set_by_chatbot_search_locations"
    }
  }
}
```

#### addCalendarAction(displayText, postbackData, startTime, endTime, title, description, fallbackUrl)

On-the-wire example:

```json
{
  "action": {
    "calendarAction": {
      "createCalendarEvent": {
        "startTime": "2017-03-14T00:00:00Z",
        "endTime": "2017-03-14T23:59:59Z",
        "title": "Meeting",
        "description": "GSG review meeting"
      }
    },
    "displayText": "Schedule Meeting",
    "postback": {
      "data": "set_by_chatbot_create_calendar_event"
    }
  }
}
```

#### addTextComposeAction(displayText, postbackData, phoneNumber, text)

On-the-wire example:

```json
{
  "action": {
    "composeAction": {
      "composeTextMessage": {
        "phoneNumber": "+1650253000",
        "text": "Draft to go into the send message text field."
      }
    },
    "displayText": "Draft a text message",
    "postback": {
      "data": "set_by_chatbot_compose_text_message"
    }
  }
}
```

#### addRecordingComposeAction(displayText, postbackData, phoneNumber, type)

On-the-wire example:

```json
{
  "action": {
    "composeAction": {
      "composeRecordingMessage": {
        "phoneNumber": "+1650253000",
        "type": "VIDEO"
      }
    },
    "displayText": "Record audio or video",
    "postback": {
      "data": "set_by_chatbot_compose_recording_message"
    }
  }
}
```

#### addDeviceAction(displayText, postbackData)

On-the-wire example:

```json
{
  "action": {
    "deviceAction": {
      "requestDeviceSpecifics": {}
    },
    "displayText": "Request device specifics",
    "postback": {
      "data": "set_by_chatbot_request_device_specifics"
    }
  }
}
```

#### addSettingsAction(displayText, postbackData, settingsType)

On-the-wire example:

```json
{
  "action": {
    "settingsAction": {
      "disableAnonymization": {}
    },
    "displayText": "Share your phone number",
    "postback": {
      "data": "set_by_chatbot_disable_anonymization"
    }
  }
},
{
  "action": {
    "settingsAction": {
      "enableDisplayedNotifications": {}
    },
    "displayText": "Send read receipts",
    "postback": {
      "data": "set_by_chatbot_enable_displayed_notifications"
    }
  }
}
```

### Events

A different event is triggered for each type of event an RCS chatbot can receive. Below are all
the possible events with an example of the payload they provide.

#### EventType.MESSAGE

Triggered when a 'message' event is sent to the bot.

* `event` - Object: An object containing the 'message' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGE)
def messageHandler(event):
  print("messageHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "Xs8CI3tdf",
    "textMessage": "hello world",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "message"
}
```

#### EventType.ISTYPING

Triggered when an 'isTyping' event is sent to the bot.

* `event` - Object: An object containing the 'isTyping' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.ISTYPING)
def isTypingHandler(event):
  print("isTypingHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "Xs8CI3tdf",
    "isTyping": "active",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "isTyping"
}
```

#### EventType.MESSAGESTATUS

Triggered when a 'messageStatus' event is sent to the bot.

* `event` - Object: An object containing the 'messageStatus' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.MESSAGESTATUS)
def messageStatusHandler(event):
  print("messageStatusHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "status": "displayed",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "messageStatus"
}
```

#### EventType.FILESTATUS

Triggered when a 'fileStatus' event is sent to the bot.

* `event` - Object: An object containing the 'fileStatus' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.FILESTATUS)
def fileStatusHandler(event):
  print("fileStatusHandler")
```

Sample payload:

```json
{
  "file": {
    "fileId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "fileUrl": "http://www.example.com/files/f.jpg",
    "fileSize": 123456,
    "status": "ready",
    "validity": "2017-10-03T22:31:00.597Z"
  },
  "event": "fileStatus"
}
```

#### EventType.RESPONSE

Triggered when a 'response' event is sent to the bot.

* `event` - Object: An object containing the 'response' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.RESPONSE)
def responseHandler(event):
  print("responseHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "suggestedResponse": {
      "response": {
        "action": {
          "displayText": "Visit Website",
          "postback": {
            "data": "set_by_chatbot_reply_yes"
          }
        }
      }
    },
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "response"
}
```

#### EventType.ALIAS

Triggered when a 'alias' event is sent to the bot.

* `event` - Object: An object containing the 'alias' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.ALIAS)
def aliasHandler(event):
  print("aliasHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567",
    "chatId": "93JF93SEIJFE"
  },
  "event": "alias"
}
```

#### EventType.NEWUSER

Triggered when a 'newUser' event is sent to the bot.

* `event` - Object: An object containing the 'newUser' event payload.

Example usage:

```python
@chatbot.registerEventHandler(rcs_chatbot.EventType.NEWUSER)
def newUserHandler(event):
  print("newUserHandler")
```

Sample payload:

```json
{
  "RCSMessage": {
    "msgId": "MzJmajlmamVzZGZ8bmk5MHNlbmRmZTAz",
    "suggestedResponse": {
      "response": {
        "reply": {
          "displayText": "Start Chat",
          "postback": {
            "data": "new_bot_user_initiation"
          }
        }
      }
    },
    "timestamp": "2017-09-26T01:33:20.315Z"
  },
  "messageContact": {
    "userContact": "+14251234567"
  },
  "event": "newUser"
}
```

