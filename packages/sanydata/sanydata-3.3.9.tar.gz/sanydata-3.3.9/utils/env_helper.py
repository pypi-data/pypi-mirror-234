import os

def get_int_from_env(envKey, defaultValue):
    envValue = os.environ.get(envKey)
    if envValue is None:
        envValue = defaultValue
    else:
        try:
            envValue = int(envValue)
        except ValueError:
            envValue = defaultValue
    return envValue