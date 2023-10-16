global fontscale
fontscale = 0.8




class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class fontsize:
    title = 30
    subtitle = 24
    label = 20
    clabel = 12
    sublabel = 12
    ticklabel = 16
    colorbarlabel = 18
    colorbarticklabel = 14
    legend = 16
    text = 16




try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from pathlib import Path
    import matplotlib.font_manager as fm
    from matplotlib.colors import LinearSegmentedColormap
    from mpl_toolkits.basemap import Basemap as Bp
    import seaborn as sns
    import numpy as np

    #! UNSOLVE: clevel not match with contourf
    #! UNSOLVE: right or top spines in subplot.twinx() or subplot.twiny() not work


    # 獲取當前檔案位址
    currentfilepath = __file__

    # 刪去__file__中最後面自"\"開始的字串(刪除檔名)
    motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]+'\\resources'
    try: # assert if font files are in the directory
        assert Path(motherpath+"\\futura medium bt.ttf").is_file() and Path(motherpath+"\\Futura Heavy font.ttf").is_file() and Path(motherpath+"\\Futura Extra Black font.ttf").is_file(), f'[FATAL ERROR] Failed to find font files in {motherpath}.\nFailed to activate fontfiles clone.\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'
    except:
        import os
        # go to motherpath
        motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]
        os.chdir(motherpath)
        # check if resources exists
        if os.path.exists(f'{motherpath}\\resources'):
            print(f'[HINT] Font files have been installed in {motherpath} already.')
        else:
        # clone github respository
            os.system(f'git clone https://github.com/VVVICTORZHOU/resources.git')
            print(f'[HINT] Try to clone github font respository into {motherpath}.')
            print(f'[HINT] Make sure the font files are in the directory:\n\t 1. {motherpath}\\resources\\futura medium bt.ttf\n\t 2. {motherpath}\\resources\\Futura Heavy font.ttf\n\t 3. {motherpath}\\resources\\Futura Extra Black font.ttf')
            print(f'\033[93m [HINT] If no, please install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder: {motherpath}. \033[0m')
        try: # assert if font files are in the directory
            motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]+'\\resources'
            assert Path(motherpath+"\\futura medium bt.ttf").is_file() and Path(motherpath+"\\Futura Heavy font.ttf").is_file() and Path(motherpath+"\\Futura Extra Black font.ttf").is_file(), f'[FATAL ERROR] Failed to find font files in {motherpath}.\nFailed to activate fontfiles clone.\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'
        except:
            motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]+'\\resources'
            raise Exception(bcolors.FAIL+f'[FATAL ERROR] Failed to find font files in {motherpath}.\nFailed to activate fontfiles clone.\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'+bcolors.ENDC)

    global fontpath, fontpath_bold, fontpath_black
    assert Path(motherpath+"\\OCR-A.ttf").is_file() and Path(motherpath+"\\OCR-A Regular.ttf").is_file() and Path(motherpath+"\\OCR-A Regular.ttf").is_file(), f'[FATAL ERROR] Failed to find font files in {motherpath}.\nFailed to activate fontfiles clone.\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'
    fontpath = Path(mpl.get_data_path(), motherpath+"\\OCR-A.ttf")
    fontpath_bold = Path(mpl.get_data_path(), motherpath+"\OCR-A Regular.ttf")
    fontpath_black = Path(mpl.get_data_path(), motherpath+"\OCR-A Regular.ttf")



    # 查看系統設置
    def inspectfontfolder():
        # print motherpath in blue
        print('Current font folder path: '+bcolors.OKBLUE+f'{motherpath}'+bcolors.ENDC)
        print(f'[HINT] Make sure the font files are in the directory:\n\t 1. {motherpath}\\futura medium bt.ttf\n\t 2. {motherpath}\\Futura Heavy font.ttf\n\t 3. {motherpath}\\Futura Extra Black font.ttf')

    # 更新
    def upgrade():
        # run pip install --upgrade pymeili in cmd
        import os
        os.system('pip install --upgrade pymeili')

    # 設定字體
    def redirectfontfolder(path):
        # add the 'r' at the beginning of the path to avoid escape character
        path = r''+path
        # 檢查是否需要刪除最後面自"\"開始的字串(刪除檔名)
        if path[-1] == '\\' or path[-1] == '/':
            path = path[:-1]
        
        print(bcolors.WARNING+f'[WARNING] Partial function may not work. \nTry to redirect font folder, but we recommend you to install Futura fonts to {motherpath} instead.'+bcolors.ENDC)
            
        try:
            # check if the font files are in the directory
            if Path(path+"\\futura medium bt.ttf").is_file() and Path(path+"\\Futura Heavy font.ttf").is_file() and Path(path+"\\Futura Extra Black font.ttf").is_file():
                global fontpath, fontpath_bold, fontpath_black
                fontpath = Path(mpl.get_data_path(), path+"\\futura medium bt.ttf")
                fontpath_bold = Path(mpl.get_data_path(), path+"\Futura Heavy font.ttf")
                fontpath_black = Path(mpl.get_data_path(), path+"\Futura Extra Black font.ttf")
                print(f'[INFO] Redirected font folder path: {path}')
            else:
                raise Exception(bcolors.FAIL+f'[FATAL ERROR] Failed to redirect the font folder (Not Found font file in redirected folder).\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'+bcolors.ENDC)
            
        except:
            print('[HINT] Proper redirected font folder path example: C:\\Users\\user\\Desktop\\font')
            print(f'[HINT] Make sure the font files are in the directory:\n\t 1. {path}\\futura medium bt.ttf\n\t 2. {path}\\Futura Heavy font.ttf\n\t 3. {path}\\Futura Extra Black font.ttf')
            raise Exception(bcolors.FAIL+f'[FATAL ERROR] Failed to redirect the font folder. \nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'+bcolors.ENDC)


    # 設定字體默認大小
    def set_fontsize(type, size):
        '''
        type: 'title', 'subtitle', 'label', 'ticklabel', 'legend', 'text', 'sublabel', 'colorbarlabel'
        size: int
        '''
        fontsize.__dict__[type] = size

    # 設定字體縮放比例
    def set_fontscale(scale):
        '''
        set the font scale of subplots
        '''
        global fontscale
        fontscale = scale

    # 設定字體
    def set_fontfamily(fontfamily='futura'):
        global fontpath, fontpath_bold, fontpath_black
        if fontfamily == 'futura' or fontfamily == 'default':
            fontpath = Path(mpl.get_data_path(), motherpath+"\\futura medium bt.ttf")
            fontpath_bold = Path(mpl.get_data_path(), motherpath+"\Futura Heavy font.ttf")
            fontpath_black = Path(mpl.get_data_path(), motherpath+"\Futura Extra Black font.ttf")     
        elif fontfamily == 'ocr':
            assert Path(motherpath+"\\OCR-A.ttf").is_file() and Path(motherpath+"\\OCR-A Regular.ttf").is_file() and Path(motherpath+"\\OCR-A Regular.ttf").is_file(), f'[FATAL ERROR] Failed to find font files in {motherpath}.\nFailed to activate fontfiles clone.\nPlease install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder{motherpath}.'
            fontpath = Path(mpl.get_data_path(), motherpath+"\\OCR-A.ttf")
            fontpath_bold = Path(mpl.get_data_path(), motherpath+"\OCR-A Regular.ttf")
            fontpath_black = Path(mpl.get_data_path(), motherpath+"\OCR-A Regular.ttf")




    # 初始化
    def initplot(style='dark',figsize=(10,8),background=True):
        global theme
        # 小寫化
        style = style.lower()
        if style == 'default'or style == 'light_background' or style == 'light' or style == 'l':
            theme = 'default'
            plt.style.use(theme)
        elif style == 'dark_background' or style == 'dark' or style == 'd':
            theme = 'dark_background'
            plt.style.use(theme)
        
        
        # size
        plt.rcParams['figure.figsize'] = figsize


        # 設定facecolor
        if background == True:
            plt.gca().set_facecolor(colorlist('bg'))
        elif background == 'bg1':
            plt.gca().set_facecolor(colorlist('bg1'))
        elif background == 'bg2':
            plt.gca().set_facecolor(colorlist('bg2'))
        elif background == 'bg3':
            plt.gca().set_facecolor(colorlist('bg3'))
        else: pass

        return plt.gcf(), plt.gca()

    # 設定圖內顏色
    def set_backgroundcolor(color='bg'):
        if type(color) != bool:
            plt.gca().set_facecolor(colorlist(color))
        elif color == False:
            plt.gca().set_facecolor('none')
        else:
            plt.gca().set_facecolor(colorlist('bg'))

    # 設定圖外顏色
    def set_framecolor(color=False):
        if type(color) != bool:
            plt.gcf().set_facecolor(colorlist(color))
        elif color == False:
            plt.gcf().set_facecolor('none')
        else:
            plt.gcf().set_facecolor(colorlist('rfg'))

    # 色票(顏色選用優先級)
    def colorlist(index):
        if type(index) == list:
            # 判斷是否所有元素都in
            if all(i in ['bg', 'bg1', 'bg2','bg3', 'fg', '1', '2', '3', '4', 'rfg'] for i in index):
                return [colorseries[i] for i in index]
            else:
                return index
        else:
            str(index)
            if index in ['bg', 'bg1', 'bg2', 'bg3', 'fg', '1', '2', '3', '4', 'rfg']:
                try:    
                    if theme == 'default':
                        colorseries = {'bg': '#080911',
                                    'bg1': '#080911',
                                    'bg2': '#080911',
                                    'bg3': '#333334',
                                    'rfg': '#080808',
                                    'fg': '#EEEEEE',
                                    '1': '#11FFFF',
                                    '2': '#F80AF8',
                                    '3': '#FCC716',
                                    '4': '#D40508',
                                    '5': '#0DFF0E'}  
                        return colorseries[index]
                                    
                    elif theme == 'dark_background':
                        colorseries = {'bg': '#080911',
                                    'bg1': '#080911',
                                    'bg2': '#080911',
                                    'bg3': '#333334',
                                    'rfg': '#080808',
                                    'fg': '#EEEEEE',
                                    '1': '#11FFFF',
                                    '2': '#F80AF8',
                                    '3': '#FCC716',
                                    '4': '#D40508',
                                    '5': '#0DFF0E'}  
                        return colorseries[index]
                                        

                except: # NameError: name 'theme' is not defined
                    raise Exception(bcolors.WARNING+'Please run initplot() first.'+bcolors.ENDC)
                    
            else:
                return index



    def cmaplist(index):
        # 如果index是list
        if type(index) == list:
            print('[HINT] Detected self-defined colormap list.')
            return LinearSegmentedColormap.from_list('mycmap', index)
        else:
            str(index)
            if index in ['-28','28','-27','-26','-25','-24','-23','-22','22','23','24','25','26','27','12','13','14','15','-12','-13','-14','-15','33','34','35','36','37','38','39','-33','-34','-35','-36','-37','-38','-39','43','44','45','46','47','48','49','-43','-44','-45','-46','-47','-48','-49']:
                try:
                    if theme == 'default':
                        if index == '15':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#47A7DE','#D5EDD5','#E08A16','#AB503B'])
                        if index == '14':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#47A7DE','#E08A16','#AB503B'])
                        if index == '13':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#D5EDD5','#AB503B'])
                        if index == '12':
                            return LinearSegmentedColormap.from_list('mycmap', ['#47A7DE','#E08A16'])

                        if index == '-15': # reversed 1
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#E08A16','#D5EDD5','#47A7DE','#454FB4'])
                        if index == '-14': # reversed 1 but 4 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#E08A16','#47A7DE','#454FB4'])
                        if index == '-13': # reversed 1 but 3 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#D5EDD5','#454FB4'])
                        if index == '-12': # reversed 1 but 2 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#E08A16','#47A7DE'])

                        if index == '28':
                            return LinearSegmentedColormap.from_list('mycmap', ['#D9EEFD','#FFFFFF','#FFFFFF','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E','#BB8263'])        
                        if index == '27':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E','#BB8263'])
                        if index == '26':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E'])
                        if index == '25':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F'])
                        if index == '24':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A'])
                        if index == '23':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4'])
                        if index == '22':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF'])

                        if index == '-28': # reversed 2
                            return LinearSegmentedColormap.from_list('mycmap', ['#BB8263','#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#FFFFFF','#FFFFFF','#D9EEFD']) 
                        if index == '-27': # reversed 2
                            return LinearSegmentedColormap.from_list('mycmap', ['#BB8263','#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE','#EEEEEE'])
                        if index == '-26': # reversed 2 but 6 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-25':
                            return LinearSegmentedColormap.from_list('mycmap', ['#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-24':
                            return LinearSegmentedColormap.from_list('mycmap', ['#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-23':
                            return LinearSegmentedColormap.from_list('mycmap', ['#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-22':
                            return LinearSegmentedColormap.from_list('mycmap', ['#F2CABF','#EEEEEE'])
                        
                        if index == '39':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438','#E9A82E','#EA6D0B'])
                        if index == '38':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438','#E9A82E'])
                        if index == '37':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438'])
                        if index == '36':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE'])
                        if index == '35':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5'])
                        if index == '34':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED'])
                        if index == '33':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B'])
                        
                        if index == '-39': 
                            return LinearSegmentedColormap.from_list('mycmap', ['#EA6D0B','#E9A82E','#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-38':
                            return LinearSegmentedColormap.from_list('mycmap', ['#E9A82E','#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-37':
                            return LinearSegmentedColormap.from_list('mycmap', ['#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-36':
                            return LinearSegmentedColormap.from_list('mycmap', ['#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-35':
                            return LinearSegmentedColormap.from_list('mycmap', ['#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-34':
                            return LinearSegmentedColormap.from_list('mycmap', ['#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-33':
                            return LinearSegmentedColormap.from_list('mycmap', ['#5E9C5B','#BCEDAC','#EEEEEE'])
                        
                        if index == '49': # 18色
                            return LinearSegmentedColormap.from_list('mycap', ['#2D889B','#5CA9BB','#86CAD7','#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402','#A164AA','#845098'])
                        if index == '48': # 16色
                            return LinearSegmentedColormap.from_list('mycap', ['#2D889B','#5CA9BB','#86CAD7','#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402'])
                        if index == '47': # 13色
                            return LinearSegmentedColormap.from_list('mycap', ['#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402'])
                        if index == '46': # 11色
                            return LinearSegmentedColormap.from_list('mycap', ['#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D'])
                        if index == '45': # 9色
                            return LinearSegmentedColormap.from_list('mycap', ['#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D'])
                        if index == '44': # 7色
                            return LinearSegmentedColormap.from_list('mycap', ['#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237'])
                        if index == '43': # 5色
                            return LinearSegmentedColormap.from_list('mycap', ['#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905'])
                        
                        if index == '-49':
                            return LinearSegmentedColormap.from_list('mycap', ['#845098','#A164AA','#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249','#86CAD7','#5CA9BB','#2D889B'])
                        if index == '-48':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249','#86CAD7','#5CA9BB','#2D889B'])
                        if index == '-47':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249'])
                        if index == '-46':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A'])
                        if index == '-45':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890'])
                        if index == '-44':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463'])
                        if index == '-43':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905'])
                        
                        
                                                                           
                                                                         

                        
                    
                    
                    elif theme == 'dark_background':
                        if index == '15':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#47A7DE','#D5EDD5','#E08A16','#AB503B'])
                        if index == '14':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#47A7DE','#E08A16','#AB503B'])
                        if index == '13':
                            return LinearSegmentedColormap.from_list('mycmap', ['#454FB4','#D5EDD5','#AB503B'])
                        if index == '12':
                            return LinearSegmentedColormap.from_list('mycmap', ['#47A7DE','#E08A16'])

                        if index == '-15': # reversed 1
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#E08A16','#D5EDD5','#47A7DE','#454FB4'])
                        if index == '-14': # reversed 1 but 4 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#E08A16','#47A7DE','#454FB4'])
                        if index == '-13': # reversed 1 but 3 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#AB503B','#D5EDD5','#454FB4'])
                        if index == '-12': # reversed 1 but 2 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#E08A16','#47A7DE'])
                                
                        if index == '28':
                            return LinearSegmentedColormap.from_list('mycmap', ['#D9EEFD','#FFFFFF','#FFFFFF','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E','#BB8263'])        
                        if index == '27':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E','#BB8263'])
                        if index == '26':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F','#CF725E'])
                        if index == '25':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A','#DB997F'])
                        if index == '24':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4','#DCB29A'])
                        if index == '23':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF','#F1C9B4'])
                        if index == '22':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#F2CABF'])
                        
                        if index == '-28': # reversed 2
                            return LinearSegmentedColormap.from_list('mycmap', ['#BB8263','#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#FFFFFF','#FFFFFF','#D9EEFD']) 
                        if index == '-27': # reversed 2
                            return LinearSegmentedColormap.from_list('mycmap', ['#BB8263','#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-26': # reversed 2 but 6 colors
                            return LinearSegmentedColormap.from_list('mycmap', ['#CF725E','#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-25':
                            return LinearSegmentedColormap.from_list('mycmap', ['#DB997F','#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-24':
                            return LinearSegmentedColormap.from_list('mycmap', ['#DCB29A','#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-23':
                            return LinearSegmentedColormap.from_list('mycmap', ['#F1C9B4','#F2CABF','#EEEEEE'])
                        if index == '-22':
                            return LinearSegmentedColormap.from_list('mycmap', ['#F2CABF','#EEEEEE'])
                        
                        if index == '39':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438','#E9A82E','#EA6D0B'])
                        if index == '38':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438','#E9A82E'])
                        if index == '37':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE','#760438'])
                        if index == '36':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5','#E90EDE'])
                        if index == '35':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED','#0C04D5'])
                        if index == '34':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B','#66B5ED'])
                        if index == '33':
                            return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#BCEDAC','#5E9C5B'])
                        
                        if index == '-39': 
                            return LinearSegmentedColormap.from_list('mycmap', ['#EA6D0B','#E9A82E','#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-38':
                            return LinearSegmentedColormap.from_list('mycmap', ['#E9A82E','#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-37':
                            return LinearSegmentedColormap.from_list('mycmap', ['#760438','#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-36':
                            return LinearSegmentedColormap.from_list('mycmap', ['#E90EDE','#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-35':
                            return LinearSegmentedColormap.from_list('mycmap', ['#0C04D5','#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-34':
                            return LinearSegmentedColormap.from_list('mycmap', ['#66B5ED','#5E9C5B','#BCEDAC','#EEEEEE'])
                        if index == '-33':
                            return LinearSegmentedColormap.from_list('mycmap', ['#5E9C5B','#BCEDAC','#EEEEEE'])
                        
                        if index == '49': # 18色
                            return LinearSegmentedColormap.from_list('mycap', ['#2D889B','#5CA9BB','#86CAD7','#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402','#A164AA','#845098'])
                        if index == '48': # 16色
                            return LinearSegmentedColormap.from_list('mycap', ['#2D889B','#5CA9BB','#86CAD7','#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402'])
                        if index == '47': # 13色
                            return LinearSegmentedColormap.from_list('mycap', ['#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D','#B10239','#740402'])
                        if index == '46': # 11色
                            return LinearSegmentedColormap.from_list('mycap', ['#0E9249','#31A054','#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D'])
                        if index == '45': # 9色
                            return LinearSegmentedColormap.from_list('mycap', ['#61BA6A','#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237','#ED175D'])
                        if index == '44': # 7色
                            return LinearSegmentedColormap.from_list('mycap', ['#99CF7B','#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905','#F05237'])
                        if index == '43': # 5色
                            return LinearSegmentedColormap.from_list('mycap', ['#CAE890','#EFEA98','#EFC463','#EB9D39','#DE7905'])
                        if index == '-49':
                            return LinearSegmentedColormap.from_list('mycap', ['#845098','#A164AA','#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249','#86CAD7','#5CA9BB','#2D889B'])
                        if index == '-48':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249','#86CAD7','#5CA9BB','#2D889B'])
                        if index == '-47':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A','#31A054','#0E9249'])
                        if index == '-46':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890','#99CF7B','#61BA6A'])
                        if index == '-45':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463','#EFEA98','#CAE890'])
                        if index == '-44':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905','#EB9D39','#EFC463'])
                        if index == '-43':
                            return LinearSegmentedColormap.from_list('mycap', ['#740402','#B10239','#ED175D','#F05237','#DE7905'])
                        
                except: # NameError: name 'theme' is not defined
                    raise Exception(bcolors.WARNING+'Please run initplot() first.'+bcolors.ENDC)
            else: 
                return index




    # LABEL設定
    '''
    默認下系統會在使用者繪製不同種類的圖形添加LABEL計數，依種類分開計數，無法在圖例中顯示出來的LABEL不用計數；使用者依然可以手動為LABEL賦值進行覆蓋
    '''
    # 點狀圖
    SCATTERNO = 0
    # 折線圖
    PLOTNO = 0
    # 直方圖
    HISTNO = 0
    # 橫向長條圖
    BARHNO = 0
    # 縱向長條圖
    BARNO = 0

    def getSCATTERNO():
        global SCATTERNO
        SCATTERNO += 1
        label = 'SCATTER'+str(SCATTERNO)
        return label

    def getPLOTNO():
        global PLOTNO
        PLOTNO += 1
        label = 'PLOT'+str(PLOTNO)
        return label

    def getHISTNO():
        global HISTNO
        HISTNO += 1
        label = 'HIST'+str(HISTNO)
        return label

    def getBARHNO():
        global BARHNO
        BARHNO += 1
        label = 'BARH'+str(BARHNO)
        return label

    def getBARNO():
        global BARNO
        BARNO += 1
        label = 'BAR'+str(BARNO)
        return label


    # 存檔
    def savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0.1, transparent=False):
        plt.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches,transparent=transparent)

    # 標題
    def title(title, color='fg', font=fontpath_bold, fontsize=fontsize.title):
        plt.suptitle(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize))

    def lefttitle(title, loc='left', color='1', font=fontpath_bold, fontsize=fontsize.subtitle):
        plt.title(title, loc=loc, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize))

    def righttitle(title, loc='right', color='2', font=fontpath_bold, fontsize=fontsize.subtitle):
        plt.title(title, loc=loc, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize))

    # scatter繪圖
    def scatter(x, y, color='fg', size=3, marker='o', linewidth=None, label=getSCATTERNO(), linestyle='-', **kwargs):
        plt.scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)

    # plot繪圖
    def plot(x, y, color='fg', linewidth=2, linestyle='-', label=getPLOTNO(),**kwargs):
        plt.plot(x, y, color=colorlist(color), linewidth=linewidth, label=label,linestyle=linestyle, **kwargs)

    # boxplot繪圖
    def boxplot(x, vert=True, patch_artist=True, showmeans = True, showcaps = True, showbox = True, widths = 0.5, boxfacecolor='1', boxcolor='fg', boxlinewidth=3, capcolor='fg', caplinewidth=3, whiskercolor='fg', whiskerlinewidth=3, fliercolor='fg', fliermarkeredgecolor='fg', flierlinewidth=3, mediancolor='fg', medianlinewidth=3, meancolor='fg', meanmarker='D', meanmarkeredgecolor='fg', meanmarkerfacecolor='2', meansize=20, meanmarkeredgewidth=3, **kwargs):
        plt.boxplot(x, vert=vert, patch_artist=patch_artist, showmeans = showmeans, showcaps = showcaps, showbox = showbox, widths = widths, boxprops=dict(facecolor=colorlist(boxfacecolor), color=colorlist(boxcolor), linewidth = boxlinewidth), capprops=dict(color=colorlist(capcolor), linewidth = caplinewidth), whiskerprops=dict(color=colorlist(whiskercolor), linewidth = whiskerlinewidth), flierprops=dict(color=colorlist(fliercolor), markeredgecolor=colorlist(fliermarkeredgecolor), linewidth = flierlinewidth), medianprops=dict(color=colorlist(mediancolor), linewidth = medianlinewidth), meanprops=dict(marker=meanmarker, markeredgecolor=colorlist(meanmarkeredgecolor), markerfacecolor=colorlist(meanmarkerfacecolor), markersize=meansize, markeredgewidth = meanmarkeredgewidth), **kwargs)

    # polar繪圖
    def polar(theta, r, color='fg', linewidth=2, linestyle='-', label=getPLOTNO(),**kwargs):
        plt.polar(theta, r, color=colorlist(color), linewidth=linewidth, label=label,linestyle=linestyle, **kwargs)

    # contour繪圖
    def contour(x, y, z, colors='fg', levels=10, linewidths=2, clabel=True, fontsize=fontsize.clabel, color='fg', **kwargs):
        CS = plt.contour(x, y, z, colors=colorlist(colors), levels=levels, linewidths=linewidths, **kwargs)
        if clabel == True:
            CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True, levels=levels, **kwargs)
            for t in CL:
                t.set_fontproperties(fm.FontProperties(fname=fontpath, size=10*fontscale))

    # 機率密度函數繪圖
    def PDFplot(x, color='fg', linewidth=2, linestyle='-', label=getPLOTNO(),**kwargs):
        sns.kdeplot(x, color=colorlist(color), linewidth=linewidth, label=label,linestyle=linestyle, **kwargs)


    # contourf繪圖
    def contourf(x, y, z, levels=10, cmap='28', contour=True, clabel=True,linewidths=1.5, color='fg', vmin='auto', vmax='auto', fontsize=fontsize.clabel, **kwargs):
        import numpy as np
        # 傳出Z值和levels值
        global contour_vmin, contour_vmax, contour_levels
        contour_levels = levels
        if vmin == 'auto':
            vmin = np.floor(z.min()/10**(len(str(int(z.min())))-2))*10**(len(str(int(z.min())))-2)
            contour_vmin = vmin
        else:
            contour_vmin = vmin
        if vmax == 'auto':
            vmax = np.ceil(z.max()/10**(len(str(int(z.max())))-2))*10**(len(str(int(z.max())))-2)
            contour_vmax = vmax
        else:
            contour_vmax = vmax
        
        if contour == True:
            CS = plt.contour(x, y, z, colors=colorlist(color), levels=levels, linewidths=linewidths)
        if clabel == True:
            CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True)
            for t in CL:
                t.set_fontproperties(fm.FontProperties(fname=fontpath, size=fontsize))
        plt.contourf(x, y, z, cmap=cmaplist(cmap), vmin=vmin, vmax=vmax, levels=levels, **kwargs)



    # colorbar顯示
    def colorbar(label=' ', orientation='vertical',shrink=0.95, aspect=10, fraction=0.046, pad=0.04, labelfontsize=fontsize.colorbarlabel, tickfontsize=fontsize.colorbarticklabel, font=fontpath, color='fg', extend='neither',**kwargs):
        if orientation == 'v' or 'V':
            orientation = 'vertical'
        elif orientation == 'h' or 'H':
            orientation = 'horizontal'

        CB = plt.colorbar(orientation=orientation, shrink=shrink, aspect=aspect, label=label, fraction=fraction, pad=pad, extend=extend, **kwargs)
        CB.ax.tick_params(labelsize=labelfontsize, labelcolor=colorlist(color), color=colorlist(color))
        CB.ax.set_ylabel(label, fontproperties=fm.FontProperties(fname=font, size=labelfontsize), color=colorlist(color))
        CB.ax.yaxis.set_tick_params(color=colorlist(color), labelcolor=colorlist(color))
        CB.outline.set_color(colorlist(color))
        CB.outline.set_linewidth(2)
        CB.ax.yaxis.label.set_font_properties(fm.FontProperties(fname = font, size = labelfontsize))
        CB.outline.set_linewidth(2)
        for l in CB.ax.yaxis.get_ticklabels():
            l.set_fontproperties(fm.FontProperties(fname = font, size = tickfontsize))

    def clim(vmin, vmax):
        plt.clim(vmin, vmax)

    # 直方圖
    def hist(x, bins=5, color='1', edgecolor='fg', linewidth=3, label=getHISTNO(), **kwargs):
        plt.hist(x, bins=bins, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label,**kwargs)

    def hist2d(x, y, bins=5, cmap='2', **kwargs):
        plt.hist2d(x, y, bins=bins, cmap=cmaplist(cmap), **kwargs)

    # 橫向長條圖
    def barh(x, y, width=0.8, color='1', edgecolor='fg', linewidth=3, label=getBARHNO(), **kwargs):
        plt.barh(x, y, height=width, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)

    # 縱向長條圖
    def bar(x, y, width=0.8, color='1', edgecolor='fg', linewidth=3, label=getBARNO(), **kwargs):
        plt.bar(x, y, width=width,color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)

    # 圓餅圖
    def pie(x, labels=None, colors=None, explode=None, autopct=None, shadow=False, startangle=90, pctdistance=0.6, labeldistance=1.1, radius=1, labelfontsize=16, labelfontcolor='fg', widgefontsize=16, widgefontcolor='fg', counterclock=True, edgecolor='fg',linewidth=3, linestyle='-', antialiased=False,textprops=None, center=(0, 0), frame=False, rotatelabels=False, **kwargs):
        PW, PT, PA = plt.pie(x, labels=labels, colors=colorlist(colors), explode=explode, autopct=autopct, shadow=shadow, startangle=startangle, pctdistance=pctdistance, labeldistance=labeldistance, radius=radius, counterclock=counterclock, wedgeprops={"edgecolor":colorlist(edgecolor),'linewidth': linewidth, 'linestyle': linestyle, 'antialiased': antialiased}, textprops=textprops, center=center, frame=frame, rotatelabels=rotatelabels, **kwargs)
        # PW: Widges, PT: Texts, PA: Autopct
        # 設定圓餅圖文字
        for t in PT:
            t.set_fontproperties(fm.FontProperties(fname=fontpath, size=labelfontsize))
            t.color = colorlist(labelfontcolor)
        # 設定圓餅圖百分比
        for t in PA:
            t.set_fontproperties(fm.FontProperties(fname=fontpath, size=widgefontsize))
            t.color = colorlist(widgefontcolor)

    # 表格
    def table(cellText, rowLabels=None, colLabels=None, rowcolor='rfg', colcolor='rfg', rowLoc='right', colLoc='center', loc='center', cellLoc='center', cellcolor='rfg', cellFontsize=16, cellFontcolor='fg', rowLabelsFontsize=16, rowLabelsFontcolor='fg', colLabelsFontsize=16, colLabelsFontcolor='fg', edgecolor='fg', **kwargs):
        # set cellcolors (must have 1 row at least)
        if type(cellcolor) == list:
            if len(cellcolor) == 1:
                cellcolors = [[colorlist(cellcolor[0]) for i in range(len(cellText[0]))]]
            else:
                cellcolors = [[colorlist(cellcolor[i]) for i in range(len(cellText[0]))]]
        else:
            cellcolors = [[colorlist(cellcolor) for i in range(len(cellText[0]))]]
        colcolors = [colorlist(colcolor) for i in range(len(cellText[0]))]
        rowcolors = [colorlist(rowcolor) for i in range(len(cellText))]
        TB = plt.table(cellText, rowLabels=rowLabels, colLabels=colLabels, rowColours=rowcolors, colColours=colcolors, rowLoc=rowLoc, colLoc=colLoc, loc=loc, cellLoc=cellLoc, cellColours=cellcolors,**kwargs)
        TB.auto_set_font_size(False)
        TB.set_fontsize(cellFontsize)
        TB.auto_set_column_width(col=list(range(len(cellText[0]))))
        for k, cell in TB.get_celld().items():
            cell.set_edgecolor(colorlist(edgecolor))
            cell.set_text_props(fontproperties=fm.FontProperties(fname=fontpath_bold, size=cellFontsize), color=colorlist(cellFontcolor))
            if k[0] == 0:
                cell.set_text_props(fontproperties=fm.FontProperties(fname=fontpath_bold, size=rowLabelsFontsize))
                cell.set_text_props(color=colorlist(rowLabelsFontcolor))
            if k[1] == -1: #
                cell.set_text_props(fontproperties=fm.FontProperties(fname=fontpath_bold, size=colLabelsFontsize))
                cell.set_text_props(color=colorlist(colLabelsFontcolor))    
            print(k,cell)

        TB.scale(2, 2.5)
        plt.axis('off')

    # 標籤
    def xlabel(xlabel, color='fg', font=fontpath, fontsize=fontsize.label, **kwargs):
        plt.xlabel(xlabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
    def ylabel(ylabel, color='fg', font=fontpath, fontsize=fontsize.label, **kwargs):
        plt.ylabel(ylabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

    # 刻度
    def xticks(ticks, labels, color='fg', font=fontpath, fontsize=fontsize.ticklabel, **kwargs):
        plt.xticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
    def yticks(ticks, labels, color='fg', font=fontpath, fontsize=fontsize.ticklabel, **kwargs):
        plt.yticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
    def xyticks(xticks, xlabels, yticks, ylabels, color='fg', font=fontpath, fontsize=fontsize.ticklabel, **kwargs):
        plt.xticks(xticks, xlabels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        plt.yticks(yticks, ylabels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

    # 限制
    def xlim(xmin=None, xmax=None, **kwargs):
        plt.xlim(xmin, xmax, **kwargs)
    def ylim(ymin=None, ymax=None, **kwargs):
        plt.ylim(ymin, ymax, **kwargs)
    def xylim(xmin=None, xmax=None, ymin=None, ymax=None, **kwargs):
        plt.xlim(xmin, xmax, **kwargs)
        plt.ylim(ymin, ymax, **kwargs)

    # 畫指數
    def xscale(scale, **kwargs):
        plt.xscale(scale, **kwargs)
    def yscale(scale, **kwargs):
        plt.yscale(scale, **kwargs)

    def xlog(base=10, **kwargs):
        plt.xscale('log', base=base, **kwargs)
    def ylog(base=10, **kwargs):
        plt.yscale('log', base=base, **kwargs)

    # 畫網格
    def grid(b=None, which='major', axis='both', color='fg', linestyle=':', linewidth=1, **kwargs):
        plt.grid(b, which=which, axis=axis, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)

    # spines
    def spines(top=True, right=True, bottom=True, left=True, color='fg', linewidth=3, tickslength = 5,**kwargs):
        if top: plt.gca().spines['top'].set_visible(top)
        if right: plt.gca().spines['right'].set_visible(right)
        if bottom: plt.gca().spines['bottom'].set_visible(bottom)
        if left: plt.gca().spines['left'].set_visible(left)
        if top: plt.gca().spines['top'].set_color(colorlist(color))
        if right: plt.gca().spines['right'].set_color(colorlist(color))
        if bottom: plt.gca().spines['bottom'].set_color(colorlist(color))
        if left: plt.gca().spines['left'].set_color(colorlist(color))
        if top: plt.gca().spines['top'].set_linewidth(linewidth)
        if right: plt.gca().spines['right'].set_linewidth(linewidth)
        if bottom: plt.gca().spines['bottom'].set_linewidth(linewidth)
        if left: plt.gca().spines['left'].set_linewidth(linewidth)
        plt.gca().tick_params(axis='x', colors=colorlist(color), width=linewidth, length=tickslength)
        plt.gca().tick_params(axis='y', colors=colorlist(color), width=linewidth, length=tickslength)
        

    # hide spines
    def hidespines(top=True, right=True, bottom=True, left=True):
        if top: plt.gca().spines['top'].set_visible(False)
        if right: plt.gca().spines['right'].set_visible(False)
        if bottom: plt.gca().spines['bottom'].set_visible(False)
        if left: plt.gca().spines['left'].set_visible(False)

    # hide ticks
    def hideticks(top=True, right=True, bottom=True, left=True):
        if top: plt.gca().tick_params(axis='x', top=False)
        if right: plt.gca().tick_params(axis='y', right=False)
        if bottom: plt.gca().tick_params(axis='x', bottom=False)
        if left: plt.gca().tick_params(axis='y', left=False)

    # hide ticks label
    def hidetickslabel(top=True, right=True, bottom=True, left=True):
        if top: plt.gca().tick_params(axis='x', labeltop=False)
        if right: plt.gca().tick_params(axis='y', labelright=False)
        if bottom: plt.gca().tick_params(axis='x', labelbottom=False)
        if left: plt.gca().tick_params(axis='y', labelleft=False)

    # 挪動坐標軸
    def xaxisposition(yposition, xaxis='bottom', **kwargs):
        plt.gca().xaxis.set_ticks_position(xaxis)
        plt.gca().spines[xaxis].set_position(('data', yposition))

    def yaxisposition(xposition, yaxis='left', **kwargs):
        plt.gca().yaxis.set_ticks_position(yaxis)
        plt.gca().spines[yaxis].set_position(('data', xposition))

    # 開啟所有坐標軸
    def ticksall(labeltop=True, labelright=True, labelleft=True, labelbottom=True):
        if labeltop: plt.tick_params(top=True, labeltop=True)
        if labelright: plt.tick_params(right=True, labelright=True)
        if labelleft: plt.tick_params(left=True, labelleft=True)
        if labelbottom: plt.tick_params(bottom=True, labelbottom=True)

    # axhline 水平線
    def axhline(y=0, color='fg', linestyle='dashed', linewidth=3, **kwargs):
        plt.axhline(y=y, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)

    # axvline 垂直線
    def axvline(x=0, color='fg', linestyle='dashed', linewidth=3, **kwargs):
        plt.axvline(x=x, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)

    # 圖例legend
    def legend(loc='best', fontsize=fontsize.legend, labelcolor='fg', frameon=True, framealpha=1, facecolor='rfg', edgecolor='fg', edgewidth=2 ,roundedge=False, **kwargs):
        LG = plt.gca().legend(loc=loc, fontsize=fontsize, labelcolor=colorlist(labelcolor), frameon=frameon, framealpha=framealpha, prop=fm.FontProperties(fname=fontpath, size=fontsize), facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor), **kwargs)
        if roundedge == False:
            LG.get_frame().set_boxstyle('Round', pad=0.2, rounding_size=-0.01)
        LG.get_frame().set_linewidth(edgewidth)

    # 文字
    def text(x, y, text, color='fg', font=fontpath, fontsize=fontsize.text, **kwargs):
        plt.text(x, y, text, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

    # 帶有標籤的文字
    '''
    標籤為反白的文字，背景需為鋪色矩形
    '''
    def labeltext(x, y, w, h,label='LABEL TEXT', text='NORMAL TEXT', color='2', font=fontpath, fontsize=fontsize.text, **kwargs):
        # 先繪製label的矩形背景
        plt.gca().add_patch(plt.Rectangle((x-0.05*w, y-0.1*h), width=w, height=h, color=colorlist(color), alpha=1))
        # 再繪製label文字於矩形中
        plt.text(x, y, label, color='#EEEEEE', fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        # 在label之後繪製text文字
        plt.text(x+w, y, text, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

    def annotate(text, xy, xytext, arrowcolor='fg', color='fg', font=fontpath, fontsize=fontsize.text, **kwargs):
        plt.annotate(text, xy, xytext, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), arrowprops=dict(arrowstyle="->", color=colorlist(arrowcolor), connectionstyle="arc3,rad=.2"), **kwargs)

    def fill_between(x, y1, y2, color='3', alpha=0.5, **kwargs):
        plt.fill_between(x, y1, y2, color=colorlist(color), alpha=alpha, **kwargs)

    def fill_betweenx(y, x1, x2, color='3', alpha=0.5, **kwargs):
        plt.fill_betweenx(y, x1, x2, color=colorlist(color), alpha=alpha, **kwargs)

    def invert_xaxis():
        plt.gca().invert_xaxis()

    def invert_yaxis():
        plt.gca().invert_yaxis()

    def twinx(color='fg', linewidth=3, tickslength = 5, **kwargs):
        # print the cautions of twinx and twiny
        print(bcolors.WARNING+'[WARNING] Some bugs have been reported when using twinx() or twiny().'+bcolors.ENDC)
        plt.gca().tick_params(axis='y', top=True, colors=colorlist(color), width=linewidth, length=tickslength)
        plt.twinx(**kwargs)
        

    def twiny(color='fg', linewidth=3, tickslength = 5, **kwargs):
        # print the cautions of twinx and twiny
        print(bcolors.WARNING+'[WARNING] Some bugs have been reported when using twinx() or twiny().'+bcolors.ENDC)
        plt.twiny(**kwargs)
        plt.gca().tick_params(axis='x', right=True, colors=colorlist(color), width=linewidth, length=tickslength)

    def tight_layout(**kwargs):
        plt.tight_layout(**kwargs)

    def gcf():
        return plt.gcf()
    
    def gca():
        return plt.gca()


    # 設定尺寸
    def figsize(width, height):
        plt.rcParams['figure.figsize'] = width, height

    # 顯示
    def show():
        plt.show()

    # 清除
    def clf():
        plt.clf()

    # 關閉
    def close():
        plt.close()

    def figure():
        plt.figure()

    # 圖像處理
    def imread(filename, format=None):
        return plt.imread(filename, format=format)

    def imshow(X, cmap='28', vmin=None, vmax=None, interpolation='nearest', alpha=None, aspect=None, **kwargs):
        plt.imshow(X, cmap=cmaplist(cmap), vmin=vmin, vmax=vmax, interpolation=interpolation, alpha=alpha, aspect=aspect, **kwargs)

    def imsave(filename, arr, vmin=None, vmax=None, cmap='2', format=None, origin=None, dpi=300, **kwargs):
        plt.imsave(filename, arr, vmin=vmin, vmax=vmax, cmap=cmaplist(cmap), format=format, origin=origin, dpi=dpi, **kwargs)

    # 重設值
    def set_xydata(x=None, y=None):
        if x != None:
            plt.gca().set_xdata(x)
        if y != None:
            plt.gca().set_ydata(y)


    # add logo
    def addlogo(logopath, x, y, width, height, alpha=1, **kwargs):
        plt.imshow(logopath, extent=[x, x+width, y, y+height], alpha=alpha, **kwargs)

    # font
    def fontprop(fontsize, **kwargs):
        if kwargs == {}:
            return fm.FontProperties(fname=fontpath, size=fontsize)
        else:
            # 如果傳入fontpath，則使用傳入的fontpath
            if 'fontpath' in kwargs:
                # 檢查傳入的fontpath是否存在
                if os.path.isfile(kwargs['fontpath']):
                    fpath = Path(mpl.get_data_path(), kwargs['fontpath'])
                    return fm.FontProperties(fname=fpath, size=fontsize)
                else:
                    print(bcolors.WARNING+'[WARNING] The fontpath given cannot not be found when using fontprop(), using default fontpath.'+bcolors.ENDC)
                    return fm.FontProperties(fname=fontpath, size=fontsize)
            else:
                print(bcolors.WARNING+'[WARNING] Invalid argument given when using fontprop(), using default fontpath.'+bcolors.ENDC)
                return fm.FontProperties(fname=fontpath, size=fontsize)


    # Basemap系列
    class Basemap():
        import numpy as np
        def __init__(self,projection='cyl', llcrnrlon=0, llcrnrlat=0, urcrnrlon=0, urcrnrlat=0, resolution='l', area_thresh=1000, zone=None,**kwargs):
            self.projection = projection # merc:麥卡托, cyl:等距圓柱, mill:米勒, cea:等距圓錐, gall:加爾-彼得, lcc:蘭伯特等角, tmerc:橫麥卡托, stere:極射, npstere:北極極射, spstere:南極極射, aeqd:等距方位, poly:多邊形, nsper:自然地球
            if zone == 'taiwan':
                self.llcrnrlat = 21.5
                self.llcrnrlon = 118
                self.urcrnrlat = 26.5
                self.urcrnrlon = 123
            elif zone == 'china':
                self.llcrnrlat = 18
                self.llcrnrlon = 73
                self.urcrnrlat = 54
                self.urcrnrlon = 135
            elif zone == 'japan':
                self.llcrnrlat = 20
                self.llcrnrlon = 120
                self.urcrnrlat = 50
                self.urcrnrlon = 150
            elif zone == 'korea':
                self.llcrnrlat = 30
                self.llcrnrlon = 115
                self.urcrnrlat = 45
                self.urcrnrlon = 135
            elif zone == 'usa':
                self.llcrnrlat = 20
                self.llcrnrlon = -130
                self.urcrnrlat = 50
                self.urcrnrlon = -60
            elif zone == 'europe':
                self.llcrnrlat = 30
                self.llcrnrlon = -15
                self.urcrnrlat = 70
                self.urcrnrlon = 45
            elif zone == 'world':
                self.llcrnrlat = -90
                self.llcrnrlon = -180
                self.urcrnrlat = 90
                self.urcrnrlon = 180
            elif zone == 'africa':
                self.llcrnrlat = -40
                self.llcrnrlon = -20
                self.urcrnrlat = 40
                self.urcrnrlon = 60
            elif zone == 'australia':
                self.llcrnrlat = -50
                self.llcrnrlon = 100
                self.urcrnrlat = -10
                self.urcrnrlon = 160
            elif zone == 'russia':
                self.llcrnrlat = 40
                self.llcrnrlon = 20
                self.urcrnrlat = 80
                self.urcrnrlon = 180
            elif zone == 'india':
                self.llcrnrlat = 5
                self.llcrnrlon = 65
                self.urcrnrlat = 40
                self.urcrnrlon = 100
            elif zone == 'arabian':
                self.llcrnrlat = 10
                self.llcrnrlon = 20
                self.urcrnrlat = 40
                self.urcrnrlon = 70
            elif zone == 'oceania':
                self.llcrnrlat = -50
                self.llcrnrlon = 100
                self.urcrnrlat = 10
                self.urcrnrlon = 180
            elif zone == 'southamerica':
                self.llcrnrlat = -60
                self.llcrnrlon = -100
                self.urcrnrlat = 20
                self.urcrnrlon = -30
            elif zone == 'northamerica':
                self.llcrnrlat = 10
                self.llcrnrlon = -180
                self.urcrnrlat = 80
                self.urcrnrlon = -30
            elif zone == 'southeastasia':
                self.llcrnrlat = -10
                self.llcrnrlon = 90
                self.urcrnrlat = 30
                self.urcrnrlon = 160
            elif zone == 'eastasia':
                self.llcrnrlat = 10
                self.llcrnrlon = 100
                self.urcrnrlat = 60
                self.urcrnrlon = 160
            elif zone == 'maritimecontinent':
                self.llcrnrlat = -20
                self.llcrnrlon = 80
                self.urcrnrlat = 20
                self.urcrnrlon = 160
            elif zone == 'pacific':
                self.llcrnrlat = -60
                self.llcrnrlon = 100
                self.urcrnrlat = 60
                self.urcrnrlon = 280
            elif zone == 'atlantic':
                self.llcrnrlat = -60
                self.llcrnrlon = -100
                self.urcrnrlat = 60
                self.urcrnrlon = 20
            elif zone == 'indian':
                self.llcrnrlat = -60
                self.llcrnrlon = 20
                self.urcrnrlat = 30
                self.urcrnrlon = 120
            elif zone == 'arctic':
                self.llcrnrlat = 50
                self.llcrnrlon = -180
                self.urcrnrlat = 90
                self.urcrnrlon = 180
            elif zone == 'antarctic':
                self.llcrnrlat = -90
                self.llcrnrlon = -180
                self.urcrnrlat = -50
                self.urcrnrlon = 180
            elif zone == 'equitoralpacific':
                self.llcrnrlat = -20
                self.llcrnrlon = 120
                self.urcrnrlat = 20
                self.urcrnrlon = 280
            elif zone == 'nino34':
                self.llcrnrlat = -5
                self.llcrnrlon = 190
                self.urcrnrlat = 5
                self.urcrnrlon = 240
            elif zone == 'amazon':
                self.llcrnrlat = -20
                self.llcrnrlon = -80
                self.urcrnrlat = 10
                self.urcrnrlon = -40

            else:
                self.llcrnrlon = llcrnrlon
                self.llcrnrlat = llcrnrlat
                self.urcrnrlon = urcrnrlon
                self.urcrnrlat = urcrnrlat
            self.resolution = resolution # c>l>i>h>f
            self.area_thresh = area_thresh
            self.kwargs = kwargs
            self.basemap = Bp(projection=self.projection, llcrnrlon=self.llcrnrlon, llcrnrlat=self.llcrnrlat, urcrnrlon=self.urcrnrlon, urcrnrlat=self.urcrnrlat, resolution=self.resolution, area_thresh=self.area_thresh, **self.kwargs)


        # convert to projection coordinates
        def convert(self, lon, lat, inverse=False):
            x, y = self.basemap(lon, lat, inverse=inverse)


        # 繪製經緯線
        def drawparallels(self, parallels = np.arange(-90.,90,30.), labels=[1,0,0,0], fontsize=fontsize.text, color='fg', linewidth=1.5, **kwargs):
            DP = self.basemap.drawparallels(parallels, labels=labels, fontsize=fontsize, color=colorlist(color), linewidth=linewidth, **kwargs)
        def drawmeridians(self, meridians = np.arange(-180.,180.,60.), labels=[0,0,0,1], fontsize=fontsize.text, color='fg', linewidth=1.5, **kwargs):
            self.basemap.drawmeridians(meridians, labels=labels, fontsize=fontsize, color=colorlist(color), linewidth=linewidth, **kwargs)
        # 根據指定地區自動繪製經緯線
        def drawparallelsmeridians(self, zone='world', latinterval=15, loninterval=15, fontsize=fontsize.text, color='fg', linewidth=1.5, **kwargs):
            import numpy as np
            if zone == 'taiwan':
                parallels = np.arange(21.5,26.5,latinterval)
                meridians = np.arange(118,123,loninterval)
            elif zone == 'china':
                parallels = np.arange(18,54,latinterval)
                meridians = np.arange(73,135,loninterval)
            elif zone == 'japan':
                parallels == np.arange(20,50,latinterval)
                meridians == np.arange(120,150,loninterval)
            elif zone == 'korea':
                parallels == np.arange(30,45,latinterval)
                meridians == np.arange(115,135,loninterval)
            elif zone == 'usa':
                parallels == np.arange(20,50,latinterval)
                meridians == np.arange(-130,-60,loninterval)
            elif zone == 'europe':
                parallels == np.arange(30,70,latinterval)
                meridians == np.arange(-15,45,loninterval)
            elif zone == 'world':
                parallels == np.arange(-90,90,latinterval)
                meridians == np.arange(-180,180,loninterval)
            elif zone == 'africa':
                parallels == np.arange(-40,40,latinterval)
                meridians == np.arange(-20,60,loninterval)
            elif zone == 'australia':
                parallels == np.arange(-50 ,-10,latinterval)
                meridians == np.arange(100,160,loninterval)
            elif zone == 'russia':
                parallels == np.arange(40,80,latinterval)
                meridians == np.arange(20,180,loninterval)
            elif zone == 'india':
                parallels == np.arange(5,40,latinterval)
                meridians == np.arange(65,100,loninterval)
            elif zone == 'arabian':
                parallels == np.arange(10,40,latinterval)
                meridians == np.arange(20,70,loninterval)
            elif zone == 'oceania':
                parallels == np.arange(-50,10,latinterval)
                meridians == np.arange(100,180,loninterval)
            elif zone == 'southamerica':
                parallels == np.arange(-60,20,latinterval)
                meridians == np.arange(-100,-30,loninterval)
            elif zone == 'northamerica':
                parallels == np.arange(10,80,latinterval)
                meridians == np.arange(-180,-30,loninterval)
            elif zone == 'southeastasia':
                parallels == np.arange(-10,30,latinterval)
                meridians == np.arange(90,160,loninterval)
            elif zone == 'eastasia':
                parallels == np.arange(10,60,latinterval)
                meridians == np.arange(100,160,loninterval)
            elif zone == 'maritimecontinent':
                parallels == np.arange(-20,20,latinterval)
                meridians == np.arange(80,160,loninterval)
            elif zone == 'pacific':
                parallels == np.arange(-60,60,latinterval)
                meridians == np.arange(100,280,loninterval)
            elif zone == 'atlantic':
                parallels == np.arange(-60,60,latinterval)
                meridians == np.arange(-100,20,loninterval)
            elif zone == 'indian':
                parallels == np.arange(-60,30,1,latinterval)
                meridians == np.arange(20,120,loninterval)
            elif zone == 'arctic':
                parallels == np.arange(50,90,latinterval)
                meridians == np.arange(-180,180,loninterval)
            elif zone == 'antarctic':
                parallels == np.arange(-90,-50,latinterval)
                meridians == np.arange(-180,180,loninterval)
            elif zone == 'equitoralpacific':
                parallels == np.arange(-20,20,latinterval)
                meridians == np.arange(120,280,loninterval)
            elif zone == 'nino34':
                parallels == np.arange(-5,5,latinterval)
                meridians == np.arange(190,240,loninterval)
            elif zone == 'amazon':
                parallels == np.arange(-20,10,latinterval)
                meridians == np.arange(-80,-40,loninterval)
                

            self.basemap.drawparallels(parallels, fontsize=fontsize, color=colorlist(color), linewidth=linewidth, **kwargs)
            self.basemap.drawmeridians(meridians, fontsize=fontsize, color=colorlist(color), linewidth=linewidth, **kwargs)





        # 繪製海岸線
        def drawcoastlines(self, linewidth=3, color='fg', **kwargs):
            self.basemap.drawcoastlines(linewidth=linewidth, color=colorlist(color), **kwargs)
        # 繪製國家
        def drawcountries(self, linewidth=2, color='fg', **kwargs):
            self.basemap.drawcountries(linewidth=linewidth, color=colorlist(color), **kwargs)
        # 繪製州界
        def drawstates(self, linewidth=1, color='fg', **kwargs):
            self.basemap.drawstates(linewidth=linewidth, color=colorlist(color), **kwargs)
        # 繪製河流
        def drawrivers(self, linewidth=1, color='bg', **kwargs):
            self.basemap.drawrivers(linewidth=linewidth, color=colorlist(color), **kwargs)
        # 繪製海陸mask
        def drawlsmask(self, land_color='rfg', ocean_color='bg', lakes=True, resolution='l', grid=5, **kwargs):
            self.basemap.drawlsmask(land_color=colorlist(land_color), ocean_color=colorlist(ocean_color), lakes=lakes, resolution=resolution, grid=grid, **kwargs)
        # 繪製陰影浮雕
        def shadedrelief(self, alpha=1, **kwargs):
            self.basemap.shadedrelief(alpha=alpha, **kwargs)
        # 繪製NASA海陸地形圖
        def etopo(self, alpha=1, **kwargs):
            self.basemap.etopo(alpha=alpha, **kwargs)
        # 繪製NASA海陸衛星圖
        def bluemarble(self, alpha=1, **kwargs):
            self.basemap.bluemarble(alpha=alpha, **kwargs)
        # 繪製陸地
        def fillcontinents(self, color='rfg', lake_color='bg', **kwargs):
            self.basemap.fillcontinents(color=colorlist(color), lake_color=colorlist(lake_color), **kwargs)
        # 繪製地圖邊界
        def drawmapboundary(self, fill_color='bg', color='fg', linewidth=3, **kwargs):
            self.basemap.drawmapboundary(fill_color=colorlist(fill_color), color=colorlist(color), linewidth=linewidth, **kwargs)
        # 轉換經緯度座標
        def transform(self, x, y):
            return self.basemap(x, y) 

            
        
        
        
        
        # 繪製點圖
        def plot(self, x, y, color='fg', linewidth=2, linestyle='-', label=getPLOTNO(), **kwargs):
            self.basemap.plot(x, y, color=colorlist(color), linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
        # 繪製等值線
        def contour(self, x, y, z, colors='fg', levels=10, linewidths=2, clabel=True, fontsize=fontsize.sublabel, color='fg', **kwargs):
            CS = self.basemap.contour(x, y, z, colors=colorlist(colors), levels=levels, linewidths=linewidths, **kwargs)
            if clabel == True:
                CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True)
        # 繪製等值線填色圖
        def contourf(self, x, y, z, levels=10, cmap='2', contour=True, clabel=True,linewidths=1.5, color='fg', fontsize=fontsize.sublabel, **kwargs):
            if contour == True:
                CS = self.basemap.contour(x, y, z, colors=colorlist(color), levels=levels, linewidths=linewidths)
            if clabel == True:
                CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True)
            self.basemap.contourf(x, y, z, cmap=cmaplist(cmap), **kwargs)
        # 繪製散點圖
        def scatter(self, x, y, color='fg', size=3, marker='o', linewidth=None, label=getSCATTERNO(), linestyle='-', **kwargs):
            self.basemap.scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
        # 繪製colorbar
        def colorbar(self, ticks,label=' ', orientation='vertical',shrink=0.95, aspect=20, labelfontsize=16, font=fontpath, color='fg',**kwargs):
            CB = self.basemap.colorbar(orientation=orientation, shrink=shrink, aspect=aspect, label=label, **kwargs)
            CB.ax.tick_params(labelsize=labelfontsize, labelcolor=colorlist(color), color=colorlist(color))
            CB.ax.set_ylabel(label, fontproperties=fm.FontProperties(fname=font, size=labelfontsize), color=colorlist(color))
            CB.ax.set_yticks(ticks,ticks, fontproperties=fm.FontProperties(fname=font, size=labelfontsize))
            CB.ax.yaxis.set_tick_params(color=colorlist(color), labelcolor=colorlist(color))
            CB.outline.set_color(colorlist(color))
            CB.outline.set_linewidth(2)
        # 繪製圖例
        def legend(self, loc='best', fontsize=fontsize.legend, labelcolor='fg', frameon=True, framealpha=1, facecolor='rfg', edgecolor='fg', edgewidth=2 ,roundedge=False, **kwargs):
            LG = self.basemap.legend(loc=loc, fontsize=fontsize, labelcolor=colorlist(labelcolor), frameon=frameon, framealpha=framealpha, prop=fm.FontProperties(fname=fontpath, size=fontsize), facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor), **kwargs)
            if roundedge == False:
                LG.get_frame().set_boxstyle('Round', pad=0.2, rounding_size=-0.01)
            LG.get_frame().set_linewidth(edgewidth)
        # 繪製文字
        def text(self, x, y, text, color='fg', font=fontpath, fontsize=fontsize.text, **kwargs):
            self.basemap.text(x, y, text, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

        


    # subplot系列
    class initsubplots():
        def __init__(self, nrows=1, ncols=1, figsize=(8,10), style='default', background=True, **kwargs):
            self.row = 0 # 標示子圖的目標列
            self.col = 0 # 標示子圖的目標行
            self.ndim = 1 # 標示子圖的維度
            self.nrows = nrows
            self.ncols = ncols
            self.figsize = figsize
            self.kwargs = kwargs
            self.fig, self.ax = plt.subplots(nrows=self.nrows, ncols=self.ncols, figsize=self.figsize, **self.kwargs)
            global theme
            if style == 'default'or style == 'light_background' or style == 'light' or style == 'l':
                theme = 'default'
                plt.style.use(theme)
            elif style == 'dark_background' or style == 'dark' or style == 'd':
                theme = 'dark_background'
                plt.style.use(theme)
                self.fig.patch.set_facecolor(colorlist('#000000'))

            # 設定facecolor
            if background == True:
                if ncols == 1 and nrows == 1:
                    self.ax.set_facecolor(colorlist('bg'))
                elif ncols == 1 and nrows != 1:
                    self.ax[0].set_facecolor(colorlist('bg'))
                    for row in range(1,nrows):
                        self.ax[row].set_facecolor(colorlist('bg'))
                elif ncols != 1 and nrows == 1:
                    self.ax[0].set_facecolor(colorlist('bg'))
                    for col in range(1,ncols):
                        self.ax[col].set_facecolor(colorlist('bg'))
                else:
                    for row in range(nrows):
                        for col in range(ncols):
                            self.ax[row,col].set_facecolor(colorlist('bg'))
        
            

            else: pass
        
        def __getitem__(self, rowcol):
            if type(rowcol) == int: # 只有一個值時，預設為row
                self.ndim = 1
                self.row = rowcol
                self.col = 0
            else:
                self.ndim = 2
                self.row = rowcol[0]
                self.col = rowcol[1]
            return self

        def get_figure_and_axes(self):
            return self.fig, self.ax    
        def get_figure(self):
            return self.fig
        def get_axes(self):
            return self.ax
        
        # 排版
        def tight_layout(self, pad=1.08, h_pad=None, w_pad=None, rect=None):
            plt.tight_layout(pad=pad, h_pad=h_pad, w_pad=w_pad, rect=rect)

        def subplot_tool(self):
            plt.subplot_tool()

        # 繪製折線圖
        def plot(self, x, y, color='fg', linewidth=2, linestyle='-', label=getPLOTNO(),**kwargs):
            if self.ndim == 1:
                self.ax[self.row].plot(x, y, color=colorlist(color), linewidth=linewidth, label=label,linestyle=linestyle, **kwargs)
            else:
                self.ax[self.row,self.col].plot(x, y, color=colorlist(color), linewidth=linewidth, label=label,linestyle=linestyle, **kwargs)
        # 繪製點圖
        def scatter(self, x, y, color='fg', size=3, marker='o', linewidth=None, label=getSCATTERNO(), linestyle='-', **kwargs):
            if self.ndim == 1:
                self.ax[self.row].scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
            else:
                self.ax[self.row,self.col].scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
        # 繪製長條圖
        def bar(self, x, y, width=0.8, color='1', edgecolor='fg', linewidth=3, label=getBARNO(), **kwargs):
            if self.ndim == 1:
                self.ax[self.row].bar(x, y, width=width,color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)
            else:
                self.ax[self.row,self.col].bar(x, y, width=width,color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)
        # 繪製橫向長條圖
        def barh(self, x, y, width=0.8, color='1', edgecolor='fg', linewidth=3, label=getBARHNO(), **kwargs):
            if self.ndim == 1:
                self.ax[self.row].barh(x, y, height=width, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)
            else:
                self.ax[self.row,self.col].barh(x, y, height=width, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label, **kwargs)
        # 繪製直方圖
        def hist(self, x, bins=5, color='1', edgecolor='fg', linewidth=3, label=getHISTNO(), **kwargs):
            if self.ndim == 1:
                self.ax[self.row].hist(x, bins=bins, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label,**kwargs)
            else:
                self.ax[self.row,self.col].hist(x, bins=bins, color=colorlist(color), edgecolor=colorlist(edgecolor), linewidth=linewidth, label=label,**kwargs)
        # 繪製散點圖
        def scatter(self, x, y, color='fg', size=3, marker='o', linewidth=None, label=getSCATTERNO(), linestyle='-', **kwargs):
            if self.ndim == 1:
                self.ax[self.row].scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
            else:
                self.ax[self.row,self.col].scatter(x, y, color=colorlist(color), s=size, marker=marker, linewidth=linewidth, label=label, linestyle=linestyle, **kwargs)
        # 繪製polar圖
        def polar(self, theta, r, color='fg', linewidth=2, linestyle='-', **kwargs):
            if self.ndim == 1:
                self.ax[self.row].polar(theta, r, color=colorlist(color), linewidth=linewidth, linestyle=linestyle, **kwargs)
            else:
                self.ax[self.row,self.col].polar(theta, r, color=colorlist(color), linewidth=linewidth, linestyle=linestyle, **kwargs)
        
        # 繪製等值線
        def contour(self, x, y, z, colors='fg', levels=10, linewidths=2, clabel=True, fontsize=fontsize.clabel*fontscale, color='fg', **kwargs):
            if self.ndim == 1:
                CS = self.ax[self.row].contour(x, y, z, colors=colorlist(colors), levels=levels, linewidths=linewidths, **kwargs)
                if clabel == True:
                    CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True)
                    for t in CL:
                        t.set_fontproperties(fm.FontProperties(fname=fontpath, size=fontsize.colorbartick*fontscale))
                self.z = z
                self.levels = levels
            else:
                CS = self.ax[self.row,self.col].contour(x, y, z, colors=colorlist(colors), levels=levels, linewidths=linewidths, **kwargs)
                if clabel == True:
                    CL = CS.clabel(fontsize=fontsize, colors=colorlist(color), inline=True)
                    for t in CL:
                        t.set_fontproperties(fm.FontProperties(fname=fontpath, size=10*fontscale))
                self.z = z
                self.levels = levels
        # 繪製等值線填色圖
        def contourf(self, x, y, z, levels=10, cmap='28', contour= True, clabel=True,linewidths=1.5, color='fg', vmin='auto', vmax='auto', fontsize=fontsize.clabel*fontscale, **kwargs):
            import numpy as np
            # 傳出Z值和levels值
            global subcontour_vmin, subcontour_vmax, subcontour_levels, CS, CT
            if contour == True:
                if self.ndim == 1:
                    CT = self.ax[self.row].contour(x, y, z, colors=colorlist(color), levels=levels, linewidths=linewidths)
                    if clabel == True:
                        CL = CT.clabel(fontsize=fontsize*fontscale, colors=colorlist(color), inline=True)
                        # set the fontname of clabel
                        for t in CL:
                            t.set_fontproperties(fm.FontProperties(fname=fontpath, size=10*fontscale))
                else:
                    CT = self.ax[self.row,self.col].contour(x, y, z, colors=colorlist(color), levels=levels, linewidths=linewidths)
                    if clabel == True:
                        CL = CT.clabel(fontsize=fontsize*fontscale, colors=colorlist(color), inline=True)
                        for t in CL:
                            t.set_fontproperties(fm.FontProperties(fname=fontpath, size=10*fontscale))

            if self.ndim == 1:
                CS = self.ax[self.row].contourf(x, y, z, cmap=cmaplist(cmap), **kwargs)
            else:
                CS = self.ax[self.row,self.col].contourf(x, y, z, cmap=cmaplist(cmap), **kwargs)
        
        
        
        
        
        # 繪製圖例
        def legend(self, loc='best', fontsize=fontsize.legend*fontscale, labelcolor='fg', frameon=True, framealpha=1, facecolor='rfg', edgecolor='fg', edgewidth=2 ,roundedge=False, **kwargs):
            if self.ndim == 1:
                LG = self.ax[self.row].legend(loc=loc, fontsize=fontsize, labelcolor=colorlist(labelcolor), frameon=frameon, framealpha=framealpha, prop=fm.FontProperties(fname=fontpath, size=fontsize), facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor), **kwargs)
            else:
                LG = self.ax[self.row,self.col].legend(loc=loc, fontsize=fontsize, labelcolor=colorlist(labelcolor), frameon=frameon, framealpha=framealpha, prop=fm.FontProperties(fname=fontpath, size=fontsize), facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor), **kwargs)
            if roundedge == False:
                LG.get_frame().set_boxstyle('Round', pad=0.2, rounding_size=-0.01)
            LG.get_frame().set_linewidth(edgewidth)
        # 繪製文字
        def text(self, x, y, text, color='fg', font=fontpath, fontsize=fontsize.text*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].text(x, y, text, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].text(x, y, text, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        
        # 繪製colorbar
        def colorbar(self,label=' ', orientation='vertical',shrink=0.95, aspect=10, labelfontsize=fontsize.colorbarlabel*fontscale, tickfontsize=fontsize.colorbarticklabel*fontscale, font=fontpath, extend='neither',color='fg',**kwargs):
            
            print('\033[33m'+'[WARNING] Some bugs have been reported when using colorbar in subplots.'+'\033[0m')
            if self.ndim == 1:
                CB = plt.colorbar(CS, orientation=orientation, shrink=shrink, aspect=aspect, label=label, extend=extend, ax=self.ax[self.row], **kwargs)
                CB.ax.tick_params(labelsize=tickfontsize, labelcolor=colorlist(color), color=colorlist(color))
                CB.ax.set_ylabel(label, fontproperties=fm.FontProperties(fname=font, size=labelfontsize), color=colorlist(color))
                CB.ax.yaxis.set_tick_params(color=colorlist(color), labelcolor=colorlist(color))
                CB.outline.set_color(colorlist(color))
                CB.outline.set_linewidth(2)
                CB.ax.yaxis.label.set_font_properties(fm.FontProperties(fname = font, size = labelfontsize))
                CB.outline.set_linewidth(2)
                for l in CB.ax.yaxis.get_ticklabels():
                    l.set_fontproperties(fm.FontProperties(fname = font, size = tickfontsize))
            else:
                CB = plt.colorbar(CS, orientation=orientation, shrink=shrink, aspect=aspect, label=label, extend=extend, cax=self.ax[self.row,self.col], **kwargs)
                CB.ax.tick_params(labelsize=labelfontsize, labelcolor=colorlist(color), color=colorlist(color))
                CB.ax.set_ylabel(label, fontproperties=fm.FontProperties(fname=font, size=labelfontsize), color=colorlist(color))
                CB.ax.yaxis.set_tick_params(color=colorlist(color), labelcolor=colorlist(color))
                CB.outline.set_color(colorlist(color))
                CB.outline.set_linewidth(2)
                CB.ax.yaxis.label.set_font_properties(fm.FontProperties(fname = font, size = labelfontsize))
                CB.outline.set_linewidth(2)
                for l in CB.ax.yaxis.get_ticklabels():
                    l.set_fontproperties(fm.FontProperties(fname = font, size = tickfontsize))

        def clim(self, vmin=None, vmax=None):
            if self.ndim == 1:
                self.ax[self.row].set_clim(vmin, vmax)
            else:
                self.ax[self.row,self.col].set_clim(vmin, vmax)
        
        # 繪製xticks、yticks
        def xticks(self, ticks, labels, color='fg', font=fontpath, fontsize=fontsize.ticklabel*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_xticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].set_xticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def yticks(self, ticks, labels, color='fg', font=fontpath, fontsize=fontsize.ticklabel*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_yticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].set_yticks(ticks, labels, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def xlabel(self, xlabel, color='fg', font=fontpath, fontsize=fontsize.label*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_xlabel(xlabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].set_xlabel(xlabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def ylabel(self, ylabel, color='fg', font=fontpath, fontsize=fontsize.label*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_ylabel(ylabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].set_ylabel(ylabel, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def spines(self, top=True, right=True, bottom=True, left=True, color='fg', linewidth=3, **kwargs):
            if self.ndim == 1:
                if top: self.ax[self.row].spines['top'].set_visible(top)
                if right: self.ax[self.row].spines['right'].set_visible(right)
                if bottom: self.ax[self.row].spines['bottom'].set_visible(bottom)
                if left: self.ax[self.row].spines['left'].set_visible(left)
                if top: self.ax[self.row].spines['top'].set_color(colorlist(color))
                if right: self.ax[self.row].spines['right'].set_color(colorlist(color))
                if bottom: self.ax[self.row].spines['bottom'].set_color(colorlist(color))
                if left: self.ax[self.row].spines['left'].set_color(colorlist(color))
                if top: self.ax[self.row].spines['top'].set_linewidth(linewidth)
                if right: self.ax[self.row].spines['right'].set_linewidth(linewidth)
                if bottom: self.ax[self.row].spines['bottom'].set_linewidth(linewidth)
                if left: self.ax[self.row].spines['left'].set_linewidth(linewidth)
                self.ax[self.row].tick_params(axis='x', colors=colorlist(color), width=3, length=5)
                self.ax[self.row].tick_params(axis='y', colors=colorlist(color), width=3, length=5)
            else:
                if top: self.ax[self.row,self.col].spines['top'].set_visible(top)
                if right: self.ax[self.row,self.col].spines['right'].set_visible(right)
                if bottom: self.ax[self.row,self.col].spines['bottom'].set_visible(bottom)
                if left: self.ax[self.row,self.col].spines['left'].set_visible(left)
                if top: self.ax[self.row,self.col].spines['top'].set_color(colorlist(color))
                if right: self.ax[self.row,self.col].spines['right'].set_color(colorlist(color))
                if bottom: self.ax[self.row,self.col].spines['bottom'].set_color(colorlist(color))
                if left: self.ax[self.row,self.col].spines['left'].set_color(colorlist(color))
                if top: self.ax[self.row,self.col].spines['top'].set_linewidth(linewidth)
                if right: self.ax[self.row,self.col].spines['right'].set_linewidth(linewidth)
                if bottom: self.ax[self.row,self.col].spines['bottom'].set_linewidth(linewidth)
                if left: self.ax[self.row,self.col].spines['left'].set_linewidth(linewidth)
                self.ax[self.row,self.col].tick_params(axis='x', colors=colorlist(color), width=3, length=5)
                self.ax[self.row,self.col].tick_params(axis='y', colors=colorlist(color), width=3, length=5)
        # 繪製標題
        def title(self, title, color='fg', font=fontpath_bold, fontsize=fontsize.title*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def lefttitle(self, title, color='1', font=fontpath_bold, fontsize=fontsize.subtitle*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs, loc='left')
            else:
                self.ax[self.row,self.col].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs, loc='left')
        def righttitle(self, title, color='2', font=fontpath_bold, fontsize=fontsize.subtitle*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs, loc='right')
            else:
                self.ax[self.row,self.col].set_title(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs, loc='right')
        # 其他
        def grid(self, b=None, which='major', axis='both', color='fg', linestyle=':', linewidth=0.8, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].grid(b, which=which, axis=axis, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
            else:
                self.ax[self.row,self.col].grid(b, which=which, axis=axis, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
        def xlim(self, xmin=None, xmax=None, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_xlim(xmin, xmax, **kwargs)
            else:    
                self.ax[self.row,self.col].set_xlim(xmin, xmax, **kwargs)
        def ylim(self, ymin=None, ymax=None, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].set_ylim(ymin, ymax, **kwargs)
            else:
                self.ax[self.row,self.col].set_ylim(ymin, ymax, **kwargs)
        def hidespines(self, top=True, right=True, bottom=True, left=True):
            if self.ndim == 1:
                if top: self.ax[self.row].spines['top'].set_visible(False)
                if right: self.ax[self.row].spines['right'].set_visible(False)
                if bottom: self.ax[self.row].spines['bottom'].set_visible(False)
                if left: self.ax[self.row].spines['left'].set_visible(False)
            else:
                if top: self.ax[self.row,self.col].spines['top'].set_visible(False)
                if right: self.ax[self.row,self.col].spines['right'].set_visible(False)
                if bottom: self.ax[self.row,self.col].spines['bottom'].set_visible(False)
                if left: self.ax[self.row,self.col].spines['left'].set_visible(False)
        def xaxisposition(self, yposition, xaxis='bottom',**kwargs):
            if self.ndim == 1:
                self.ax[self.row].xaxis.set_ticks_position(xaxis)
                self.ax[self.row].xaxis.set_label_position(yposition)
            else:
                self.ax[self.row,self.col].xaxis.set_ticks_position(xaxis)
                self.ax[self.row,self.col].xaxis.set_label_position(yposition)
        def yaxisposition(self, xposition, yaxis='left',**kwargs):
            if self.ndim == 1:
                self.ax[self.row].yaxis.set_ticks_position(yaxis)
                self.ax[self.row].yaxis.set_label_position(xposition)
            else:
                self.ax[self.row,self.col].yaxis.set_ticks_position(yaxis)
                self.ax[self.row,self.col].yaxis.set_label_position(xposition)
        def axhline(self, y=0, color='fg', linestyle='dashed', linewidth=3, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].axhline(y=y, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
            else:
                self.ax[self.row,self.col].axhline(y=y, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
        def axvline(self, x=0, color='fg', linestyle='dashed', linewidth=3, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].axvline(x=x, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
            else:
                self.ax[self.row,self.col].axvline(x=x, color=colorlist(color), linestyle=linestyle, linewidth=linewidth, **kwargs)
        def annotate(self, text, xy, xytext, arrowprops=dict(facecolor='black', shrink=0.05), color='fg', font=fontpath, fontsize=20*fontscale, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].annotate(text, xy=xy, xytext=xytext, arrowprops=arrowprops, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
            else:
                self.ax[self.row,self.col].annotate(text, xy=xy, xytext=xytext, arrowprops=arrowprops, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)
        def fill_between(self, x, y1, y2=0, where=None, interpolate=False, step=None, color='fg', alpha=0.5, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].fill_between(x, y1, y2=y2, where=where, interpolate=interpolate, step=step, color=colorlist(color), alpha=alpha, **kwargs)
            else:
                self.ax[self.row,self.col].fill_between(x, y1, y2=y2, where=where, interpolate=interpolate, step=step, color=colorlist(color), alpha=alpha, **kwargs)
        def fill_betweenx(self, y, x1, x2=0, where=None, interpolate=False, step=None, color='fg', alpha=0.5, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].fill_betweenx(y, x1, x2=x2, where=where, interpolate=interpolate, step=step, color=colorlist(color), alpha=alpha, **kwargs)
            else:
                self.ax[self.row,self.col].fill_betweenx(y, x1, x2=x2, where=where, interpolate=interpolate, step=step, color=colorlist(color), alpha=alpha, **kwargs)
        def ticksall(self, labeltop=True, labelbottom=True, labelleft=True, labelright=True, **kwargs):
            if self.ndim == 1:
                if labeltop: self.ax[self.row].tick_params(labeltop=labeltop, **kwargs)
                if labelbottom: self.ax[self.row].tick_params(labelbottom=labelbottom, **kwargs)
                if labelleft: self.ax[self.row].tick_params(labelleft=labelleft, **kwargs)
                if labelright: self.ax[self.row].tick_params(labelright=labelright, **kwargs)
            else:
                if labeltop: self.ax[self.row,self.col].tick_params(labeltop=labeltop, **kwargs)
                if labelbottom: self.ax[self.row,self.col].tick_params(labelbottom=labelbottom, **kwargs)
                if labelleft: self.ax[self.row,self.col].tick_params(labelleft=labelleft, **kwargs)
                if labelright: self.ax[self.row,self.col].tick_params(labelright=labelright, **kwargs)

        def invert_xaxis(self):
            if self.ndim == 1:
                self.ax[self.row].invert_xaxis()
            else:
                self.ax[self.row,self.col].invert_xaxis()
        
        def invert_yaxis(self):
            if self.ndim == 1:
                self.ax[self.row].invert_yaxis()
            else:
                self.ax[self.row,self.col].invert_yaxis()

        # 共用軸
        def twinx(self,color='fg', linewidth=3, tickslength = 5, **kwargs):
            # print the cautions that some bugs have been reported when using twinx() and twiny(), using yellow color
            print('\033[33m'+'[WARNING] Some bugs have been reported when using twinx() or twiny().'+'\033[0m')
            if self.ndim == 1:
                
                self.ax[self.row].tick_params(axis='y', top=True, colors=colorlist(color), width=linewidth, length=tickslength)
                self.ax[self.row].twinx()
            else:
                
                self.ax[self.row,self.col].tick_params(axis='y', top=True, colors=colorlist(color), width=linewidth, length=tickslength)
                self.ax[self.row,self.col].twinx()
        
        def twiny(self,color='fg', linewidth=3, tickslength = 5, **kwargs):
            print('\033[33m'+'[WARNING] Some bugs have been reported when using twinx() or twiny().'+'\033[0m')
            if self.ndim == 1:
                self.ax[self.row].twiny()
                self.ax[self.row].tick_params(axis='x', right=True, colors=colorlist(color), width=linewidth, length=tickslength)
            else:
                self.ax[self.row,self.col].twiny()
                self.ax[self.row,self.col].tick_params(axis='x', right=True, colors=colorlist(color), width=linewidth, length=tickslength)

        # 大標題
        def suptitle(self, title, color='fg', font=fontpath_bold,fontsize=fontsize.title, **kwargs):
            self.fig.suptitle(title, color=colorlist(color), fontproperties=fm.FontProperties(fname=font, size=fontsize), **kwargs)

        # 挪出額外空間
        def adjust(self, left=None, bottom=None, right=None, top=None, wspace=None, hspace=None):
            plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        # 新增軸
        def addaxes(self, position, **kwargs):
            if self.ndim == 1:
                self.ax[self.row].add_axes(position, **kwargs)
            else:
                self.ax[self.row,self.col].add_axes(position, **kwargs)

        # 重設值
        def set_xydata(self, x=None, y=None):
            if self.ndim == 1:
                if x != None: self.ax[self.row].set_xdata(x)
                if y != None: self.ax[self.row].set_ydata(y)
            else:
                if x != None: self.ax[self.row,self.col].set_xdata(x)
                if y != None: self.ax[self.row,self.col].set_ydata(y)
        
        # add logo
        def addlogo(self, logo, position='bottomright', size=0.1, **kwargs):
            print('\033[33m'+'[WARNING] Some bugs have been reported when using addlogo() in subplot.'+'\033[0m')
            if position == 'bottomright':
                self.fig.figimage(logo, xo=1-size, yo=0, origin='lower', **kwargs)
            elif position == 'bottomleft':
                self.fig.figimage(logo, xo=0, yo=0, origin='lower', **kwargs)
            elif position == 'topright':
                self.fig.figimage(logo, xo=1-size, yo=1-size, origin='upper', **kwargs)
            elif position == 'topleft':
                self.fig.figimage(logo, xo=0, yo=1-size, origin='upper', **kwargs)
            else:
                raise Exception(bcolors.FAIL+'[ERROR] Position not found.'+bcolors.ENDC+'\n Please use "bottomright", "bottomleft", "topright", "topleft" instead.')
        
    # 動畫
    from matplotlib.widgets import Slider, Button, RadioButtons
    def pause(interval=0.01):
        plt.pause(interval)

    def normalize(data, vmin=None, vmax=None):
        plt.Normalize(data, vmin=vmin, vmax=vmax)

    def slider(ax, label, valmin, valmax, valinit=0, valfmt='%1.2f', valstep=None, orientation='horizontal', **kwargs):
        return Slider(ax, label, valmin, valmax, valinit=valinit, valfmt=valfmt, valstep=valstep, orientation=orientation, **kwargs)


    # https://matplotlib.org/stable/gallery/widgets/slider_demo.html



except FileNotFoundError:
    # FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Windows\\Fonts\\msjh.ttc'
    raise Exception(bcolors.FAIL+'[ERROR] Font file not found. Please check your fontpath.'+bcolors.ENDC+'\n To inspect the correct fontpath, try to use the following code:\n\n'+bcolors.OKBLUE+'from pymeili import beautifyplot as bplt\n\nbplt.inspectfontfolder()'+bcolors.ENDC+'\n\nIf the fontpath is correct, please check your font file.\n\n If you try to use the "redirectfontfolder" function, and still get this error, which means that you have used some unsupported function, reinstall the font file to default path instead.')

except ModuleNotFoundError as e:
    raise Exception(bcolors.FAIL+'[ERROR] Module not found. Please check your matplotlib version.'+bcolors.ENDC+'\n To install the correct version, try to use the following code for example:\n\n'+bcolors.OKBLUE+'pip install matplotlib==3.3.4'+bcolors.ENDC+'\n\nIf the version is correct, please check the error message below and make sure your python version is > 3.7.\n\n',e)

except ImportError:
    raise Exception(bcolors.FAIL+'[ERROR] Module not found. Please check your matplotlib version.'+bcolors.ENDC+'\n To install the correct version, try to use the following code:\n\n'+bcolors.OKBLUE+'pip install matplotlib==3.3.4'+bcolors.ENDC+'\n\nIf the version is correct, please check the "pathlib" module.')

except SyntaxError as e:
    raise Exception(bcolors.FAIL+'[ERROR] Unicode error. Please check your fontpath.'+bcolors.ENDC+'\n add the "r" at the beginning of the fontpath, for example:\n\n'+bcolors.OKBLUE+'fontpath = r"C:\\Windows\\Fonts\\msjh.ttc"'+bcolors.ENDC+'\n\nIf the fontpath is correct, please check your font file.\n\n If you try to use the "redirectfontfolder" function, and still get this error, try to reinstall the font file to default path instead.\n\n'+bcolors.FAIL+str(e)+bcolors.ENDC)

except Exception as e:
    raise Exception(bcolors.FAIL+str(e)+bcolors.ENDC)