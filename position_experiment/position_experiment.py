#!/usr/bin/env python3

import numpy as np
import torch
import scipy as scp
import matplotlib.pyplot as plt
from tqdm import tqdm

DEVICE = "cpu"
MODEL = "vanilla"
TAU = 100
TRANSFORMATION = TAU != 1  # Use transformation if TAU != 1


# plot loss functions as function of training steps
def plot_losses(title, losses):
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    ax.plot(losses, label=title)

    ax.legend()
    ax.set_xlabel("epoch")


def plot_prediction(t_eval, y_pred, y_true, y_label, ax, color="black"):
    ax.set_ylabel(y_label)
    ax.set_xlabel("t [s]")

    ax.plot(t_eval, y_true, c="black", label="true")  # True is black
    ax.plot(t_eval, y_pred, c=color, linestyle="--", label="predicted")


def plot_sample_points(t_vals, sample_points, ax):
    ax.scatter(
        t_vals,
        sample_points,
        c="black",
        linestyle="None",
        label="Sample point",
    )


def make_nn(input_dim, output_dim):
    hidden_dim = 32
    hidden_layers = 5

    # Create input layer with `N_inputs` and `hidden_dim` outputs. Apply softplus.
    layers = [torch.nn.Linear(input_dim, hidden_dim), torch.nn.Softplus()]
    for _ in range(hidden_layers):
        layers.extend([torch.nn.Linear(hidden_dim, hidden_dim), torch.nn.Softplus()])
    layers.append(torch.nn.Linear(hidden_dim, output_dim))
    net = torch.nn.Sequential(*layers).double().to(DEVICE)
    return net


# `torch.autograd.grad` supports only lists of scalar values (e.g. single evaluation of network).
# however the function accepts a list of these.
# (Converts tensor with list to list of tensors)
def listify(A):
    return [a for a in A.flatten()]

def main():
    """
    NOTE:
    This works in the simulation but it may or may not be that useable for real-world examples.
    When we calculate `y_true` we essentially cheat a little by calculating with the new time scale directly.
    If the data was sampled through the real world, this transformation would not be possible to make, as
    we would then have to calculate "x0", "v0" and "a" through our input data.
    In order to calculate this, we would strictly impose that the data adheres to the physics equations.
    I.e., we enforce a strict relationship between the equations and our data - even though that may not be 100 % true
    in a real-world scenario.
    Furthermore, if this strict relationship was true then it would not make any sense to create a data-driven model in the
    first place, since we can use a first-principle model.
    I.e., a program that takes a "t" and returns x0*t + v0*t + 1/2*a*t².
    """

    y0 = [0, 0, 0.01]  # Start at 0, driving with 0 m/s, accelerating with 1 mm/s²
    step_size = 10.0  # [s]
    t_start = 0
    t_end = 2000
    t_eval = np.arange(t_start / TAU, t_end / TAU, step_size / TAU)
    t_eval_non_transformed = np.arange(t_start, t_end, step_size)
    subsample_every = 10
    N_epochs = 2000

    # Formula for position and velocity
    pos = lambda t: y0[0] + t * y0[1] + 1 / 2 * y0[2] * t**2
    vel = lambda t: y0[1] + y0[2] * t

    y_true = torch.tensor(
        np.array(
            [
                [pos(t) for t in t_eval_non_transformed],
                [vel(t) for t in t_eval_non_transformed],
            ]
        )
    )
    y_transf = torch.tensor(
        np.array([[pos(t) for t in t_eval], [vel(t) for t in t_eval]])
    )

    t = torch.tensor(t_eval, device="cpu", requires_grad=True)
    y_train = torch.tensor(y_transf[:, ::subsample_every]).to(DEVICE)
    t_train = torch.tensor(t_eval[::subsample_every], requires_grad=True).to(DEVICE)

    output_dim = 2 if MODEL == "vanilla" else 1
    nn = make_nn(1, output_dim)
    optim = torch.optim.Adam(nn.parameters())
    losses = []

    loss_func = torch.nn.functional.mse_loss

    for epoch in tqdm(range(N_epochs), desc=f"{MODEL}: training epoch"):
        out = None
        if MODEL == "vanilla":
            out = nn(t_train.unsqueeze(-1)).T
        elif MODEL == "autodiff":
            theta_pred = nn(t_train.unsqueeze(-1)).T
            theta_tmp = listify(theta_pred)
            # [0] since we differentiate with respect to an "single input",
            # which is coincidentially a tensor.
            # in this case  ω ≜ dθ
            omega_pred = torch.autograd.grad(
                theta_tmp,
                t_train,
                only_inputs=True,
                retain_graph=True,
                create_graph=True,
            )[0].unsqueeze(0)
            out = torch.cat((theta_pred, omega_pred), dim=0)
        elif MODEL == "pinn":
            # When calculating equation loss we use the full time scale.
            # This is OK as long as we don't use the true-values.
            # (We can always make a time-axis...)
            t_train_dense = torch.tensor(t_eval, requires_grad=True).to(DEVICE)
            theta_pred = nn(t_train_dense.unsqueeze(-1)).T
            theta_tmp = listify(theta_pred)

            omega_pred = torch.autograd.grad(
                theta_tmp,
                t_train_dense,
                only_inputs=True,
                retain_graph=True,
                create_graph=True,
            )[0].unsqueeze(0)

            omega_tmp = listify(omega_pred)
            a_pred = torch.autograd.grad(
                omega_tmp,
                t_train_dense,
                only_inputs=True,
                retain_graph=True,
                create_graph=True,
            )[0].unsqueeze(0)

            # Enforce relation that velocity can be calculated through
            # v = v0 + a*t
            # (There are many different options here but this gives best results)
            omega_eq = omega_pred[0][0] + a_pred * t
            loss_equation = loss_func(omega_pred, omega_eq)

            # collocation loss only uses training data
            theta_omega_dense = torch.cat((theta_pred, omega_pred), dim=0)
            out = theta_omega_dense[:, ::subsample_every]

        if MODEL == "pinn":
            loss_collocation = loss_func(out, y_train) + loss_equation
        else:
            loss_collocation = loss_func(out, y_train)
        loss_collocation.backward()

        if MODEL == "autodiff" or MODEL == "pinn":
            # sanity check
            max_grad = next(nn.modules())[0].weight.grad.max()
            assert (
                max_grad != 0.0
            ), "maximal gradient of first layer was zero, something is up!"

        optim.step()
        nn.zero_grad()
        losses.append(loss_collocation.item())

    if MODEL == "vanilla":
        y_pred = (
            nn(t.unsqueeze(-1)).detach().cpu().T
        )  # Make predictions, detach tensor from graph, move to cpu and transpose
    elif MODEL == "autodiff" or MODEL == "pinn":
        x_pred = nn(t.unsqueeze(-1)).T
        x_tmp = listify(x_pred)
        v_pred = torch.autograd.grad(x_tmp, t, only_inputs=True)[0].unsqueeze(0)
        y_pred = torch.cat((x_pred, v_pred), dim=0).detach().cpu()

    ############### Inverse transform ###############
    if TRANSFORMATION:
        # We the parameters to make the inverse transformation
        x0 = y_pred[0][0]
        v0 = y_pred[1][0]
        a = torch.mean((y_pred[1][1:] - v0) / (t[1:]))
        v = v0 + a * (t * TAU)
        x = x0 + 1 / 2 * (v0 + v) * (t * TAU)
        y_pred = torch.cat((x.view(1, -1), v.view(1, -1)), dim=0).detach().cpu()

    ############### Print ###############
    # (For real tests the training data should be excluded)
    print(
        f"Score (with training data): {torch.nn.functional.mse_loss(y_pred, y_true)}"
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.canvas.manager.set_window_title(
        f"{MODEL} model{' - with tau' if TRANSFORMATION else ''}"
    )
    plot_prediction(
        t_eval_non_transformed, y_pred[0], y_true[0], "x(t)", ax1, "b"
    )
    plot_prediction(
        t_eval_non_transformed, y_pred[1], y_true[1], "v(t)", ax2, "r"
    )

    t_samples = t_train.detach().cpu()
    if TRANSFORMATION:
        t_samples = t_samples * TAU
    x_samples = y_true[:, ::subsample_every][0]
    v_samples = y_true[:, ::subsample_every][1]
    plot_sample_points(t_samples, x_samples, ax1)
    plot_sample_points(t_samples, v_samples, ax2)

    ax1.legend()
    plt.tight_layout()

    plot_losses(f"Loss {MODEL}", losses)

    plt.show()


if __name__ == "__main__":
    main()
