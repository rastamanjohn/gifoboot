import os
from PIL import Image
from shutil import copyfile


def desc(out, width, height, fps):
    parts = []
    with os.scandir(out) as files:
        for i in files:
            if i.is_dir() and i.name.startswith('part'):
                parts.append(i.name)

    with open(f'{out}{os.sep}desc.txt', 'w') as txt:
        txt.write(f'{width} {height} {fps}\n')
        for i in parts:
            txt.write(f'p 0 0 {i}\n')

    return True


def mirror(path):
    files = os.listdir(path)
    ext = os.path.splitext(files[0])[-1]
    for i in files:
        files[files.index(i)] = os.path.splitext(i)[0]
    files.sort(reverse=True)
    n, l = int(files[0]), len(files[0])
    files = files[1:-1]

    for i in files:
        n += 1
        copyfile(f'{path}{os.sep}{i}{ext}', f'{path}{os.sep}{n:0{l}d}{ext}')


def splitter(gif, out):
    # https://gist.github.com/revolunet/848913
    frame = Image.open(gif)
    n = 0
    while frame:
        frame.save(f'{out}{os.sep}{n:04d}.png', 'PNG')
        n += 1
        try:
            frame.seek(n)
        except EOFError:
            break
    return out


def new_part(out):
    n = 0
    while os.path.exists(f'{out}{os.sep}part{n}'):
        n += 1
    p = f'{out}{os.sep}part{n}'
    os.makedirs(p)
    return p


def ratio(out):
    from PIL import Image
    with os.scandir(out) as files:
        for i in files:
            if i.is_dir() and i.name.startswith('part'):
                with os.scandir(i) as images:
                    for j in images:
                        if j.is_file() and j.name.endswith('.png'):
                            img = Image.open(j.path)
                            return img.size[0] / float(img.size[1])
    return None
