from numpy import log
import pandas as pd
import os


def removeMergeDir(n):
    filepath = os.path.join(os.getcwd(), n)
    if os.path.isfile(filepath):
        os.remove(filepath)


def saveArr2Xlsx(h, a, n):
    fn = ''.join([str(n), '.xlsx'])
    removeMergeDir(fn)
    df = pd.DataFrame(a, columns=h)

    df.to_excel(fn, index=True)


if __name__ == '__main__':
    h = ['x', 'y', 'z']
    # a = []
    a = [
[-1788725.1639002285, 4636048.680280418, 3986096.0409621145]
,[-1787751.0994722918, 4634471.751605769, 3988379.7647923394]
,[-1790603.2298112044, 4634378.273365438, 3987527.4901110902]
,[-1790635.4256365304, 4634367.7941191355, 3987529.4824083475]
,[-1790657.3142265, 4634247.976010648, 3987665.6343464013]
,[-1791378.401066831, 4634227.145224555, 3987454.6522788485]
,[-1791426.818445931, 4634120.279786811, 3987613.661945174]
         ]
    n = "轨迹坐标"
    saveArr2Xlsx(h, a, n)
