import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

FLOW_SHOWER_TEST_1 = np.array([ 
    3.53707192, #~2L (in (10**-5) * m3/s)
    5.17677951, #~3L (in (10**-5) * m3/s)
    6.63845366, #~4L (in (10**-5) * m3/s)
    8.24241012, #~5L (in (10**-5) * m3/s)
    9.96364749, #~6L (in (10**-5) * m3/s)
    11.90556348 #~7L (in (10**-5) * m3/s)
]) * (10**(-5))

R_PIPE_SHOWER_TEST_1 = np.array([
    285.382325, # in MhOhm
    220.460624, # in MhOhm
    197.286520, # in MhOhm
    187.639841, # in MhOhm
    187.732639, # in MhOhm
    191.593376  # in MhOhm
]) * (10**6)


DELTA_PRESSURE_PIPE_SHOWER_TEST_1 = (FLOW_SHOWER_TEST_1 * R_PIPE_SHOWER_TEST_1) - 8065.01239286441

PRESSURE_TOTAL_SHOWER_1 = np.array([
    387720.890,
    387727.865,
    387758.833,
    387644.474,
    387651.163,
    387616.262
])

FLOW_SHOWER_TEST_2 = np.array([ 
    3.37029080, #~2L (in (10**-5) * m3/s)
    5.14770394, #~3L (in (10**-5) * m3/s)
    6.51961259, #~4L (in (10**-5) * m3/s)
    8.53605300  #~5L (in (10**-5) * m3/s)
]) * (10**(-5))

R_PIPE_SHOWER_TEST_2 = np.array([
    292.035569, # in MhOhm
    217.874984, # in MhOhm
    196.092996, # in MhOhm
    186.754026  # in MhOhm
]) * 10**6

DELTA_PRESSURE_PIPE_SHOWER_TEST_2 = (FLOW_SHOWER_TEST_2 * R_PIPE_SHOWER_TEST_2) - 8065.01239286441

PRESSURE_TOTAL_SHOWER_2 = np.array([
    339265.625,
    339252.836,
    339203.390,
    339217.573    
])

def plot_x_y(x, x_axis_name, y, y_axis_name, title):
    print(title)
    # Create polynomial features
    degree = 2  # Adjust the degree as needed for your polynomial regression
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))

    # Create a linear regression model
    model = LinearRegression()
    # Fit the model to the data
    model.fit(x_poly, y)

    x_test = np.linspace(0, max(x) + max(x)/2, 2000)  # Generate test data
    x_test_poly = poly.transform(x_test.reshape(-1, 1))
    y_pred = model.predict(x_test_poly)

    x_real_poly = poly.transform(x.reshape(-1, 1))
    y_pred_real_x = model.predict(x_real_poly)

    r_squared = r2_score(y, y_pred_real_x)
    print(f"R² value: {r_squared}")

    # Print the equation of the polynomial regression
    equation = f'y = '
    for i, coeff in enumerate(model.coef_):
        equation += f' + {coeff:e}x^{i}' if i > 0 else f'{model.intercept_}'

    print("Polynomial Regression Equation:")
    print(equation)

    # Plot the original data and the regression curve
    plt.scatter(x, y, label='Data points')
    plt.plot(x_test, y_pred, color='red', label=f'Polynomial Regression (degree {degree})')
    plt.title(title)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.legend()
    plt.show()
    print("")

def plot_flow_to_pipe_pressure(both_sample_sets=True):
    
    x = FLOW_SHOWER_TEST_1
    y = DELTA_PRESSURE_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        x = np.hstack((x, FLOW_SHOWER_TEST_2))
        y = np.hstack((y, DELTA_PRESSURE_PIPE_SHOWER_TEST_2))
    
    plot_x_y(x, "Flow [m3/s]", y, "Pressure difference pipe [Pa]", "Pressure drop in pipe over flow")

def plot_flow_squared_to_pipe_pressure(both_sample_sets=True):
    
    x = FLOW_SHOWER_TEST_1
    y = DELTA_PRESSURE_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        x = np.hstack((x, FLOW_SHOWER_TEST_2))
        y = np.hstack((y, DELTA_PRESSURE_PIPE_SHOWER_TEST_2))
    
    plot_x_y(x*x, "Flow [m3/s]", y, "Pressure difference pipe [Pa]", "Pressure drop in pipe over flow")


def plot_resistance_to_flow(both_sample_sets=True):
    x = FLOW_SHOWER_TEST_1
    y = R_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        x = np.hstack((x, FLOW_SHOWER_TEST_2))
        y = np.hstack((y, R_PIPE_SHOWER_TEST_2))

    plot_x_y(x, "Flow [m3/s]", y, "Resistance pipe [MhOhm]", "Resistance over flow")

def plot_resistance_to_flow_squared(both_sample_sets=True):
    x = FLOW_SHOWER_TEST_1
    y = R_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        x = np.hstack((x, FLOW_SHOWER_TEST_2))
        y = np.hstack((y, R_PIPE_SHOWER_TEST_2))
    plot_x_y(x*x, "Flow² [m3/s]", y, "Resistance pipe [MhOhm]", "Resistance over flow")


def plot_flow_to_resistance(both_sample_sets=True):
    x = FLOW_SHOWER_TEST_1
    y = R_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        x = np.hstack((x, FLOW_SHOWER_TEST_2))
        y = np.hstack((y, R_PIPE_SHOWER_TEST_2))

    plot_x_y(y, "Resistance pipe [MhOhm]", x, "Flow [m3/s]", "Resistance over flow")

def plot_flow_to_resistance_squared(both_sample_sets=True):
    flow = PRESSURE_TOTAL_SHOWER_1
    x = DELTA_PRESSURE_PIPE_SHOWER_TEST_1
    y = R_PIPE_SHOWER_TEST_1
    if both_sample_sets:
        flow = np.hstack((flow, PRESSURE_TOTAL_SHOWER_2))
        x = np.hstack((x, DELTA_PRESSURE_PIPE_SHOWER_TEST_2))
        y = np.hstack((y, R_PIPE_SHOWER_TEST_2))

    plot_x_y((flow)/(y*y), "Resistance pipe [MhOhm]", x, "Flow [m3/s]", "Resistance over flow")

def plot_test():
    flow = np.hstack((FLOW_SHOWER_TEST_1, FLOW_SHOWER_TEST_2))
    pressure = np.hstack((PRESSURE_TOTAL_SHOWER_1, PRESSURE_TOTAL_SHOWER_2))
    resistance = np.hstack((R_PIPE_SHOWER_TEST_1, R_PIPE_SHOWER_TEST_2))
    dpipe_pressure = np.hstack((DELTA_PRESSURE_PIPE_SHOWER_TEST_1, DELTA_PRESSURE_PIPE_SHOWER_TEST_2))

    tests = [(flow, "flow"), (pressure, "pressure"), (resistance, "resistance"), (dpipe_pressure, "pipe_pressure")]

    for i in range(len(tests)):
        for j in range(len(tests)):
            if i == j: continue
            x, name_x = tests[i]
            y, name_y = tests[j]
            plot_x_y(x, name_x, y, name_y, f"{name_y} over {name_x}")
            plot_x_y(x*x, f"{name_x}²", y, name_y, f"{name_y} over {name_x}²")
            plot_x_y(x, f"{name_x}", y*y, f"{name_y}²", f"{name_y}² over {name_x}")
            plot_x_y(x*x, f"{name_x}²", y*y, f"{name_y}²", f"{name_y}² over {name_x}²")
            
plot_test()

x = 42