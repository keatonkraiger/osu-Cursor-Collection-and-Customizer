# osu! Cursors and Cursor Customization

**This is an *unofficial* collection of osu! cursors and tools to customize them.** I'll be continuously adding more cursors and customization tools to this repository. If you have any cursors you would like to add, please lmk.

## <a name="curors">Cursors</a>

Below is a collection of popular cursors for osu! std. These cursors are not mine, but I have collected them from various skins. If you are the creator of one of these cursors and would like it removed, please contact me.

## <a name="cursor_customize">Curosr Customization</a>

You can try the cursor colorizer in Google Colab: [[`colab`](https://colab.research.google.com/drive/1H4RPVcEK7wWOP_IHA_TFOqppY2LJNmNX?usp=sharing)]

I've created a few tools to customize existing curors. Customization is currently limited to changing the color of the cursor. I plan to add more customization options in the future.

### <a name="cursor_customize">Cursor Colorizer</a>

The cursor colorizer is a tool that allows you to change the color of a cursor. It is a command line tool that takes in a cursor image and a color. It outputs a new cursor image with the specified color. 

#### Requirements

- Python 3.0+
- Pillow

#### Installation



To run the cursor colorizer locally, you must first have Python 3.0+ installed. You can download Python [here](https://www.python.org/downloads/). You will then need to use pip to install Pillow. You can do this by running the following commands in your terminal:

```
pip install Pillow
```

#### Local Usage

You will run the colorizer through the command line using Python and different arguments. We recommend using the Google Colab link above to try out the colorizer before running it locally. When running locally you will need to provide certain arguments to specify the customization. Below is a list of the arguments you can provide:

- `--file_path`: The path of the original cursor or cursor tail you want to customize.
- `--color`: The color you want to change the cursor to. This should be a hex color code. For example, `#FFFFFF`.
- `--shiny_center`: Whether or not to apply a shiny (white) center similar to the default rafis yellow cursor.
- `--cursor_type`: The type of cursor you are customizing. Really only needed when customizing the Xootynator smile cursor.

Below are some examples of how to run the colorizer locally:

Changing the color of a shiny rafis cursor:

```
python cursor_colorizer.py --file_path "Cursors/rafis/Yellow_Original/cursor.png" --color "#ffb6c1" --shiny_center True
```

Changing the color of the 404 cursor:

```
python cursor_colorizer.py --file_path "Cursors/404/original_cursor.png" --color "#ffb6c1"
```

Changing the color of the Xootynator smile cursor:

```
python cursor_colorizer.py --file_path "Cursors/Xooty/Xooty_Smile/cursor.png" --color "#ffb6c1" --cursor_type "xooty_smile"
```
