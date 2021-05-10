import random
import string
 
def random_string(str_size=10):
    return ''.join(random.choice(string.ascii_letters + string.punctuation) for x in range(str_size))
 