### INTRODUCTION
> pymeili.為美麗而生

pymeili is a module to beautify your python plot or terminal text with more simple way. the design idea is from Navigraph aeronautical chart.

### IMPORTANT
If you encounter the FileNotFound error when using this module, you need to manually install font-packages: https://dwl.freefontsfamily.com/download/futura/; 
moving the font file to installed module folder, for instance: `C:\Users\Username\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymeili\resources`

If you encounter the ModuleNotFoundError when using this module, you need to manually install the module in the lastest version:
`pip install matplotlib`
`pip install numpy`
`pip install seaborn`
`pip install pathlib`
`pip install pathlib2`
`pip install metpy`
`pip install colored`
`pip install basemap`
Also, some modules do not support the previous version of python, make sure you are using the version 3.7 or above.

If you encounter the problem about 'git clone' when using this module, you need to manually install the git package from https://github.com/VVVICTORZHOU/resources.git and move the font file to installed module folder, for instance: `C:\Users\Username\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymeili\resources`. Or directly set the default git path.

For more information and instruction, please go to: https://github.com/VVVICTORZHOU/resources.git or you can just download the font file from the link above.

There still exist some bugs in this module, if you find any, please contact me by email: vichouro@gmail.com . Thank you. Some function reported bugs have added the caution hint when called.

### INSTALLATION
- Install guide: (run on your powershell or cmd)

    `pip install pymeili`

- Update guide: (run on your powershell or cmd)

    `pip install --upgrade pymeili`
    
    or directly run the python script below:
    ```python
    from pymeili import upgrade
    ```


