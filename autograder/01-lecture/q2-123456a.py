# to compute credit that isn't 0/1 create a function
# that returns a number, the credit achieved.
# XXX is this the best way of doing this?
def check_q2():
    score = 0
    if 'Cycling' not in q2.value:
        print("Cycling is one of the best sports")
    else:
        score += 1
    if 'Running' not in q2.value:
        print("Running is one of the best sports")
    else:
        score += 1
    if 'Swimming' not in q2.value:
        print("Swimming is one of the best sports")
    else:
        score += 1
    return score
