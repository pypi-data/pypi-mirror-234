from typing import Union
from plac import Interpreter
from chat_companion.chat_commands import (
                                      generate_response,
                                      get_key,
                                      set_default_model,
                                      get_default_model,
                                      talk,
                                      summarize,
                                      review,
                                      resummarize,
                                      translate,
                                      proof_read,
                                    )
from toolbox.companion_logger import logger



prompt_doc = 'The prompt you input'
temperature_doc = '1 for more random'
engine_doc = f'The engine you use if none the default is {get_default_model()}'
max_token_doc = 'max tokens used in response'
n_doc = 'The number of responses generated'
filename_doc = 'The file name to output review for example scratch.py'
bulk_doc = 'If set will return all responses as a list'
profile_doc = 'The profile to load in from contexts'

class Companion(object):
    """
    Companion is a command line interface for chat gpt,
    with extra features like translate and proof reading,
    """    
    
    commands = [
                'generate_response',
                'set_default_model',
                'show_default_model',
                'show_key',
                'talk', 
                'summarize', 
                'review',
                'resummarize',
                'translate',
                'proof_read',
                ]
    
    def show_key(self):
        print(get_key())
    
    def show_default_model(self):
        print(get_default_model())
    
    def set_default_model(self,
                          value:('The new default value','positional')
                          ):
        '''
        Sets the default model used.
        '''
        return set_default_model(value)
    
    def proof_read(self,
                   prompt:(prompt_doc,'positional'),
                   temperature: (temperature_doc,'option','t') = 0.5,
                   )->str:
        """
        proof reads a prompt
        """        
        return proof_read(prompt,temperature)
    
    def translate(self,
                  prompt:(prompt_doc,'positional'),
                  language:(f'The language you want to translate to','option','l')='english',
                  temperature: (temperature_doc,'option','t') = 0.5,
                  )->str:
        return translate(prompt,temperature,language)
    
    def generate_response(self,
                          prompt: (prompt_doc,'positional'),
                          temperature: (temperature_doc,'option','t') = 0.5,
                          engine: (engine_doc,'option','e',)=None,
                          max_tokens:(max_token_doc,'option','max')=1024,
                          n: (n_doc,'option')=1,
                          filename:(filename_doc,'option','f')='',
                          bulk:(bulk_doc,'flag','b')=False,
            )-> Union[str,list[str]]:
        '''
        This Generates a response, it doesn't store it context.db.
        '''
        return generate_response(prompt,temperature,engine,max_tokens,n,filename,bulk)
    
    def summarize(self, 
                  prompt: (prompt_doc,'positional'),
                  temperature: (temperature_doc,'option','t') = 0.5,
                  engine: (engine_doc,'option','e',)=None,
                  n: (n_doc,'option')=1,
                  t: ('The type of thing you are summarizing, e.g. a conversation','option','type') = '',
                  ) -> str:
        '''
        Summarizes input
        '''
        return summarize(prompt=prompt,engine=engine,
                         n=n,temperature=temperature,type_=t)
        
    def talk(self,
             prompt: (prompt_doc,'positional') = '',
             temperature: (temperature_doc,'option','t') = 0.5,
             engine: (engine_doc,'option','e',)=None,
             max_tokens:(max_token_doc,'option','max')=1024,
             n: (n_doc,'option')=1,
             filename:(filename_doc,'option','f')='',
             profile:(profile_doc,'option','p')='default',
             in_file:('File that is input to the prompt use {in_file} to reference it','option','In')='',
             **kwargs,
             )->str:
        '''
        This allows you save your companion's responses, they are stored in context.db.
        '''
        return talk(prompt,engine=engine,max_tokens=max_tokens,n=n,
                    temperature=temperature,filename=filename,
                    profile=profile,in_file=in_file,**kwargs)
   
    def review(self,
               filename:(filename_doc,'option','f')='',
               profile:(profile_doc,'option','p')='default',
               summary:('show summary','flag','s')=False,
               )->str:
        '''
        To review previous questions and responses,
        use the `review` subcommand. This will bring up a list of previous questions.
        You can then select a question to view the response.
        '''
        return review(filename=filename,profile=profile,summary=summary)

    def resummarize(self,
                    temperature: (temperature_doc,'option','t') = 0.5,
                    n: (n_doc,'option')=1,
                    profile:(profile_doc,'option','p')='default',
                    )->dict[str,dict[str,str]]:
        '''
        Creates an updated summary for question.
        '''
        return resummarize(profile=profile,n=n,temperature=temperature)

def main():
    Interpreter.call(Companion)
       
if __name__ == '__main__':
    main()