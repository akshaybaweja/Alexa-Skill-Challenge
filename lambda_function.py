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
            'title': title,
            'content': output
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
    card_title = "Welcome to Element Trivia"
    session_attributes = {}
    should_end_session = False
    speech_output = "Welcome to Element Trivia. You can ask me about various properties of elements such as"\
        " atomic mass, atomic radius, electronic configuration, etc, "\
        "Just say get property-name of element-name."
    reprompt_text=speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_element_details(givenElement):
    with open('data.json') as data:
        elements = json.load(data)
        for element in elements:
            name = element["name"]
            if name.lower() == givenElement.lower():
                return element

def get_name_from_symbol(symbol):
    with open('data.json') as data:
        elements = json.load(data)
        for element in elements:
            sym = element["symbol"]
            if sym.lower() == symbol.lower():
                return element["name"]

def process_electronic_config(electronic_config):
    if '[' in electronic_config:
        text = electronic_config.split(']')
        symbol = text[0].split('[')
        symbol = "".join(symbol)
        name = get_name_from_symbol(symbol)
        return name+text[1]
    else:
        return electronic_config

def get_element_property(element, property):
    if property == "year":
        return element["yearDiscovered"]
    elif property == "group":
        return element["groupBlock"]
    elif property == "density":
        return str(element["density"])+"gram per centimeter cube"
    elif property == "boiling point":
        return str(element["boilingPoint"])+" degree celcius per molal"
    elif property == "melting point":
        return str(element["meltingPoint"])+" degree celcius per molal"
    elif property == "bonding type":
        return element["bondingType"]
    elif property == "standard state":
        return element["standardState"]
    elif property == "oxidation states":
        return element["oxidationStates"]
    elif property == "electron affinity":
        return element["electronAffinity"]
    elif property == "ionization energy":
        return str(element["ionizationEnergy"])+" electron volt"
    elif property == "van der waals radius":
        return str(element["vanDelWaalsRadius"])+" pico meter"
    elif property == "ion radius":
        return str(element["ionRadius"])+" pico meter"
    elif property == "atomic radius":
        return str(element["atomicRadius"])+" pico meter"
    elif property == "electronegativity":
        return element["electronegativity"]
    elif property == "electronic configuration":
        return process_electronic_config(element["electronicConfiguration"])
    elif property == "atomic mass":
        return str(element["atomicMass"])+" gram per mole"
    elif property == "name":
        return element["name"]
    elif property == "symbol":
        return element["symbol"]
    elif property == "atomic number":
        return element["atomicNumber"]
    else:
        return None

def get_property(intent, session):
    card_title = "Element Property"
    session_attributes = {}
    should_end_session = True
    speech_output=""
    if "element_name" in intent['slots']:
        givenElement = intent['slots']['element_name']
        if(givenElement.has_key('value')):
            givenElement = givenElement['value']
            data = get_element_details(givenElement)
            if data != None:
                if "Property" in intent['slots']:
                    property_value = intent['slots']['Property']['value']
                    data_property = get_element_property(data,property_value.lower())
                    speech_output = "The "+property_value+" of "+givenElement+" is "+str(data_property)
                    card_title = "Element Trivia - Property"
                else:
                    speech_output = "No property found"
           else:
               speech_output = "Element data not found"
        else:
            speech_output = "Please specify an element name and try again, "\
                "Say help for more info."
    else:
        speech_output = "No Element Name Found"

    reprompt_text=speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Thank you for using Element Trivia"
    speech_output = "Thank you for using Element Trivia."
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def get_help():
    card_title = "Help"
    speech_output = "You can ask me about various properties of elements such "\
        "as atomic mass, atomic radius, electronic configuration, symbol, etc, "\
        "Just say get property-name of element-name."
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, speech_output, should_end_session))

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
    elif intent_name == "AMAZON.HelpIntent":
        return get_help(intent,session)
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
