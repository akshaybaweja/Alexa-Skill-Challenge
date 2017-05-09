from __future__ import print_function
import json
# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    card_title = "Welcome to Elements"
    session_attributes = {}
    should_end_session = False
    speech_output = "Welcome to Elements"
    reprompt_text=speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_element_details(givenElement):
    with open('data.json') as data:
        elements = json.load(data)
        for element in elements:
            name = element["name"]
            #print("UPR WALA NAAM: "+name)
            if name.lower() == givenElement.lower():
                return element
            else:
                return None

def get_element_property(element, property):
    if property == "year":
        return element["yearDiscovered"]
    elif property == "group":
        return element["groupBlock"]
    elif property == "density":
        return element["density"]
    elif property == "boiling point":
        return element["boilingPoint"]
    elif property == "melting point":
        return element["meltingPoint"]
    elif property == "bonding type":
        return element["bondingType"]
    elif property == "standard state":
        return element["standardState"]
    elif property == "oxidation states":
        return element["oxidationStates"]
    elif property == "electron affinity":
        return element["electronAffinity"]
    elif property == "ionization energy":
        return element["ionizationEnergy"]
    elif property == "van der waals radius":
        return element["vanDelWaalsRadius"]
    elif property == "ion radius":
        return element["ionRadius"]
    elif property == "atomic radius":
        return element["atomicRadius"]
    elif property == "electronegativity":
        return element["electronegativity"]
    elif property == "electronic configuration":
        return element["electronicConfiguration"]
    elif property == "atomic mass":
        return element["atomicMass"]
    elif property == "name":
        return element["name"]
    elif property == "symbol":
        return element["symbol"]
    elif property == "atomic number":
        return element["atomicNumber"]
    else:
        return None

def get_property(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    speech_output=""
    if "element_name" in intent['slots']:
        givenElement = intent['slots']['element_name']['value']
        print("ELEMENT : "+givenElement)
        data = get_element_details(givenElement)
        if data != None:
            if "Property" in intent['slots']:
                property_value = intent['slots']['Property']['value']
                print("PROPERTY : "+property_value)
                data_property = get_element_property(data,property_value.lower())
                speech_output = "The "+property_value+" of "+givenElement+" is "+str(data_property)
            else:
                speech_output = "No property found"
        else:
            speech_output = "Element data not found"
    else:
        speech_output = "No Element Name Found"

    reprompt_text=speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Elemento."
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetInfo":
        return get_property(intent, session)
    elif intent_name == "getAll":
        return get_all(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(intent,session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])