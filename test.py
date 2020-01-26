from operator import itemgetter


def sort_file():
    list_scores1 = []
    with open("highscores.txt", "r") as f:
        for line in f:
            temp = line.splitlines()
            temp2 = (temp[0].split(' '))
            list_scores1.append((temp2[0], int(temp2[1])))
    # print(list_scores1)
    list_scores1 = sorted(list_scores1, key=lambda s: s[1], reverse=True)
    # output this data to file
    i = 0
    with open("highscores.txt", "w") as file_ptr:
        for line in list_scores1:
            file_ptr.write("%s %d\n" % (list_scores1[i][0], list_scores1[i][1]))
            i += 1
    print("saved score to txt file")


sort_file()
