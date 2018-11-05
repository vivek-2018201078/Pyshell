import os
import glob
import re
import shutil
import difflib

home_dir = os.environ['HOME']
cur_dir = os.getcwd()


def parse_path(command):
    list = []
    global cur_dir, home_dir
    parts = command.split()
    for part in parts:
        if part[0] == '/':
            temp_dir = "/"
            parsed = part[1:]
        elif part[0] == '~':
            temp_dir = home_dir
            parsed = part[1:]
        else:
            temp_dir = cur_dir
            parsed = part
        spiltted = parsed.split('/')
        for elem in spiltted:
            if elem == "":
                continue
            elif elem == "..":
                temp_dir = temp_dir.rsplit('/', 1)[0];
            else:
                if temp_dir == "/":
                    temp_dir = temp_dir + elem
                else:
                    temp_dir = temp_dir + '/' + elem
        list.append(temp_dir)
    return list


def parse_path_space(command):
    list = []
    global cur_dir, home_dir
    if command[0] == '/':
        temp_dir = "/"
        parsed = command[1:]
    elif command[0] == "~":
        temp_dir = home_dir
        parsed = command[1:]
    else:
        temp_dir = cur_dir
        parsed = command
    spiltted = parsed.split('/')
    for elem in spiltted:
        if elem == "":
            continue
        elif elem == "..":
            temp_dir = temp_dir.rsplit('/', 1)[0]
        else:
            if temp_dir == "/":
                temp_dir = temp_dir + elem
            else:
                temp_dir = temp_dir + '/' + elem
    list.append(temp_dir)
    return list


def cd(command):
    if len(command) == 2:
        global cur_dir
        global home_dir
        cur_dir = home_dir
        print(cur_dir)
        return
    if len(command) > 3:
        print("Too many arguments")
        return
    if command[2] == ".":
        print(cur_dir)
        return
    tilda_present = 0
    if command[2][0] == '/':
        temp_dir = "/"
    elif command[2][0] == "~":
        tilda_present = 1
        temp_dir = home_dir
        # command[2] = command[2][1:]
        after_tilda = command[2][1:]
        parts = after_tilda.split('/')
        # print(command[1])
    else:
        temp_dir = cur_dir
    if tilda_present == 0:
        parts = command[2].split('/')
    # print(parts)
    for subpart in parts:
        if subpart == "":
            continue
        if subpart == "..":
            if cur_dir.count('/') == 1:
                temp_dir = "/"
            else:
                temp_dir = temp_dir.rsplit('/', 1)[0]
        else:
            if temp_dir == "/":
                temp_dir = temp_dir + subpart
            else:
                temp_dir = temp_dir + "/" + subpart
            if not os.path.isdir(temp_dir):
                print(command[1], ": no such directory")
                return
    cur_dir = temp_dir
    print(cur_dir)


def ls(command):
    global cur_dir
    temp_dir = cur_dir + "/*"
    list = glob.glob(temp_dir)
    for elem in list:
        print(elem.rsplit('/', 1)[1])


def pwd(command):
    print(cur_dir)


def touch(command):
    if len(command) < 3:
        print("Too few arguments to touch")
        return
    path_list = parse_path(command[2])
    for path in path_list:
        if os.path.exists(path):
            temp_file = path.rsplit('/', 1)[0] + "temp_file"
            shutil.copy(path, temp_file)
            shutil.move(temp_file, path)
            continue  # can add timestamp
        else:
            if os.path.exists(path.rsplit('/', 1)[0]):
                fp = open(path, "w")
                fp.close()
            else:
                print(path, ": No such file or Directory")


def head(command):
    # print(command)
    if command[2].__contains__("-n"):
        if command[2].partition(' ')[0] != "-n":
            print("Invalid command")
            return
        else:
            n_str = command[2].split()[1]
            if re.match("^\d+?$", n_str) is None:
                print(n_str, ":not a number")
            else:
                n = int(n_str)
                temp1 = command[2].partition(' ')[2]
                temp2 = temp1.partition(' ')[2]
                paths = parse_path_space(temp2)
                for path in paths:
                    if os.path.exists(path):
                        fp = open(path, "r")
                        for line in fp:
                            if n == 0:
                                break
                            print(line, end='')
                            n -= 1
                        fp.close()
                    else:
                        print(path, ":file does not exists")

    else:
        paths = parse_path_space(command[2])
        for path in paths:
            if os.path.exists(path):
                fp = open(path, "r")
                n = 0
                for line in fp:
                    if n == 10:
                        break
                    print(line, end='')
                    n += 1
                fp.close()
            else:
                print(path, ":file does not exist")


def tail(command):
    # print(command)
    if command[2].__contains__("-n"):
        if command[2].partition(' ')[0] != "-n":
            print("Invalid command")
            return
        else:
            n_str = command[2].split()[1]
            if re.match("^\d+?$", n_str) is None:
                print(n_str, ":not a number")
            else:
                n = int(n_str)
                temp1 = command[2].partition(' ')[2]
                temp2 = temp1.partition(' ')[2]
                paths = parse_path_space(temp2)
                for path in paths:
                    if os.path.exists(path):
                        n_lines = 0
                        with open(path, 'r') as f:
                            for line in f:
                                n_lines += 1
                        fp = open(path, "r")
                        to_print_from = n_lines - n
                        line_itr = 0
                        for line in fp:
                            if to_print_from <= line_itr < n_lines:
                                print(line, end='')
                            line_itr += 1
                        fp.close()
                    else:
                        print(path, ":file does not exists")

    else:
        paths = parse_path_space(command[2])
        for path in paths:
            if os.path.exists(path):
                n_lines = 0
                with open(path, 'r') as f:
                    for line in f:
                        n_lines += 1
                fp = open(path, "r")
                to_print_from = n_lines - 10
                line_itr = 0
                for line in fp:
                    if to_print_from <= line_itr < n_lines:
                        print(line, end='')
                    line_itr += 1
                fp.close()
            else:
                print(path, ":file does not exist")


def grep(command):
    if command[2][0] == '-':
        flags = command[2].partition(' ')[0]
        flags = flags[1:]
        temp1 = command[2].partition(' ')[2]
        path_unreal = temp1.partition(' ')[2]
        pattern = temp1.split()[0]
        pattern = re.sub("'", "", pattern)
        path = parse_path_space(path_unreal)[0]
        if not os.path.exists(path):
            print(path, ":path does not exist")
            return
        matched = []
        unmatched = []
        line_no_matched = []
        line_no_unmatched = []
        line_no = 1
        with open(path, 'r') as f:
            for line in f:
                if flags.__contains__('i'):
                    if re.search(pattern, line, re.I) is None:
                        unmatched.append(line)
                        line_no_unmatched.append(line_no)
                    else:
                        matched.append(line)
                        line_no_matched.append(line_no)
                else:
                    if re.search(pattern, line) is None:
                        unmatched.append(line)
                        line_no_unmatched.append(line_no)
                    else:
                        matched.append(line)
                        line_no_matched.append(line_no)
                line_no += 1

        if flags.__contains__('c'):
            if flags.__contains__('v'):
                print(len(unmatched))
                return
            else:
                print(len(matched))
                return
        if flags.__contains__('n'):
            if flags.__contains__('v'):
                for i in range(len(unmatched)):
                    print(line_no_unmatched[i], ":", unmatched[i], end='')
                return
            else:
                for i in range(len(matched)):
                    print(line_no_matched[i], ":", matched[i], end='')
                return
        else:
            if flags.__contains__('v'):
                for i in range(len(unmatched)):
                    print(unmatched[i], end='')
                return
            else:
                for i in range(len(matched)):
                    print(matched[i], end='')
                return

    else:
        pattern = command[2].partition(' ')[0]
        pattern = re.sub("'", "", pattern)
        path_unreal = command[2].partition(' ')[2]
        path = parse_path_space(path_unreal)[0]
        if not os.path.exists(path):
            print(path, ":path does not exist")
        with open(path, 'r') as f:
            for line in f:
                if re.search(pattern, line) is None:
                    continue
                else:
                    print(line, end='')


def sed(command):
    if command[2][0] == '-':
        flags = command[2].partition(' ')[0]
        flags = flags[1:]
        temp1 = command[2].partition(' ')[2]
        sed_command = temp1.partition(' ')[0]
        sed_command = re.sub("'", "", sed_command)
        sed_split = sed_command.split(sep='/')
        path_unreal = temp1.partition(' ')[2]
        path = parse_path_space(path_unreal)[0]
        if not os.path.exists(path):
            print(path, ":Invalid path")
            return
        if sed_split[0] == 's':
            if len(sed_split) != 4:
                print("Invalid command")
                return
            pattern = sed_split[1]
            replace = sed_split[2]
            last_op = sed_split[-1]
            with open(path, 'r') as fp:
                for line in fp:
                    if flags.__contains__('n') and last_op == 'p':
                        if re.search(pattern, line):
                            line = re.sub(pattern, replace, line, 1)
                            print(line, end='')
                    elif flags.__contains__('n'):
                        break
                    elif last_op == 'p':
                        if re.search(pattern, line):
                            line = re.sub(pattern, replace, line, 1)
                            print(line, end='')
                            print(line, end='')
                        else:
                            print(line)
                    elif last_op == 'g':
                        re.sub(pattern, replace, line)
                        print(line, end='')
                    else:
                        print("Invalid command")
            return
        elif sed_split[-1] == 'p':
            pattern = sed_split[1]
            with open(path, 'r') as fp:
                for line in fp:
                    if re.search(pattern, line):
                        print(line, end='')
            return
        elif sed_split[-1] == 'd':
            return
    else:
        temp1 = command[2].partition(' ')[0]
        sed_command = temp1.partition(' ')[0]
        sed_command = re.sub("'", "", sed_command)
        path_unreal = command[2].partition(' ')[2]
        path = parse_path_space(path_unreal)[0]
        if not os.path.exists(path):
            print(path, ":invalid path")
            return
        sed_split = sed_command.split(sep='/')
        if sed_split[0] == 's':
            if len(sed_split) != 4:
                print("Invalid command")
                return
            pattern = sed_split[1]
            replace = sed_split[2]
            last_op = sed_split[-1]
            with open(path, 'r') as fp:
                for line in fp:
                    if last_op == 'p':
                        if re.search(pattern, line):
                            line = re.sub(pattern, replace, line, 1)
                            print(line, end='')
                            print(line, end='')
                        else:
                            print(line, end='')
                    elif last_op == 'g':
                        line = re.sub(pattern, replace, line)
                        print(line, end='')
                    elif last_op == '':
                        line = re.sub(pattern, replace, line, 1)
                        print(line, end='')
                    else:
                        print("Invalid command")
            return
        elif sed_split[-1] == 'p':
            pattern = sed_split[1]
            with open(path, 'r') as fp:
                for line in fp:
                    if re.search(pattern, line):
                        print(line, end='')
                        print(line, end='')
                    else:
                        print(line, end='')
            return
        elif sed_split[-1] == 'd':
            pattern = sed_split[1]
            with open(path, 'r') as fp:
                for line in fp:
                    if re.search(pattern, line) is None:
                        print(line, end='')
            return


def diff(command):
    path1_unreal = command[2].split()[0]
    path2_unreal = command[2].split()[1]
    path1 = parse_path_space(path1_unreal)[0]
    path2 = parse_path_space(path2_unreal)[0]
    if not os.path.exists(path1):
        print(path1, ":Invalid path")
        return
    if not os.path.exists(path2):
        print(path2, ":Invalid path")
        return

    with open(path1, 'r') as fp:
        path1_data = fp.read()
    with open(path2, 'r') as fp2:
        path2_data = fp2.read()
    for line in difflib.unified_diff(path1_data, path2_data, fromfile=path1, tofile=path2, lineterm=''):
        print(line)


def tr(command):
    string1 = command[2].split()[0]
    string1 = re.sub("'", "", string1)
    string2 = command[2].split()[1]
    string2 = re.sub("'", "", string2)
    path_unreal = command[2].split()[2]
    path = parse_path_space(path_unreal)[0]
    len1 = len(string1)
    len2 = len(string2)
    if len1 > 0 and len2 == 0:
        print("tr: when not truncating set1, string2 must be non-empty")
        return
    itr1 = 0
    itr2 = 0
    list1 = []
    list2 = []
    if len1 <= len2:
        for i in range(len1):
            list1.append(string1[i])
            list2.append(string2[i])
    else:
        for i in range(len1):
            if itr2 == len2 - 1:
                list1.append(string1[itr1])
                list2.append(string2[itr2])
                itr1 += 1
            else:
                list1.append(string1[itr1])
                list2.append(string2[itr2])
                itr1 += 1
                itr2 += 1
    if not os.path.exists(path):
        print(path, ":Invalid path")
    with open(path, 'r') as fp:
        for line in fp:
            for i in range(len(list1)):
                line = re.sub(list1[i], list2[i], line)
            print(line, end='')



def main():
    while (True):
        command_real = input(">>")
        if command_real == "":
            continue
        command = command_real.partition(' ')
        # print(command)
        if command[0] == "exit":
            exit()
        if command[0] == "cd":
            cd(command)
            continue
        if command[0] == "ls":
            ls(command)
            continue
        if command[0] == "pwd":
            pwd(command)
            continue
        if command[0] == "touch":
            touch(command)
            continue
        if command[0] == "head":
            head(command)
            continue
        if command[0] == "tail":
            tail(command)
            continue
        if command[0] == "grep":
            grep(command)
            continue
        if command[0] == "sed":
            sed(command)
            continue
        if command[0] == "diff":
            diff(command)
            continue
        if command[0] == "tr":
            tr(command)
            continue
        else:
            print("Invalid Command")
            continue


if __name__ == '__main__':
    main()
