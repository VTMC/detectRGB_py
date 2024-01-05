#pip install rawpy -> rawpy : get Raw image to get RGB values
#pip install imageio -> imageio : save RGB channels of image
#pip install pandas -> pandas : tablulate of RGB data with row and col value
#pip install openpyxl -> openpyxl : save table made by pandas to xlsx file
#pip install opencv-python -> opencv-python : draw red point by opencv on image which made by RGB channels
#pip install -U matplotlib -> matplotlib.pyplot : show pointed image to comfortable to see image
#pip list -> check installed packages (package list in 2024_01_05)
#→ contourpy       1.2.0
#→ cycler          0.12.1
#→ et-xmlfile      1.1.0
#→ fonttools       4.47.0
#→ imageio         2.33.1
#→ kiwisolver      1.4.5
#→ matplotlib      3.8.2
#→ numpy           1.26.3
#→ opencv-python   4.9.0.80
#→ openpyxl        3.1.2
#→ packaging       23.2
#→ pandas          2.1.4
#→ pillow          10.2.0
#→ pip             23.3.2
#→ pyparsing       3.1.1
#→ python-dateutil 2.8.2
#→ pytz            2023.3.post1
#→ rawpy           0.19.0
#→ six             1.16.0
#→ tzdata          2023.4

import sys
import subprocess
import rawpy
import imageio
import pandas as pd
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import datetime

# path = "E:/VTMC_GitHub/StoredProject_LibRaw_0.21.2/StoredProject_LibRaw_0.21.2/LibRaw-0.21.2/testFile/test_A80.dng"
# path = "E:/VTMC_GitHub/StoredProject_LibRaw_0.21.2/StoredProject_LibRaw_0.21.2/LibRaw-0.21.2/testFile/test_A80_onlyTiff.tiff"

def restart():
    python_executable = sys.executable
    script_path = sys.argv[0]
    subprocess.run([python_executable, script_path])
    sys.exit()

def getParentPath(path):
    #setting path
        path_split = path.split('/')
        print(path_split)

        path = ""
        for i in path_split:
            if(i == path_split[len(path_split)-1]):
                break
            path += i + "/"
        print("path : "+path)

        #setting name
        name = path_split[len(path_split)-1]
        name_split = name.split('.')
        print(name_split)
        name = name_split[0]
        print("name : "+name)

        #setting Final Path
        path = path + name
        print("final path : "+path)
        return path

print("setting PATH...")
print("set path in command (YOU MUST INPUT ABSOLUTE PATH)")

try:
    path = input("path : ")
    path_split = path.split(':')
    print(path_split)
    path_split = path_split[1].split('/')
    print(path_split)
    path_split = path_split[len(path_split)-1].split('.')
    print(path_split)
except:
    print("!!!!!WRONG INPUT!!!!!\n")
    print("check path of this image\n")
    sys.exit()

if(len(path_split) > 2):
    print("!!!!!WRONG INPUT!!!!!\n")
    print("Don't use your image's name include '.'\n")
    sys.exit()
else:
    imageType = path_split[1]
    if(imageType == 'dng'): # dng ... only RAW image
        imageFile = rawpy.imread(path)
        with imageFile as rp:
            rgb = rp.postprocess(
                # output_bps=16,
                # output_color=rawpy.ColorSpace.sRGB,
            ) #gamma=(1,1), no_auto_bright=True, output_bps=16
            # print(len(rgb))
            # print(rgb)

            # Extract each R,G,B Channels to save Separately
            r = rgb[:,:,0]
            g = rgb[:,:,1]
            b = rgb[:,:,2]
    else: #tiff, jpeg, png ... not RAW image
        im = Image.open(path)
        rgb = np.array(im)

        r = rgb[:,:,0]
        g = rgb[:,:,1]
        b = rgb[:,:,2]

print("R vlaues : rows="+str(len(r))+"* cols="+str(len(r[0])))
print(r)
print("G vlaues : rows="+str(len(g))+"* cols="+str(len(g[0])))
print(g)
print("B vlaues : rows="+str(len(b))+"* cols="+str(len(b[0])))
print(b)

while True:
    print("====================================\n"
          + "This is command of this program\n"
          + "rows : "+str(len(rgb))+" / cols : "+str(len(rgb[0]))+"\n"
          + "q : quit this program\n"
          + "c : restart this program to change directory of image path\n"
          + "s : save each R,G,B channels of this image\n"
          + "p : check RGB values of plural images and save points of Result, RGBValues xlsx file\n"
          + "else : check RGB values of one image and save points of Result, RGBValues txt file\n")
    inputCommand = input("command :")
    if(inputCommand == 'q' or inputCommand == 'Q'):
        print("----------[result]----------")
        print("quit this program\n")
        break
    elif(inputCommand == 'c' or inputCommand == 'C'):
        print("program restart")
        restart()
    elif(inputCommand == 's' or inputCommand == 'S'):
        # Save each R,G,B Channels Separately
        #setting path
        path_split = path.split('/')
        print(path_split)

        path = ""
        for i in path_split:
            if(i == path_split[len(path_split)-1]):
                break
            path += i + "/"
        print("path : "+path)

        #setting name
        name = path_split[len(path_split)-1]
        name_split = name.split('.')
        print(name_split)
        name = "detect_RGB_"+name_split[0]
        print("name : "+name)

        #setting Final Path
        path = path + name
        print("final path : "+path)
        
        imageio.imsave(path + "_r.tiff", r)
        imageio.imsave(path + "_g.tiff", g)
        imageio.imsave(path + "_b.tiff", b)
        imageio.imsave(path + "_rgb.tiff", rgb)
        print("----------[result]----------")
        print("save each R,G,B channels of this image\n")
    elif(inputCommand == 'p' or inputCommand == 'P'):

        #split command to get row, col value
        print("input row col value like below example.")
        rowCol = input("row col / row col / ... : ")
        rowCol_split = rowCol.split('/')
        print(rowCol_split)

        row = []
        col = []
        rgb_value = []
        num = len(rowCol_split)
        cn = num

        for i in range(num):
            rowCol_split_inner = rowCol_split[i].split(' ')
            print("input : "+str(rowCol_split_inner))

            row.append(int(rowCol_split_inner[0]))
            col.append(int(rowCol_split_inner[1]))

            # print(type(int(row)))
            # print(type(int(col)))

            print("----------[result point"+str(i)+"]----------")

            try:
                rgb_value.append(rgb[row[i], col[i], :])
                print("row="+str(row[i])+"/ col="+str(col[i])+" : "+str(rgb_value[i]))
            except Exception as e:
                print("!!!!!WRONG INPUT!!!!!\n")
                print("check Row, Col value of this image")
                print("this [point] have no RGB values")
                print("Erorr contents : ",e)
                print("-------------------------------\n")
                continue

            cn-=1
            print("remain : "+str(cn))  
            print("-------------------------------\n")    


        #show where point did you see
        rgb_drawing = rgb.copy()
        red = (255,0, 0)
        for i in range(num):
            cv2.line(rgb_drawing, (col[i], row[i]), (col[i], row[i]), red, 10)

        size = (600, 800) #3000, 4000
        resized_rgb_drawing = cv2.resize(rgb_drawing, size)
        # dst_resize_rgb_drawing = cv2.cvtColor(resized_rgb_drawing, cv2.COLOR_BGR2RGB)

        # cv2.imshow('result',dst_resize_rgb_drawing)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        parent_path = getParentPath(path)

        img_pil = Image.fromarray(resized_rgb_drawing)
        img_pil.save(parent_path+"_RGBpointsResult.png")
        img_pil.show()

        #save result to xlsx file
        while True:
            print("do you want to save this result to xlsx file?")
            answer = input("y(Y)/n(N) : ")
            if(answer == 'y' or answer == 'Y'):
                # Save each RGB values in xlsx file
                row_data = []
                col_data = []
                r_data = []
                g_data = []
                b_data = []
                for i in range(num):
                    row_data.append(row[i])
                    col_data.append(col[i])
                    r_data.append(rgb_value[i][0])
                    g_data.append(rgb_value[i][1])
                    b_data.append(rgb_value[i][2])

                result_data = pd.DataFrame({
                    'row' : row_data,
                    'col' : col_data,
                    'R' : r_data,
                    'G' : g_data,
                    'B' : b_data
                })
                print(result_data)

                filePath = parent_path+"_RGBValues.xlsx"
                
                result_data.to_excel(filePath, sheet_name='RGBValues')
                print("this result saved in \n"+filePath)
                break
            elif(answer == 'n' or answer == 'N'):
                print("don't save this result")
                break
            else:
                continue
    else:
        try:
            row = int(input("row : "))
            col = int(input("col : "))
            print("----------[result]----------")
            rgb_value = rgb[row, col, :]
            print(rgb_value)
        except:
            print("!!!!!WRONG INPUT!!!!!\n")
            print("check Row, Col value of this image\n")
            continue

        rgb_drawing = rgb.copy()
        red = (255,0, 0)
        cv2.line(rgb_drawing, (col, row), (col, row), red, 10)

        size = (600, 800) #3000, 4000
        resized_rgb_drawing = cv2.resize(rgb_drawing, size)

        img_pil = Image.fromarray(resized_rgb_drawing)
        img_pil.show()

        parent_path = getParentPath(path)
        
        while True:
            print("do you want to save this result to txt file?")
            answer = input("y(Y)/n(N) : ")
            if(answer == 'y' or answer =='Y'):
                result = "File : "+path+"\n"
                result += "row : "+str(row)+" / col : "+str(col)+"\n"
                result += "RGB values : "+str(rgb_value)+"\n"

                # ct = datetime.datetime.now()
                # ct_str = ct.strftime("%Y-%m-%D_%H%M%S")
                filePath = parent_path +"_RGBValues.txt"
                
                file = open(filePath, 'w')
                file.write(result)
                file.close()
                print("this result saved in \n"+filePath)
                break
            elif(answer == 'n' or answer =='N'):
                print("don't save this result")
                break
            else:
                continue
    
# rgb_value = rgb[0, 0, :]
# print(rgb_value)





