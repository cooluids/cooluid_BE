import string, random
import json
from django.core.exceptions import ImproperlyConfigured


#랜덤 코드 생성기
def generate_code(length=15):
    upper_case_letters = string.ascii_uppercase
    lower_case_letters = string.ascii_lowercase
    digits = string.digits

    upper_case = random.choices(upper_case_letters, k=5)
    lower_case = random.choices(lower_case_letters, k=5)
    numbers = random.choices(digits, k=5)

    code = ''.join(upper_case + lower_case + numbers)

    code_list = list(code)
    random.shuffle(code_list)
    code = ''.join(code_list)

    return code


#시크릿
def get_secret(value, secrets):
    try:
        return secrets[value]
    except KeyError:
        error_msg = "Set the {} environment variable".format(value)
        raise ImproperlyConfigured(error_msg)

def load_secrets(value):
    with open(value) as f:
        secrets = json.loads(f.read())
    return secrets