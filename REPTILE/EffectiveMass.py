from dataclasses import dataclass
import pandas as pd

__all__ = ["EffectiveMass"]

@dataclass
class EffectiveMass:
    deposit_id: str
    detector_id: str
    data: pd.DataFrame
    bins: int
    composition: pd.DataFrame = None

    @property
    def composition_(self) -> pd.DataFrame:
        """
        The material composition of the fission chamber.

        Returns
        -------
        pd.DataFrame
            the material composition nuclide by nuclide with
            absolute uncertainty.
        """
        data = pd.DataFrame({'nuclide': [self.deposit_id],
                             'share': [1],
                             'uncertainty': [0]})
        return data if self.composition is None else self.composition

    @property
    def R_channel(self) -> int:
        """
        Calculates the channel where half maximum of the fission fragment spectrum
        was found during the calibration.

        Returns
        -------
        int
            The channel of the calibration half maximum.

        Examples
        --------
        >>> eff_mass = EffectiveMass(...)
        >>> channel = eff_mass.R_channel
        """
        return int(self.integral.channel[0] / 0.15)

    @property
    def integral(self):
        """
        Computes the EffectiveMass values. Alias for self.data.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the EffectiveMass values.

        Examples
        --------
        """
        return self.data

    @classmethod
    def from_xls(cls, file: str):
        """
        Reads data from an Excel file and extracts deposit and detector ID from the file name.
        The filename is expected to be formatted as:
        {Deposit}_{Detector}.xlsx

        Parameters
        ----------
        file : str
            File path of an Excel file containing the effective mass data.

        Returns
        -------
        EffectiveMass
            Effective mass instance.

        Examples
        --------
        >>> eff_mass = EffectiveMass.from_xls('filename.xlsx')
        """
        _, deposit_id, detector_id = file.split('\\')[-1].replace('.xlsx','').replace('.xls','').split('_')
        integral = pd.read_excel(file, sheet_name='Meff')
        bins = pd.read_excel(file, sheet_name='R', header=None).iloc[1][0]
        try:
            composition = pd.read_excel(file, sheet_name='Composition')
        except ValueError:
            composition = None
        return cls(deposit_id, detector_id, integral, bins=bins, composition=composition)