# Remove background - rembg

https://github.com/danielgatis/rembg

```bash

pip install rembg
pip install rembg[cli]

# single filesfiles
rembg i [inputfile]  
rembg i ./tmp/1.jpg ./tmp/1-out.png
rembg i ./tmp/2.jpg ./tmp/2-out.png
rembg i ./tmp/3.jpg ./tmp/3-out.png
rembg i ./tmp/4.jpg ./tmp/4-out.png
rembg i ./tmp/eva-1961-098.jpg ./out01/eva-1961-098.jpg.png


# additional params
rembg i -m sam -x '{"input_labels": [1], "input_points": [[100,100]]}' path/to/input.png path/to/output.png

# folders
rembg p ...

# stream from stdin
rembg b ...

# params
rembg -m [model name]


```