from pymatgen.core.structure import Structure
from mlipdockers.dkreq import DockerSocket, image
import json

class MlipCalc:
    """
    MLIP calculator
    """
    def __init__(self, image_name, user_settings = None):
        """
        Args:
        image_name (str): MLIP image name
        user_settings (dict): mlip version, device to use (cpu, gpu) ...
        """
        self.mlip = image_name
        self.image_name, self.dinput = image(image_name)
        self.dinput['start_port'] = 5000
        self.dinput['end_port'] = 6000
        self.dinput['init_timeout'] = 300
        if user_settings != None:
            for i in user_settings.keys():
                self.dinput[i] = user_settings[i]
        self.dkskt = DockerSocket(self.image_name, self.dinput, self.dinput['start_port'], self.dinput['end_port'], self.dinput['init_timeout'])
        
    def calculate(self, structure):
        """
        predict potential energy of a structure
        
        Args:
        structure (Structure)
        """
        self.dinput['structure'] = json.loads(structure.to_json())
        if self.mlip == 'chgnet':
            return self.dkskt.request(self.dinput)['energy'] * len(structure)
        else:
            return self.dkskt.request(self.dinput)['energy']
    
    def close(self):
        """
        shut down container
        """
        self.dkskt.close()
    
    
        
