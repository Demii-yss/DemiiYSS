from PIL import Image, ImageOps


def generateGIF(frames, duration, path):
    border_color = 'black'
    max_width = 0
    max_height = 0
    for f in frames:
        max_width = max(max_width, f.size[0])
        max_height = max(max_height, f.size[1])

    for i in range(len(frames)):
        a, b = frames[i].size[1], frames[i].size[0]
        if max_width / frames[i].size[0] < max_height / frames[i].size[1]:
            print('A')
            print(b, a)
            w = max_width
            h = int(a * (max_width / b))
            print('w=', w, ', h=', h)
            frames[i] = frames[i].resize((w, h))
            print('resize: ', frames[i].size)
            border = (0, (max_height - h) // 2, 0, (max_height - h) // 2)
            frames[i] = ImageOps.expand(frames[i], border=border, fill=border_color)
            print('border:', frames[i].size)
        else:
            print('B')
            print(b, a)
            w = int(b * (max_height / a))
            h = max_height
            print('w=', w, ', h=', h)
            frames[i] = frames[i].resize((w, h))
            print('resize: ', frames[i].size)
            border = ((max_width - w) // 2, 0, (max_width - w) // 2, 0)
            frames[i] = ImageOps.expand(frames[i], border=border, fill=border_color)
            print('border:', frames[i].size)

    frames[0].save(path, format="gif", save_all=True, append_images=frames[1:],
                   duration=duration, loop=0)
