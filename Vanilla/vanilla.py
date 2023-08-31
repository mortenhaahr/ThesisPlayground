
from argparse import ArgumentParser
from collections import defaultdict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from tqdm import tqdm
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib as mpl


if __name__ == "__main__":  
    parser = ArgumentParser()
    parser.add_argument("--hidden_dim", default=32, type=int)
    parser.add_argument("--n_layers", default=5, type=int)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--model", choices=["vanilla"], default="vanilla")
    parser.add_argument("--n_epochs", default=20000, type=int)
    parser.add_argument("--step_size", default=0.1, type=float)
    parser.add_argument("--t_start", default=0.0, type=float)
    parser.add_argument("--t_end", type=float, default=np.pi * 4)
    args = parser.parse_args()


    ############### Setup Experiment ###############
    y0 = [np.pi / 4, 0]
    step_size = args.step_size
    t_start = args.t_start
    t_end = args.t_end
    t_span = (t_start, t_end)
    t_eval = np.arange(t_start, t_end, step_size)  # 0.0 , 0.01

    g = 1.0  # gravitational acceleration [m/s^2]
    l = 1.0  # length of pendulum [m]

    model = args.model
    n_epochs = args.n_epochs
    device = args.device
    subsample_every = int(2.5 / step_size)

    ############### Define Derivative ###############
    def f(t, y):
        θ, ω = y  # state variables go in
        dω = -(g / l) * np.sin(θ)
        dθ = ω  # special case (common for mechanical systems), the state variable ω is per definition dθ

        return dθ, dω  # derivatives of state variables go out

    ############### Solve ODE ###############

    res = solve_ivp(f, t_span, t_eval=t_eval, y0=y0, method="RK45")
    θ, ω = res.y

    ############### Model construction ###############
    def construct_network(input_dim, output_dim):
        hidden_dim = args.hidden_dim
        hidden_layers = args.n_layers

        layers = [nn.Linear(input_dim, hidden_dim), nn.Softplus()]
        for _ in range(hidden_layers):
            layers.extend([nn.Linear(hidden_dim, hidden_dim), nn.Softplus()])
        layers.append(nn.Linear(hidden_dim, output_dim))

        net = nn.Sequential(*layers).double().to(device)

        def xavier_init(module):
            for m in module.modules():
                if type(m) == nn.Linear:
                    nn.init.xavier_uniform_(m.weight)

        xavier_init(net)
        return net
    
    ############### Modelling ####################

    t = torch.tensor(t_eval, device=device, requires_grad=True)
    losses = defaultdict(lambda: defaultdict(list))

    y_train = torch.tensor(res.y[:, ::subsample_every]).to(device)
    t_train = torch.tensor(t_eval[::subsample_every], requires_grad=True).to(device)

    nn_vanilla = construct_network(1,2)
    opt_vanilla = torch.optim.Adam(nn_vanilla.parameters())

    for epoch in tqdm(range(n_epochs), desc="vanilla: training epoch"):
        out = nn_vanilla(t_train.unsqueeze(-1)).T

        loss_collocation = F.mse_loss(out, y_train)

        loss_collocation.backward()
        opt_vanilla.step()
        nn_vanilla.zero_grad()
        losses["vanilla"]["collocation"].append(loss_collocation.item())

    θω_pred = nn_vanilla(t.unsqueeze(-1)).detach().detach().cpu().T



    # `torch.autograd.grad` supports only lists of scalar values (e.g. single evaluation of network).
    # however the function accepts a list of these.
    def listify(A):
        return [a for a in A.flatten()]

    ############### Plot ###############

    def plot_colored(ax, x, y, c, cmap=plt.cm.jet, steps=10, **kwargs):
        a = c.size
        c = np.asarray(c)
        c -= c.min()
        c = c / c.max()
        it = 0
        while it < c.size - steps:
            x_segm = x[it : it + steps + 1]
            y_segm = y[it : it + steps + 1]
            c_segm = cmap(c[it + steps // 2])
            ax.plot(x_segm, y_segm, c=c_segm, **kwargs)
            it += steps

    def plot_predictions(model, θω_pred):
        ω_numerical = np.diff(θω_pred[:1]) / step_size
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        fig.canvas.manager.set_window_title(model)
        ax1.set_ylabel("θ(t)")
        ax2.set_ylabel("ω(t)")
        ax2.set_xlabel("t")

        ax1.plot(t_eval, θ, c="black", label="true")
        ax1.plot(t_eval, θω_pred[0], c="b", linestyle="--", label="predicted")

        ax2.plot(t_eval, ω, c="black", label="true")
        ax2.plot(t_eval, θω_pred[1], c="r", linestyle="--", label="predicted")
        ax2.plot(
            t_eval[1:],
            ω_numerical.T,
            c="r",
            linestyle="dotted",
            label="numerical",
        )

        ax1.scatter(
            t_eval[::subsample_every],
            res.y[:, ::subsample_every][0],
            c="black",
            linestyle="None",
            label="collocation point",
        )
        ax2.scatter(
            t_eval[::subsample_every],
            res.y[:, ::subsample_every][1],
            c="black",
            linestyle="None",
            label="collocation point",
        )
        ax2.legend()
        plt.tight_layout()

    # plot loss functions as function of training steps
    def plot_losses(model, losses):
        fig, ax = plt.subplots()
        fig.canvas.manager.set_window_title(f"loss terms '{model}'")

        for loss_name, loss in losses.items():
            ax.plot(loss, label=loss_name)

        ax.legend()
        ax.set_xlabel("epoch")

    plot_predictions(model, θω_pred)
    plot_losses(model, losses[model])

    fig = plt.figure()
    x, y = np.meshgrid(
        np.arange(-np.pi, np.pi, 0.01),
        np.arange(-np.pi, np.pi, 0.01),
    )
    dθ, dω = f(None, (x, y))
    plt.streamplot(x, y, dθ, dω, density=2)
    plt.xlabel("θ")
    plt.ylabel("ω")
    fig.canvas.manager.set_window_title(f"phase portrait '{model}'")

    ax = plt.gca()
    plot_colored(ax, θ, ω, t_eval)
    cmap = plt.cm.jet

    norm = mpl.colors.Normalize(vmin=t_eval.min(), vmax=t_eval.max())
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

    # draw initial state
    plt.scatter(θ[0], ω[0], label="$y_0$", marker="*", c="g", s=200, zorder=100)
    plt.legend(loc="upper right")
    ax.set_aspect(1)

    plt.show()

    