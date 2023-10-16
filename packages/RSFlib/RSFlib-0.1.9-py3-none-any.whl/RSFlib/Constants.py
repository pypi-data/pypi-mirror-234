''' Physical constants '''
class PhysConst:
    def __init__(self):
        self.planck = 6.62607015e-34
        self.light_speed = 299792458
        self.elem_charge = 1.602176e-19
        self.electron_mass = 9.109382e-31
        self.proton_mass = 1.67262192e-27
        self.neutron_mass = 1.67492749804e-27
        self.vac_el_perm = 8.8541878128e-12
        self.vac_mag_perm = 1.25663706212e-6
        self.boltzman = 1.380649e-23
        self.newt_grav = 6.67430e-11

    def __str__(self):
        text = (f"\nPlanc const. = {self.planck}\n"
                f"Boltzman const. = {self.boltzman}\n"
                f"Newton gravity const. = {self.newt_grav}\n"
                f"Speed of light = {self.light_speed}\n"
                f"Elem. charge = {self.elem_charge}\n"
                f"Mass of electron = {self.electron_mass}\n"
                f"Mass of proton = {self.proton_mass}\n"
                f"Mass of neutron = {self.neutron_mass}\n"
                f"Electric permitivity in vac. = {self.vac_el_perm}\n"
                f"Magnetick permitivity in vac. = {self.vac_mag_perm}")
        return text
