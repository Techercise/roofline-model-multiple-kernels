import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

font = {'size': 13}
plt.rc('font', **font)

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
          'tab:olive', 'tab:cyan']
styles = ['o', 's', 'v', '^', 'D', ">", "<", "*", "h", "H", "+", "1", "2", "3", "4", "8", "p", "d", "|", "_", ".", ","]

markersize = 10
markerwidth = 2
maxchar = 25


def roofline(flops, hbm_ai, ranks, api, labels=None, flag='HBM'):
    if not flops:
        print('FLOPS can not be empty!')
        return
    if max(flops) == 0:
        print('FLOPS are all 0s!')
        return
    if not hbm_ai:
        print('AIHBM cannot be empty!')
        return
    if len(flops) != len(hbm_ai):
        print('FLOPS needs to have the same length as AI!')
        return
    if (flag != 'HBM') and (flag != 'L2') and (flag != 'L1') and (flag != 'all'):
        print('flag needs to be one of HBM, L2, L1, and all!')
        return
    labels = [x[:maxchar] for x in labels]

    # Memory Bandwidths
    # mem_roofs = [('L1', 53764596694247.59/pow(10, 9)), ('L2', 2565679718831.03/pow(10, 9)),
    #              ('HBM', 900000000000.00/pow(10, 9))]

    mem_roofs = [('HBM', (900))]

    # Peak Theoretical TFLOPS
    cmp_roofs = [('SP', 19.5), ('DP', 9.7)]

    fig = plt.figure(1, figsize=(10.67, 6.6))
    plt.clf()
    ax = fig.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel('Arithmetic Intensity [FLOPs/Byte]')
    ax.set_ylabel('Performance [GFLOP/sec]')

    nx = 10000
    xmin = -3
    xmax = 5
    ymin = 1
    ymax = 200000

    ax.set_xlim(10 ** xmin, 10 ** xmax)
    ax.set_ylim(ymin, ymax)

    ixx = int(nx * 0.02)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    scomp_x_elbow = []
    scomp_ix_elbow = []
    smem_x_elbow = []
    smem_ix_elbow = []

    x = np.logspace(xmin, xmax, nx)
    for roof in cmp_roofs:
        for ix in range(1, nx):
            if float(mem_roofs[0][1] * x[ix]) >= roof[1]*1024 > (mem_roofs[0][1] * x[ix - 1]):
                scomp_x_elbow.append(x[ix - 1])
                scomp_ix_elbow.append(ix - 1)
                break

    for roof in mem_roofs:
        for ix in range(1, nx):
            if roof[1] * x[ix] >= cmp_roofs[0][1] * 1024 > roof[1] * x[ix - 1]:
                smem_x_elbow.append(x[ix - 1])
                smem_ix_elbow.append(ix - 1)
                break

    for i in range(len(cmp_roofs)):
        roof = cmp_roofs[i][1] * 1024
        y = np.ones(len(x)) * roof
        ax.plot(x[scomp_ix_elbow[i]:], y[scomp_ix_elbow[i]:], c='k', ls='-', lw='2')

    for i in range(len(mem_roofs)):
        roof = mem_roofs[i][1]
        y = x * roof
        ax.plot(x[:smem_ix_elbow[i] + 1], y[:smem_ix_elbow[i] + 1], c='k', ls='-', lw='2')

    for i in range(len(hbm_ai)):
        if flag == 'L1':
            ax.plot(float(l1_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[0], linestyle='None',
                    ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
        elif flag == 'L2':
            ax.plot(float(l2_ai[i]), float(flops[i]), c=colors[i % 10], marker=styles[1],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")
        elif flag == 'HBM':
            ax.plot(float(hbm_ai[i]), float(flops[i]/pow(10, 9)), c=colors[i % 10], marker=styles[i],
                    linestyle='None', ms=markersize, markerfacecolor='none',
                    markeredgewidth=markerwidth, label=labels[i] if labels else "unknown")

    marker_handles = []

    if flag == 'L1':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[0], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[0][0])[0])
    elif flag == 'L2':
        marker_handles.append(ax.plot([], [], c='k', marker=styles[1], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[1][0])[0])
    elif flag == 'HBM':
        for i in range(len(hbm_ai)):
            marker_handles.append(ax.plot([], [], c=colors[i % 10], marker=styles[i], linestyle='None', ms=markersize,
                                      markerfacecolor='none', markeredgewidth=markerwidth, label=labels[i])[0])

    elif flag == 'all':
        for i in range(len(mem_roofs)):
            marker_handles.append(ax.plot([], [], c=colors[2], marker=styles[i], linestyle='None', ms=markersize,
                                          markerfacecolor='none', markeredgewidth=markerwidth, label=mem_roofs[i][0])[
                                      0])

    for roof in cmp_roofs:
        ax.text(x[-ixx], roof[1] * 1024,
                roof[0] + ': ' + '{0:.1f}'.format(roof[1]) + ' TFLOP/s',
                horizontalalignment='right',
                verticalalignment='bottom')
    for roof in mem_roofs:
        ang = np.arctan(np.log10(xlim[1] / xlim[0]) / np.log10(ylim[1] / ylim[0])
                        * fig.get_size_inches()[1] / fig.get_size_inches()[0])

        if x[ixx] * roof[1] > ymin:
            ax.text(x[ixx], x[ixx] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
                    roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
                    horizontalalignment='left',
                    verticalalignment='bottom',
                    rotation=180 / np.pi * ang)

        else:
            ymin_ix_elbow = list()
            ymin_x_elbow = list()
            for ix in range(1, nx):
                if roof[1] * x[ix] >= ymin > roof[1] * x[ix - 1]:
                    ymin_x_elbow.append(x[ix - 1])
                    ymin_ix_elbow.append(ix - 1)
                    break
            ax.text(x[ixx + ymin_ix_elbow[0]], x[ixx + ymin_ix_elbow[0]] * roof[1] * (1 + 0.25 * np.sin(ang) ** 2),
                    roof[0] + ': ' + '{0:.1f}'.format(float(roof[1])) + ' GB/s',
                    horizontalalignment='left',
                    verticalalignment='bottom',
                    rotation=180 / np.pi * ang)

    leg1 = plt.legend(handles=marker_handles, loc='lower right', ncol=len(flag[0]) if 'all' not in flag else 3,
                      bbox_to_anchor=(1, 0))
    ax.add_artist(leg1)

    patch_handles = list()
    for i in range(0, len(hbm_ai)):
        if flops[i] > 0:
            patch_handles.append(mpatches.Patch(color=colors[i % 10], label=labels[i] if labels else "unknown"))

    # The string here is the text that will be displayed on your plot.
    ax.text(xlim[0] * 1.1, ylim[1] / 1.1, 'LBM C Kernel', horizontalalignment='left',
            verticalalignment='top')

    plt.savefig('LBM_C_Kernel.png')

    plt.show()

