from ECG_getter import get_mini_ECG
from scene_navigator import SceneNavigator
from draw_utils import draw_ECG

import matplotlib.pyplot as plt


if __name__ == '__main__':
    signal = get_mini_ECG()

    scene = SceneNavigator(signal)

    # выбираем точку
    start_point =205

    qs = []
    # перебираем всех остальных кандидатов на роль второй точки и-конгломерата
    for point in range(len(signal)):
        q = sum(scene.get_full_errs(point, start_point))
        qs.append(q)

    fig, axs = plt.subplots(nrows=2, sharex=True)
    draw_ECG(axs[0], signal)
    axs[0].vlines(x=start_point, ymin=0, ymax=max(signal), colors='orange', lw=1, label='опорник 1', alpha=0.5)
    axs[0].legend(fancybox=True, framealpha=0.5)

    axs[1].plot(qs)
    best_index = qs.index(min(qs))
    axs[0].vlines(x=best_index, ymin=0, ymax=max(signal), colors='green', lw=1, label='лучший второй опорник', alpha=0.5)

    plt.show()
    




