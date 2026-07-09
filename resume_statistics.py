def resume_statistics(text):

    words = len(text.split())
    characters = len(text)
    lines = len(text.split("\n"))

    return words, characters, lines