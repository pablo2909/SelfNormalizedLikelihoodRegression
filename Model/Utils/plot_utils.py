import os

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import torchvision


def print_discrete_params(algo, save_dir, step=""):
    if algo.args_dict["dataset_name"] == "poisson":
        print(f"self.ebm.energy.theta {algo.ebm.energy.lambda_}")
    elif algo.args_dict["dataset_name"] == "categorical":
        print(f"self.ebm.energy.theta {F.softmax(algo.ebm.energy.theta)}")
    elif algo.args_dict["dataset_name"] == "ising":
        plot_log_rmse(algo, save_dir, name="log_rmse", step=step)
    else:
        raise NotImplementedError


def plot_log_rmse(algo, save_dir, name="log_rmse", step=""):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    fig, ax = plt.subplots()
    ax.plot([k[1] for k in algo.log_rmse], [k[0] for k in algo.log_rmse], "o-")
    ax.set(xlabel="iteration", ylabel="log_rmse")
    plt.savefig(os.path.join(save_dir, "{}_{}.png".format(name, step)))
    print(f"Saved at {os.path.join(save_dir, '{}_{}.png'.format(name, step))}")

    if algo.args_dict["decay_ema"] is not None:
        fig, ax = plt.subplots()
        ax.plot(
            [k[1] for k in algo.log_rmse_val], [k[0] for k in algo.log_rmse_val], "o-"
        )
        ax.set(xlabel="iteration", ylabel="log_rmse_val")
        plt.savefig(
            os.path.join(save_dir, "{}_val_{}.png".format(name, step)),
        )
        print(
            f"Saved at {os.path.join(save_dir, '{}_val_{}.png'.format(name, step))}",
        )


def plot_energy_2d(
    algo,
    save_dir,
    energy_function=None,
    name="contour_best",
    samples=[],
    samples_title=[],
    step="",
    energy_type=True,
):
    """
    Plot the energy of the EBM in 2D and the data points
    """

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if energy_function is None:
        energy_function = lambda x: algo.ebm.calculate_energy(x)[0]
    nx = 1000
    ny = 1000
    min_x, max_x = algo.min_x, algo.max_x
    min_y, max_y = algo.min_y, algo.max_y

    for s, title in zip(samples, samples_title):
        min_x, max_x = min(
            torch.min(
                s[:, 0],
            ),
            min_x,
        ), max(torch.max(s[:, 0]), max_x)
        min_y, max_y = min(
            torch.min(
                s[:, 1],
            ),
            min_y,
        ), max(torch.max(s[:, 1]), max_y)

    x = np.linspace(min_x, max_x, nx)
    y = np.linspace(min_y, max_y, ny)

    xx, yy = np.meshgrid(x, y)
    xy = np.concatenate([xx.reshape(-1, 1), yy.reshape(-1, 1)], axis=1)
    xy = torch.from_numpy(xy).float()
    if energy_type:
        z = (-energy_function(xy)).exp().detach().cpu().numpy()
    else:
        z = energy_function(xy).detach().cpu().numpy()
    z = z.reshape(nx, ny)
    assert len(samples_title) == len(samples)
    fig, axs = plt.subplots(1, 2 + len(samples), figsize=(10 + 5 * len(samples), 5))

    axs[0].contourf(x, y, z, 100)
    axs[0].set_title("Energy")
    for i, (s, s_title) in enumerate(zip(samples, samples_title)):
        axs[i + 1].contourf(x, y, z, 100)
        axs[i + 1].scatter(s[:, 0], s[:, 1], c="r", alpha=0.1)
        axs[i + 1].set_title(s_title)
    fig.colorbar(axs[0].contourf(x, y, z, 100), cax=axs[-1])
    plt.savefig(os.path.join(save_dir, "{}_{}.png".format(name, step)))
    try:
        algo.logger.log_image(
            key="{}.png".format(
                name,
            ),
            images=[fig],
        )
    except AttributeError as e:
        print(
            e,
        )
    plt.close()


def plot_energy_1d_1d_regression(
    algo,
    save_dir,
    energy_function=None,
    name="contour_best",
    samples_x=[],
    samples_y=[],
    samples_title=[],
    step="",
    energy_type=True,
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if energy_function is None:
        energy_function = lambda x, y: algo.ebm.calculate_energy(x, y)[0]

    nx = 1000
    ny = 1000
    min_x, max_x = algo.min_x, algo.max_x
    min_y, max_y = algo.min_y, algo.max_y

    for s_x, s_y, title in zip(samples_x, samples_y, samples_title):
        min_x, max_x = min(
            torch.min(
                s_x,
            ),
            min_x,
        ), max(torch.max(s_x), max_x)
        min_y, max_y = min(
            torch.min(
                s_y,
            ),
            min_y,
        ), max(torch.max(s_y), max_y)

    x = np.linspace(min_x, max_x, nx)
    y = np.linspace(min_y, max_y, ny)

    xx, yy = np.meshgrid(x, y)
    xy = np.concatenate([xx.reshape(-1, 1), yy.reshape(-1, 1)], axis=1)
    xy = torch.from_numpy(xy).to(algo.dtype)
    if energy_type:
        z = (
            (
                -energy_function(
                    xy[
                        :,
                        0,
                        None,
                    ],
                    xy[:, 1, None],
                )
            )
            .exp()
            .detach()
            .cpu()
            .numpy()
        )
    else:
        z = (
            energy_function(
                xy[
                    :,
                    0,
                    None,
                ],
                xy[:, 1, None],
            )
            .detach()
            .cpu()
            .numpy()
        )
    z = z.reshape(nx, ny)
    assert len(samples_title) == len(samples_x)
    assert len(samples_title) == len(samples_y)
    fig, axs = plt.subplots(1, 2 + len(samples_x), figsize=(10 + 5 * len(samples_x), 5))
    x = x.flatten()
    y = y.flatten()
    axs[0].contourf(x, y, z, 100)
    axs[0].set_title("Energy")
    for i, (s_x, s_y, s_title) in enumerate(zip(samples_x, samples_y, samples_title)):
        axs[i + 1].contourf(x, y, z, 100)
        axs[i + 1].scatter(s_x.flatten(), s_y.flatten(), c="r", alpha=0.1)
        axs[i + 1].set_title(s_title)
    fig.colorbar(axs[0].contourf(x, y, z, 100), cax=axs[-1])
    plt.savefig(os.path.join(save_dir, "{}_{}.png".format(name, step)))
    try:
        algo.logger.log_image(
            key="{}.png".format(
                name,
            ),
            images=[fig],
        )
    except AttributeError as e:
        print(
            e,
        )
    print("Saved at ", os.path.join(save_dir, "{}_{}.png".format(name, step)))
    plt.close()


def plot_energy_image_1d_regression(
    algo,
    save_dir,
    samples_x,
    energy_function=None,
    name="energy_image",
    samples_y=[],
    samples_title=[],
    step="",
    energy_type=True,
    transform_back=None,
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    batch_size = samples_x.shape[0]
    nb_sample = samples_x.shape[1]

    for s_y, s_t in zip(samples_y, samples_title):
        assert s_y.shape[0] == batch_size
        assert s_y.shape[1] == nb_sample

    assert len(samples_title) == len(samples_y)

    min_y, max_y = algo.min_y, algo.max_y
    step_size = (max_y - min_y) / 100
    range_y = torch.arange(min_y, max_y, step_size).to(
        dtype=algo.dtype, device=algo.device
    )[:100]
    range_y = range_y.reshape(100, 1)

    if energy_function is None:
        energy_function = lambda x, y: algo.ebm.calculate_energy(x, y)[0]

    fig, axs = plt.subplots(
        min(batch_size, 10),
        len(samples_y) + 2,
        figsize=(
            (len(samples_y) + 2) * 5,
            min(batch_size, 10) * 5,
        ),
    )
    for k in range(min(batch_size, 10)):
        current_image = samples_x[k]
        energy = energy_function(
            current_image.to(dtype=algo.dtype, device=algo.device), range_y
        ).reshape(nb_sample, 1)
        if energy_type:
            energy = (-energy).exp()
        energy = energy.detach().cpu().numpy()
        if transform_back is not None:
            current_image = transform_back(current_image)
        axs[k, 0].imshow(
            current_image[0].permute(1, 2, 0).detach().cpu().numpy(),
            aspect="auto",
            origin="upper",
        )
        axs[k, 0].set_title("Image")
        axs[k, 1].plot(range_y.detach().cpu().numpy(), energy)
        argmax_energy = range_y[energy.flatten().argmax()].detach().cpu().numpy()[0]
        axs[k, 1].axvline(argmax_energy, c="r", alpha=0.5)
        # Add the value next to the line
        axs[k, 1].text(
            argmax_energy - 5 * step_size,
            energy.max(),
            "{:.2f}".format(argmax_energy),
            rotation=0,
            va="bottom",
            ha="center",
            multialignment="center",
        )
        axs[k, 1].set_title("Energy")
        for l, (y_sample, title_sample) in enumerate(zip(samples_y, samples_title)):
            axs[k, l + 2].plot(range_y.detach().cpu().numpy(), energy)
            axs[k, l + 2].scatter(
                y_sample[k].detach().cpu().numpy(),
                np.ones(y_sample[k].shape) * energy.min(),
                c="r",
                alpha=0.1,
            )
            mean_sample_y = torch.mean(y_sample[k]).detach().cpu().numpy()
            axs[k, l + 2].axvline(mean_sample_y, c="r", alpha=0.5)
            # Add the value next to the line
            axs[k, l + 2].text(
                mean_sample_y - 5 * step_size.item(),
                energy.mean(),
                "{:.2f}".format(mean_sample_y),
                rotation=0,
                va="bottom",
                ha="center",
                multialignment="center",
            )
            axs[k, l + 2].set_title(title_sample)

    plt.savefig(os.path.join(save_dir, "{}_{}.png".format(name, step)))
    try:
        algo.logger.log_image(
            key="{}.png".format(
                name,
            ),
            images=[fig],
        )
    except AttributeError as e:
        print(
            e,
        )
    plt.close()


def plot_images(
    images,
    save_dir,
    transform_back=None,
    algo=None,
    name="samples",
    init_samples=None,
    step="",
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if transform_back is not None:
        images = transform_back(images)
        if len(images.shape) == 3:
            images = images.unsqueeze(1)

    if init_samples is not None:
        init_samples = transform_back(init_samples)
        if len(init_samples.shape) == 3:
            init_samples = init_samples.unsqueeze(1)
        images = torch.cat([init_samples, images], dim=0)
    grid = torchvision.utils.make_grid(
        images,
    )
    torchvision.utils.save_image(
        grid, os.path.join(save_dir, "{}_{}.png".format(name, step))
    )
    try:
        algo.logger.log_image(
            key="{}.png".format(
                name,
            ),
            images=[grid],
        )
    except AttributeError as e:
        print(
            e,
        )
