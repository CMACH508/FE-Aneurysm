import os
from PIL import Image


#此脚本将一张大图切割为9张小图，并存入原来和大图一样的路径中
in_path = "../data/imgdata"


img_file = os.listdir(in_path)
for file_name in img_file:
    print(file_name)
    values = os.listdir(os.path.join(in_path,file_name))
    for value in values:
        directions = os.listdir(os.path.join(in_path,file_name,value))
        for direction in directions:
            if(direction[0] == "."):
                continue
            files = os.listdir(os.path.join(in_path,file_name,value,direction))
            for file in files:
                this_path = os.path.join(in_path,file_name,value,direction,file)
                if(len(this_path.split("_")) > 5):
                    os.remove(this_path)
                    print("delete  ", this_path)
                    continue
                f = Image.open(os.path.join(in_path,file_name,value,direction,file))
                size_row = [0,f.size[0]//4,f.size[0]//2,f.size[0]//4 * 3,f.size[0]]
                size_col = [0, f.size[1] // 4, f.size[1] // 2, f.size[1] // 4 * 3, f.size[1]]
                location = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
                for i in range(9):
                    loc = location[i]
                    cropped = f.crop((size_row[loc[0]],size_col[loc[1]],size_row[loc[0] + 2],size_col[loc[1] + 2]))

                    file_path = os.path.join(os.path.join(in_path,file_name,value,direction,file.split(".")[0] +"_"+str(i)+".jpg"))
                    cropped.save(file_path)