def round_min(ch):
    if int(ch) != ch:
        return int(str(ch)[:str(ch).index('.')])
    else:
        return ch

# print(round_min(56.9))