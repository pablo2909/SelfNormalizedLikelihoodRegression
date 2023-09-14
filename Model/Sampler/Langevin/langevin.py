import numpy as np
import torch
import torch.distributions as dist
import tqdm
import torch.autograd as autograd

def langevin_step(x_init, energy, step_size, sigma,  clip_max_norm=None, clip_max_value=None):
    """
    Performs a single step of the Langevin algorithm.
    """

    x_init.requires_grad = True
    energy_value = energy(x_init)
    x_grad = autograd.grad(energy_value.sum(), x_init, )[0]
    if clip_max_norm is not None and clip_max_norm != np.inf:
        norm = torch.norm(x_grad.flatten(1), p=2, dim=1, keepdim=True)
        while len(norm.shape) < len(x_grad.shape):
            norm = norm.unsqueeze(-1)
        x_grad = torch.where(norm > clip_max_norm, x_grad/norm * clip_max_norm, x_grad)
    
    if clip_max_value is not None and clip_max_value != np.inf:
        x_grad.clamp_(min=-clip_max_value, max=clip_max_value)

    x_init.requires_grad = False
    noise = torch.randn_like(x_init) * sigma
    x_step = x_init - step_size * x_grad + np.sqrt(2*step_size)*noise
    return x_step


def langevin_sample(x_init, energy, step_size, sigma, num_samples, clip_max_norm = None, clip_max_value = None, burn_in=0, thinning=0):
    """
    Performs a single step of the Langevin algorithm.
    """
    print("Burn in: ", burn_in)
    for k in tqdm.tqdm(range(burn_in)):
        x_init = langevin_step(x_init, energy, step_size, sigma, clip_max_norm=clip_max_norm, clip_max_value=clip_max_value)
    x_samples = []
    for k in tqdm.tqdm(range(num_samples)):
        for t in range(thinning):
            x_init = langevin_step(x_init, energy, step_size, sigma, clip_max_norm=clip_max_norm, clip_max_value=clip_max_value)
        x_samples.append(x_init)

    x_samples = torch.cat(x_samples, dim=0)

    return x_samples






class LangevinSampler:
    def __init__(
        self,
        input_size=(1, 2),
        num_chains=10,
        num_samples=100,
        warmup_steps=100,
        thinning=10,
        step_size=1e-2,
        sigma=1e-2,
        clip_max_norm=None,
        clip_max_value=None,
        **kwargs,
    ):
        self.input_size = input_size
        self.num_samples = num_samples
        self.warmup_steps = warmup_steps
        self.step_size = step_size
        self.sigma = sigma
        self.num_chains = num_chains
        self.thinning = thinning
        self.clip_max_norm = clip_max_norm
        self.clip_max_value = clip_max_value


    def sample(self, energy_function, proposal=None, num_samples=None):
        if num_samples is None:
            num_samples = self.num_samples

        # current_energy_function = lambda x: energy_function(x[0].unsqueeze(0))
        if torch.is_tensor(proposal):
            x_init = proposal
        elif proposal is None:
            x_init = dist.Normal(
                torch.zeros(self.input_size), torch.ones(self.input_size)
            )(self.num_chains).to(torch.float32)
        else:
            x_init = proposal.sample(self.num_chains).to(torch.float32).detach()
        
        
        langevin_samples = langevin_sample(
            x_init,
            energy_function,
            step_size=self.step_size,
            sigma = self.sigma,
            num_samples=num_samples,
            burn_in=self.warmup_steps,
            thinning=self.thinning,
            clip_max_norm=self.clip_max_norm,
            clip_max_value=self.clip_max_value,
        )
     
        return langevin_samples, x_init
