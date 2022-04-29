def lib_get_words_from_chunks(chunks):
    alphabet = 'abcdefghijklmnoprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print(alphabet)
    for chunk in chunks:
        buffer = ''
        for char in chunk:
            if char in alphabet:
                buffer += char
            else:
                if buffer:
                    yield buffer
                buffer = ''
        if buffer:
            yield buffer
