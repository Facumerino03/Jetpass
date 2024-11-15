from dataclasses import dataclass

@dataclass
class Message():
    '''
    Class that represents a message
    '''
    message: str = ''
    code: int = None
    data: dict = None

@dataclass(init=False)
class MessageBuilder():
    '''
    Class that builds a message
    '''
    message: str = ''
    code: int = None
    data: dict = None

    def build(self) -> Message:
        '''
        Builds the message
        
        return:
            Message
        '''
        return Message(message=self.message, code=self.code, data=self.data)
    
    def add_message(self, message: str) -> 'MessageBuilder':
        '''
        Adds a message to the builder
        
        param:
            message: str
        return:
            MessageBuilder
        '''
        self.message = message
        return self
    
    def add_code(self, code: int) -> 'MessageBuilder':
        '''
        Adds a code to the builder
        
        param:
            code: int
        return:
            MessageBuilder
        '''
        self.code = code
        return self
    
    def add_data(self, data: dict) -> 'MessageBuilder':
        '''
        Adds data to the builder
        
        param:
            data: dict
        return:
            MessageBuilder
        '''
        self.data = data
        return self