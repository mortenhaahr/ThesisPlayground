import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn import metrics


"""All measurements are based off the shower appliance and made from datasets from 2023.11.01"""

# Total P = calc.json line 105 = The pressure measured at pump outlet
TOTAL_P = np.array(
    [
        # Test 1 - stable_shower_XL - 2023.11.01 around 12 O'clock:
        387720.8904109589,
        387727.8645833334,
        387758.83256528416,
        387644.4740346205,
        387651.1627906977,
        387616.2624821683,
        # Test 2 - stable_shower_XL - 2023.11.01 around 13 O'clock. (1L not included):
        339265.625,
        339252.8363047002,
        339203.38983050844,
        339217.5732217573,
        # Stable_shower_full
        339191.5204678363,
    ]
)

# Bathroom P = calc.json line 114 = The pressure measured at the bathroom appliances
BATHROOM_P = np.array(
    [
        # Test 1 - stable_shower_XL - 2023.11.01 around 12 O'clock:
        377626.7123287672,
        376315.1041666666,
        374662.0583717358,
        372178.4287616511,
        368946.1444308446,
        364805.99144079885,
        # Test 2 - stable_shower_XL - 2023.11.01 around 13 O'clock. (1L not included):
        329423.1770833333,
        328037.2771474879,
        326418.8861985472,
        323276.1506276151,
        # Stable_shower_full
        322241.2280701754,
    ]
)

# Flow = calc.json line 101 = The flow going out of the pump
FLOW_MEASUREMENTS = np.array(
    [
        # Test 1 - stable_shower_XL - 2023.11.01 around 12 O'clock:
        3.53707191780822e-05,
        5.176779513888888e-05,
        6.638453661034308e-05,
        8.242410119840214e-05,
        9.963647490820074e-05,
        0.00011905563480741797,
        # Test 2 - stable_shower_XL - 2023.11.01 around 13 O'clock. (1L not included):
        3.3702907986111107e-05,
        5.147703943814154e-05,
        6.519612590799032e-05,
        8.536052998605299e-05,
        # Stable_shower_full
        9.10672514619883e-05,
    ]
)

# Main pipe + bathroom pipe = calc.json line 163 = The resistance that was calculated
CALC_RESISTANCE = np.array(
    [
        # Test 1 - stable_shower_XL - 2023.11.01 around 12 O'clock:
        1650353588650.0317,
        1262477595976.519,
        1149861718133.747,
        1094627207625.4003,
        1075361957841.3368,
        1042794943531.3098,
        # Test 2 - stable_shower_XL - 2023.11.01 around 13 O'clock. (1L not included):
        1596117060360.324,
        1202360693360.6538,
        1118697513515.0212,
        1085853083558.3383,
        # Stable_shower_full
        1075676925006.1124,
    ]
)

# The average pressure loss due to height (constant across all measurements) = calc.json line 8
CALC_CONSTANT_HEIGHT_PRES = 8029.440882715899


def lin_reg(x, y):
    """Calculates a 2nd degree linear regression based on X and Y"""

    # Transform the features to include polynomial features up to degree 2
    poly_features = PolynomialFeatures(degree=2, include_bias=False)
    x_poly = poly_features.fit_transform(x.reshape(-1, 1))

    # Create a linear regression model
    lin_reg = LinearRegression(fit_intercept=True)

    # Fit the model to the transformed features
    lin_reg.fit(x_poly, y)

    # Make predictions using the model
    x_new = np.linspace(0, max(x), 100).reshape(-1, 1)
    x_new_poly = poly_features.transform(x_new)
    y_pred = lin_reg.predict(x_new_poly)
    # y_calc = parms_calc * x**2 + parms_const
    # y_calc = np.multiply(parms_calc, np.linspace(0, max(x), 100))

    # Calculate and print the scores
    y_pred_train = lin_reg.predict(x_poly)
    r2 = metrics.r2_score(y, y_pred_train)
    mse = metrics.mean_absolute_error(y, y_pred_train)
    rmse = np.sqrt(mse)
    print(f"Scores (X^2). R2 Score: {r2}. MSE: {mse}. RMSE: {rmse}")

    # Retrieve the coefficients
    coef = lin_reg.coef_
    intercept = lin_reg.intercept_

    # Print the regression equation
    print(
        f"Regression Equation: y = {coef[1]:.2f} * X^2 + {coef[0]:.2f} * X + {intercept:.2f}"
    )

    # Plot the original data and the regression curve
    plt.scatter(x, y, label="Original Data")
    # plt.scatter(x, y_calc, label="Calc data")
    plt.plot(x_new, y_pred, "r-", label="Regression Curve", linewidth=2)
    plt.xlabel("Flow [m3/s]")
    plt.ylabel("Pressure loss over pipes [Pa]")
    plt.legend()
    plt.show()


def lin_reg_no_x1(x, y):
    """Calculates a 2nd degree linear regression without the a1 term based on x and y"""

    # Use only the X^2 term for linear regression
    x_squared = x**2

    # Create a linear regression model with a bias term
    lin_reg = LinearRegression(fit_intercept=True)

    # Reshape X_squared to have a single feature (required by scikit-learn)
    x_squared = x_squared.reshape(-1, 1)

    # Fit the model to the X^2 term
    lin_reg.fit(x_squared, y)

    # Make predictions using the model
    x_new = np.linspace(0, max(x), 100).reshape(-1, 1)
    x_new_squared = x_new**2
    y_pred = lin_reg.predict(x_new_squared)

    # Calculate and print the scores
    y_pred_train = lin_reg.predict(x_squared)
    r2 = metrics.r2_score(y, y_pred_train)
    mse = metrics.mean_absolute_error(y, y_pred_train)
    rmse = np.sqrt(mse)
    print(f"Scores (X^2). R2 Score: {r2}. MSE: {mse}. RMSE: {rmse}")

    # Retrieve the coefficients
    coef = lin_reg.coef_
    intercept = lin_reg.intercept_

    # Print the regression equation
    print(f"Regression Equation (X^2): y = {coef[0]:.2f} * X^2 + {intercept:.2f}")

    # Calculate residuals (deviation from the regression)
    # y_pred_residuals = lin_reg.predict(x_squared)
    # residuals = y - y_pred_residuals
    # plt.scatter(x, residuals, label='Residuals', color='green', marker='x')
    # plt.axhline(0, color='black', linestyle='--', linewidth=1)  # Horizontal line at y=0

    # # Plot the original data and the regression curve
    plt.scatter(x, y, label="Original Data")
    plt.plot(x_new, y_pred, "r-", label="Regression Curve (X^2 Term Only)", linewidth=2)
    plt.xlabel("Flow [m3/s]")
    plt.ylabel("Pressure loss over pipes [Pa]")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    measured_flow = FLOW_MEASUREMENTS
    measured_pressure = TOTAL_P - BATHROOM_P
    calc_resistance = CALC_RESISTANCE
    calc_constant_loss = CALC_CONSTANT_HEIGHT_PRES

    ### Playground for finding the first resistance value:
    # (This can be made comparable to the regression X^2 constant, by `press1 = saying measured_pressure[0] - regression_constant` instead)
    # flow1 = measured_flow[0]
    # press1 = measured_pressure[0] - calc_constant_loss
    # res1 = press1/(flow1**2)
    # print(f"Press1: {press1}. Flow1: {flow1}. Resistance 1: {res1}")
    # lin_reg_p = 996769707605.53 * flow1**2
    # print(f"LinReg P: {lin_reg_p}")

    ### Comparison to Bathroom leakage:
    # LEAKAGE_F = 0.00022462993197278912
    # LEAKAGE_TOTAL_P = 338972.7891156463
    # LEAKAGE_BATHROOM_P = 282530.612244898

    # REG_SAYS_P = 996769707605.53 * LEAKAGE_F**2 + 8697.55
    # print(f"Reg p: {REG_SAYS_P}. Actual P = {LEAKAGE_TOTAL_P - LEAKAGE_BATHROOM_P}")

    lin_reg(measured_flow, measured_pressure)
    lin_reg_no_x1(measured_flow, measured_pressure)

    # When constant drop is taken off:
    # lin_reg(measured_flow, measured_pressure - calc_constant_loss)
    # lin_reg_no_x1(measured_flow, measured_pressure - calc_constant_loss)
