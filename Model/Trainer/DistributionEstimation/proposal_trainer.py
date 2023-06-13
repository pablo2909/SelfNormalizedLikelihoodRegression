import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pytorch_lightning as pl
import torch
import yaml

from ...Sampler import get_sampler
from ...Utils.optimizer_getter import get_optimizer, get_scheduler
from ...Utils.plot_utils import plot_energy_2d, plot_images
from .abstract_trainer import AbstractDistributionEstimation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)
logger = logging.getLogger(__name__)


class ProposalTrainer(AbstractDistributionEstimation):
    """
    Trainer for the an importance sampling estimator of the partition function, which can be either importance sampling (with log) or self.normalized (with exp).
    Here, the proposal is trained by maximizing the likelihood of the data under the proposal.
    """

    def __init__(
        self, ebm, cfg, complete_dataset=None, nb_sample_train_estimate=1024, **kwargs
    ):
        super().__init__(
            ebm=ebm,
            cfg=cfg,
            complete_data=complete_dataset,
            nb_sample_train_estimate=nb_sample_train_estimate,
            **kwargs
        )
        assert self.ebm.proposal is not None, "The proposal should not be None"

    def training_step(self, batch, batch_idx):
        # Get parameters
        ebm_opt, proposal_opt = self.optimizers_perso()
        x = batch["data"]
        log_prob_proposal_data = self.ebm.proposal.log_prob(
            x,
        )
        self.log("train_proposal_log_likelihood", log_prob_proposal_data.mean())
        loss_proposal = -log_prob_proposal_data.mean()
        self.manual_backward(
            (loss_proposal), inputs=list(self.ebm.proposal.parameters())
        )
        self.log("train_loss", loss_proposal)
        proposal_opt.step()
        # Update the parameters of the ebm
        ebm_opt.step()

        return loss_proposal.mean()
