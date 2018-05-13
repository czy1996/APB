from matplotlib import pyplot as plt


def init_fig_axes(depth):
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_ylim(top=0, bottom=depth)
    axes.xaxis.tick_top()  # 将 x 坐标移到上方
    axes.grid()
    return fig, axes


def plot(oil_temp, annular_temp):
    set_ch()
    depth = oil_temp.params['well']['casing1']['depth']
    fig, axes = init_fig_axes(depth)

    oil_temp.plot(axes)
    annular_temp.plot(axes)

    axes.set_xlabel('温度 ℃')
    axes.set_ylabel('深度 m')

    axes.legend()
    fig.savefig('temp.png')
    # fig.show()


def set_ch():
    """
    这个函数的作用是防止 pylab 画出来的图里汉字是方块
    :return:
    """
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
