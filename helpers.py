from config import DEBUG, PROJECT_ROOT


# Display a debug message when debug messages are enabled in the config
def debug(message):
    if DEBUG:
        print(message)


# Gets absolute path of file
def get_path(file):
    print(PROJECT_ROOT)
    if file[:1] == '/':
        return PROJECT_ROOT + file
    else:
        return PROJECT_ROOT + "/" + file


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return "".join(x.title() for x in components)