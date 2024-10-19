def read_file(path):
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_file(path,content):
    file = open(path, "w")
    content = file.write(content)
    file.close()
    return True