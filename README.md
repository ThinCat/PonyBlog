# PonyBlog
A tiny blog system base on web.py

# Install
pip install -r requirements.txt

------

The problem of "ImportError: The _imagingft C module is not installed"?
'''
Because the captcha need the PIL, and the PIL need the freetype, but the PIL install or compile without freetype library.
So, you have to install freetype library first, and then install PIL with the freetype library.
Just edit the setup.py of PIL, and fill the freetype library path of your system in: FREETYPE_ROOT block.
'''

------
