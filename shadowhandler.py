def valid_user(path_shadow_file, user):
    shadow_file = open(path_shadow_file, 'r')
    lines = shadow_file.read()
    shadow_file.close()

    lines = lines.split('\n')

    result = False
    for line in lines:
        fields = line.split(':')

        result = fields[0] == user
        if result:
            break

    return result


def get_hash_password(path_shadow_file, user):
    shadow_file = open(path_shadow_file, 'r')
    lines = shadow_file.read()
    shadow_file.close()

    lines = lines.split('\n')

    hash_password = ''
    for line in lines:
        fields = line.split(':')

        if fields[0] == user:
            hash_password = fields[1]
            break

    return hash_password


def get_salt(path_shadow_file, user):
    shadow_file = open(path_shadow_file, 'r')
    lines = shadow_file.read()
    shadow_file.close()

    lines = lines.split('\n')

    salt = ''
    for line in lines:
        fields = line.split(':')

        if fields[0] == user:
            chunks = fields[1].split('$')
            salt = '$' + chunks[1] + '$' + chunks[2] + '$'
            break

    return salt


def change_hash(path_shadow_file, user, new_hash):
    shadow_file = open(path_shadow_file, 'r')
    lines = shadow_file.read()
    shadow_file.close()

    lines = lines.split('\n')

    for i in range(len(lines)):
        line_atual = lines[i]
        fields = line_atual.split(':')
        if fields[0] == user:
            nova_line = ''
            for j in range(len(fields)):
                if nova_line != '':
                    nova_line += ':'
                if j == 1:
                    nova_line += new_hash
                else:
                    nova_line += fields[j]

            lines.remove(line_atual)
            lines.insert(i, nova_line)
            break
    return lines


def write_file(path_shadow_file, new_content):
    file_text = ''
    for line in new_content:
        file_text += line + '\n'

    shadow_file = open(path_shadow_file, 'w')
    shadow_file.write(file_text)
    shadow_file.close()