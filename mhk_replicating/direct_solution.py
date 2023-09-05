#!/usr/bin/env python3

import numpy as np
import torch
import scipy as scp
import matplotlib.pyplot as plt
from tqdm import tqdm

g = 1.0  # gravitational acceleration [m/s^2]
l = 1.0  # length of pendulum [m]

DEVICE = "cpu"


def pendulum_derivative(t, y):
    # Used when solving for the ideal pendulum
    theta, omega = y
    d_omega = -(g / l) * np.sin(theta)
    return omega, d_omega


def init_tensors(module):
    # Init the tensors with random values based on a xavier uniform distribution
    for m in module.modules():
        if type(m) == torch.nn.Linear:
            # NOTE: Weights are technically already initialized - so xavier is not needed
            torch.nn.init.xavier_uniform_(m.weight)


# plot loss functions as function of training steps
def plot_losses(title, losses):
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    ax.plot(losses, label=title)

    ax.legend()
    ax.set_xlabel("epoch")


def plot_prediction(y_pred, y_true, y_label, ax, color="black"):
    ax.set_ylabel(y_label)
    ax.set_xlabel("t [s]")

    ax.plot(t_eval, y_true, c="black", label="true") # True is black
    ax.plot(t_eval, y_pred, c=color, linestyle="--", label="predicted")

def plot_sample_points(t_vals, sample_points, ax):
    ax.scatter(
        t_vals,
        sample_points,
        c="black",
        linestyle="None",
        label="Sample point",
    )


def make_nn():
    hidden_dim = 32
    hidden_layers = 5
    N_inputs = 1
    N_outputs = 2

    # Create input layer with `N_inputs` and `hidden_dim` outputs. Apply softplus.
    layers = [torch.nn.Linear(N_inputs, hidden_dim), torch.nn.Softplus()]
    for _ in range(hidden_layers):
        layers.extend([torch.nn.Linear(hidden_dim, hidden_dim), torch.nn.Softplus()])
    layers.append(torch.nn.Linear(hidden_dim, N_outputs))
    net = torch.nn.Sequential(*layers).double().to(DEVICE)
    init_tensors(net)
    return net


if __name__ == "__main__":
    y0 = [np.pi / 4, 0]  # Dropping location
    step_size = 0.01  # [s]
    t_start = 0
    t_end = np.pi * 4
    t_eval = np.arange(t_start, t_end, step_size)
    subsample_every = int(2.5 / step_size)
    N_epochs = 2000

    y_true = scp.integrate.solve_ivp(
        pendulum_derivative, (t_start, t_end), t_eval=t_eval, y0=y0, method="RK45"
    ).y

    theta, omega = y_true

    t = torch.tensor(t_eval, device="cpu", requires_grad=True)
    y_train = torch.tensor(y_true[:, ::subsample_every]).to(DEVICE)
    t_train = torch.tensor(t_eval[::subsample_every], requires_grad=True).to(DEVICE)
    d_omega_pred = None
    print(y_train)

    nn = make_nn()
    optim = torch.optim.Adam(nn.parameters())
    losses = []

    for epoch in tqdm(range(N_epochs), desc="vanilla: training epoch"):
        out = nn(t_train.unsqueeze(-1)).T
        loss_collocation = torch.nn.functional.mse_loss(out, y_train)
        loss_collocation.backward()
        optim.step()
        nn.zero_grad()
        losses.append(loss_collocation.item())

    y_pred = nn(t.unsqueeze(-1)).detach().cpu().T  # Make predictions, detach tensor from graph, move to cpu and transpose

    ############### Print ###############
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.canvas.manager.set_window_title("Vanilla model")
    plot_prediction(y_pred[0], y_true[0], "θ(t)", ax1, "b")
    plot_prediction(y_pred[1], y_true[1], "ω(t)", ax2, "r")

    t_samples = t_train.detach().cpu()
    theta_samples = y_true[:, ::subsample_every][0]
    omega_samples = y_true[:, ::subsample_every][1]
    plot_sample_points(t_samples, theta_samples, ax1)
    plot_sample_points(t_samples, omega_samples, ax2)

    ax2.legend()
    plt.tight_layout()

    plot_losses("Loss vanilla", losses)

    plt.show()
