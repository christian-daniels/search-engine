from collections import defaultdict






def make_positions(filename):
    a_dict = {"a": 0, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1, "i": 1, "j": 1,
              "k": 1, "l": 1, "m": 1, "n": 1, "o": 1, "p": 1, "q": 1, "r": 1, "s": 1, "t": 1,
              "u": 1, "v": 1, "w": 1, "x": 1, "y": 1, "z": 1}
    a_list = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
              'e', 'd', 'c', 'b', 'a',"9","8",'7','6','5','4','3','2','1','0']
    print("making positions dictionary for",filename)
    with open(filename, 'r') as file:

        a_dict["a"] = 0
        to_compare = a_list.pop()
        can_compare = True
        previous = 0
        line = file.readline()
        while line != '':
            lineStart = file.tell()
            if (to_compare == line[0] and can_compare):
                a_dict[to_compare] = previous
                if (len(a_list) != 0):
                    to_compare = a_list.pop()
                else:
                    break
            # FOR DEBUGGING
            # print('line:' + str(lineStart) + " value",line)
            line = file.readline()
            previous = lineStart
    name = filename[:-4] + "positions.txt"
    # print(a_dict)
    with open(name, "w") as file:
        # for k,v in a_dict.items():
        file.write(str(a_dict))




# make_positions("finishedimportant.txt")
# make_positions("finishedindex.txt")