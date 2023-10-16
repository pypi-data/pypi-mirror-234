import sys


def main(lines):
    id_list = []
    npu_type = ''
    flag = False
    for line in lines:
        if flag:
            info_list = line.split()
            if len(info_list) < 3:
                break
            if not info_list[1].isdigit():
                break
            npu_type = info_list[2]
            id_list.append(info_list[1])
            flag = False
        if "====" in line:
            flag = True
    if len(id_list) == 0:
        print('0')
    else:
        print('{}:{}'.format(npu_type, len(id_list)))


if __name__ == '__main__':
    main(sys.argv)
