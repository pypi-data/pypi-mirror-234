#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymeili.beautifyplot import (
    initplot,
    colorlist,
    cmaplist,
    getBARHNO,
    getBARNO,
    getHISTNO,
    getPLOTNO,
    getSCATTERNO,
    title, lefttitle, righttitle,
    scatter, plot, bar, hist, hist2d, pie, barh, table,
    contour, contourf, colorbar, polar,
    xlabel, ylabel, xticks, yticks, xyticks, ticksall,
    xlim, ylim, xylim, xscale, yscale, xlog, ylog,
    grid, spines, legend, hidespines, xaxisposition, yaxisposition,
    axhline, axvline, text, labeltext, annotate,
    fill_between, fill_betweenx,
    pause, normalize, slider, set_xydata,
    figsize, show, clf, close, figure, savefig,
    imread, imshow, imsave, fontprop,
    
)

from pymeili.beautifyterminal import (
    fg, bg, DEFAULT,
    bprint, inspectfg, inspectbg,
)

from pymeili.beautifymeteogram import (
    SkewT_plot, SurfaceAnalysis_plot
)

__version__: str = '0.4.6'


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


# 獲取當前檔案位址
currentfilepath = __file__

# 刪去__file__中最後面自"\"開始的字串(刪除檔名)
motherpath = currentfilepath[:-len(currentfilepath.split('\\')[-1])]
# 檢查是否為空路徑
if motherpath == '':
    print(bcolors.FAIL+'[FATAL ERROR] Invalid installed module path. \nPlease install this module in a directory with no Chinese characters.'+bcolors.ENDC)
    motherpath = '.'

#print(bcolors.BOLD+'Expected clone destination path: '+bcolors.OKBLUE+f'{motherpath}'+bcolors.ENDC)


import os
# go to motherpath
os.chdir(motherpath)
# check if resources exists
if os.path.exists(f'{motherpath}\\resources'):
    pass
    #print(f'[HINT] Font files have been installed in {motherpath} already.')
else:
# clone github respository
    os.system(f'git clone https://github.com/VVVICTORZHOU/resources.git')
    print(f'[HINT] Try to clone github font respository into {motherpath}.')
    print(f'[HINT] Make sure the font files are in the directory:\n\t 1. {motherpath}\\resources\\futura medium bt.ttf\n\t 2. {motherpath}\\resources\\Futura Heavy font.ttf\n\t 3. {motherpath}\\resources\\Futura Extra Black font.ttf')
    print(f'\033[93m [HINT] If no, please install Futura fonts in the same directory as this file.\ninstall font-packages: https://dwl.freefontsfamily.com/download/futura/;\n Moving the font file to installed module folder: {motherpath}\\resources. \033[0m')