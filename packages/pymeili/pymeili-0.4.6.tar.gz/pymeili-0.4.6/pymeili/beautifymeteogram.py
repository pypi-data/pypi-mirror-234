import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap as Bp
import seaborn as sns
import numpy as np

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


theme = 'default'

def set_theme(theme_name):
    global theme
    theme = theme_name
    print(f'[HINT] Theme has been set to {theme}.')


# 色票(顏色選用優先級)
def colorlist(index):
    if type(index) == list:
        # 判斷是否所有元素都in
        if all(i in ['bg', 'bg1', 'bg2', 'fg', '1', '2', '3', '4', 'rfg'] for i in index):
            return [colorseries[i] for i in index]
        else:
            return index
    else:
        str(index)
        if index in ['bg', 'bg1', 'bg2', 'fg', '1', '2', '3', '4', 'rfg']:
            try:    
                if theme == 'default':
                    colorseries = {'bg': '#D9EEFD',
                                'bg1': '#D9EEFD',
                                'bg2': '#F7DCD1',
                                'rfg': '#F5F5F5',
                                'fg': '#111111',
                                '1': '#0A9CCF',
                                '2': '#AC005A',
                                '3': '#A19253',
                                '4': '#A43713'}
                    return colorseries[index]
                                
                elif theme == 'dark_background':
                    colorseries = {'bg': '#122D64',
                                'bg1': '#122D64',
                                'bg2': '#122D64',
                                'rfg': '#080808',
                                'fg': '#EEEEEE',
                                '1': '#0A9CCF',
                                '2': '#AC005A',
                                '3': '#A19253',
                                '4': '#A43713'}
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
        if index in ['-28','28','-27','-26','-25','-24','-23','-22','22','23','24','25','26','27','12','13','14','15','-12','-13','-14','-15','33','34','35','36','37','38','39','-33','-34','-35','-36','-37','-38','-39','43','44','45','46','47','48','49','-43','-44','-45','-46','-47','-48','-49','59','58','57','-57','-58','-59']:
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
                    
                    if index == '59':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#CACACA','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801','#AA21A3','#DA2DD3','#FB39FA','#FED5FD'])
                    if index == '58':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801','#AA21A3','#DA2DD3','#FB39FA','#FED5FD'])
                    if index == '57':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801'])
                    
                    if index == '-59':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD','#9DFEFF','#EEEEEE'])
                    if index == '-58':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD','#9DFEFF'])
                    if index == '-57':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD'])

                                                                        
                                                                        

                    
                
                
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
                    
                    if index == '59':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#CACACA','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801','#AA21A3','#DA2DD3','#FB39FA','#FED5FD'])
                    if index == '58':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801','#AA21A3','#DA2DD3','#FB39FA','#FED5FD'])
                    if index == '57':
                        return LinearSegmentedColormap.from_list('mycmap', ['#EEEEEE','#9DFEFF','#01D1FD','#00A5FD','#0177FD','#26A41C','#00FB30','#FDFD32','#FFD329','#FFA71F','#FFA71F','#DA2304','#AA1801'])
                    
                    if index == '-59':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD','#9DFEFF','#EEEEEE'])
                    if index == '-58':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD','#9DFEFF'])
                    if index == '-57':
                        return LinearSegmentedColormap.from_list('mycmap', ['#FED5FD','#FB39FA','#DA2DD3','#AA21A3','#AA1801','#DA2304','#FFA71F','#FFA71F','#FFD329','#FDFD32','#00FB30','#26A41C','#0177FD','#00A5FD','#01D1FD'])
                    
            except: # NameError: name 'theme' is not defined
                raise Exception(bcolors.WARNING+'Please run initplot() first.'+bcolors.ENDC)
        else: 
            return index












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
fontpath = Path(mpl.get_data_path(), motherpath+"\\futura medium bt.ttf")
fontpath_bold = Path(mpl.get_data_path(), motherpath+"\Futura Heavy font.ttf")
fontpath_black = Path(mpl.get_data_path(), motherpath+"\Futura Extra Black font.ttf")


class SkewT_plot():
    def __init__(self, pressure, temperature, dewpoint, windspeed=False, winddirection=False, Uwind=False, Vwind=False, height=np.array([]), title='SKEW-T DIAGRAM', hodograph=True, lefttitle=None, righttitle=None, xlabel='Temperature [°C]', ylabel='Pressure [hPa]', logopath=False, style='default'):
        '''
        This function is used to plot SkewT diagram.
        Input:
            pressure: pressure data [hPa]
            temperature: temperature data [degC]
            dewpoint: dewpoint data [degC]
            windspeed: windspeed data [m/s]
            winddirection: winddirection data [deg]
            Uwind: Uwind data [m/s]
            Vwind: Vwind data [m/s]
            height: height data [m]
        Output:
            SkewT diagram
        '''

        style = style.lower()
        global theme
        if style == 'default' or style == 'light' or style == 'l':
            theme = 'default'
        elif style == 'dark' or style == 'd':
            theme = 'dark_background'
        else: raise Exception(bcolors.WARNING+'Please choose a valid style: default, light, l, dark, d.'+bcolors.ENDC)

        from metpy.plots import SkewT
        from metpy.units import units
        import metpy.calc as mpcalc

        # Set up plot
        fig = plt.figure(figsize=(9, 9))
        skew = SkewT(fig, rotation=45)

        # set background color of skewT
        skew.ax.set_facecolor(colorlist('bg'))

        # set background color of figure
        if theme == 'dark_background': fig.patch.set_facecolor(colorlist('rfg'))

        # set variables unit
        pressure = pressure *units('hPa')
        temperature = temperature *units('degC')
        dewpoint = dewpoint *units('degC')
        

        # Plot the data using normal plotting functions, in this case using
        # log scaling in Y, as dictated by the typical meteorological plot
        skew.plot(pressure, temperature, linewidth=2.5,color=colorlist('2'),label='Temperature')
        skew.plot(pressure, dewpoint, linewidth=2.5, color=colorlist('1'),label='Dewpoint')
        
        # create an axis for wind barbs and set its position at right side of the plot
        box = skew.ax.get_position()
        ax2 = fig.add_axes([box.x1*1.0515,box.y0*0.999,0,box.y0+box.height*0.835])
        # set color of wind barbs axis
        ax2.spines['top'].set_color(colorlist('fg'))
        ax2.spines['right'].set_color(colorlist('fg'))
        ax2.spines['bottom'].set_color(colorlist('fg'))
        ax2.spines['left'].set_color(colorlist('fg'))
        ax2.set_xticks([])
        ax2.set_yticks([])
        

        # Add wind barbs, if winddirection and windspeed are provided, transform them to Uwind and Vwind, then plot
        if winddirection.all()!=False and windspeed.all()!=False:
            Uwind, Vwind = mpcalc.wind_components(windspeed*units('m/s'), winddirection*units('deg'))
            # plot wind barbs
            skew.plot_barbs(pressure, Uwind, Vwind, xloc=1.06, color=colorlist('fg'))
            
            if hodograph:
                # determine if height data is not a empty array
                if height.shape[0] == 0:
                    pass
                else:
                    from metpy.plots import Hodograph
                    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
                    # Create a hodograph inside the skew ( upper right corner )
                    ax_hod = inset_axes(skew.ax, '30%', '30%', loc='upper right')
                    h = Hodograph(ax_hod, component_range=80.)
                    h.add_grid(increment=10)
                    h.plot_colormapped(Uwind, Vwind, height, cmap=cmaplist('-28'))
                    # set the facecolor of hodograph and spine color
                    ax_hod.set_facecolor(colorlist('bg'))
                    ax_hod.spines['top'].set_color(colorlist('fg'))
                    ax_hod.spines['right'].set_color(colorlist('fg'))
                    ax_hod.spines['bottom'].set_color(colorlist('fg'))
                    ax_hod.spines['left'].set_color(colorlist('fg'))
                    ax_hod.spines['top'].set_linewidth(2.5)
                    ax_hod.spines['right'].set_linewidth(2.5)
                    ax_hod.spines['bottom'].set_linewidth(2.5)
                    ax_hod.spines['left'].set_linewidth(2.5)
                    ax_hod.tick_params(axis='both', colors=colorlist('fg'), which='major', width=2.5, length=5)
                    ax_hod.tick_params(axis='both', colors=colorlist('fg'), which='minor', width=2.5, length=5)

                    # set ticklabel font and color
                    for label in (ax_hod.get_xticklabels() + ax_hod.get_yticklabels()):
                        label.set_fontproperties(fm.FontProperties(fname=fontpath, size=fontsize.ticklabel*0.8))
                        label.set_color(colorlist('fg'))

                    # set xyticks
                    ax_hod.set_xticks(np.arange(-60, 61, 20))
                    ax_hod.set_yticks(np.arange(-60, 61, 20))

                    # set xylimit of hodograph
                    ax_hod.set_xlim(-50, 50)
                    ax_hod.set_ylim(-50, 50)

                    # add the title of hodograph at the inside upper right corner
                    ax_hod.text(0.98, 0.98, 'Hodograph', transform=ax_hod.transAxes, fontsize=fontsize.text*0.8, verticalalignment='top', horizontalalignment='right', color=colorlist('fg'), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.text*0.8))
                    # set grid color
                    #h.gridlines.set_color(colorlist('fg'), linewidth=1.5, alpha=0.5)


                    #h.plot(Uwind, Vwind, color='tab:red')





        elif Uwind.all()!=False and Vwind.all()!=False:
            skew.plot_barbs(pressure, Uwind, Vwind, xloc=1.06)
        else: pass

        # Calculate LCL height and plot as black dot
        lcl_pressure, lcl_temperature = mpcalc.lcl(pressure[0], temperature[0], dewpoint[0])
        skew.plot(lcl_pressure, lcl_temperature, marker='o', color=colorlist('fg'), markersize=5, markerfacecolor=colorlist('fg'), markeredgecolor=colorlist('fg'), markeredgewidth=2, alpha=0.7, label='LCL')

        # Calculate full parcel profile and add to plot as black line
        prof = mpcalc.parcel_profile(pressure, temperature[0], dewpoint[0]).to('degC')
        skew.plot(pressure, prof, colorlist('fg'), linewidth=2, label='Parcel Profile')

        # Shade areas of CAPE and CIN
        if theme == 'default':
            skew.shade_cin(pressure, temperature, prof, color=colorlist('3'), alpha=0.3, label='CIN')
            skew.shade_cape(pressure, temperature, prof, color=colorlist('4'), alpha=0.3, label='CAPE')
        else:
            skew.shade_cin(pressure, temperature, prof, color=colorlist('3'), alpha=0.5, label='CIN')
            skew.shade_cape(pressure, temperature, prof, color=colorlist('4'), alpha=0.5, label='CAPE')

        # An example of a slanted line at constant T -- in this case the 0
        # isotherm
        #skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

        # Add the relevant special lines
        if theme == 'default':
            skew.plot_dry_adiabats()
        else:
            skew.plot_dry_adiabats(colors='tab:red')
        if theme == 'default':
            skew.plot_moist_adiabats()
        else:
            skew.plot_moist_adiabats(colors='tab:blue')
        if theme == 'default':
            skew.plot_mixing_lines()
        else:
            skew.plot_mixing_lines(colors='tab:green')

        # Add some keyvalue: CAPE[J/kg], CIN[J/kg], TLCL[degC], LCL[hPa], LFC[hPa], EL[hPa], PWAT[mm]
        CAPE, CIN = mpcalc.cape_cin(pressure, temperature, dewpoint, prof)
        CAPE = CAPE.magnitude
        CIN = CIN.magnitude
        TLCL = mpcalc.lcl(pressure[0], temperature[0], dewpoint[0])[1].magnitude
        LCL = mpcalc.lcl(pressure[0], temperature[0], dewpoint[0])[0].magnitude
        LFC = mpcalc.lfc(pressure, temperature, dewpoint)[0].magnitude
        EL = mpcalc.el(pressure, temperature, dewpoint)[0].magnitude
        PWAT = mpcalc.precipitable_water(pressure, dewpoint).magnitude
        labelcolor='fg'
        frameon=True
        framealpha=1
        facecolor='rfg'
        edgecolor='fg'
        edgewidth=2
        roundedge=False

        self.CAPE = CAPE
        self.CIN = CIN
        self.TLCL = TLCL
        self.LCL = LCL
        self.LFC = LFC
        self.EL = EL
        self.PWAT = PWAT



        skew.ax.text(0.02, 0.98, 'CAPE = {:.0f} [J/kg]\nCIN = {:.0f} [J/kg]\nTLCL = {:.0f} [°C]\nLCL = {:.0f} [hPa]\nLFC = {:.0f} [hPa]\nEL = {:.0f} [hPa]\nPWAT = {:.0f} [mm]'.format(CAPE, CIN, TLCL, LCL, LFC, EL, PWAT), transform=skew.ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor), alpha=framealpha), color=colorlist('fg'), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.text))

        LG = skew.ax.legend(loc='lower left', fontsize='x-large', labelcolor=colorlist(labelcolor), frameon=frameon, framealpha=framealpha, facecolor=colorlist(facecolor), edgecolor=colorlist(edgecolor),prop=fm.FontProperties(fname=fontpath, size=fontsize.legend))
        if roundedge == False:
            LG.get_frame().set_boxstyle('Round', pad=0.2, rounding_size=-0.01)
        LG.get_frame().set_linewidth(edgewidth)
        skew.ax.set_xlabel(xlabel, color=colorlist('fg'), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.ticklabel))
        skew.ax.set_ylabel(ylabel, color=colorlist('fg'), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.ticklabel))
        skew.ax.set_title(title, color=colorlist('fg'), fontproperties=fm.FontProperties(fname=fontpath_bold, size=fontsize.title))
        if lefttitle != None:
            skew.ax.set_title(lefttitle, color=colorlist('1'), loc='left', fontproperties=fm.FontProperties(fname=fontpath_bold, size=fontsize.subtitle*0.7))
        if righttitle != None:
            skew.ax.set_title(righttitle, color=colorlist('2'), loc='right', fontproperties=fm.FontProperties(fname=fontpath_bold, size=fontsize.subtitle*0.7))

        skew.ax.spines['top'].set_visible(True)
        skew.ax.spines['right'].set_visible(True)
        skew.ax.spines['bottom'].set_visible(True)
        skew.ax.spines['left'].set_visible(True)
        skew.ax.spines['top'].set_linewidth(3)
        skew.ax.spines['right'].set_linewidth(3)
        skew.ax.spines['bottom'].set_linewidth(3)
        skew.ax.spines['left'].set_linewidth(3)
        skew.ax.spines['top'].set_color(colorlist('fg'))
        skew.ax.spines['right'].set_color(colorlist('fg'))
        skew.ax.spines['bottom'].set_color(colorlist('fg'))
        skew.ax.spines['left'].set_color(colorlist('fg'))
        skew.ax.tick_params(axis='both', colors=colorlist('fg'), which='major', width=3, length=5)
        skew.ax.tick_params(axis='both', colors=colorlist('fg'), which='minor', width=3, length=5)
        skew.ax.set_yticks(np.arange(1000, 99, -100),np.arange(1000, 99, -100), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.ticklabel))
        skew.ax.set_xticks(np.arange(-100, 51, 10),np.arange(-100, 51, 10), fontproperties=fm.FontProperties(fname=fontpath, size=fontsize.ticklabel))
        skew.ax.set_ylim(1000, 100)
        skew.ax.set_xlim(-40, 50)

        if logopath == False:
            pass
        else:
            # add logo to the left bottom corner of the figure with size 0.05
            im = plt.imread(logopath)
            newax = fig.add_axes([0.04, 0.04, 0.05, 0.05], anchor='SW', zorder=-1, aspect='equal')
            newax.imshow(im)
            newax.axis('off')





    def __getitem__(self):
        return self
    
    def get_CAPE(self):
        return self.CAPE

    def get_CIN(self):
        return self.CIN
    
    def get_TLCL(self):
        return self.TLCL
    
    def get_LCL(self):
        return self.LCL
    
    def get_LFC(self):
        return self.LFC
    
    def get_EL(self):
        return self.EL
    
    def get_PWAT(self):
        return self.PWAT



class SurfaceAnalysis_plot():
    def __init__(self, lon, lat, data, title='Surface Analysis', lefttitle=None, righttitle=None, xlabel='Longitude', ylabel='Latitude', cmap='jet', vmin=None, vmax=None, cbarlabel='Surface Analysis', cbarlabelsize=fontsize.colorbarlabel, cbarlabelcolor='fg', cbarlabelweight='normal', cbarlabelrotation=0, cbarlabelpad=10, cbarlabelcolorbar=False, cbarlabelcolorbarlabel='[°C]', cbarlabelcolorbarlabelsize=fontsize.colorbarlabel, cbarlabelcolorbarlabelcolor='fg', cbarlabelcolorbarlabelweight='normal', cbarlabelcolorbarlabelrotation=0, cbarlabelcolorbarlabelpad=10, cbarlabelcolorbarlabelcolorbar=False, cbarlabelcolorbarlabelcolorbarlabel='[°C]', cbarlabelcolorbarlabelcolorbarlabelsize=fontsize.colorbarlabel, cbarlabelcolorbarlabelcolorbarlabelcolor='fg', cbarlabelcolorbarlabelcolorbarlabelweight='normal', cbarlabelcolorbarlabelcolorbarlabelrotation=0, cbarlabelcolorbarlabelcolorbarlabelpad=10, cbarlabelcolorbarlabelcolorbarlabelcolorbar=False, cbarlabelcolorbarlabelcolorbarlabelcolorbarlabel='[°C]', cbarlabelcolorbarlabelcolorbarlabelcolorbarlabelsize=fontsize.colorbarlabel, cbarlabelcolorbarlabelcolorbarlabelcolorbarlabelcolor='fg', cbarlabelcolorbarlabelcolorbarlabelcolorbarlabelweight='normal', cbarlabelcolorbarlabelcolorbarlabelcolorbarlabelrotation=0, cbarlabelcolorbarlabelcolorbarlabelcolorbarlabelpad=10):
        '''
        This function is used to plot Surface Analysis.
        Input:
            lon: longitude data [deg]
            lat: latitude data [deg]
            data: data to be plotted
        Output:
            Surface Analysis
        '''
        from metpy.plots import (
            ColdFront, WarmFront, ScallopedStroke, ColdFrontogenesis, WarmFrontogenesis, StationPlot, ColdFrontolysis, WarmFrontolysis, OccludedFront, OccludedFrontolysis, OccludedFrontogenesis, RidgeAxis, Squall, StationaryFront, StationaryFrontogenesis, StationaryFrontolysis
            )

        pass

    def __getitem__(self):
        return self