def comparison(start,end, path_to_file):
    file = open(path_to_file)
    for res in file:
        pred_start = int(res.split(" ")[1])
        pred_end = int(res.split(" ")[2].split("\t")[0])
        if not (pred_end < int(start) or pred_start > int(end)):
            return res.split("\t")[-1]
    return ''


