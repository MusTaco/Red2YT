def split_sen(sen):
    split_chars = ['.', ',', ':', ';', '?']
    ignore_chars = { '(', ')', '[', ']'}
    newArr = []
    newLine = ''
    in_quotes_or_brackets = False

    for c in sen:
        newLine += c

        if c in ignore_chars:
            in_quotes_or_brackets = not in_quotes_or_brackets

        if not in_quotes_or_brackets and c in split_chars:
            newArr.append(newLine.strip())
            newLine = ''

    # Append the last part of the sentence if not empty
    if newLine:
        newArr.append(newLine.strip())

    return newArr