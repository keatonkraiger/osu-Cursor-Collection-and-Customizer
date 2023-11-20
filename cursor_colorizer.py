import argparse
from collections import Counter
from PIL import Image
import os
import colorsys

# Pixels to preserve for the xooty smile cursor. Not an elegant solution, but it works for now
xooty_smile_preserve_color = ['#e8e8e8', '#d9d4d7', '#c6c6c6', '#4c4c4c', '#414141', '#afafaf', '#f9c8ea', '#6a6a6a', '#f6bce6', '#d8a7c8', '#e1e1e1', 
                              '#504c4f', '#f489d3', '#f0f0f0', '#dbdbdb', '#d8b2cc', '#f6b7e4', '#6e6e6e', '#1b1b1b', '#f9f9f9', '#ededed', '#e7e6e8', '#efefef', '#0c0c0c', '#9d9d9d', '#f7b8e4', '#ffffff', '#787176', '#a8a8a8', 
                              '#f48dd4', '#4b4b4b', '#f6a2dd', '#545454', '#f7afe1', '#7c7c7c', '#fbd2ee', '#2c2c2c', '#777777', '#eeeeee', '#515151', '#bcb7ba', '#808080', '#f8d5f0', '#717071', '#f8e6f6', '#f7a5dd', '#e6e6e6', '#fcfcfc', '#e9e9e9', '#fac9eb', '#565556', '#cbcbcb', '#f3f3f3', '#292929', '#f596d8', 
                              '#181818', '#474747', '#f2f2f2', '#c7c7c7', '#a896a3', '#f197d6', '#ddd4db', '#dadada', '#f9c5ea', '#e890cc', '#fefefe', '#eaeaea', '#020202', '#ececec']

def hex_to_rgb(hex_color):
    """Convert a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_color_to_preserve(rgb, preserve_colors, threshold=12):
    """Check if the color should be preserved."""
    for color in preserve_colors:
        if all(abs(channel - target_channel) < threshold for channel, target_channel in zip(rgb, color)):
            return True
    return False

def apply_gradient_color_change(image, target_color, preserve_colors=xooty_smile_preserve_color, threshold=12):
    """Apply the new color with a gradient to white, avoiding changing grey, black, and pink pixels."""
    pixels = image.load()
    width, height = image.size
    target_hls = colorsys.rgb_to_hls(*[c/255.0 for c in target_color])

    preserve_colors = [hex_to_rgb(color) for color in preserve_colors]
    
    for y in range(height):
        for x in range(width):
            current_pixel = pixels[x, y]
            current_rgb = current_pixel[:3]
            
            if current_pixel[3] != 0 and not is_color_to_preserve(current_rgb, preserve_colors):  # Not transparent or to be preserved
                h, l, s = colorsys.rgb_to_hls(*[c/255.0 for c in current_rgb])
                if l < target_hls[1]:
                    l = target_hls[1]
                new_h, new_l, new_s = target_hls[0], l, s
                new_rgb = colorsys.hls_to_rgb(new_h, new_l, new_s)
                new_rgb = tuple(int(255 * c) for c in new_rgb)
                pixels[x, y] = new_rgb + (current_pixel[3],)

    return image


def adjust_color(image, target_color_rgb):
    """Adjust the cursor image to match the target color's hue, saturation, and lightness."""
    image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size

    # Convert target RGB to HLS for comparison
    target_hls = colorsys.rgb_to_hls(*[c/255.0 for c in target_color_rgb])

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Only adjust non-white, non-transparent pixels
            if a != 0 and (r, g, b) != (255, 255, 255):
                # Convert RGB to HLS
                h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)

                # Use target hue, but adjust lightness and saturation relative to the original
                new_h, new_l, new_s = target_hls[0], max(l, target_hls[1]), s * target_hls[2]

                # Convert back to RGB
                new_r, new_g, new_b = colorsys.hls_to_rgb(new_h, new_l, new_s)
                new_r, new_g, new_b = [int(255 * i) for i in (new_r, new_g, new_b)]
                pixels[x, y] = (new_r, new_g, new_b, a)

    return image

def change_full_cursor_color(cursor_img, new_color):
    """Change the entire cursor to one solid color."""
    cursor_img = cursor_img.convert("RGBA")
    data = cursor_img.getdata()
    new_data = [(new_color + (item[3],)) if item[3] != 0 else item for item in data]
    cursor_img.putdata(new_data)
    return cursor_img

def change_specific_color(cursor_img, base_color, new_color, threshold):
    """Change shades of the base color within a certain threshold to the new color."""
    cursor_img = cursor_img.convert("RGBA")
    pixels = cursor_img.load()
    width, height = cursor_img.size

    base_color_hls = colorsys.rgb_to_hls(*[c/255.0 for c in base_color])
    new_color_hls = colorsys.rgb_to_hls(*[c/255.0 for c in new_color])

    for y in range(height):
        for x in range(width):
            current_pixel = pixels[x, y]
            current_pixel_hls = colorsys.rgb_to_hls(current_pixel[0]/255.0, current_pixel[1]/255.0, current_pixel[2]/255.0)

            # Calculate the color distance
            dist = sum((a - b) ** 2 for a, b in zip(current_pixel_hls, base_color_hls)) ** 0.5

            # If the color is within the threshold, change it
            if dist < threshold and current_pixel[3] != 0:  # alpha not 0
                new_r, new_g, new_b = colorsys.hls_to_rgb(new_color_hls[0], current_pixel_hls[1], current_pixel_hls[2])
                new_r, new_g, new_b = [int(255 * i) for i in (new_r, new_g, new_b)]
                pixels[x, y] = (new_r, new_g, new_b, current_pixel[3])
    
    return cursor_img

def change_cursor_color(args):
    save_path = args.output_path
    file_path = args.file_path
    color = args.color
    shiny_center = args.shiny_center

    assert os.path.exists(file_path), "Cursor path does not exist"

    # Convert the new color from hex to an RGB tuple if it's in hex format
    if color.startswith('#'):
        color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Load cursor image
    cursor = Image.open(file_path)

    if args.cursor_type == 'xooty_smile':
        # Use the border color as the base color
        threshold = args.threshold
        apply_gradient_color_change(cursor, color, preserve_colors=xooty_smile_preserve_color, threshold=threshold)
    elif shiny_center:
        cursor = adjust_color(cursor, color)
    else:
        cursor = change_full_cursor_color(cursor, color)
        
    # Save the modified image
    cursor.save(save_path)
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Change cursor color with optional shiny center effect')
    parser.add_argument('--file_path', type=str, default='cursor.png', help='path to cursor image file')
    parser.add_argument('--color', type=str, default='#ffb6c1', help='color to change to in hex or RGB')
    parser.add_argument('--output_path', type=str, default='modified_cursor.png', help='path to save the modified cursor')
    parser.add_argument('--shiny_center', action='store_true', help='apply a shiny center effect to the cursor')
   
    # Specific cursor types
    parser.add_argument('--cursor_type', type=str, default='rafis', choices=['rafis', 'xooty_smile', '404'], help='type of cursor to change')
    parser.add_argument('--threshold', type=float, default=0.1, help='threshold for color change sensitivity')


    args = parser.parse_args()
    change_cursor_color(args)
