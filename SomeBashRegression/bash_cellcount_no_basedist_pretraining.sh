# Self normalized test
CUDA_VISIBLE_DEVICES=4 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/self_normalized_train_proposal_both.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml


CUDA_VISIBLE_DEVICES=4 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/self_normalized_train_proposal_logprob.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml

# Log prob test
CUDA_VISIBLE_DEVICES=5 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/importance_sampling_train_proposal_both.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml

CUDA_VISIBLE_DEVICES=5 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/importance_sampling_train_proposal_kl.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml 

CUDA_VISIBLE_DEVICES=5 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/importance_sampling_train_proposal_logprob.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml


# NCE Test
CUDA_VISIBLE_DEVICES=6 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/nce_train_proposal_both.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml

CUDA_VISIBLE_DEVICES=6 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/nce_train_proposal_kl.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml 

CUDA_VISIBLE_DEVICES=6 python main_trainer_regression.py --output_folder '/scratch/hhjs/selfnormalized/Results_pretraining' --ebm_pretraining gaussian --proposal_pretraining data \
--yamldataset 'Dataset/MissingDataDataset/YAMLExamples/cell_count.yaml' \
--yamlebm Model/YAMLREGRESSION/YAMLEBM_Image/nce_train_proposal_logprob.yaml Model/YAMLREGRESSION/YAMLPROPOSAL/mdn_k4.yaml \
Model/YAMLREGRESSION/YAMLBASEDIST/none.yaml \
Model/YAMLREGRESSION/YAMLENERGY/energy_fc_large_bias.yaml Model/YAMLREGRESSION/YAMLOPTIMIZATION/adam1e-3.yaml

# AUX
