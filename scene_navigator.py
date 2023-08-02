from ECG_getter import get_mini_ECG
from draw_utils import draw_ECG


import matplotlib.pyplot as plt



class SceneNavigator:
    def __init__(self, signal):
        self.signal = signal

    def get_indexes_of_region_from_min(self, point1, point2):
        if point1 == point2:
            return [point2]
        left = point1
        right = point2
        if point2 < point1:
            left = point2
            right = point1

        indexes = list(range(left, right + 1))
        return indexes

    def get_full_indexes(self):
        return list(range(0, len(self.signal)))


    def get_indexes_left_to_region(self, point1, point2):
        inner_indexes = self.get_indexes_of_region_from_min(point1, point2)
        min_index = min(inner_indexes)
        if min_index>0:
            return list(range(0, min_index))
        return []

    def get_indexes_right_to_region(self, point1, point2):
        inner_indexes = self.get_indexes_of_region_from_min(point1, point2)
        max_index = max(inner_indexes)
        last_index = len(self.signal)-1
        if max_index<last_index:
            return list(range(max_index, last_index+1))
        return []

    def get_mean_in_indexes(self, indexes):
        sum = 0
        for i in indexes:
            sum+=self.signal[i]
        return sum/len(indexes)

    def get_inner_prediction(self, point1, point2):
        prediction = []
        if point1 == point2:
            return [self.signal[point1]]
        inner_indexes_sorted = self.get_indexes_of_region_from_min(point1, point2)
        val_left = self.signal[inner_indexes_sorted[0]]
        val_right = self.signal[inner_indexes_sorted[-1]]

        step = (val_right - val_left)/(len(inner_indexes_sorted)-1)
        for i in range(0, len(inner_indexes_sorted)):
            prediction.append(val_left+ i*step)
        return prediction

    def get_full_predicion(self, point1, point2):
        full_pred = []
        indexes_left = self.get_indexes_left_to_region(point1, point2)
        if len(indexes_left)>0:
            mean_left = self.get_mean_in_indexes(indexes_left)
            full_pred= full_pred + [mean_left]*(len(indexes_left))

        inner_prediction = self.get_inner_prediction(point1, point2)
        full_pred = full_pred + inner_prediction

        indexes_right = self.get_indexes_right_to_region(point1, point2)
        if len(indexes_right)>0:
            mean_right = self.get_mean_in_indexes(indexes_right)
            full_pred = full_pred + [mean_right]*(len(indexes_right))

        return full_pred

    def get_full_errs(self, point1, point2):
        errs = []
        prediction = self.get_full_predicion(point1, point2)
        for i in range(len(self.signal)):
            err = abs(self.signal[i] - prediction[i])
            errs.append(err)
        return errs

    def get_err_in_inner(self, point1, point2):
        prediction = self.get_inner_prediction(point1, point2)
        indexes = self.get_indexes_of_region_from_min(point1, point2)
        pass


if __name__ == '__main__':
    signal = get_mini_ECG()

    point1= 216
    point2= 205

    fig, axs = plt.subplots()
    draw_ECG(axs, signal)

    scene = SceneNavigator(signal)
    prediction= scene.get_full_predicion(point1, point2)
    axs.plot(prediction, label="prediction")

    axs.vlines(x=point1, ymin=0, ymax=max(signal), colors='orange', lw=1, label='опорники', alpha=0.5)

    axs.vlines(x=point2, ymin=0, ymax=max(signal), colors='orange', lw=1, alpha=0.5)

    err = scene.get_full_errs(point1, point2)
    axs.plot(err, '--', label="err")
    axs.legend(fancybox=True, framealpha=0.5)
    plt.show()

