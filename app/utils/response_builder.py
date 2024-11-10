from app.mapping import MessageSchema
from app.services import Message, MessageBuilder

def build_response(message: str, data=None, code=200):
    '''
    Build a response with a message, data and a status code
    '''
    message_schema = MessageSchema()
    message_builder = MessageBuilder()
    message_builder.add_message(message)
    
    if data:
        message_builder.add_data(data)
    if code:
        message_builder.add_code(code)
    
    message_filled = message_builder.build()
    return message_schema.dump(message_filled), code