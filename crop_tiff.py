import numpy as np
import rasterio
from pathlib import Path
from rasterio.plot import show
from rasterio.windows import Window


if __name__ == '__main__':

    grd_file = Path('s1a-vv-20191004-full.tif')

    # region of zurich
    win = Window(10500, 2800, 1000, 1000)

    with rasterio.open(grd_file, 'r') as src:
        grd_zh = src.read(1, window=win)
        window_trans = src.window_transform(win)
        grd_meta = src.profile
        grd_meta.update(
            {'dtype': 'float32',
             'height': win.height,
             'width': win.width,
             'transform': window_trans}
        )

    show(np.log10(grd_zh), transform=grd_meta['transform'], cmap='gray')

    dst_file = '_'.join(grd_file.stem.split('-')[0:-1]) + '_zurich.tif'

    with rasterio.open(dst_file, 'w', **grd_meta) as dst:
        dst.write(grd_zh.astype('float32'), 1)

    prew_file = '_'.join(grd_file.stem.split('-')[0:-1]) + '_zurich_preview.tif'

    with rasterio.open(prew_file, 'w', **grd_meta) as dst:
        dst.write(np.log10(grd_zh), 1)
