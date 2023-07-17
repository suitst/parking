import numpy as np
import matplotlib.pyplot as plt


class Road:
    def __init__(self, length):
        self.length = length
        self.cars_parked = []
        self.is_space = True


class Car:
    def __init__(self, length, back):
        self.length = length
        self.back = back
        self.front = self.back + self.length
        self.is_parked = False


def check_car_width_at_start(road, car_length):
    if road.cars_parked[0].back > car_length:
        return True
    else:
        return False


def check_car_width_at_end(road, car_length):
    if (road.length - road.cars_parked[-1].front) > car_length:
        return True
    else:
        return False


def check_width_between_cars(road, car_length):
    spaces = 0
    for i in range(len(road.cars_parked) - 1):
        if (road.cars_parked[i + 1].back - road.cars_parked[i].front) > car_length:
            spaces += 1

    if spaces > 0:
        return True
    else:
        return False


def check_space_at_start(road, car):
    if 0 <= car.back <= road.cars_parked[0].back:
        if 0 <= car.front <= road.cars_parked[0].back:
            return True
        else:
            return False
    else:
        return False


def check_space_at_end(road, car):
    if road.cars_parked[-1].front <= car.back <= road.length:
        if road.cars_parked[-1].front <= car.front <= road.length:
            return True
        else:
            return False
    else:
        return False


def check_space_between_cars(road, car):
    spaces = 0
    for i in range(len(road.cars_parked) - 1):
        if road.cars_parked[i].front <= car.back <= road.cars_parked[i + 1].back:
            if road.cars_parked[i].front <= car.front <= road.cars_parked[i + 1].back:
                spaces += 1
    if spaces == 0:
        return False
    else:
        return True


def check_not_in_car(road, car):
    in_car = 0
    for i in range(len(road.cars_parked)):
        if road.cars_parked[i].back <= car.back <= road.cars_parked[i].front:
            in_car += 1
        elif road.cars_parked[i].back <= car.front <= road.cars_parked[i].front:
            in_car += 1
    if in_car == 0:
        return True
    else:
        return False


def check_for_car_width(road, car):
    if len(road.cars_parked) == 0:
        return True
    elif len(road.cars_parked) == 1:
        width_at_start = check_car_width_at_start(road, car.length)
        width_at_end = check_car_width_at_end(road, car.length)
        if width_at_start or width_at_end:
            return True
        else:
            return False
    else:
        width_at_start = check_car_width_at_start(road, car.length)
        width_at_end = check_car_width_at_end(road, car.length)
        width_between = check_width_between_cars(road, car.length)
        if width_at_start or width_at_end or width_between:
            return True
        else:
            return False


def check_for_space(road, car):
    if len(road.cars_parked) == 0:
        return True
    elif len(road.cars_parked) == 1:
        not_in_car = check_not_in_car(road, car)
        space_at_start = check_space_at_start(road, car)
        space_at_end = check_space_at_end(road, car)
        if not_in_car:
            if space_at_start or space_at_end:
                return True
            else:
                return False
        else:
            return False
    else:
        not_in_car = check_not_in_car(road, car)
        space_at_start = check_space_at_start(road, car)
        space_at_end = check_space_at_end(road, car)
        space_between = check_space_between_cars(road, car)
        if not_in_car:
            if space_at_start or space_at_end or space_between:
                return True
            else:
                return False
        else:
            return False


def create_car(road, mean_length, normal_dist):
    if normal_dist:
        length = round(np.random.normal(mean_length, mean_length/5), 0)
    else:
        length = mean_length
    while road.is_space:
        rand_space = np.random.randint(0, road.length)
        car = Car(length, rand_space)
        in_bounds = check_if_in_bounds(road, car)
        if in_bounds:
            road.is_space = check_for_car_width(road, car)
            if road.is_space:
                car_fits = check_for_space(road, car)
                if car_fits:
                    car.is_parked = True
                    return car
                else:
                    continue
            else:
                return car
        else:
            return car


def check_if_in_bounds(road, car):
    if car.front < road.length:
        return True
    else:
        return False


def park_cars(road, mean_length):
    while road.is_space:
        car = create_car(road, mean_length, normal_dist=True)
        if car.is_parked:
            road.cars_parked.append(car)
            road.cars_parked.sort(key=lambda x: x.back, reverse=False)

    else:
        print(f'{len(road.cars_parked)} cars parked')


def get_distances(road):
    distances = []
    for i in range(len(road.cars_parked) - 1):
        difference = road.cars_parked[i + 1].back - road.cars_parked[i].front
        distances.append(difference)

    distance_array = np.array(distances)
    return distance_array


def plot_distances(distances):
    plt.hist(distances, density=True, bins=10)
    plt.xlabel('Distance between cars (mm)')
    plt.ylabel('Frequency')
    plt.show()


def main():
    mean_car_length = 3000
    road_length = 1000000
    road = Road(road_length)
    print(f'Road length: {road.length/1000} meters')
    print(f'Mean car length: {mean_car_length/1000} meters')
    park_cars(road, mean_length=mean_car_length)
    distances = get_distances(road)
    print(f'mean distance between cars: {distances.mean()/1000} meters')
    print(f'median distance between cars: {np.median(distances)/1000} meters')
    plot_distances(distances)


if __name__ == "__main__":
    main()
