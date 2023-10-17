from pyroll.core import RollPass, Hook
from pyroll.integral_thermal.helper import mean_temperature, mean_density, mean_specific_heat_capacity

RollPass.deformation_heat_efficiency = Hook[float]()
"""Efficiency of heat generation through deformation. 1 means that all forming energy is dissipated as heat, 0 that all energy is saved in microstructure."""

RollPass.temperature_change_by_contact = Hook[float]()
"""Get the change in temperature by contact transfer within the roll pass."""

RollPass.temperature_change_by_deformation = Hook[float]()
"""Get the change in temperature by deformation heat within the roll pass."""

RollPass.temperature_change = Hook[float]()
"""Get the change in temperature within the roll pass."""

RollPass.Roll.contact_heat_transfer_coefficient = Hook[float]()
"""Get the heat transfer coefficient for contact of rolls and workpiece."""


@RollPass.Roll.contact_heat_transfer_coefficient
def default_contact_heat_transfer_coefficient(self: RollPass.Roll):
    return 6e3


@RollPass.Roll.temperature
def default_roll_temperature(self: RollPass.Roll):
    return 293.15


@RollPass.OutProfile.temperature
def out_temperature(self: RollPass.OutProfile):
    return self.roll_pass.in_profile.temperature + self.roll_pass.temperature_change


@RollPass.deformation_heat_efficiency
def default_deformation_heat_efficiency(self: RollPass):
    return 0.95


@RollPass.temperature_change_by_contact
def temperature_change_by_contact(self: RollPass):
    return -(
            (
                    self.roll.contact_heat_transfer_coefficient
                    * (mean_temperature(self) - self.roll.temperature)
                    * self.duration
                    * self.contact_area
            ) / (
                    mean_density(self)
                    * mean_specific_heat_capacity(self)
                    * self.volume
            )
    )


@RollPass.temperature_change_by_deformation
def temperature_change_by_deformation(self: RollPass):
    deformation_resistance = (
        self.deformation_resistance
        if self.has_value("deformation_resistance")
        else (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3
    )
    return (
            (
                    self.deformation_heat_efficiency
                    * deformation_resistance
                    * self.strain
            ) / (
                    mean_density(self)
                    * mean_specific_heat_capacity(self)
            )
    )


@RollPass.temperature_change
def temperature_change(self: RollPass):
    return self.temperature_change_by_contact + self.temperature_change_by_deformation
