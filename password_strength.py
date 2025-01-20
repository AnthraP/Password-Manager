import string

"""
Name: strength_checker
Parameters: password: String
Returns: Score: Integer
Purpose: Takes a password and returns a score of its strength
"""
def strength_checker(password):
    upper_case = []
    for i in password:
        if i in string.ascii_uppercase:
            upper_case.append(1)
        else:
            upper_case.append(0)
    upper_case = any(upper_case)

    lower_case = []
    for i in password:
        if i in string.ascii_lowercase:
            lower_case.append(1)
        else:
            lower_case.append(0)
    lower_case = any(lower_case)

    special = []
    for i in password:
        if i in string.punctuation:
            special.append(1)
        else:
            special.append(0)
    special = any(special)

    numbers = []
    for i in password:
        if i in string.digits:
            numbers.append(1)
        else:
            numbers.append(0)
    numbers = any(numbers)

    characters = [upper_case, lower_case, special, numbers]
    score = 0

    length = len(password)
    if length > 7:
        score += 1
    if length > 11:
        score += 1
    if length > 15:
        score += 1

    with open("common_passwords.txt", "r") as f:
        common = f.read().splitlines()
    if password in common:
        return "Very common password"
    f.close()

    if sum(characters) > 1:
        score += 1
    if sum(characters) > 2:
        score += 1
    if sum(characters) > 3:
        score += 1

    return score


