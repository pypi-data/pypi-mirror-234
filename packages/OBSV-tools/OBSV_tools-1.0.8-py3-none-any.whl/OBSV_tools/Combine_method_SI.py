from PIL import Image, ImageDraw, ImageFont
import os
#method_dirs [g16 gfn2-xtb ani-2x aiqm1]
#methods [DFT GFN2-xTB ANI-2x AIQM1]
#fignames M1_M2 [M1_frag M2_total M2_bond M2_angle]
#fignames M3 [M3_total M3_bond M3_angle M3_frag]
method_space = 150
type_space = 500
img_width = 1200
img_height = 1200
font = ImageFont.truetype('timesbd.ttf', 99)

def Combine_Image_methods(fignames,figlabels,method_dirs,methodlabels,name='XX'):
    numdirs = len(method_dirs)
    new_img = Image.new('RGB', (img_width*numdirs + type_space, img_height*4 + method_space), (255, 255, 255))
    current_dir = os.getcwd()
    
    for i, dirtmp in enumerate(method_dirs):
        for j, figtmp in enumerate(fignames):
            img = Image.open(os.path.join(current_dir,dirtmp,'pymol',figtmp+'.png'))

            new_img.paste(img, (type_space+i * img_width, method_space+j * img_height))
    # 创建一个新的画布
    draw = ImageDraw.Draw(new_img)
    
    # 添加行头文字
    for i, figlabel in enumerate(figlabels):
        draw.text((10, (i+0.4) * img_height+method_space), figlabel, font=font, fill=(0, 0, 0))

    # 添加列名文字
    for j, methodlabel in enumerate(methodlabels):
        draw.text(((j+0.4) * img_width+type_space, 10), methodlabel, font=font, fill=(0, 0, 0))
    
    # 绘制表格
    for i in range(4):
        draw.line((0, method_space + i * img_height, type_space+img_width*numdirs, method_space+i * img_height), fill=(0, 0, 0), width=5)
    for j in range(numdirs):
        draw.line((type_space + j * img_width, 0, type_space + j * img_width, method_space+img_height*4), fill=(0, 0, 0), width=5)

    new_img.save(name+'.png')
    
def run():
    method_dirs = ['g16','gfn2-xtb','ani-2x','aiqm1']
    method_labels = ['DFT','GFN2-xTB','ANI-2x','AIQM1']
    
    figns = ['M1_frag', 'M2_total', 'M2_bond', 'M2_angle']
    
    figls = ['    M1\n fragment', 'M2 total', 'M2 bond', 'M2 angle']
    
    figns_M3 = ['M3_total', 'M3_bond', 'M3_angle', 'M3_frag']
    
    figls_M3 = ['M3 total', 'M3 bond', 'M3 angle', '    M3\n fragment']
    
    method_ds = []
    method_ls = []
    for i, method_d in enumerate(method_dirs):
        if os.path.exists(method_d):
            method_ds.append(method_d)
            method_ls.append(method_labels[i])
            
    Combine_Image_methods(figns,figls,method_ds,method_ls,'M1_M2')
    
    current_dir = os.getcwd()
    
    if os.path.exists(os.path.join(current_dir,method_ds[0],'pymol','M3_total.png')):
        Combine_Image_methods(figns_M3,figls_M3,method_ds,method_ls,'M3')