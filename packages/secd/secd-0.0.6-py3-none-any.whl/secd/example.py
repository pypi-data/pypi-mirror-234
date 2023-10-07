import pandas as pd
import matplotlib.pyplot as plt
import random
import secd


@secd.cache
def generate_data():
    return [random.randint(0, 500) for _ in range(1000)]


@secd.cache
def clean_data(data):
    return [x for x in data if x in [69, 420]]


def plot_data(data):
    print("plotting data")
    # plot the data as histogram, save to plot.png
    plt.hist(data)
    plt.savefig("plot.png")
    return data


@secd.cache
def get_r_cars_dataset():
    # load the r_cars dataset from github
    url = 'https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json'
    df = pd.read_json(url)
    return df


data = generate_data()
cleaned_data = clean_data(data)
plot = plot_data(cleaned_data)

df = get_r_cars_dataset()


@secd.cache
def expensive_calculation(x, y):
    return x + y


# Function is executed and result is saved
result1 = expensive_calculation(2, 3)
# Cached result is used, function is skipped
result2 = expensive_calculation(2, 3)
