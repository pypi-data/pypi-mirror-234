import os
from termcolor import colored

_bubble_chars = {
    'A': (
        '''   __   
  /  \  
 / /\ \ 
/_/¯¯\_\\
'''
    ),
    'B': (
        ''' ___ 
| _ \\
| _ |
|___/
'''
    ),
    'C': (
        '''  ___ 
 / __|
| (__ 
 \___|
'''
    ),
    'D': (
        ''' ____  
|  _ \ 
| |_| |
|____/ 
'''
    ),

    'E': (
        ''' ___ 
| __|
| _| 
|___|
'''
    ),
    'F': (
        ''' ___ 
| __|
| _| 
|_|  
'''
    ),
    'G': (
        '''  ___ 
 / __\\
| ( -¬
 \___|
'''
    ),
    'H': (
        ''' _   _ 
| |_| |
|  _  |
|_| |_|
'''
    ),
    'I': (
        ''' _ 
| |
| |
|_|
'''
),
    'J': (
        ''' _____ 
|_   _|
 _| |  
|___|  
'''
),
    'K': (
        ''' _  _ 
| \/ /
|   / 
|_/\_\\
'''
),
    'L': (
        ''' _   
| |  
| |_ 
|___|
'''
    ),
    'M': (
        ''' _   _ 
| \_/ |
|  _  |
|_| |_|
'''
),
    'N': (
        ''' _   _ 
| \ | |
|  \| |
|_|\__|
'''
),
    'O': (
        ''' _____ 
|  _  |
| |_| |
|_____|
'''
),
    'P': (''' ___ 
| _ \\
|  _/
|_|  
'''
),
    'Q': (''' _____ 
|  _  |
| |_| |
|____\\\\
'''
),
    'R': (''' ___ 
| _ \\
|   /
|_|_\\
'''
),
    'S': (
        ''' ___ 
| __|
|__ |
\___|
'''
),
    'T': (
        ''' _____ 
|_   _|
  | |  
  |_|  
'''
    ),
    'U': (
        ''' _   _ 
| | | |
| |_| |
|_____|
'''
    ),
    'V': (
        ''' _   _ 
\ \ / /
 \ ¯ / 
  \_/  
'''
    ),
    'W': (
        ''' _   __   _ 
\ \ /  \ / /
 \ ¯ /\ ¯ / 
  \_/  \_/  
'''
    ),
    'X': (
        '''__  __
\ \/ /
 \  / 
/_/\_\\
'''
    ),
    'Y': (
        '''__  __
\ \/ /
 \  /
 |__|
'''
    ),
    'Z': (        ''' _____
|__  /
  / /_
 /____|
'''
    ),
    '1': (        ''' __ 
/  |
 | |
 |_|
'''
    ),
    '2': (        ''' ___  
|_  ) 
 / /  
|____|
'''
    ),
    '3': (        ''' ____
|__ /
 |_ \\
|___/
'''
    ),
    '4': (        '''  /_|  
 /_||_
/__  _|
   ||
'''
    ),
    ' ': (        ''' 
 
 
 
'''
    ),
}

def get_bubble_text(text: str, overlap: bool = True, color_gradient: bool = False) -> str:
    bubble_text_rows = ['','','','']
    text = text.upper()
    for i, char in enumerate(text):
        if char not in _bubble_chars:
            continue

        bubble_char_rows =  _bubble_chars[char].split('\n')
        for j, row in enumerate(bubble_char_rows):
            if overlap and i > 0 and char != " " and text[i-1] != " ":
                if text[i-1] == "A" or char == "A" or text[i-1] == "J":
                    # Overlap new char by two spaces
                    if bubble_text_rows[j][-2] == " ":
                        # If second to last char is a space, check next char along for same
                        if bubble_text_rows[j][-1] == " ":
                            bubble_text_rows[j] = bubble_text_rows[j][:-2] + row[0] + row[1]
                        else:
                            bubble_text_rows[j] = bubble_text_rows[j][:-1] + row[1]
                    elif bubble_text_rows[j][-1] == " ":
                            bubble_text_rows[j] = bubble_text_rows[j][:-1] + row[1]
                    row = row[2:]
                else:
                    # Overlap new char by a space
                    if bubble_text_rows[j][-1] == " ":
                        bubble_text_rows[j] += '\b' + row[0]
                    row = row[1:]
            bubble_text_rows[j] += row

            # All characters are a maximum of 4 rows in height
            if j >= 3:
                break

    # Create text and delete any backspace characters
    btext = '\n'.join(bubble_text_rows).replace(' \x08', '')
    if color_gradient:
        btext = _rainbowify(btext)

    return btext

def print_bubble_text(text: str, overlap: bool = True, color_gradient: bool = True):
    bubble_text = get_bubble_text(text, overlap, color_gradient)
    print(bubble_text)

def _rainbowify(text: str) -> str:
    os.system('color')

    colours = [
        'blue',
        'cyan',
        'green',
        'magenta',
        'red',
        'yellow'
    ]

    rows = text.split('\n')

    colour_length = len(rows[0]) // len(colours)
    for i, row in enumerate(rows):
        coloured_row = ''
        for j, colour in enumerate(colours):
            section = row[j*colour_length:] if j == len(colours) - 1 else row[j*colour_length:j*colour_length+colour_length]
            coloured_row += colored(section, colour)
        rows[i] = coloured_row
    
    text = '\n'.join(rows)
    return colored(text, 'red')
    
