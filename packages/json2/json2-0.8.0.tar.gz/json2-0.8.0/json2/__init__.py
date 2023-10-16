from json import *

def load_file(filename):
    with open(filename, "r") as f:
        return loads(f.read())


def dump_file(filename, content):
    with open(filename, "w") as f:
        f.write(json.dumps(content))


class MLFrienldyEncoder(JSONEncoder):
    """
        A custom JSON encoder that can handle NumPy arrays and PyTorch tensors.
    """
    def default(self, obj):
        import torch
        import numpy as np
        if isinstance(obj, (np.ndarray, torch.Tensor)):
            if isinstance(obj, torch.Tensor):
                obj = obj.detach().cpu().numpy()  # Convert PyTorch tensor to NumPy array
            return obj.tolist()  # Convert NumPy array to Python list
        return super(MLFrienldyEncoder, self).default(obj)

