VERSION = "2.0.0"

from pyroll.core import RollPass, Transport, Profile, Hook
from shapely.affinity import scale

Profile.thermal_expansion_coefficient = Hook[float]()
"""Linear thermal expansion factor of the profile material."""


@Profile.thermal_expansion_coefficient
def steel_default(self: Profile):
    """Default approximate value for general steel materials."""
    if "steel" in self.material:
        return 15.0e-6


@Transport.OutProfile.cross_section
def transport_thermal_expansion_cross_section(self: Transport.OutProfile, cycle):
    """Scaling the cross-section in dependence on temperature change."""

    if cycle:
        return None

    orig_cross_section = Transport.OutProfile.cross_section.get_result(self) or self.transport.in_profile.cross_section
    scale_factor = (1 + (self.temperature - self.transport.in_profile.temperature)
                    * self.thermal_expansion_coefficient)

    return scale(orig_cross_section, scale_factor, scale_factor)


@Transport.OutProfile.length
def transport_thermal_expansion_length(self: Transport.OutProfile, cycle):
    """Scaling the length in dependence on temperature change."""

    if cycle:
        return None

    orig_length = Transport.OutProfile.length.get_result(self) or self.transport.in_profile.length
    scale_factor = (1 + (self.temperature - self.transport.in_profile.temperature)
                    * self.thermal_expansion_coefficient)

    return orig_length * scale_factor


@RollPass.OutProfile.length
def roll_pass_thermal_expansion_length(self: RollPass.OutProfile, cycle):
    """Scaling the length in dependence on temperature change.
     Since cross-section is constrained by contour and spread, full expansion goes to length."""

    if cycle:
        return None

    orig_length = RollPass.OutProfile.length.get_result(self) or self.roll_pass.in_profile.length
    scale_factor = (1 + (self.temperature - self.roll_pass.in_profile.temperature)
                    * 3 * self.thermal_expansion_coefficient)

    return orig_length * scale_factor
