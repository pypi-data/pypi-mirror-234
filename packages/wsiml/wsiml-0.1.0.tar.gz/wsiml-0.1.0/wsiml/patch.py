from typing import NamedTuple

class ModelShape(NamedTuple):
  pad : int
  stride : int

def _keras_config_change_padding(config, padding="valid"):
  """
  Convert Keras model config into an equivalent config that uses "valid."
  """
  
  if isinstance(config, list):
    return [_keras_config_change_padding(x) for x in config]

  if isinstance(config, tuple):
    return tuple([_keras_config_change_padding(x) for x in config])

  if isinstance(config, dict):
    if "padding" in config:
      config["padding"] = padding
  
    for k in list(config):
      config[k] = _keras_config_change_padding(config[k])
    
    return config
  
  return config
      
