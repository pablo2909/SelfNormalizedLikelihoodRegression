from math import prod
from typing import Tuple

import torch
import torch.nn as nn
from jaxtyping import Float


class EnergyPoissonDistribution(nn.Module):
    """Implement the energy of a poisson distribution. C.f. Oops I took a gradient from Grathwohl et al.

    According to table 1 of the paper the energy is defined as:

    p(x) = exp(-E(x)) / Z

    with E(x) = log(Gamma(x+1)) - x*log(lambda)

    where Gamma is the gamma function.

    Args:
        input_size: tuple of ints, size of the input. This has to be a tuple of size 1.
        lambda_: float, the real valued parameter of the poisson distribution
        learn_lambda: bool, whether to learn lambda or not

    Attributes:
        lambda_: nn.Parameter that represents the real valued parameter of the poisson distribution.
        It is initialized with a random value sampled from N(0,1).

    Raises:
        AssertionError: if the input_size is not a tuple of size 1.

    """

    def __init__(
        self,
        input_size: Tuple[int],
        lambda_: float,
        learn_lambda: bool = False,
    ) -> None:
        super().__init__()
        assert len(input_size) == 1
        lambda_ = torch.Tensor([lambda_])
        self.lambda_ = nn.parameter.Parameter(lambda_, requires_grad=learn_lambda)

    def forward(
        self, x: Float[torch.Tensor, "batch_size"]
    ) -> Float[torch.Tensor, "batch_size"]:
        """Compute the energy of the poisson distribution

        Args:
            x: Float[torch.Tensor, "batch_size"], batch input of the energy.

        Returns:
            Float[torch.Tensor, "batch_size"], E(x), the energy of the poisson distribution
        """

        return torch.lgamma(x + 1) - x * torch.log(self.lambda_)
