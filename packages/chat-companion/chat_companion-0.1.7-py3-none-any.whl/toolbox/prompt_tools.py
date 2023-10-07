def clean_f_str(f_str:str)->str:
    '''
    Takes a f string and removes the leading spaces.
    '''
    return '\n'.join(
                        map(lambda l:l.strip(),
                        filter(bool,f_str.split('\n')
                    )))