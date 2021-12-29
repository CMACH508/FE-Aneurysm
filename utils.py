

def read_list(data, line_num):
                line_num = line_num + 1
                line = data[line_num][:-1]
                im_num = str(line)
                gt_box = []
                up_list = []
                back_list = []
                down_list = []
                front_list = []
                left_list = []
                right_list = []
                while True:
                    line_num = line_num + 1
                    line = data[line_num][:-1]
                    if (line == "backlist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            split = line.split(" ")
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            back_list.append(List)
                    if (line == "frontlist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            front_list.append(List)

                    if (line == "rightlist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            right_list.append(List)

                    if (line == "leftlist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            left_list.append(List)

                    if (line == "downlist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            down_list.append(List)

                    if (line == "uplist:"):
                        while True:
                            line_num = line_num + 1
                            line = data[line_num][:-1]
                            if (len(line.split(" ")) == 1):
                                break
                            List = [float(line.split(" ")[0]), float(line.split(" ")[1]), float(line.split(" ")[2]),
                                    float(line.split(" ")[3]), float(line.split(" ")[4]), float(line.split(" ")[5])]
                            up_list.append(List)
                    if (line == "gt_box:"):
                        line_num = line_num + 1
                        line = data[line_num][:-1]
                        List = [int(line.split(" ")[0]), int(line.split(" ")[1]), int(line.split(" ")[2]),
                                int(line.split(" ")[3]), int(line.split(" ")[4]), int(line.split(" ")[5])]
                        gt_box = List
                        break
                return line_num,im_num,gt_box,up_list,back_list,down_list,front_list,left_list,right_list
