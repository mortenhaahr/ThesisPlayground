#!/usr/bin/env python3

import numpy as np
import torch
import scipy as scp
import matplotlib.pyplot as plt
from tqdm import tqdm

DEVICE = "cpu"
MODEL = "vanilla"


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


def make_nn(N_inputs, N_outputs):
    hidden_dim = 32
    hidden_layers = 5

    # Create input layer with `N_inputs` and `hidden_dim` outputs. Apply softplus.
    layers = [torch.nn.Linear(N_inputs, hidden_dim), torch.nn.Softplus()]
    for _ in range(hidden_layers):
        layers.extend([torch.nn.Linear(hidden_dim, hidden_dim), torch.nn.Softplus()])
    layers.append(torch.nn.Linear(hidden_dim, N_outputs))
    net = torch.nn.Sequential(*layers).double().to(DEVICE)
    return net


def main():
    y0 = [0, 0, 0.001]  # Start at 0, driving with 0 m/s, accelerating with 1 mm/s²
    step_size = 10.0  # [s]
    t_start = 0
    t_end = 2000
    t_eval = np.arange(t_start, t_end, step_size)
    subsample_every = 10
    N_epochs = 2000

    # Formula for position and velocity
    pos = lambda t: y0[0] + t * y0[1] + 1 / 2 * y0[2] * t**2
    vel = lambda t: y0[2] * t

    y_true = np.array([[pos(t) for t in t_eval], [vel(t) for t in t_eval]])

    t = torch.tensor(t_eval, device="cpu", requires_grad=True)
    y_train = torch.tensor(y_true[:, ::subsample_every]).to(DEVICE)
    t_train = torch.tensor(t_eval[::subsample_every], requires_grad=True).to(DEVICE)

    losses = []
    if MODEL == "vanilla":
        nn = make_nn(1, 2)
        optim = torch.optim.Adam(nn.parameters())
        for epoch in tqdm(range(N_epochs), desc="vanilla: training epoch"):
            out = nn(t_train.unsqueeze(-1)).T
            loss_collocation = torch.nn.functional.mse_loss(out, y_train)
            loss_collocation.backward()
            optim.step()
            nn.zero_grad()
            losses.append(loss_collocation.item())

    y_pred = (
        nn(t.unsqueeze(-1)).detach().cpu().T
    )  # Make predictions, detach tensor from graph, move to cpu and transpose

    ############### Print ###############

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    fig.canvas.manager.set_window_title("Vanilla model")
    plot_prediction(t_eval, y_pred[0], y_true[0], "x(t)", ax1, "b")
    plot_prediction(t_eval, y_pred[1], y_true[1], "v(t)", ax2, "r")

    t_samples = t_train.detach().cpu()
    x_samples = y_true[:, ::subsample_every][0]
    v_samples = y_true[:, ::subsample_every][1]
    plot_sample_points(t_samples, x_samples, ax1)
    plot_sample_points(t_samples, v_samples, ax2)

    ax1.legend()
    plt.tight_layout()

    plot_losses("Loss vanilla", losses)

    plt.show()


if __name__ == "__main__":
    main()
