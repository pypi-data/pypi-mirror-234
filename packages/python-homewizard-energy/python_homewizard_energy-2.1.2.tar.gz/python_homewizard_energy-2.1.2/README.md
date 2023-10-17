# python-homewizard-energy

Asyncio package to communicate with HomeWizard Energy devices
This package is aimed at basic control of the device. Initial setup and configuration is assumed to done with the official HomeWizard Energy app.

## Disclaimer

This package is not developed, nor supported by HomeWizard.

## Installation
```bash
python3 -m pip install python-homewizard-energy
```

# Usage
Instantiate the HWEnergy class and access the API.

For more details on the API see the official API documentation on
https://homewizard-energy-api.readthedocs.io

# Example
The example below is available as a runnable script in the repository.

```python
from homewizard_energy import HomeWizardEnergy

# Make contact with a energy device
async with HomeWizardEnergy(args.host) as api:

    # Use the data
    print(await api.device())
    print(await api.data())
    print(await api.state())

    await api.state_set(power_on=True)
```
