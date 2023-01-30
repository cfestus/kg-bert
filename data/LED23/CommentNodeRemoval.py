with open('led23.nt', 'r') as file:
    lines = file.readlines()

with open('led23_without_comments.nt', 'w') as file:
    for line in lines:
        if '--' not in line:
            file.write(line)