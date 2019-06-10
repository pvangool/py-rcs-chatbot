import json
import logging
import requests
from enum import Enum

class EventType(Enum):
  MESSAGE = "message"
  ISTYPING = "isTyping"
  MESSAGESTATUS = "messageStatus"
  FILESTATUS = "fileStatus"
  RESPONSE = "response"
  ALIAS = "alias"
  NEWUSER = "newUser"

class DialType(Enum):
  PHONE = "dialPhoneNumber"
  ENRICHED = "dialEnrichedCall"
  VIDEO = "dialVideoCall"

class SettingsType(Enum):
  DISABLEANONYMIZATION = "disableAnonymization"
  ENABLEDISPLAYEDNOTIFICATIONS = "enableDisplayedNotifications"

class MessageContact:
  def __init__(self, userContact, chatId):
    self.userContact = userContact
    self.chatId = chatId

  def generate(self):
    return {
      "userContact": self.userContact,
      "chatId": self.chatId
    }

class Suggestions:
  def __init__(self):
    self.suggestions = []

  def addReply(self, displayText, postbackData):
    suggestion = {
      "reply": {
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addUrlAction(self, displayText, postbackData, url):
    suggestion = {
      "action": {
        "urlAction": {
          "openUrl": {
            "url": url
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addDialerAction(self, displayText, postbackData, dialType, phoneNumber, fallbackUrl, subject):
    suggestion = {
      "action": {
        "dialerAction": {},
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    if dialType is DialType.PHONE:
        suggestion["dialerAction"] = {
          "dialPhoneNumber": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl
          }
        }
    elif dialType is DialType.ENRICHED:
        suggestion["dialerAction"] = {
          "dialEnrichedCall": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl,
            "subject": subject,
          }
        }
    elif dialType is DialType.VIDEO:
        suggestion["dialerAction"] = {
          "dialVideoNumber": {
            "phoneNumber": phoneNumber,
            "fallbackUrl": fallbackUrl
          }
        }
    else:
      raise TypeError("Unknown dialType")

    self.suggestions.append(suggestion)

  def addRequestLocationPushMapAction(self, displayText, postbackData):
    suggestion = {
      "action": {
        "mapAction": {
          "requestLocationPush": {}
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addShowLocationMapAction(self, displayText, postbackData, latitude, longitude, label, query, fallbackUrl):
    suggestion = {
      "action": {
        "mapAction": {
          "showLocation": {
            "location": {
              "latitude": latitude,
              "longitude": longitude,
              "label": label,
              "query": query
            },
            "fallbackUrl": fallbackUrl
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addCalendarAction(self, displayText, postbackData, startTime, endTime, title, description, fallbackUrl):
    suggestion = {
      "action": {
        "calendarAction": {
          "createCalendarEvent": {
            "startTime": startTime,
            "endTime": endTime,
            "title": title,
            "description": description,
            "fallbackUrl": fallbackUrl
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addTextComposeAction(self, displayText, postbackData, phoneNumber, text):
    suggestion = {
      "action": {
        "composeAction": {
          "composeTextMessage": {
            "phoneNumber": phoneNumber,
            "text": text
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addRecordingComposeAction(self, displayText, postbackData, phoneNumber, type):
    suggestion = {
      "action": {
        "composeAction": {
          "composeRecordingMessage": {
            "phoneNumber": phoneNumber,
            "type": type
          }
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addDeviceAction(self, displayText, postbackData):
    suggestion = {
      "action": {
        "deviceAction": {
          "requestDeviceSpecifics": {}
        },
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    self.suggestions.append(suggestion)

  def addSettingsAction(self, displayText, postbackData, settingsType):
    suggestion = {
      "action": {
        "settingsAction": {},
        "displayText": displayText,
        "postback": {
          "data": postbackData
        }
      }
    }

    if settingsType is SettingsType.DISABLEANONYMIZATION:
        suggestion["settingsAction"] = {
          "disableAnonymization": {}
        }
    elif settingsType is SettingsType.ENABLEDISPLAYEDNOTIFICATION:
        suggestion["settingsAction"] = {
          "enableDisplayedNotifications": {}
        }
    else:
      raise TypeError("Unknown settingsType")

    self.suggestions.append(suggestion)

  def generate(self):
    return self.suggestions

class Chatbot:
  eventHandlers = {}

  def __init__(self, apiUrl, botId, accessToken, logger=None, logger_level=None):
    self.apiUrl = apiUrl
    self.botId = botId
    self.accessToken = accessToken

    if logger is not None:
      self.logger = logger
    else:
      logging.basicConfig()
      self.logger = logging.getLogger(__name__)
      self.logger.setLevel(logging.INFO)

    if logger_level is not None:
      self.logger.setLevel(logger_level)

  def registerEventHandler(self, eventType):
    def decorator(function):
      if eventType not in EventType:
        self.logger.warn("{} is not event type".format(eventType))
        return function

      self.logger.info("{} event handler has been added".format(eventType))
      self.eventHandlers[eventType] = function
      return function

    return decorator

  def processEvent(self, body):
    self.logger.debug(body)

    if body is None:
      self.logger.warn("Empty POST body")
      raise Exception("Empty POST body")
    if "event" not in body:
      self.logger.warn("Invalid POST body")
      raise Exception("Invalid POST body")

    event = body["event"]
    eventType = None
    if ("message" == event):
      eventType = EventType.MESSAGE
    elif ("isTyping" == event):
      eventType = EventType.ISTYPING
    elif ("messageStatus" == event):
      eventType = EventType.MESSAGESTATUS
    elif ("fileStatus" == event):
      eventType = EventType.FILESTATUS
    elif ("response" == event):
      eventType = EventType.RESPONSE
    elif ("alias" == event):
      eventType = EventType.ALIAS
    elif ("newUser" == event):
      eventType = EventType.NEWUSER
    else:
      self.logger.warn("Invalid event type: {}".format(event))
      raise Exception("Invalid event type")

    if eventType in self.eventHandlers:
      self.eventHandlers[eventType](body)
    else:
      self.logger.debug("No event handler register for event type: {}".format(eventType))

  def sendMessage(self, messageContact, text, suggestions):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " +  self.accessToken
    }

    message = {
      "RCSMessage": {
        "textMessage": text
      },
      "messageContact": messageContact.generate()
    }

    if suggestions != None:
      message["RCSMessage"]["suggestedChipList"] = {
        "suggestions": suggestions.generate()
      }

    r = requests.post(self.apiUrl + "/" + self.botId + "/messages",
        headers=headers, data=json.dumps(message))

    if r.status_code != 202:
        raise("Unexpected status code")

