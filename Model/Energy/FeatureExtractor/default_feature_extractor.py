import torch.nn as nn

class MockFeatureExtractor(nn.Module):
    '''
    Mock feature extractor returning the input.
    '''
    def __init__(self, input_size_x=1, ):
        super().__init__()
        self.input_size_x = input_size_x
        self.output_size = input_size_x
    
    def forward(self, x):
        return x.reshape(-1, *self.input_size_x)