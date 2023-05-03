from argparse import ArgumentParser
from .EBMsAndMethod import dic_ebm
from .Energy import dic_energy
from .Trainer import dic_trainer
from .Proposals import dic_proposals


def default_args_ebm(parser = None):
    if parser is None :
        parser = ArgumentParser()

    parser.add_argument('--yamlebm', type=str, nargs='*', help='YAML File path to override the EBM parameters')

    parser.add_argument('--ebm_name', type=str, default='self_normalized', help='Name of the EBM', choices = dic_ebm.keys())
    parser.add_argument('--energy_name', type=str, default='fc', help='Name of the network', choices = dic_energy.keys())
    parser.add_argument('--trainer_name', type=str, default='self_normalized', help='Name of the trainer', choices = dic_trainer.keys())
    parser.add_argument('--proposal_name', type=str, default='standard_gaussian', help='Name of the proposal', choices = dic_proposals.keys())
    parser.add_argument('--num_sample_proposal', type=float, default=512, help='Standard deviation of the proposal')
    parser.add_argument('--num_sample_proposal_test', type=float, default=1024, help='Standard deviation of the proposal')
    parser.add_argument('--train_proposal', action='store_true', help='Train the proposal')
    parser.add_argument('--ebm_pretraining', type = str, default = None, help='Choose what type of pretraining is done on the network')
    parser.add_argument('--switch_mode', type = int, default = None, help='Number of steps before switching loss to self-normalized')

    parser.add_argument('--base_dist_name', type=str, default='none', help='Base distribution to multiply the energy with', choices = ['none', 'Normal', 'proposal'])
    

    parser.add_argument('--output_folder', type=str, default='./Results', help='Output folder')
    parser.add_argument('--load_from_checkpoint', action='store_true', help='Load from checkpoint')

    parser.add_argument('--max_steps', type=int, default=3000, help='Number of steps')
    parser.add_argument('--batch_size', type=int, default=128, help='Batch size')
    parser.add_argument('--num_workers', type=int, default=0, help='Number of workers')
    parser.add_argument('--dataloader_name', type=str, default='default', help='Name of the dataloader')
    parser.add_argument('--decay_ema', type=float, default=None, help='Decay of the EMA') # reg 0.999

    return parser