import matplotlib.pyplot as plt
from matplotlib import animation


class SimpleGraph:
    def __init__(
            self, x, y, xerr=None, yerr=None, title='', xlabel='', ylabel='', xticks=None, yticks=None,
            xscale='linear', yscale='linear', grid=True, linestyle='-', marker='', show=True, save=True
    ):
        self.plt = plt
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, capsize=3, linestyle=linestyle, marker=marker)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        ax = plt.gca()
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        if xticks is not None:
            plt.xticks(xticks)
        if yticks is not None:
            plt.yticks(yticks)
        if grid:
            ax.grid()
        if save:
            plt.savefig(f'{title}', dpi=300)
        if show:
            plt.show()

        pass

    def savefig(self, title=None, dpi=300):
        if title is None:
            pass
        self.plt.savefig(f'{title}', dpi=dpi)


class ManyLinesGraph:
    def __init__(
            self, X, Y, labels, Xerr=None, Yerr=None, title='', xlabel='', ylabel='', xticks=None, yticks=None,
            xscale='linear', yscale='linear', grid=True, linestyle='-', marker='', show=True, save=True
    ):
        self.plt = plt
        self.is_x_2d = self.__is_x_2d(X)

        if self.is_x_2d:
            for i, y in enumerate(Y):
                x = X[i]
                label = labels[i]
                xerr = None
                yerr = None
                if Xerr is not None and Yerr is not None:
                    xerr = Xerr[i]
                    yerr = Yerr[i]
                plt.errorbar(x, y, label=label, xerr=xerr, yerr=yerr, capsize=3, linestyle=linestyle, marker=marker)
        else:
            for i, y in enumerate(Y):
                label = labels[i]
                xerr = None
                yerr = None
                if Xerr is not None and Yerr is not None:
                    xerr = Xerr
                    yerr = Yerr[i]
                plt.errorbar(X, y, label=label, xerr=xerr, yerr=yerr, capsize=3, linestyle=linestyle, marker=marker)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()

        ax = plt.gca()
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        if xticks is not None:
            plt.xticks(xticks)
        if yticks is not None:
            plt.yticks(yticks)
        if grid:
            ax.grid()
        if save:
            plt.savefig(f'{title}', dpi=300)
        if show:
            plt.show()

        pass

    @staticmethod
    def __is_x_2d(X):
        res = all(type(i) is list for i in X)
        return res

    def savefig(self, title=None, dpi=300):
        if title is None:
            pass
        self.plt.savefig(f'{title}', dpi=dpi)


class BinsGraph:
    def __init__(
            self, x, y, title='', xlabel='', ylabel='', xticks=None, yticks=None,
            xscale='linear', yscale='linear', grid=True, linestyle='-', marker='', show=True, save=True
    ):
        x_new = [x[0]]
        y_new = [y[0]]
        for i, el in enumerate(x[1:-1]):
            x_new += [el, x[i+1]]
            y_new += [y[i], y[i+1]]
        x_new.append(x[-1])
        y_new.append(y[-1])
        print(x, x_new)
        print(y, y_new)

        self.plt = plt
        plt.plot(x_new, y_new, linestyle=linestyle, marker=marker)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # plt.legend()

        ax = plt.gca()
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
        if xticks is not None:
            plt.xticks(xticks)
        if yticks is not None:
            plt.yticks(yticks)
        if grid:
            ax.grid()
        if save:
            plt.savefig(f'{title}', dpi=300)
        if show:
            plt.show()

    def savefig(self, title=None, dpi=300):
        if title is None:
            pass
        self.plt.savefig(f'{title}', dpi=dpi)


class AnimatedBarPlot:
    def __init__(self, x, Y, xscale='linear', yscale='linear'):
        self.x = x
        self.Y = Y
        self.plt = plt
        self.xscale = xscale
        self.yscale = yscale
        fig = plt.figure()
        n = len(Y)


        # plt.xlabel(xlabel)
        # plt.ylabel(ylabel)

        anim = animation.FuncAnimation(fig, self._animate, repeat=False, blit=False, frames=n,
                                       interval=500)

        # anim.save('mymovie.mp4', writer=animation.FFMpegWriter(fps=10))
        plt.show()
        pass

    def _animate(self, i):
        plt.clf()
        x = self.x
        print(x)
        y = self.Y[i]
        plt.bar(x, y)
        plt.xticks(rotation='vertical')
        plt.title(f'{i}')
        ax = plt.gca()
        ax.set_ylim(1.0E-10, self.__get_max(self.Y))
        # ax.set_xscale(self.xscale)
        ax.set_yscale(self.yscale)
        # for i, b in enumerate(barcollection):
        #     b.set_height(y[i])

    def __get_max(self, li):
        m = None
        for item in li:
            if isinstance(item, list):
                item = self.__get_max(item)
            if not m or m < item:
                m = item
        return m


class S0MatrixGraph:
    def __init__(self):
        pass


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5]
    y = [5, 3, 10, 3, 5, 1]
    y1 = [2, 20, 70, 5, 8, 10]
    Y = [y, y1]
    xerr = [0.1, 0.1, 0.1, 0.1, 0.3, 0.3]
    yerr = [[0.1, 0.1, 0.1, 0.1, 0.3, 0.3], [0.4, 0.9, 0.4, 0.99, 0.5, 0.3]]
    xticks = list(range(0, 10, 1))
    yticks = [1, 5, 10, 50, 100]  # list(range(0, 100, 1))
    s = SimpleGraph(x, y, xerr=xerr, yerr=yerr, xticks=xticks, yticks=yticks, title='test', save=True, yscale='log')
    labels = ['1', '2']
    ss = ManyLinesGraph(x, Y, labels, Xerr=xerr, Yerr=yerr, xticks=xticks, yticks=yticks, title='test', save=True, yscale='log')
    x = [0, 1, 2, 3, 4, 5]
    y = [5, 3, 10, 3, 5]
    sss = BinsGraph(x, y)

    x = [0, 1, 2, 3, 4, 5]
    y = [5, 3, 10, 3, 5, 1]
    y1 = [2, 20, 70, 5, 8, 10]
    Y = [y, y1]
    ssss = AnimatedBarPlot(x, Y)
