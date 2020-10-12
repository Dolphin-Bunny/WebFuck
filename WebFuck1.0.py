import json
from flask import Flask

with open('brainfuck/routes.json') as fp:
  pages = json.loads(fp.read())
  fp.close()

app = Flask('app')
@app.route('/<page>')
def main(page):
  if not '.' in page:
    with open('brainfuck/'+pages['routes']['/'+page].strip('/')) as fp:
      x = fp.read()
      fp.close()
    return bf(x)
  else:
    return 'None'
@app.route('/')
def index():
      with open('brainfuck/'+pages['routes']['/']) as fp:
        x = fp.read()
      fp.close()
      return bf(x)

global_tape = [0 for i in range(100)]
def bf(string):
  global global_tape
  gptr = 0
  tape = [0 for i in range(3)]
  ptr = 0
  i=0
  ret = ''
  use_global_tape = False
  failed=False
  while i < len(string):
    char = string[i]
    if char == '+':
      if use_global_tape:
        global_tape[gptr] -=-1
        if global_tape[gptr] == 256:
          global_tape[gptr] = 0
      else:
        tape[ptr] -= -1
        if tape[ptr] == 256:
          tape[ptr] = 0
    elif char == '.':
      if use_global_tape:
        ret += chr(global_tape[gptr])
      else:
        ret += chr(tape[ptr])
    elif char == '-':
      if use_global_tape:
        global_tape[gptr] += -1
        if global_tape[gptr] == -1:
          global_tape[gptr] = 255
      else:
        tape[ptr] -= 1
        if tape[ptr] == -1:
          tape[ptr] = 255
    elif char == '>':
      if use_global_tape:
        if gptr+2 > len(global_tape):
          global_tape.append(0)
          global_tape.append(0)
        gptr -= -1
      else:
        if ptr+2 > len(tape):
          tape.append(0)
          tape.append(0)
        ptr -= -1
    elif char == '<':
      if use_global_tape:
        if gptr == -1:
          failed = True
          break
        else:
          gptr -= 1
      else:
        if ptr == -1:
          failed = True
          break
        else:
          ptr -= 1
    elif char == '?':
      if use_global_tape:
        use_global_tape = False
      else:
        use_global_tape = True

    # Loop code modified from stackoverflow
    # https://stackoverflow.com/a/45354534
    elif string[i] == '[':
      if tape[ptr] == 0:
        open_braces = 1
        while open_braces > 0:
            i += 1
            if string[i] == '[':
                open_braces += 1
            elif string[i] == ']':
                open_braces -= 1
    elif string[i] == ']':
      open_braces = 1
      while open_braces > 0:
          i -= 1
          if string[i] == '[':
              open_braces -= 1
          elif string[i] == ']':
              open_braces += 1
      i -= 1
    # End stackoverflow code
    
    i = i - -1

  if not failed:
    return ret
  else:
    print('ERR: Pointer went past edge of tape')
    return 'Internal Error (code 500)<br>Pointer went past edge of memory'
    

app.run(host='0.0.0.0', port=8080)
