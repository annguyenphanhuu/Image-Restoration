from guided_diffusion.models import Model
import torch
import yaml
from utils import dict2namespace


def load_pretrained_diffusion_model(config):
    model = Model(config)
    ckpt = "checkpoints/celeba_hq.ckpt"
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    config.device = device
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.to(device)
    model.eval()
    for param in model.parameters():
        param.requires_grad = False
    model = torch.nn.DataParallel(model)    
    return model, device


with open( "data/celeba_hq.yml", "r") as f:
    config1 = yaml.safe_load(f)

config = dict2namespace(config1)

model, device = load_pretrained_diffusion_model(config)

# push to hub
model.push_to_hub("nielsr/bird-demo")

# reload
model = Model.from_pretrained("nielsr/bird-demo")