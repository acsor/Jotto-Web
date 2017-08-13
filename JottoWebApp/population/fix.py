with open("English dictionary.txt", "r") as input_file, open("English dictionary.out", "w") as output_file:
    row_id = 2

    for line in input_file:
        line = line.strip()
        output_file.write("%d,%s\n" % (row_id, line.split(",")[1]))

        row_id += 1
