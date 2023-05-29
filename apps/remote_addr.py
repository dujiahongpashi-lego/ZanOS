from filesystem import FS

def get_addr():
    lines = FS().open('apps/_remote_server_addr.txt')
    return lines[0]