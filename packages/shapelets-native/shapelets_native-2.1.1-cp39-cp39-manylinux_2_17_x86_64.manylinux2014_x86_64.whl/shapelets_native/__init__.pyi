# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

import typing

import numpy
import pandas
import pyarrow
import pyarrow.dataset

ArrowObject = typing.Union[pyarrow.Table, pyarrow.RecordBatchReader,
                           pyarrow.dataset.FileSystemDataset, pyarrow.dataset.InMemoryDataset, pyarrow.dataset.Scanner]


########################
# Units of Measure
########################


class Unit:
    r"""
    Represents a unit of measure.

    Units of measure implementation is a Python port of the excellent C++ library
    `units <https://github.com/LLNL/units>`_ `(BSD 3-Clause) <https://github.com/LLNL/units/blob/main/LICENSE>`_,
    created at `Lawrence Livermore National Laboratory (LLNV) <https://software.llnl.gov>`_.

    Attributes
    ----------
    base_units
    inv
    multiplier

    """

    def __eq__(self, other: Unit) -> bool: ...
    def __mul__(self, other: typing.Union[float, Unit]) -> Unit: ...
    def __pow__(self, power: int) -> Unit: ...
    def __rmul__(self, other: typing.Union[float, Unit]) -> Unit: ...
    def __rtruediv__(self, other: float) -> Unit: ...
    def __truediv__(self, other: typing.Union[float, Unit]) -> Unit: ...

    def __repr__(self) -> str: ...

    def __getstate__(self) -> tuple: ...
    def __setstate__(self, arg0: tuple) -> None: ...

    def is_convertible(self, other: Unit) -> bool:
        r"""
        Checks if this unit may be converted to another unit

        Parameters
        ----------
        other: Unit
            The desired unit.

        Returns
        -------
        bool: True if there is a conversion algorithm between this unit and 
        the other unit; False otherwise.
        """
        ...

    def root(self, power: int) -> Unit:
        r"""
        Returns a new unit as the root, of some power, of this unit

        Examples
        --------
        >>> import shapelets as sh
        >>> sh.parse_unit("1/s^2").root(2)
        Hz
        """
        ...

    @property
    def base_units(self) -> Unit:
        r"""
        Returns the base units 

        Examples
        --------
        >>> import shapelets as sh
        >>> kmh = sh.parse_unit("km/h")
        >>> kmh.base_units
        m/s
        >>> kmh.multiplier
        0.2777777777777778
        >>> fts2 = sh.parse_unit("ft/s^2")
        >>> fts2.base_units 
        m/s^2
        >>> fts2.multiplier
        0.3048
        """

    @property
    def inv(self) -> Unit:
        r"""
        Returns a new unit, which is the reciprocal of this unit.

        Examples
        --------
        >>> import shapelets as sh
        >>> kmh = sh.parse_unit("km/h")
        >>> kmh.inv
        hr/km
        """

    @property
    def multiplier(self) -> float:
        r"""
        Returns the scaling factor associated with this unit

        Examples
        --------
        >>> import shapelets as sh
        >>> kmh = sh.parse_unit("km/h")
        >>> kmh.multiplier
        0.2777777777777778
        """

    __hash__ = None
    pass


def convert_unit(fromUnits: Unit, toUnits: Unit, value: numpy.ndarray[numpy.float64]) -> typing.Union[numpy.float64, numpy.ndarray[numpy.float64]]:
    pass


class UnitPriority:
    """
    Members:

      Astronomy

      Climate

      Cooking

      NoPriority

      Nuclear

      Surveying

      US
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Astronomy: UnitPriority  # value = <UnitPriority.Astronomy: 2>
    Climate: UnitPriority  # value = <UnitPriority.Climate: 5>
    Cooking: UnitPriority  # value = <UnitPriority.Cooking: 1>
    NoPriority: UnitPriority  # value = <UnitPriority.NoPriority: 0>
    Nuclear: UnitPriority  # value = <UnitPriority.Nuclear: 4>
    Surveying: UnitPriority  # value = <UnitPriority.Surveying: 3>
    US: UnitPriority  # value = <UnitPriority.US: 6>
    __members__: dict  # value = {'Astronomy': <UnitPriority.Astronomy: 2>, 'Climate': <UnitPriority.Climate: 5>, 'Cooking': <UnitPriority.Cooking: 1>, 'NoPriority': <UnitPriority.NoPriority: 0>, 'Nuclear': <UnitPriority.Nuclear: 4>, 'Surveying': <UnitPriority.Surveying: 3>, 'US': <UnitPriority.US: 6>}
    pass


class UnitStandard:
    """
    Members:

      DoD

      IS

      R20

      UCUM

      NoStandard

      X12
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    DoD: UnitStandard  # value = <UnitStandard.DoD: 4>
    IS: UnitStandard  # value = <UnitStandard.IS: 2>
    NoStandard: UnitStandard  # value = <UnitStandard.NoStandard: 0>
    R20: UnitStandard  # value = <UnitStandard.R20: 5>
    UCUM: UnitStandard  # value = <UnitStandard.UCUM: 1>
    X12: UnitStandard  # value = <UnitStandard.X12: 3>
    # value = {'DoD': <UnitStandard.DoD: 4>, 'IS': <UnitStandard.IS: 2>, 'R20': <UnitStandard.R20: 5>, 'UCUM': <UnitStandard.UCUM: 1>, 'NoStandard': <UnitStandard.NoStandard: 0>, 'X12': <UnitStandard.X12: 3>}
    __members__: dict
    pass


def parse_unit(str: str, caseInsensitive: bool = False, priority: UnitPriority = UnitPriority.NoPriority,
               standard: UnitStandard = UnitStandard.NoStandard) -> typing.Optional[Unit]:
    pass


class AngleUnits:
    r"""
    Angle units
    """

    @property
    def arcmin(self) -> Unit:
        r"""
        A minute of arc, arcminute (arcmin), arc minute, or minute arc, denoted by the symbol ′,
        is a unit of angular measurement equal to 1/60 of one degree.
        """
        ...

    @property
    def arcsec(self) -> Unit:
        r"""
        A second of arc, arcsecond (arcsec), or arc second, denoted by the symbol ″, is
        1/60 of an arcminute.
        """
        ...

    @property
    def brad(self) -> Unit:
        r"""
        Binary radian (1/256 of a circle)
        """
        ...

    @property
    def deg(self) -> Unit:
        r"""
        A degree (in full, a degree of arc, arc degree, or arcdegree), usually
        denoted by ° (the degree symbol), is a measurement of a plane angle in
        which one full rotation is 360 degrees.
        """
        ...

    @property
    def gon(self) -> Unit:
        r"""
        Same as :obj:`~AngleUnits.grad`.

        See also
        --------
        grad

        """
        ...

    @property
    def grad(self) -> Unit:
        r"""
        The gradian, also known as the gon, grad, or grade, is a unit of measurement of an angle,
        defined as one hundredth of the right angle; in other words, there are 100 gradians in 90 degrees.
        """
        ...


class AreaUnits:
    @property
    def are(self) -> Unit:
        """
        An are is defined as 100 squared meters.
        """
        ...

    @property
    def arpent(self) -> Unit:
        """
        A square arpent.  An arpent is a pre-metric French measurement of approximately 192 feet (59 m).

        Examples
        --------
        >>> import shapelets as sh
        >>> sh.convert_unit(sh.units.Areas.arpent, sh.units.British.acre, 1.0)
        0.8462847178614697
        >>> sh.convert_unit(sh.units.Areas.arpent, sh.units.USA.acre, 1.0)
        0.84628
        """
        ...

    @property
    def barn(self) -> Unit:
        """
        A barn (symbol: b) is a metric unit of area equal to 10^-28 m^2 

        Examples
        --------
        >>> import shapelets as sh
        >>> sqm = sh.parse_unit("m^2")
        >>> sh.convert_unit(sh.units.Areas.barn, sqm, 1.0)
        1e-28
        """
        ...

    @property
    def hectare(self) -> Unit:
        """
        An hectare is defined as 10000 squared meters.
        """
        ...


class AustraliaUnits:
    @property
    def cup(self) -> Unit: ...
    @property
    def tbsp(self) -> Unit: ...
    @property
    def tsp(self) -> Unit: ...


class AvoirdupoisUnits:
    @property
    def dram(self) -> Unit: ...
    @property
    def hundredweight(self) -> Unit: ...
    @property
    def lbf(self) -> Unit: ...
    @property
    def longhundredweight(self) -> Unit: ...
    @property
    def longton(self) -> Unit: ...
    @property
    def ounce(self) -> Unit: ...
    @property
    def ozf(self) -> Unit: ...
    @property
    def pound(self) -> Unit: ...
    @property
    def poundal(self) -> Unit: ...
    @property
    def slug(self) -> Unit: ...
    @property
    def stone(self) -> Unit: ...
    @property
    def ton(self) -> Unit: ...


class BritishUnits:
    @property
    def acre(self) -> Unit: ...
    @property
    def barleycorn(self) -> Unit: ...
    @property
    def barrel(self) -> Unit: ...
    @property
    def bushel(self) -> Unit: ...
    @property
    def chain(self) -> Unit: ...
    @property
    def cup(self) -> Unit: ...
    @property
    def drachm(self) -> Unit: ...
    @property
    def dram(self) -> Unit: ...
    @property
    def floz(self) -> Unit: ...
    @property
    def foot(self) -> Unit: ...
    @property
    def furlong(self) -> Unit: ...
    @property
    def gallon(self) -> Unit: ...
    @property
    def gill(self) -> Unit: ...
    @property
    def hundredweight(self) -> Unit: ...
    @property
    def inch(self) -> Unit: ...
    @property
    def knot(self) -> Unit: ...
    @property
    def league(self) -> Unit: ...
    @property
    def link(self) -> Unit: ...
    @property
    def mile(self) -> Unit: ...
    @property
    def minim(self) -> Unit: ...
    @property
    def nautical_mile(self) -> Unit: ...
    @property
    def pace(self) -> Unit: ...
    @property
    def peck(self) -> Unit: ...
    @property
    def perch(self) -> Unit: ...
    @property
    def pint(self) -> Unit: ...
    @property
    def quart(self) -> Unit: ...
    @property
    def rod(self) -> Unit: ...
    @property
    def rood(self) -> Unit: ...
    @property
    def slug(self) -> Unit: ...
    @property
    def stone(self) -> Unit: ...
    @property
    def tbsp(self) -> Unit: ...
    @property
    def thou(self) -> Unit: ...
    @property
    def ton(self) -> Unit: ...
    @property
    def tsp(self) -> Unit: ...
    @property
    def yard(self) -> Unit: ...


class CGSUnits:
    @property
    def RAD(self) -> Unit:
        r"""
        A unit of absorbed dose of ionizing radiation equal to an energy of
        100 ergs per gram of irradiated material
        """
        ...

    @property
    def REM(self) -> Unit:
        r"""
        The dosage of an ionizing radiation that will cause the same biological
        effect as one roentgen of X-ray or gamma-ray exposure
        """
        ...

    @property
    def abFarad(self) -> Unit:
        r"""
        A cgs electromagnetic unit of capacitance equal to one billion farads that measures the
        capacitance of a condenser that when charged to a potential difference of one abvolt has
        a charge of one abcoulomb
        """
        ...

    @property
    def abHenry(self) -> Unit:
        r"""
        A cgs electromagnetic unit of inductance equal to one billionth of a henry that measures
        the self-inductance of a circuit or the mutual inductance of two circuits in which the
        variation of current at the rate of one abampere per second results in an induced
        electromotive force of one abvolt
        """
        ...

    @property
    def abOhm(self) -> Unit:
        r"""
        The cgs electromagnetic unit of resistance equal to one billionth of an ohm that measures
        the resistance of a conductor that with a constant current of one abampere flowing through
        it maintains between its terminals a potential difference of one abvolt
        """
        ...

    @property
    def abVolt(self) -> Unit:
        r"""
        The cgs electromagnetic unit of electrical potential and electromotive force equal to one
        one-hundred-millionth of a volt and being the potential difference through which transference
        of one abcoulomb of electricity involves a change of one erg in energy
        """
        ...

    @property
    def barye(self) -> Unit:
        r"""
        The cgs unit of pressure equal to 0.1 pascal or to one dyne per square centimeter
        """
        ...

    @property
    def biot(self) -> Unit:
        r"""
        The magnetic intensity at any point due to a steady current in an infinitely long
        straight wire is directly proportional to the current and inversely proportional
        to the distance from point to wire
        """
        ...

    @property
    def curie(self) -> Unit:
        r"""
        A unit quantity of any radioactive nuclide in which 3.7 x 10^10 disintegrations occur per second
        """
        ...

    @property
    def debye(self) -> Unit:
        r"""
        The debye is a CGS unit of electric dipole moment. It is defined as 1x10^-18 statcoulomb-centimeters.
        """
        ...

    @property
    def dyn(self) -> Unit:
        r"""
        The dyne is defined as "the force required to accelerate a mass of one gram at a rate
        of one centimetre per second squared".

        1 N = 10^5 dyn
        """
        ...

    @property
    def emu(self) -> Unit: ...

    @property
    def erg(self) -> Unit:
        r"""
        A centimeter-gram-second unit of work equal to the work done by a force of
        one dyne acting through a distance of one centimeter and equivalent to
        10^-7 joule
        """
        ...

    @property
    def gal(self) -> Unit: ...

    @property
    def gauss(self) -> Unit:
        r"""
        The centimeter-gram-second unit of magnetic flux density that is equal to 1 x 10^-4 tesla
        """
        ...

    @property
    def gilbert(self) -> Unit:
        r"""
        The centimeter-gram-second unit of magnetomotive force equivalent to 10/4π ampere-turn
        """
        ...

    @property
    def kayser(self) -> Unit: ...

    @property
    def lambert(self) -> Unit: ...

    @property
    def langley(self) -> Unit:
        r"""
        A unit of solar radiation equivalent to one gram calorie per square
        centimeter of irradiated surface
        """
        ...

    @property
    def maxwell(self) -> Unit:
        r"""
        The centimeter-gram-second electromagnetic unit of magnetic flux equal
        to the flux per square centimeter of normal cross section in a region
        where the magnetic induction is one gauss : 10^-8 weber
        """
        ...

    @property
    def oersted(self) -> Unit:
        r"""
        The unit of magnetic field strength in the centimeter-gram-second system
        """
        ...

    @property
    def phot(self) -> Unit: ...

    @property
    def poise(self) -> Unit:
        r"""
        A centimeter-gram-second unit of viscosity equal to the viscosity of a fluid
        that would require a shearing force of one dyne to impart to a one-square-centimeter
        area of an arbitrary layer of the fluid a velocity of one centimeter per second
        relative to another layer separated from the first by a distance of one centimeter
        """
        ...

    @property
    def roentgen(self) -> Unit:
        r"""
        Unit of x-radiation or gamma radiation equal to the amount of radiation that
        produces in one cubic centimeter of dry air at 0°C and standard atmospheric
        pressure ionization of either sign equal to one electrostatic unit of charge
        """
        ...

    @property
    def statC_charge(self) -> Unit: ...

    @property
    def statC_flux(self) -> Unit: ...

    @property
    def statFarad(self) -> Unit:
        r"""
        The cgs electrostatic unit of capacitance equal to about 1.113x10^-12 farads
        """
        ...

    @property
    def statHenry(self) -> Unit:
        r"""
        The cgs electrostatic unit of inductance equal to about 8.9x10^11 henries
        """
        ...

    @property
    def statOhm(self) -> Unit:
        r"""
        The cgs electrostatic unit of resistance equal to about 8.9x10^11 ohms
        """
        ...

    @property
    def statT(self) -> Unit: ...

    @property
    def statV(self) -> Unit: ...

    @property
    def stilb(self) -> Unit:
        r"""
        A cgs unit of brightness equal to one candle per square centimeter
        of cross section perpendicular to the rays
        """
        ...

    @property
    def stokes(self) -> Unit: ...

    @property
    def unitpole(self) -> Unit: ...


class CanadaUnits:
    @property
    def bushel_oats(self) -> Unit:
        r"""
        34 lb (15.4221 kg)
        """
        ...

    @property
    def cup(self) -> Unit: ...
    @property
    def cup_trad(self) -> Unit: ...
    @property
    def gallon(self) -> Unit: ...
    @property
    def tbsp(self) -> Unit: ...
    @property
    def tsp(self) -> Unit: ...


class ChinaUnits:
    @property
    def chi(self) -> Unit: ...
    @property
    def cun(self) -> Unit: ...
    @property
    def jin(self) -> Unit: ...
    @property
    def li(self) -> Unit: ...
    @property
    def liang(self) -> Unit: ...
    @property
    def qian(self) -> Unit: ...
    @property
    def zhang(self) -> Unit: ...


class ClimateUnits:
    @property
    def gtp(self) -> Unit:
        r"""
        Global temperature potential
        """
        ...

    @property
    def gwp(self) -> Unit:
        r"""
        Global warming potential
        """
        ...


class ClinicalUnits:
    @property
    def charriere(self) -> Unit: ...
    @property
    def diopter(self) -> Unit: ...
    @property
    def drop(self) -> Unit: ...
    @property
    def hounsfield(self) -> Unit: ...
    @property
    def mesh(self) -> Unit: ...
    @property
    def met(self) -> Unit: ...
    @property
    def prism_diopter(self) -> Unit: ...
    @property
    def pru(self) -> Unit: ...
    @property
    def woodu(self) -> Unit: ...


class ComputationUnits:
    @property
    def flop(self) -> Unit: ...
    @property
    def flops(self) -> Unit: ...
    @property
    def mips(self) -> Unit: ...


class DataUnits:
    @property
    def GB(self) -> Unit: ...
    @property
    def GiB(self) -> Unit: ...
    @property
    def MB(self) -> Unit: ...
    @property
    def MiB(self) -> Unit: ...
    @property
    def ban(self) -> Unit: ...
    @property
    def bit(self) -> Unit: ...

    @property
    def bit_s(self) -> Unit:
        r"""
        Shannon bit for information theory
        """
        ...

    @property
    def byte(self) -> Unit:
        """
        Defined as 8 bits
        """
        ...

    @property
    def deciban(self) -> Unit: ...
    @property
    def digits(self) -> Unit: ...
    @property
    def dit(self) -> Unit: ...
    @property
    def hartley(self) -> Unit: ...
    @property
    def kB(self) -> Unit: ...
    @property
    def kiB(self) -> Unit: ...
    @property
    def nat(self) -> Unit: ...

    @property
    def nibble(self) -> Unit:
        """
        A group of four bits, or half a byte, is sometimes called a nibble, nybble or nyble.
        """
        ...

    @property
    def shannon(self) -> Unit: ...

    @property
    def trit(self) -> Unit:
        ...


class DistanceUnits:
    @property
    def angstrom(self) -> Unit:
        """
        The angstrom or ångström is a metric unit of length equal to 10e-10 m (100 picometres). 
        """
        ...

    @property
    def arpent_fr(self) -> Unit:
        """
        An arpent is a unit of length and a unit of area. It is used in Quebec, some areas of the 
        United States that were part of French Louisiana, and in Mauritius and the Seychelles.

        The French interpretation sets its value to 71.46466 meters

        See Also
        --------
        arpent_us

        """
        ...

    @property
    def arpent_us(self) -> Unit:
        """
        An arpent is a unit of length and a unit of area. It is used in Quebec, some areas of the 
        United States that were part of French Louisiana, and in Mauritius and the Seychelles.

        The US interpretation sets its value to 58.47131 meters

        See Also
        --------
        arpent_fr

        """
        ...

    @property
    def au(self) -> Unit:
        """
        The astronomical unit is a unit of length, roughly the distance from Earth to the Sun.

        Defined as 149597870700.0 meters.
        """
        ...

    @property
    def au_old(self) -> Unit:
        """
        The astronomical unit is a unit of length, roughly the distance from Earth to the Sun.

        Defined as 149597900000.0 meters.
        """
        ...

    @property
    def cubit(self) -> Unit:
        """
        The cubit is an ancient unit of length based on the distance from the elbow to the tip of the middle finger.

        It is defined as 1.5 ft 
        """
        ...

    @property
    def longcubit(self) -> Unit:
        """
        It is defined as 21 inches
        """
        ...

    @property
    def ly(self) -> Unit:
        """
        A light-year, alternatively spelled lightyear, is a large unit of length used to express astronomical
        distances and is equivalent to about 9.46 trillion kilometers (9.46x1012 km), or 5.88 trillion miles 
        (5.88x1012 mi).

        As defined by the International Astronomical Union (IAU), a light-year is the distance that light travels 
        in a vacuum in one Julian year (365.25 days).
        """
        ...

    @property
    def parsec(self) -> Unit:
        """
        The parsec is a unit of length used to measure the large distances to astronomical objects 
        outside the Solar System, approximately equal to 3.26 light-years or 206,000 astronomical 
        units (au), i.e. 30.9 trillion kilometres (19.2 trillion miles)
        """
        ...

    @property
    def smoot(self) -> Unit:
        """
        The smoot is a nonstandard, humorous unit of length created as part of an MIT fraternity prank. 

        It is named after Oliver R. Smoot, who in October 1958 lay down repeatedly on the Harvard Bridge 
        (between Boston and Cambridge, Massachusetts) so that his fraternity brothers could use his 
        height to measure the length of the bridge.        

        One smoot is equal to Oliver Smoot's height at the time of the prank, 5 feet 7 inches (1.70 m). 
        """
        ...

    @property
    def xu(self) -> Unit:
        """
        The x unit (symbol xu) is a unit of length approximately equal to 0.1 pm (10e-13 m). 

        It is used to quote the wavelength of X-rays and gamma rays.
        """
        ...


class ElectricalUnits:
    @property
    def MJ(self) -> Unit:
        """
        The megajoule (MJ) is equal to one million joules
        """
        ...

    @property
    def MVAR(self) -> Unit:
        """
        The mega volt-ampere reactive is equal to one million VAR
        """
        ...

    @property
    def MW(self) -> Unit:
        """
        The mega watt is defined as one million watts.
        """
        ...

    @property
    def VAR(self) -> Unit:
        """
        In electric power transmission and distribution, volt-ampere reactive is a unit of measurement of reactive power. 
        """
        ...

    @property
    def kV(self) -> Unit:
        """
        Equates to 1000 Volts
        """
        ...

    @property
    def kVAR(self) -> Unit:
        """
        Equates to 1000 VAR
        """
        ...

    @property
    def kW(self) -> Unit:
        """
        Equates to 1000 Watts
        """
        ...

    @property
    def mA(self) -> Unit:
        """
        Equates to one thousand of an Ampere
        """
        ...

    @property
    def mV(self) -> Unit:
        """
        Equates to one thousand of a Volt
        """
        ...

    @property
    def mW(self) -> Unit:
        """
        Equates to one thousand of a Watt
        """
        ...

    @property
    def puA(self) -> Unit:
        """
        Represents a percentage over a current reference value.
        """
        ...

    @property
    def puHz(self) -> Unit:
        """
        Represents a percentage over a frequency reference value.
        """
        ...

    @property
    def puMW(self) -> Unit:
        """
        Represents a percentage over a power reference value.
        """
        ...

    @property
    def puOhm(self) -> Unit:
        """
        Represents a percentage over a resistance reference value.
        """
        ...

    @property
    def puV(self) -> Unit:
        """
        Represents a percentage over a voltage reference value.
        """
        ...


class EnergyUnits:
    @property
    def EER(self) -> Unit:
        r"""
        Energy efficiency ratio
        """
        ...

    @property
    def MWh(self) -> Unit:
        """
        Defined as 1000 kWh
        """
        ...

    @property
    def SG(self) -> Unit:
        r"""
        Specific gravity
        """
        ...

    @property
    def boe(self) -> Unit:
        r"""
        Barrel of oil equivalent
        """
        ...

    @property
    def btu_39(self) -> Unit:
        r"""
        BTU at 39 deg C
        """
        ...

    @property
    def btu_59(self) -> Unit:
        r"""
        BTU at 59 deg C
        """
        ...

    @property
    def btu_60(self) -> Unit:
        r"""
        BTU at 60 deg C
        """
        ...

    @property
    def btu_iso(self) -> Unit:
        r"""
        Rounded btu_it
        """
        ...

    @property
    def btu_it(self) -> Unit:
        r"""
        International table BTU
        """
        ...

    @property
    def btu_mean(self) -> Unit:
        r"""
        Mean BTU
        """
        ...

    @property
    def btu_th(self) -> Unit:
        r"""
        Thermochemical BTU
        """
        ...

    @property
    def cal_15(self) -> Unit:
        r"""
        calorie at 15 deg C
        """
        ...

    @property
    def cal_20(self) -> Unit:
        r"""
        calorie at 20 deg C
        """
        ...

    @property
    def cal_4(self) -> Unit:
        r"""
        Calorie at 4 deg C
        """
        ...

    @property
    def cal_it(self) -> Unit:
        r"""
        International table calorie
        """
        ...

    @property
    def cal_mean(self) -> Unit:
        r"""
        Mean calorie
        """
        ...

    @property
    def cal_th(self) -> Unit:
        r"""
        Thermochemical calorie
        """
        ...

    @property
    def eV(self) -> Unit:
        """
        An electronvolt is the measure of an amount of kinetic energy gained by a single electron accelerating 
        from rest through an electric potential difference of one volt in vacuum.

        It equates to 1.602176634e-19 J.
        """
        ...

    @property
    def foeb(self) -> Unit:
        """
        Defined as 6.05e6 btu_59
        """
        ...

    @property
    def hartree(self) -> Unit:
        """
        Defined as 27.211 eV (4.3597447222071e-18 J)
        """
        ...

    @property
    def kWh(self) -> Unit:
        """
        The kilowatt-hour is a unit of energy equal to one kilowatt of power sustained for one hour.
        One kilowatt-hour is equal to 3600 kilojoules 
        """
        ...

    @property
    def kcal(self) -> Unit:
        """
        A kilo calory
        """
        ...

    @property
    def lge(self) -> Unit:
        r"""
        Liter of gasoline equivalent
        """
        ...

    @property
    def quad(self) -> Unit:
        """
        A quad is a unit of energy equal to 10e15 (a short-scale quadrillion) BTU
        """
        ...

    @property
    def tce(self) -> Unit:
        r"""
        Ton of coal equivalent
        """
        ...

    @property
    def therm_br(self) -> Unit: ...
    @property
    def therm_ec(self) -> Unit: ...
    @property
    def therm_us(self) -> Unit: ...
    @property
    def ton_tnt(self) -> Unit: ...

    @property
    def tonc(self) -> Unit:
        r"""
        Cooling ton
        """
        ...

    @property
    def tonhour(self) -> Unit: ...


class FDAUnits:
    @property
    def carat(self) -> Unit: ...
    @property
    def cup(self) -> Unit: ...
    @property
    def cup_uslegal(self) -> Unit: ...
    @property
    def floz(self) -> Unit: ...
    @property
    def tbsp(self) -> Unit: ...
    @property
    def tsp(self) -> Unit: ...


class GFUnits:
    @property
    def PS(self) -> Unit: ...
    @property
    def at(self) -> Unit: ...
    @property
    def hyl(self) -> Unit: ...
    @property
    def poncelet(self) -> Unit: ...
    @property
    def pond(self) -> Unit: ...


class InternationalUnits:
    @property
    def board_foot(self) -> Unit: ...
    @property
    def circ_mil(self) -> Unit: ...
    @property
    def cord(self) -> Unit: ...
    @property
    def foot(self) -> Unit: ...
    @property
    def grain(self) -> Unit: ...
    @property
    def hand(self) -> Unit: ...
    @property
    def inch(self) -> Unit: ...
    @property
    def league(self) -> Unit: ...
    @property
    def mil(self) -> Unit: ...
    @property
    def mile(self) -> Unit: ...
    @property
    def pica(self) -> Unit: ...
    @property
    def point(self) -> Unit: ...
    @property
    def yard(self) -> Unit: ...


class JapanUnits:
    @property
    def cup(self) -> Unit:
        """
        The cup (Japan) is a unit of volume equal to 0.0002 cubic meters (1 cup (Japan) = 0.0002 m^3)
        """
        ...

    @property
    def go(self) -> Unit:
        """
        The gō is the traditional amount used for a serving of rice and a cup of sake in Japanese cuisine. 
        Although the gō is no longer used as an official unit, 1-gō measuring cups or their 180 mL metric 
        equivalents are often included with Japanese rice cookers
        """
        ...

    @property
    def kan(self) -> Unit:
        """
        A kan (貫) is defined as 3.75 kilograms
        """
        ...

    @property
    def ken(self) -> Unit:
        """
        A ken (間) is defined as 6 Shaku or 1.818 meters
        """
        ...

    @property
    def shaku(self) -> Unit:
        """
        Shaku (尺), or Japanese foot, is defined as 30.3 centimeters 
        """
        ...

    @property
    def sho(self) -> Unit:
        """
        Sho is a standard unit of volume (capacity) in the East Asian system of weights and measures. 
        10 go (合; a unit of volume) is equal to 1 sho, and 10 sho is equal to 1 to (斗; a unit of volume). 
        """
        ...

    @property
    def sun(self) -> Unit:
        """
        One sun is set at a tenth length of 1 shaku (unit of distance approximately equal to 30.3 centimeters)
        """
        ...

    @property
    def tsubo(self) -> Unit:
        """
        A tsubo (坪) is unit measuring an area of 3.3m², the square area covered by two tatami mats side by side.
        """
        ...


class LaboratoryUnits:
    @property
    def HPF(self) -> Unit: ...

    @property
    def IR(self) -> Unit:
        r"""
        Index of reactivity
        """
        ...

    @property
    def IU(self) -> Unit: ...

    @property
    def LPF(self) -> Unit: ...

    @property
    def Lf(self) -> Unit:
        r"""
        Limit of flocculation
        """
        ...

    @property
    def PFU(self) -> Unit: ...

    @property
    def arbU(self) -> Unit:
        r"""
        Arbitrary unit
        """
        ...

    @property
    def enzyme_unit(self) -> Unit: ...

    @property
    def molality(self) -> Unit: ...

    @property
    def molarity(self) -> Unit: ...

    @property
    def pH(self) -> Unit: ...

    @property
    def svedberg(self) -> Unit: ...


class LogUnits:
    @property
    def BZ(self) -> Unit:
        r"""
        Radar reflectivity
        """
        ...

    @property
    def B_10nV(self) -> Unit: ...
    @property
    def B_SPL(self) -> Unit: ...
    @property
    def B_V(self) -> Unit: ...
    @property
    def B_W(self) -> Unit: ...
    @property
    def B_kW(self) -> Unit: ...
    @property
    def B_mV(self) -> Unit: ...
    @property
    def B_uV(self) -> Unit: ...
    @property
    def bel(self) -> Unit: ...

    @property
    def belA(self) -> Unit:
        r"""
        Bel of an amplitude based unit
        """
        ...

    @property
    def belP(self) -> Unit:
        r"""
        Bel of a power based unit
        """
        ...

    @property
    def dB(self) -> Unit: ...

    @property
    def dBA(self) -> Unit:
        r"""
        dB of an amplitude based unit
        """
        ...

    @property
    def dBP(self) -> Unit: ...

    @property
    def dBZ(self) -> Unit:
        r"""
        Radar reflectivity
        """
        ...

    @property
    def dB_10nV(self) -> Unit: ...
    @property
    def dB_SPL(self) -> Unit: ...
    @property
    def dB_V(self) -> Unit: ...
    @property
    def dB_W(self) -> Unit: ...
    @property
    def dB_kW(self) -> Unit: ...
    @property
    def dB_mV(self) -> Unit: ...
    @property
    def dB_uV(self) -> Unit: ...
    @property
    def logE(self) -> Unit: ...
    @property
    def logbase10(self) -> Unit: ...
    @property
    def logbase2(self) -> Unit: ...
    @property
    def neglog10(self) -> Unit: ...
    @property
    def neglog100(self) -> Unit: ...
    @property
    def neglog1000(self) -> Unit: ...
    @property
    def neglog50000(self) -> Unit: ...
    @property
    def neper(self) -> Unit: ...

    @property
    def neperA(self) -> Unit:
        r"""
        Neper of amplitude unit
        """
        ...

    @property
    def neperP(self) -> Unit:
        r"""
        Neper of a power unit
        """
        ...


class MTSUnits:
    @property
    def pieze(self) -> Unit:
        """
        Defined as one sthène per square metre; equivalent to 1 kilopascal.
        """
        ...

    @property
    def sthene(self) -> Unit:
        """
        Equivalent to one kilo newton.
        """
        ...

    @property
    def thermie(self) -> Unit:
        """
        Denotes the quantity of heat necessary to raise the temperature of a mass of 1 ton 
        of pure water by 1 C to 14.5 C under normal atmospheric pressure.

        Equivalent to one million calories.
        """
        ...


class MassUnits:
    @property
    def longton_assay(self) -> Unit:
        """
        A mass unit, roughly equivalent to 3.2667*10^-2 kg
        """
        ...

    @property
    def quintal(self) -> Unit:
        """
        Defined as 100 kilograms
        """
        ...

    @property
    def ton_assay(self) -> Unit:
        """
        A mass unit, roughly equivalent to 2.91667*10^-2 kilograms
        """
        ...


class NauticalUnits:
    @property
    def cable(self) -> Unit:
        r"""
        One tenth of a nautical mile, or (approximately) 100 fathoms.
        """
        ...

    @property
    def fathom(self) -> Unit:
        r"""
        72 inches of depth.
        """
        ...

    @property
    def knot(self) -> Unit:
        r"""
        1 nautical mile per hour.
        """
        ...

    @property
    def league(self) -> Unit:
        r"""
        3 nautical miles
        """
        ...

    @property
    def mile(self) -> Unit:
        r"""
        Historically, it was defined as the meridian arc length corresponding to
        one minute (60th of a degree) of latitude. Nowadays, the international
        nautical mile is defined as exactly 1,852 metres.
        """
        ...


class OtherUnits:
    @property
    def GigaBuck(self) -> Unit:
        """
        1000000000 $
        """
        ...

    @property
    def MegaBuck(self) -> Unit:
        """
        1000000 $
        """
        ...

    @property
    def candle(self) -> Unit: ...

    @property
    def faraday(self) -> Unit:
        """
        Faraday constant, which defines the electrical charge in one mol of electrons.  

        It is defined as 96485.3321233100141 C/mol
        """
        ...

    @property
    def ppb(self) -> Unit:
        r"""
        Part per billion
        """
        ...

    @property
    def ppm(self) -> Unit:
        r"""
        Part per million
        """
        ...

    @property
    def rpm(self) -> Unit:
        r"""
        Revolution per minute
        """
        ...


class PharmaUnits:
    @property
    def drachm(self) -> Unit:
        r"""
        One eight of a pharma ounce.
        """
        ...

    @property
    def floz(self) -> Unit:
        r"""
        One litter (SI) equates to 35.1951 (approx)
        """
        ...

    @property
    def gallon(self) -> Unit:
        r"""
        160 pharma floz
        """
        ...

    @property
    def metric_ounce(self) -> Unit:
        r"""
        A pharma ounce equates to 28 grams.
        """
        ...

    @property
    def minim(self) -> Unit:
        r"""
        The minim is a unit of volume in both the imperial and U.S. customary systems of measurement.
        Specifically it is 480th of a fluid ounce.
        """
        ...

    @property
    def ounce(self) -> Unit:
        r"""
        A SI Kg equates to 32.1507 (approx) pharma ounces.
        """
        ...

    @property
    def pint(self) -> Unit:
        r"""
        A litter (SI) equates to 1.75975 (approx) pharma pints.
        """
        ...

    @property
    def pound(self) -> Unit:
        r"""
        12 pharma ounces.
        """
        ...

    @property
    def scruple(self) -> Unit:
        r"""
        Unit of weight in the apothecaries' system, equivalent to 1.296 grams.
        """
        ...


class PowerUnits:
    @property
    def hpE(self) -> Unit:
        r"""
        Electrical horsepower (746 W)
        """
        ...

    @property
    def hpI(self) -> Unit:
        r"""
        Mechanical horsepower (745.69987 W)
        """
        ...

    @property
    def hpM(self) -> Unit:
        r"""
        Metric horsepower (735.49875 W)
        """
        ...

    @property
    def hpS(self) -> Unit:
        r"""
        Boiler horsepower (9812.5 W)
        """
        ...


class Prefixes:
    @property
    def atto(self) -> Unit:
        r"""
        1e-18 Factor
        """
        ...

    @property
    def exa(self) -> Unit:
        r"""
        1e+18 Factor
        """
        ...

    @property
    def exbi(self) -> Unit:
        r"""
        2^60 Factor
        """
        ...

    @property
    def femto(self) -> Unit:
        r"""
        1e-15 Factor
        """
        ...

    @property
    def gibi(self) -> Unit:
        r"""
        2^30 Factor
        """
        ...

    @property
    def giga(self) -> Unit:
        r"""
        1e+9 Factor
        """
        ...

    @property
    def hecto(self) -> Unit:
        r"""
        1e+2 Factor
        """
        ...

    @property
    def kibi(self) -> Unit:
        r"""
        2^10 Factor
        """
        ...

    @property
    def kilo(self) -> Unit:
        r"""
        1e+3 Factor
        """
        ...

    @property
    def mebi(self) -> Unit:
        r"""
        2^20 Factor
        """
        ...

    @property
    def mega(self) -> Unit:
        r"""
        1e+6 Factor
        """
        ...

    @property
    def micro(self) -> Unit:
        r"""
        1e-6 Factor
        """
        ...

    @property
    def milli(self) -> Unit:
        r"""
        1e-3 Factor
        """
        ...

    @property
    def nano(self) -> Unit:
        r"""
        1e-9 Factor
        """
        ...

    @property
    def one(self) -> Unit: ...

    @property
    def pebi(self) -> Unit:
        r"""
        2^50 Factor
        """
        ...

    @property
    def peta(self) -> Unit:
        r"""
        1e+15 Factor
        """
        ...

    @property
    def pico(self) -> Unit:
        r"""
        1e-12 Factor
        """
        ...

    @property
    def tebi(self) -> Unit:
        r"""
        2^40 Factor
        """
        ...

    @property
    def tera(self) -> Unit:
        r"""
        1e+12 Factor
        """
        ...

    @property
    def yobi(self) -> Unit:
        r"""
        2^80 Factor
        """
        ...

    @property
    def yocto(self) -> Unit:
        r"""
        1e-24 Factor
        """
        ...

    @property
    def yotta(self) -> Unit:
        r"""
        1e+24 Factor
        """
        ...

    @property
    def zebi(self) -> Unit:
        r"""
        2^70 Factor
        """
        ...

    @property
    def zepto(self) -> Unit:
        r"""
        1e-21 Factor
        """
        ...

    @property
    def zetta(self) -> Unit:
        r"""
        1e+21 Factor
        """
        ...


class PressureUnits:
    @property
    def atm(self) -> Unit:
        r"""
        An atmosphere (atm) is a unit of pressure based on the average atmospheric pressure at sea
        level. The actual atmospheric pressure depends on many conditions, e.g. altitude and temperature.
        """
        ...

    @property
    def att(self) -> Unit:
        r"""
        Technical atmosphere
        """
        ...

    @property
    def inH2O(self) -> Unit:
        r"""
        The inch of water (inH2O) is defined as the pressure exerted at the base of a column of fluid
        exactly 1 inch (in) high, and the fluid density is exactly 1.004514556 gram per cubic centimeter
        (g/cm³), at a physical location where the gravity acceleration is exactly 9.80665 m/sec²
        """
        ...

    @property
    def inHg(self) -> Unit:
        r"""
        The inch of mercury (inHg) is defined as the pressure exerted at the base of a column of fluid
        exactly 1 inch (in) high, and the fluid density is exactly 13.5951 gram per cubic centimeter (g/cm³),
        at a physical location where the gravity acceleration is exactly 9.80665 m/sec²
        """
        ...

    @property
    def mmH2O(self) -> Unit:
        r"""
        The millimeter of water (mmH2O) is defined as the pressure exerted at the base of a column of
        fluid exactly 1 millimeter (mm) high, and the fluid density is exactly 1.004514556 gram per cubic
        centimeter (g/cm³), at a physical location where the gravity acceleration is exactly 9.80665 m/sec²
        """
        ...

    @property
    def mmHg(self) -> Unit:
        r"""
        The millimeter of mercury (mmHg) is defined as the pressure exerted at the base of a column of
        fluid exactly 1 millimeter (mm) high, and the fluid density is exactly 13.5951 gram per cubic
        centimeter (g/cm³), at a physical location where the gravity acceleration is exactly
        9.80665 m/sec²
        """
        ...

    @property
    def psi(self) -> Unit:
        r"""
        A pound-force per square inch (psi) is a unit of pressure where a force of one pound-force (lbf)
        is applied to an area of one square inch.
        """
        ...

    @property
    def torr(self) -> Unit:
        r"""
        A torr (Torr) is a unit of pressure applied by a depth of one millimeter of mercury (mmHg). The unit
        is named after Italian physicist and mathematician Evangelista Torricelli.
        """
        ...


class SpecialUnits:
    @property
    def ASD(self) -> Unit:
        r"""
        Amplitude spectral density
        """
        ...

    @property
    def beaufort(self) -> Unit:
        r"""
        Beaufort wind scale
        """
        ...

    @property
    def fujita(self) -> Unit:
        r"""
        The Fujita scale, or Fujita-Pearson scale (FPP scale), is a scale for rating tornado intensity.
        """
        ...

    @property
    def mach(self) -> Unit:
        r"""
        Mach number (multiplier of the speed of sound)
        """
        ...

    @property
    def moment_energy(self) -> Unit: ...

    @property
    def moment_magnitude(self) -> Unit:
        r"""
        Moment magnitude for earthquake scales (related to richter scale)
        """
        ...

    @property
    def rootHertz(self) -> Unit:
        r"""
        Square root of Hertz
        """
        ...

    @property
    def rootMeter(self) -> Unit:
        r"""
        Square root of meter
        """
        ...

    @property
    def sshws(self) -> Unit:
        r"""
        The Saffir-Simpson Hurricane Wind Scale is a 1 to 5 rating based only on a hurricane's
        maximum sustained wind speed.
        """
        ...


class TemperatureUnits:
    @property
    def celsius(self) -> Unit: ...
    @property
    def fahrenheit(self) -> Unit: ...

    @property
    def rankine(self) -> Unit:
        """
        The Rankine scale is an absolute scale of thermodynamic temperature. 

        Similar to the Kelvin scale, zero on the Rankine scale is absolute zero, but a temperature difference of one 
        Rankine degree (°R or °Ra) is defined as equal to one Fahrenheit degree, rather than the Celsius degree 
        used on the Kelvin scale. 
        """
        ...

    @property
    def reaumur(self) -> Unit:
        """
        The Réaumur scale, also known as the "octogesimal division", is a temperature scale for which the melting and 
        boiling points of water are defined as 0 and 80 degrees respectively. 
        """
        ...


class TextileUnits:
    r"""
    Textile Units
    """

    @property
    def denier(self) -> Unit:
        r"""
        Grams per 9,000 metres of yarn. Den is a direct measure of linear density
        """
        ...

    @property
    def finger(self) -> Unit:
        r"""
        0.1143m
        """
        ...

    @property
    def nail(self) -> Unit:
        r"""
        0.05715m
        """
        ...

    @property
    def span(self) -> Unit:
        r"""
        0.2286m
        """
        ...

    @property
    def tex(self) -> Unit:
        r"""
        Grams per 1,000 metres of yarn. Tex is a direct measure of linear density.[
        """
        ...


class TroyUnits:
    r"""
    Most commonly used for precious metals.
    """
    @property
    def oz(self) -> Unit:
        r"""
        31.1034768g
        """
        ...

    @property
    def pennyweight(self) -> Unit:
        r"""
        A pennyweight (dwt) is now defined as a unit of mass equal to 24 grains,
        20th of a troy ounce and exactly 1.55517384 grams.
        """
        ...

    @property
    def pound(self) -> Unit:
        r"""
        Twelve troy ounces and thus is 5760 grains (373.24172 grams)
        """
        ...


class USAUnits:
    @property
    def Dry(self) -> USADryUnits:
        r"""
        Dry measures are units of volume to measure bulk commodities that are not
        fluids and that were typically shipped and sold in standardized containers
        such as barrels.

        They have largely been replaced by the units used for measuring volumes in
        the metric system and liquid volumes in the imperial system but are still
        used for some commodities in the US customary system.

        They were or are typically used in agriculture, agronomy, and commodity markets
        to measure grain, dried beans, dried and fresh produce, and some seafood. They
        were formerly used for many other foods, such as salt pork and salted fish,
        and for industrial commodities such as coal, cement, and lime.
        """
        ...

    @property
    def Engineering(self) -> USAEngUnits: ...
    @property
    def Grain(self) -> USAGrainUnits: ...
    @property
    def acre(self) -> Unit: ...
    @property
    def barrel(self) -> Unit: ...

    @property
    def chain(self) -> Unit:
        """
        100 links
        """
        ...

    @property
    def cord(self) -> Unit: ...
    @property
    def cup(self) -> Unit: ...
    @property
    def dash(self) -> Unit: ...
    @property
    def dram(self) -> Unit: ...
    @property
    def fifth(self) -> Unit: ...

    @property
    def flbarrel(self) -> Unit:
        r"""
        Fluid barrel
        """
        ...

    @property
    def floz(self) -> Unit: ...
    @property
    def foot(self) -> Unit: ...
    @property
    def furlong(self) -> Unit: ...
    @property
    def gallon(self) -> Unit: ...
    @property
    def gill(self) -> Unit: ...

    @property
    def hogshead(self) -> Unit:
        """
        Defined as 2 fluid barrels
        """
        ...

    @property
    def homestead(self) -> Unit:
        """
        Defined as 160 USA acres.
        """
        ...

    @property
    def inch(self) -> Unit: ...

    @property
    def league(self) -> Unit:
        """
        Defined as 3 miles (USA)
        """
        ...

    @property
    def link(self) -> Unit:
        """
        The link is exactly 66/100 of a US survey foot or 7.92 inches or (approximately) 20.12 cm.
        """
        ...

    @property
    def mil(self) -> Unit: ...

    @property
    def mile(self) -> Unit:
        """
        Defined as 1760 USA yards
        """
        ...

    @property
    def minim(self) -> Unit: ...
    @property
    def pinch(self) -> Unit: ...
    @property
    def pint(self) -> Unit: ...
    @property
    def quart(self) -> Unit: ...
    @property
    def rod(self) -> Unit: ...
    @property
    def section(self) -> Unit: ...
    @property
    def shot(self) -> Unit: ...
    @property
    def tbsp(self) -> Unit: ...
    @property
    def township(self) -> Unit: ...
    @property
    def tsp(self) -> Unit: ...

    @property
    def yard(self) -> Unit:
        """
        Defined as 22 chains.

        1250 yards represent 1143.002286004572 meters
        """
        ...


class USADryUnits:
    @property
    def barrel(self) -> Unit:
        r"""
        Dry barrel is defined as 7,056 cubic inches (115.6 L) ( ≈ 3.28 US bushels)
        """
        ...

    @property
    def bushel(self) -> Unit:
        r"""
        One US dry bushel equates to 8 US dry gallons
        """
        ...

    @property
    def gallon(self) -> Unit:
        r"""
        Its implicit value in the US system was originally one eighth of the Winchester bushel, which
        was a cylindrical measure of 18.5 inches (469.9 mm) in diameter and 8 inches (203.2 mm) in depth,
        which made the dry gallon an irrational number in cubic inches whose value to seven significant
        digits was 268.8025 cubic inches (4.404884 litres), or exact 9.252π cubic inches. Since the
        bushel was later defined to be exactly 2150.42 cubic inches, this figure became the exact value
        for the dry gallon (268.8025 cubic inches gives exactly 4.40488377086 L).
        """
        ...

    @property
    def peck(self) -> Unit:
        r"""
        2 dry gallons.
        """
        ...

    @property
    def pint(self) -> Unit:
        r"""
        8 dry pints make a dry gallon.
        """
        ...

    @property
    def quart(self) -> Unit:
        r"""
        2 dry pints.
        """
        ...

    @property
    def sack(self) -> Unit:
        r"""
        12 pecks.
        """
        ...

    @property
    def strike(self) -> Unit:
        r"""
        Half a bushel
        """
        ...


class USAEngUnits:
    @property
    def chain(self) -> Unit:
        r"""
        100 links
        """
        ...

    @property
    def link(self) -> Unit:
        r"""
        Ramsden Chain link, which is exactly 1 USA foot.
        """
        ...


class USAGrainUnits:
    @property
    def bushel_barley(self) -> Unit:
        r"""
        48 lb (units.Avoirdupois.pound)
        """
        ...

    @property
    def bushel_corn(self) -> Unit:
        r"""
        Shelled maize (corn) at 15.5% moisture by weight: 56 lb (units.Avoirdupois.pound)
        """
        ...

    @property
    def bushel_oats(self) -> Unit:
        r"""
        32 lb (units.Avoirdupois.pound)
        """
        ...

    @property
    def bushel_wheat(self) -> Unit:
        r"""
        Wheat at 13.5% moisture by weight: 60 lb (units.Avoirdupois.pound)
        """
        ...


class SIUnits:
    @property
    def L(self) -> Unit: ...

    @property
    def bar(self) -> Unit:
        r"""
        The bar is a metric unit of pressure, but not part of the International System of Units (SI).
        It is defined as exactly equal to 100,000 Pa (100 kPa), or slightly less than the current
        average atmospheric pressure on Earth at sea level (approximately 1.013 bar).

        By the barometric formula, 1 bar is roughly the atmospheric pressure on Earth at an altitude
        of 111 metres at 15 °C.
        """
        ...

    @property
    def becquerel(self) -> Unit: ...
    @property
    def cm(self) -> Unit: ...
    @property
    def coulomb(self) -> Unit: ...

    @property
    def farad(self) -> Unit:
        r"""
        The farad is the SI derived unit of electrical capacitance, the ability of a body
        to store an electrical charge.

        In SI base units 1 F = 1 kg-1⋅m-2⋅s^4⋅A^2.
        """
        ...

    @property
    def g(self) -> Unit: ...

    @property
    def gray(self) -> Unit:
        r"""
        The gray is a derived unit of ionizing radiation dose in the International System
        of Units (SI). It is defined as the absorption of one joule of radiation energy
        per kilogram of matter
        """
        ...

    @property
    def henry(self) -> Unit:
        r"""
        The henry is the SI derived unit of electrical inductance.

        If a current of 1 ampere flowing through a coil produces
        flux linkage of 1 weber turn, that coil has a self inductance
        of 1 henry.
        """
        ...

    @property
    def hertz(self) -> Unit:
        r"""
        The hertz is the unit of frequency in the International System of Units (SI)
        and is defined as one cycle per second.
        """
        ...

    @property
    def joule(self) -> Unit:
        r"""
        The joule is a derived unit of energy in the International System of Units.

        It is equal to the amount of work done when a force of 1 Newton displaces a mass
        through a distance of 1 metre in the direction of the force applied.
        """
        ...

    @property
    def katal(self) -> Unit:
        r"""
        The katal is the unit of catalytic activity in the International System of Units (SI).

        It is a derived SI unit for quantifying the catalytic activity of enzymes (that is,
        measuring the enzymatic activity level in enzyme catalysis) and other catalysts.
        """
        ...

    @property
    def km(self) -> Unit: ...

    @property
    def lumen(self) -> Unit:
        r"""
        The lumen is the SI derived unit of luminous flux, a measure of the total quantity of
        visible light emitted by a source per unit of time. Luminous flux differs from power
        (radiant flux) in that radiant flux includes all electromagnetic waves emitted, while
        luminous flux is weighted according to a model (a "luminosity function") of the human
        eye's sensitivity to various wavelengths. One lux is one lumen per square metre.
        """
        ...

    @property
    def lux(self) -> Unit:
        r"""
        The lux is the SI derived unit of illuminance, measuring luminous flux per unit area.

        It is equal to one lumen per square metre. In photometry, this is used as a measure of
        the intensity, as perceived by the human eye, of light that hits or passes through a
        surface. It is analogous to the radiometric unit watt per square metre, but with the
        power at each wavelength weighted according to the luminosity function, a standardized
        model of human visual brightness perception.
        """
        ...

    @property
    def mL(self) -> Unit: ...

    @property
    def mg(self) -> Unit: ...

    @property
    def mm(self) -> Unit: ...

    @property
    def newton(self) -> Unit:
        r"""
        The newton is the International System of Units (SI) derived unit of force. It is defined
        as 1 kg⋅m/s2, the force which gives a mass of 1 kilogram an acceleration
        of 1 metre per second per second.
        """
        ...

    @property
    def nm(self) -> Unit: ...

    @property
    def pascal(self) -> Unit:
        r"""
        The pascal (symbol: Pa) is the SI derived unit of pressure used to quantify internal
        pressure, stress, Young's modulus, and ultimate tensile strength. The unit, named
        after Blaise Pascal, is defined as one newton per square metre[1] and is equivalent to
        10 barye (Ba) in the CGS system. The unit of measurement called standard atmosphere
        (atm) is defined as 101,325 Pa.

        Common multiple units of the pascal are the hectopascal (1 hPa = 100 Pa), which is
        equal to one millibar, and the kilopascal (1 kPa = 1000 Pa), which is equal to
        one centibar.
        """
        ...

    @property
    def siemens(self) -> Unit:
        r"""
        The siemens is the derived unit of electric conductance, electric susceptance,
        and electric admittance
        """
        ...

    @property
    def sievert(self) -> Unit:
        r"""
        The sievert is a derived unit of ionizing radiation dose and it is a measure of
        the health effect of low levels of ionizing radiation on the human body.
        """
        ...

    @property
    def sr(self) -> Unit:
        r"""
        The steradian, or square radian, is the SI unit of solid angle.
        """
        ...

    @property
    def tesla(self) -> Unit:
        r"""
        The tesla is a derived unit of the magnetic B-field strength (also, magnetic flux density)
        """
        ...

    @property
    def volt(self) -> Unit:
        r"""
        One volt is defined as the electric potential between two points of a conducting wire when
        an electric current of one ampere dissipates one watt of power between those points.

        Equivalently, it is the potential difference between two points that will impart one joule
        of energy per coulomb of charge that passes through it.
        """
        ...

    @property
    def watt(self) -> Unit:
        r"""
        The watt is a unit of power or radiant flux. In the International System of Units (SI), it is
        defined as a derived unit of (in SI base units) 1 kg⋅m2⋅s-3 or, equivalently, 1 joule per second.
        """
        ...

    @property
    def weber(self) -> Unit:
        r"""
        A weber is the SI derived unit of magnetic flux, whose units are volt-second.
        """
        ...

    @property
    def rampere(self) -> Unit:
        """
        An ampere is an electrical current equivalent to 1019 elementary charges passing every 1.602176634 seconds
        """
        ...

    @property
    def candela(self) -> Unit:
        r"""
        The candela is the base unit of luminous intensity in the International System of Units (SI); that is,
        luminous power per unit solid angle emitted by a point light source in a particular direction
        """
        ...

    @property
    def count(self) -> Unit: ...

    @property
    def kelvin(self) -> Unit:
        r"""
        The Kelvin scale is an absolute thermodynamic temperature scale, meaning it uses absolute zero as its null point.
        """
        ...

    @property
    def kilogram(self) -> Unit: ...

    @property
    def meter(self) -> Unit:
        r"""
        The metre is currently defined as the length of the path travelled by light in a vacuum in
        1/299 792 458 of a second.
        """
        ...

    @property
    def radian(self) -> Unit: ...

    @property
    def second(self) -> Unit: ...

    @property
    def liters(self) -> Unit: ...


class TimeCatalogue:
    r"""
    Measures of time.
    """

    @property
    def hr(self) -> Unit:
        r"""
        An hour (60 minutes)
        """
        ...

    @property
    def min(self) -> Unit:
        r"""
        A minute (60 seconds)
        """
        ...

    @property
    def day(self) -> Unit:
        r"""
        An exact day, as in a fixed number of seconds (86400)
        """
        ...

    @property
    def week(self) -> Unit:
        r"""
        An exact week, as in a fixed number of days (7) and seconds (604800)
        """
        ...

    @property
    def year(self) -> Unit:
        r"""
        An exact year, made of 365 days or 31536000 seconds
        """
        ...

    @property
    def fortnight(self) -> Unit:
        r"""
        A fortnight equates to exactly 14 days (1209600 seconds)
        """
        ...

    @property
    def sday(self) -> Unit:
        r"""
        Sidereal time (as a unit also sidereal day or sidereal rotation period) is
        a timekeeping system that astronomers use to locate celestial objects.

        A sidereal day on Earth is approximately 86164.08912188729 seconds
        """
        ...

    @property
    def syr(self) -> Unit:
        r"""
        A sidereal year, also called a sidereal orbital period, is the time that Earth
        or another planetary body takes to orbit the Sun once with respect to the fixed stars.

        It corresponds to 366.25640780468996 sidereal days.
        """
        ...

    @property
    def at(self) -> Unit:
        r"""
        A tropical year (also known as a solar year or tropical period) is the time that the Sun
        takes to return to the same position in the sky of a celestial body of the Solar System
        such as the Earth, completing a full cycle of seasons; for example, the time from vernal
        equinox to vernal equinox, or from summer solstice to summer solstice. It is the type of
        year used by tropical solar calendars.
        """
        ...

    @property
    def aj(self) -> Unit:
        r"""
        In astronomy, a Julian year is a unit of measurement of time defined as exactly 365.25
        days of 86400 seconds each.
        """
        ...

    @property
    def ag(self) -> Unit:
        r"""
        Average duration of a Georgian year, which equates approximately to 365.2425 days (24h days.)
        """
        ...

    @property
    def mos(self) -> Unit:
        r"""
        The period of the lunar phases (the synodic month), e.g. the full moon to full moon period.
        Equates approximately to 29.53 days.
        """
        ...

    @property
    def moj(self) -> Unit:
        r"""
        Average duration of a Julian month, approximately 30.4375 days.
        """
        ...

    @property
    def mog(self) -> Unit:
        r"""
        Average duration of a Georgian month, approximately 30.436875 days.
        """
        ...


class VolumeUnits:
    @property
    def acre_foot(self) -> Unit:
        r"""
        The acre-foot is a non-SI unit of volume equal to about 1,233 m3 commonly used in
        the United States in reference to large-scale water resources, such as reservoirs,
        aqueducts, canals, sewer flow capacity, irrigation water, and river flows.
        """
        ...

    @property
    def drum(self) -> Unit:
        r"""
        A drum (also called a barrel) is a cylindrical shipping container used for shipping
        bulk cargo.

        Drums nominally measure just under 880 millimetres (35 in) tall with a diameter just
        under 610 millimetres (24 in), and have a common nominal volume of 208 litres
        (55 US gal).
        """
        ...

    @property
    def stere(self) -> Unit:
        r"""
        The stere, or stère, is a unit of volume in the original metric system equal to
        one cubic metre. The stère is typically used for measuring large quantities of firewood
        or other cut wood, while the cubic meter is used for uncut wood.
        """
        ...


class UnitsCatalogue:
    def __init__(self) -> None: ...

    @property
    def Angles(self) -> AngleUnits:
        r"""
        Angle related units
        """
        ...

    @property
    def Areas(self) -> AreaUnits: ...
    @property
    def Australia(self) -> AustraliaUnits: ...
    @property
    def Avoirdupois(self) -> AvoirdupoisUnits: ...
    @property
    def British(self) -> BritishUnits: ...
    @property
    def CGS(self) -> CGSUnits: ...
    @property
    def Canada(self) -> CanadaUnits: ...
    @property
    def Chinese(self) -> ChinaUnits: ...
    @property
    def Climate(self) -> ClimateUnits: ...
    @property
    def Clinical(self) -> ClinicalUnits: ...
    @property
    def Compute(self) -> ComputationUnits: ...
    @property
    def Data(self) -> DataUnits: ...
    @property
    def Distances(self) -> DistanceUnits: ...
    @property
    def Electrical(self) -> ElectricalUnits: ...
    @property
    def Energy(self) -> EnergyUnits: ...
    @property
    def FDA(self) -> FDAUnits: ...
    @property
    def GF(self) -> GFUnits: ...
    @property
    def International(self) -> InternationalUnits: ...
    @property
    def Japan(self) -> JapanUnits: ...
    @property
    def Laboratory(self) -> LaboratoryUnits: ...
    @property
    def Logarithmic(self) -> LogUnits: ...
    @property
    def MTS(self) -> MTSUnits: ...
    @property
    def Mass(self) -> MassUnits: ...
    @property
    def Nautical(self) -> NauticalUnits: ...
    @property
    def Other(self) -> OtherUnits: ...
    @property
    def Pharma(self) -> PharmaUnits: ...
    @property
    def Power(self) -> PowerUnits: ...
    @property
    def Prefix(self) -> Prefixes: ...
    @property
    def Pressure(self) -> PressureUnits: ...
    @property
    def SI(self) -> SIUnits: ...
    @property
    def Special(self) -> SpecialUnits: ...
    @property
    def Temperature(self) -> TemperatureUnits: ...
    @property
    def Textile(self) -> TextileUnits: ...
    @property
    def Troy(self) -> TroyUnits: ...
    @property
    def USA(self) -> USAUnits: ...
    @property
    def Volumes(self) -> VolumeUnits: ...
    @property
    def Time(self) -> TimeCatalogue: ...

    @property
    def kg(self) -> Unit:
        r"""
        kilograms
        """
        ...

    @property
    def L(self) -> Unit:
        r"""
        liter
        """
        ...

    @property
    def m(self) -> Unit:
        r"""
        meter
        """
        ...

    @property
    def s(self) -> Unit:
        r"""
        seconds
        """
        ...

    @property
    def A(self) -> Unit:
        r"""
        ampere
        """
        ...

    @property
    def W(self) -> Unit:
        r"""
        watt
        """
        ...

    @property
    def J(self) -> Unit:
        r"""
        Joules
        """
        ...

    @property
    def N(self) -> Unit:
        r"""
        newton
        """
        ...

    @property
    def K(self) -> Unit:
        r"""
        Kelvin
        """
        ...

    @property
    def degC(self) -> Unit:
        r"""
        Temperature Celsius
        """
        ...

    @property
    def degF(self) -> Unit:
        r"""
        Temperature Fahrenheit
        """
        ...

    @property
    def one(self) -> Unit:
        r"""
        Counting unit
        """
        ...

########################
# Bitmaps
########################


class Bitmap:
    r"""
    A compressed bitmap structure.

    Bitmaps are a generalization of `Roaring Bitmaps <https://roaringbitmap.readthedocs.io/en/latest/>`_,
    (`Apache License 2.0 <https://github.com/RoaringBitmap/RoaringBitmap/blob/master/LICENSE>`_), working
    on a 64 bit addressing space.

    Bitmap instances are iterable, returning the positions of those elements set.

    """

    def __init__(self, indices: typing.Optional[numpy.ndarray[numpy.uint64]] = None) -> None:
        r"""
        Creates a new Bitmap instance.

        Parameters
        ----------
        indices: optional numpy array like, defaults None
            Indices to be set.

        """
        ...

    @property
    def cardinality(self) -> int:
        r"""
        int: Returns the number of bits set.  Equivalent to invoke `len` function on this instance.
        """
    @property
    def empty(self) -> bool:
        r"""
        bool: Returns True when this instance doesn't have any bit set; otherwise, it returns False.
        """
    @property
    def first(self) -> typing.Optional[int]:
        r"""
        int: Returns an unsigned integer, which corresponds to the index position of the first bit set; when
        the Bitmap is empty, it returns None, to differentiate from the case where the first set index is
        at position zero.
        """
    @property
    def last(self) -> typing.Optional[int]:
        r"""
        int: Returns an unsigned integer, which corresponds to the index position of the last bit set; when
        the Bitmap is empty, it returns None, to differentiate from the case where the last set index is at
        position zero.
        """
    @property
    def in_memory_size(self) -> int:
        r"""
        int: Returns the amount of memory (in bytes) currently consumed by this instance
        """
    @property
    def persisted_size(self) -> int:
        r"""
        int: Returns the amount of storage (in bytes) that would be required to persist this instance
        """
    # Extraction methods

    def bool_array(self, *, invert: bool = True, relative: bool = True) -> numpy.ndarray[bool]:
        r"""
        Returns a numpy boolean array.

        Notes
        -----
        This method doesn't make any attempt to protect against memory consumption. If the positions
        of the indices are really high and a non relative to first extraction is requested, it is
        possible the resulting array would be so large it won't fit in memory.

        Parameters
        ----------
        invert: boolean, defaults to True
            When invert is set, flags currently unset in the bitmap will be reported as True in the
            output array; otherwise, there will be no translation in the conversion process.

        relative: boolean, defaults to True
            When relative is set, the first position of the output array (zero) would refer to the
            first position set in the bitmap.  When relative is set to false, the extraction
            process will start at bitmap's position zero.
        """
        ...

    def index_array(self) -> numpy.ndarray[numpy.uint64]:
        """
        Returns a numpy unsigned int (64 bits) array with the indices to the positions currently set.
        """
        ...
    # Bit manipulation methods

    def set(self, position: int, endEx: typing.Optional[int] = None) -> None:
        r"""
        Sets either a single position or a continuous range of positions
        """
        ...

    def unset(self, position: int, endEx: typing.Optional[int] = None) -> None:
        """
        Unsets either a single position or a continuous range of positions
        """
        ...

    def flip(self, position: int, endEx: typing.Optional[int]) -> None:
        """
        Inverts the bit flag of a single position or a continuous range of positions.
        """
        ...

    def contract(self, position: int, by: int) -> None:
        """
        Shifts left a bitmap, by a number of positions, at a particular location.
        """
        ...

    def expand(self, position: int, by: int) -> None:
        """
        Expands a bitmap, by adding a number of positions set to zero, at a particular location
        """
        ...

    def copy(self) -> Bitmap:
        """
        Clones this instance.
        """
        ...

    def slice(self, startInc: int, endInc: int) -> Bitmap:
        """
        Clones (extracts) a continuous range of this instance.
        """
        ...
    # Querying Methods

    def self_or_next(self, position: int) -> typing.Optional[int]:
        """
        Returns the next set position, or position itself when set.
        """
        ...

    def self_or_previous(self, position: int) -> typing.Optional[int]:
        """
        Returns the previous set position, or position itself when set.
        """
        ...

    def lower_cardinality(self, position: int) -> int:
        """
        Returns the total number of bits set whose index is strictly less than the given position.
        """
        ...

    def upper_cardinality(self, position: int) -> int:
        """
        Returns the total number of bits set, whose index is strictly greater than the given position.
        """
        ...

    def contains(self, position: int) -> bool:
        """
        Checks if a particular position is set or unset.

        Notes
        -----
        Bitmap instances has support for `in` idiom, which is
        equivalent to invoke this method.

        Parameters
        ----------
        position: unsigned integer, required
            Position to test

        """
        ...

    def nth(self, ordinal: int) -> int:
        """
        Returns the index of a position set by its relative order.

        Parameters
        ----------
        ordinal: unsigned integer, required
            Ordinal position to query (first, second, third, ...)
        """
        ...
    # Set Operations

    def all(self, startInc: int, endEx: int) -> bool:
        """
        Checks if all bits within a continuous range are set
        """
        ...

    def any(self, startInc: int, endEx: int) -> bool:
        """
        Checks if any bits within a continuous range are set
        """
        ...

    def difference(self, other: Bitmap) -> Bitmap:
        """
        Computes a set difference, that is, it returns a bitmap with all bits
        set in this instance but not set in `other`, union with all bits set
        in `other` but not set in this instance.

        This is equivalent to execute an `xor` operation between Bitmaps.
        """
        ...

    def intersect(self, other: Bitmap) -> Bitmap:
        """
        Computes a set intersection, that is, it returns a new bitmap with
        the common positions between this set and another set.

        This is equivalent to execute an `and` operation between Bitmaps.
        """
        ...

    def symmetric_difference(self, other: Bitmap) -> Bitmap:
        """
        Returns a new Bitmap, whose set positions corresponds to those set positions
        in this instance that are not set in `other` bitmap.

        This is equivalent to an "and not in" operation.
        This is equivalent to execute an `-` operation between Bitmaps.
        """
        ...

    def union(self, other: Bitmap) -> Bitmap:
        """
        Returns a new Bitmap, whose set positions corresponds set positions in either
        this instance or `other` Bitmap.

        This is equivalent to execute an `or` operation between Bitmaps.
        """
        ...

    def strict_subset_of(self, other: Bitmap) -> bool:
        """
        Checks if all bits set in this instance are also set in `other` instance, but
        the cardinality of the sets is difference.
        """
        ...

    def subset_of(self, other: Bitmap) -> bool:
        """
        Checks if all bits set in this instance are also set in `other` instance.
        """
        ...

    def inplace_difference(self, other: Bitmap) -> Bitmap:
        """
        Inplace difference operation.

        See Also
        --------
        difference

        """
        ...

    def inplace_intersect(self, other: Bitmap) -> Bitmap:
        """
        Inplace intersect operation

        See Also
        --------
        intersect

        """
        ...

    def inplace_symmetric_difference(self, other: Bitmap) -> Bitmap:
        """
        Inplace symmetric difference

        See Also
        --------
        symmetric_difference

        """
        ...

    def inplace_union(self, other: Bitmap) -> Bitmap:
        """
        Inplace union operation

        See Also
        --------
        union

        """
        ...

    def __and__(self, other: Bitmap) -> Bitmap: ...
    def __contains__(self, position: int) -> bool: ...
    def __eq__(self, other: Bitmap) -> bool: ...
    def __iand__(self, other: Bitmap) -> Bitmap: ...
    def __ior__(self, other: Bitmap) -> Bitmap: ...
    def __isub__(self, other: Bitmap) -> Bitmap: ...
    def __iter__(self) -> typing.Iterator: ...
    def __ixor__(self, other: Bitmap) -> Bitmap: ...
    def __len__(self) -> int: ...
    def __or__(self, other: Bitmap) -> Bitmap: ...
    def __sub__(self, other: Bitmap) -> Bitmap: ...
    def __xor__(self, other: Bitmap) -> Bitmap: ...

    __hash__ = None
    pass


########################
# Relations
########################

class ParquetCodec():
    """
    Members:

      UNCOMPRESSED

      SNAPPY

      ZSTD

      GZIP
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """

    @property
    def value(self) -> int:
        """
        :type: int
        """

    GZIP: ParquetCodec  # value = <ParquetCodec.GZIP: 3>
    SNAPPY: ParquetCodec  # value = <ParquetCodec.SNAPPY: 1>
    UNCOMPRESSED: ParquetCodec  # value = <ParquetCodec.UNCOMPRESSED: 0>
    ZSTD: ParquetCodec  # value = <ParquetCodec.ZSTD: 2>
    # value = {'UNCOMPRESSED': <ParquetCodec.UNCOMPRESSED: 0>, 'SNAPPY': <ParquetCodec.SNAPPY: 1>, 'ZSTD': <ParquetCodec.ZSTD: 2>, 'GZIP': <ParquetCodec.GZIP: 3>}
    __members__: dict


class CSVCodec():
    """
    Members:

      UNCOMPRESSED

      ZSTD

      GZIP
    """

    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...

    @property
    def name(self) -> str:
        """
        :type: str
        """

    @property
    def value(self) -> int:
        """
        :type: int
        """

    GZIP: CSVCodec
    UNCOMPRESSED: CSVCodec
    ZSTD: CSVCodec
    __members__: dict


class ParquetImportOptions():
    def __init__(self) -> None:
        ...

    @property
    def hive_partitioning(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @hive_partitioning.setter
    def hive_partitioning(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def include_filename(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @include_filename.setter
    def include_filename(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def binary_string(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @binary_string.setter
    def binary_string(self, arg0: typing.Optional[bool]) -> None:
        pass


class CSVImportOptions():
    def __init__(self) -> None:
        ...

    @property
    def auto_detect(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @auto_detect.setter
    def auto_detect(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def hive_partitioning(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @hive_partitioning.setter
    def hive_partitioning(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def compression(self) -> typing.Optional[CSVCodec]:
        """
        :type: typing.Optional[str]
        """
    @compression.setter
    def compression(self, arg0: typing.Optional[CSVCodec]) -> None:
        pass

    @property
    def date_format(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @date_format.setter
    def date_format(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def delimiter(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @delimiter.setter
    def delimiter(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def escape(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @escape.setter
    def escape(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def has_header(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @has_header.setter
    def has_header(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def include_filename(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @include_filename.setter
    def include_filename(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def null_string(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @null_string.setter
    def null_string(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def quote(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @quote.setter
    def quote(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def sample_size(self) -> typing.Optional[int]:
        """
        :type: typing.Optional[int]
        """

    @sample_size.setter
    def sample_size(self, arg0: typing.Optional[int]) -> None:
        pass

    @property
    def skip_detection(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """

    @skip_detection.setter
    def skip_detection(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def skip_top_lines(self) -> typing.Optional[int]:
        """
        :type: typing.Optional[int]
        """

    @skip_top_lines.setter
    def skip_top_lines(self, arg0: typing.Optional[int]) -> None:
        pass

    @property
    def timestamp_format(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """

    @timestamp_format.setter
    def timestamp_format(self, arg0: typing.Optional[str]) -> None:
        pass


class CSVExportOptions():
    def __init__(self) -> None: ...

    @property
    def delimiter(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @delimiter.setter
    def delimiter(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def escape(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @escape.setter
    def escape(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def force_quote(self) -> typing.Optional[typing.List[str]]:
        """
        :type: typing.Optional[typing.List[str]]
        """
    @force_quote.setter
    def force_quote(self, arg0: typing.Optional[typing.List[str]]) -> None:
        pass

    @property
    def has_header(self) -> typing.Optional[bool]:
        """
        :type: typing.Optional[bool]
        """
    @has_header.setter
    def has_header(self, arg0: typing.Optional[bool]) -> None:
        pass

    @property
    def null_string(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @null_string.setter
    def null_string(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def quote(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @quote.setter
    def quote(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def date_format(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @date_format.setter
    def date_format(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def timestamp_format(self) -> typing.Optional[str]:
        """
        :type: typing.Optional[str]
        """
    @timestamp_format.setter
    def timestamp_format(self, arg0: typing.Optional[str]) -> None:
        pass

    @property
    def compression(self) -> typing.Optional[CSVCodec]:
        """
        :type: typing.Optional[str]
        """
    @compression.setter
    def compression(self, arg0: typing.Optional[CSVCodec]) -> None:
        pass

    pass


class VirtualFile:
    def __init__(self) -> None: ...
    def read_at(self, buffer: memoryview, bytes: int, location: int) -> None: ...
    def write_at(self, buffer: memoryview, bytes: int, location: int) -> None: ...
    def read(self, buffer: memoryview, bytes: int) -> int: ...
    def write(self, buffer: memoryview, bytes: int) -> int: ...
    def size(self) -> int: ...
    def last_modified_time(self) -> int: ...
    def is_file(self) -> bool: ...
    def truncate(self, new_size: int) -> None: ...
    def sync(self) -> None: ...
    def set_position(self, location: int) -> None: ...
    def get_position(self) -> int: ...
    def close(self) -> None: ...


class VirtualFileSystem:
    READ: int = ...
    WRITE: int = ...
    CREATE: int = ...
    CREATE_NEW: int = ...
    APPEND: int = ...

    def __init__(self) -> None: ...
    def open_file(self, path: str, flags: int) -> VirtualFile: ...
    def directory_exists(self, directory: str) -> bool: ...
    def create_directory(self, directory: str) -> None: ...
    def remove_directory(self, directory: str) -> None: ...
    def list_files(self, directory: str) -> typing.List[typing.Tuple[str, bool]]: ...
    def move_file(self, src: str, dst: str) -> None: ...
    def file_exists(self, path: str) -> bool: ...
    def delete_file(self, path: str) -> None: ...
    def glob(self, path: str) -> typing.List[str]: ...
    def can_handle(self, path: str) -> bool: ...


class VirtualFileSystemFactory:
    def __init__(self) -> None: ...
    def create(self) -> VirtualFileSystem: ...


class Result():
    BLOCK_SIZE: int = ...

    def close(self) -> None:
        ...

    def fetch_one(self) -> typing.Optional[typing.Tuple[typing.Any, ]]:
        ...

    def fetch_single(self) -> typing.Optional[typing.Any]:
        ...

    def fetch_all(self) -> typing.List[typing.Tuple[typing.Any, ]]:
        ...

    def fetch_many(self, maxRows: int) -> typing.List[typing.Tuple[typing.Any, ]]:
        ...

    def to_numpy(self,) -> typing.Dict[str, numpy.array]:
        ...

    def to_numpy_batch(self, maxRows: int) -> typing.Dict[str, numpy.array]:
        ...

    def to_pandas(self) -> pandas.DataFrame:
        ...

    def to_pandas_batch(self, maxRows: int) -> pandas.DataFrame:
        ...

    def to_arrow_table(self, blocks: int = 1024) -> pyarrow.lib.Table:
        ...

    def to_arrow_record_batch_reader(self, blocks: int = 1024) -> pyarrow.lib.RecordBatchReader:
        ...


class Relation():

    def count(self) -> typing.Optional[int]: ...

    def describe(self) -> Result: ...
    def execute(self) -> Result: ...

    def relation_from_query(self, sql: str) -> Relation: ...

    def reservoir_sample(self, size: int) -> Relation: ...
    def system_sample(self, size: float, seed: typing.Optional[int] = None) -> Relation: ...

    def distinct(self) -> Relation: ...
    def cross_product(self, other: Relation) -> Relation: ...
    def union(self, other: Relation) -> Relation: ...
    def intersect(self, other: Relation) -> Relation: ...
    def minus(self, other: Relation) -> Relation: ...
    def limit(self, n: int, offset: typing.Optional[int] = None) -> Relation: ...
    def order(self, criteria: typing.List[typing.Tuple[str, bool]]) -> Relation: ...
    def keep_columns(self, columns: typing.List[str]) -> Relation: ...
    def rename_columns(self, columns: typing.List[str], aliases: typing.List[str]) -> Relation: ...

    def to_csv(self, file: str, options: CSVExportOptions) -> None: ...
    def to_parquet(self, file: str, codec: ParquetCodec = ParquetCodec.SNAPPY) -> None: ...

    @property
    def alias(self) -> str:
        """
        :type: str
        """

    @property
    def columns(self) -> typing.List[str]:
        """
        :type: typing.List[str]
        """

    @property
    def dtypes(self) -> dict:
        """
        :type: dict
        """


class Connection:
    def begin(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def close(self) -> None:
        ...

    def execute(self, query: str, params: typing.Any = None, many: bool = False) -> Result:
        ...


class Database:

    def __init__(self,
                 optPath: typing.Optional[str] = None,
                 optReadOnly: typing.Optional[bool] = None,
                 optOptions: typing.Optional[typing.List[typing.Tuple[str, str]]] = None) -> None: ...

    def connect(self) -> Connection:
        ...


class SandBoxConnection:

    def begin(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def close(self) -> None:
        ...

    def execute(self, query: str, params: typing.Any = None, many: bool = False) -> Result:
        ...

    def parquet(self, files: typing.List[str], options: ParquetImportOptions) -> Relation:
        ...

    def csv(self, file: str, options: CSVImportOptions) -> Relation:
        ...

    def pandas(self, dataFrame: pandas.DataFrame) -> Relation:
        ...

    def arrow(self, arrowObj: ArrowObject) -> Relation:
        ...

    def relation_from_query(self, query: str) -> Relation:
        ...

    def table(self, name: str, schema: typing.Optional[str] = None) -> Relation:
        ...


class SandBox:

    def __init__(self,
                 optPath: typing.Optional[str] = None,
                 optReadOnly: typing.Optional[bool] = None,
                 optVFS: typing.Optional[VirtualFileSystemFactory] = None,
                 optOptions: typing.Optional[typing.List[typing.Tuple[str, str]]] = None) -> None: ...

    def connect(self) -> SandBoxConnection:
        ...

def computeLevels( x: typing.List[float], y: typing.List[float], n_points: int, scale: int = 1000000000 ) -> typing.List[typing.List[typing.Tuple[typing.List[float], typing.List[float]]]] :
    pass
