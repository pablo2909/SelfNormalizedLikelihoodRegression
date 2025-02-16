import torch

from ...Utils.noise_annealing import calculate_current_noise_annealing
from .abstract_trainer import AbstractDistributionEstimation


def set_bn_to_eval(m):
    classname = m.__class__.__name__
    if classname.find("BatchNorm") != -1:
        m.eval()


def set_bn_to_train(m):
    classname = m.__class__.__name__
    if classname.find("BatchNorm") != -1:
        m.train()


class SelfNormalizedTrainer(AbstractDistributionEstimation):
    """
    Trainer for the an importance sampling estimator of the partition function, which can be either importance sampling (with log) or self.normalized (with exp).
    Here, the proposal is trained by maximizing the likelihood of the data under the proposal.
    """

    def __init__(
        self,
        ebm,
        cfg,
        device,
        logger,
        complete_dataset=None,
    ):
        super().__init__(
            ebm=ebm,
            cfg=cfg,
            device=device,
            logger=logger,
            complete_dataset=complete_dataset,
        )

    def training_energy(self, x):
         # Get parameters
        f_theta_opt, explicit_bias_opt, base_dist_opt, proposal_opt = self.optimizers
        f_theta_opt.zero_grad()
        explicit_bias_opt.zero_grad()

    
        current_noise_annealing = calculate_current_noise_annealing(
            self.current_step,
            self.cfg.train.noise_annealing_init,
            self.cfg.train.noise_annealing_gamma,
        )

        if hasattr(self.ebm.proposal, "set_x"):
            self.ebm.proposal.set_x(x)

        estimate_log_z, dic, energy_samples, x_gen, x_gen_noisy = self.ebm.estimate_log_z(
            x,
            self.num_samples_train,
            detach_sample=True,
            requires_grad=False,
            return_samples=True,
            noise_annealing=current_noise_annealing,
        )


        energy_data, dic_output = self.ebm.calculate_energy(x)
        dic_output.update(dic)
        # estimate_log_z = estimate_log_z.mean()
        if (
            self.cfg.train.start_with_IS_until is not None
            and self.current_step < self.cfg.train.start_with_IS_until
        ):
            loss_estimate_z = estimate_log_z
        else:
            loss_estimate_z = estimate_log_z.exp() - 1


        loss_energy = energy_data.mean()
        loss_total = self.backward_and_reg(loss_energy=loss_energy,
                        loss_samples=loss_estimate_z,
                        x=x,
                        x_gen=x_gen,
                        energy_data=energy_data,
                        energy_samples=energy_samples,)
        self.grad_clipping()




        self.log("train/loss_total", loss_total)
        self.log("train/loss_energy", loss_energy)
        self.log("train/loss_sample", loss_estimate_z)
        self.log(
            "train/noise_annealing",
            current_noise_annealing,
        )



        f_theta_opt.step()
        explicit_bias_opt.step()
        if self.train_base_dist:
            base_dist_opt.step()
        f_theta_opt.zero_grad()
        base_dist_opt.zero_grad()
        explicit_bias_opt.zero_grad()


        return loss_total, dic_output
