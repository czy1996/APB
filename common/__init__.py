from matplotlib import pyplot as plt


def init_fig(depth):
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_ylim(top=0, bottom=depth)
    axes.xaxis.tick_top()  # 将 x 坐标移到上方
    return fig, axes
