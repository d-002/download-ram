with open('script.js', encoding='utf-8') as f:
    data = f.read()

vars = {}
forbidden = 'setDarkMode'.split(' ')

def getname():
    n = len(vars)
    if n < 26: return chr(65+n)
    if n < 52: return chr(39+n)+chr(71+n)
    raise ValueError

# /!\ doesn't handle comments in strings, ' or ` strings, var keyword,
# local variables, used packed variable names

# remove comments
data2 = ''
in_comment = 0 # 1: //, 2: /*
prev = None
for c in data:
    if prev == '/' and not in_comment:
        if c == '/':
            in_comment = 1
        elif c == '*':
            in_comment = 2
        data2 = data2[:-1]
    elif in_comment == 1 and c == '\n':
        in_comment = 0
    elif in_comment == 2 and prev+c == '*/':
        in_comment = 0
        data2 = data2[:-1]
    elif not in_comment:
        data2 += c

    prev = c

# minify code, rename variables
data = data2
data2 = ''
word = ''
prev_word = None # prev alphanumeric word
prev_thing = '' # prev non-alphanumeric word
prev = -1
in_string = False

# whether the current word is a variable being defined:
# 0: no, 1: let/const, 2: function argument
defining = 0

for c in data:
    now = c.isalnum()
    if now:
        if prev:
            word += c
        else:
            if in_string:
                data2 += word
            else:
                data2 += word.strip() or ' '

            if ';' in word:
                defining = 0
            elif (')' in word or '=>' in word) and defining == 2:
                defining = 0

            prev_thing = word
            word = c
    else:
        if prev:
            if in_string:
                data2 += word
            elif word in ('const', 'let'):
                # compress const into let
                word = 'let'
                data2 += word
                defining = 1
            elif word == 'function':
                data2 += word
                defining = 2
            else:
                # try to store a new variable
                if (len(word) > 1
                    and (prev_word == 'function' or
                         defining == 1 and (
                             prev_word == 'let' or prev_thing.endswith(',')) or
                         defining == 2)
                    and word not in forbidden and word not in vars):
                    vars[word] = getname()

                # replace with a packed variable name if needed
                if prev_thing.endswith('.'):
                    data2 += word
                else:
                    data2 += vars.get(word) or word

            prev_word = word
            word = c
        else:
            if c in '\n\t\r ' and not (c == ' ' and in_string):
                continue
            if word and c in ')}' and word[-1] == ';':
                word = word[:-1]
            word += c

    if c == '"':
        in_string = not in_string

    prev = now

if word.endswith(';'):
    word = word[:-1]
data2 += word

print(data2)
print('\nPacked vars: '+str(vars))
with open('packed.js', 'w', encoding='utf-8') as f:
    f.write(data2)
