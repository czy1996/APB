from matplotlib import pyplot as plt


def init_fig_axes(depth):
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_ylim(top=0, bottom=depth)
    axes.xaxis.tick_top()  # 将 x 坐标移到上方
    axes.grid()
    return fig, axes


def plot(oil_temp, annular_temp):
    depth = oil_temp.params['well']['casing1']['depth']
    fig, axes = init_fig_axes(depth)

    oil_temp.plot(axes)
    annular_temp.plot(axes)

    fig.show()
