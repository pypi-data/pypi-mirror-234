import numpy as np
from petitRADTRANS import Radtrans
from . import mu, w_mu
from . import fort_spec as fs
from tqdm import tqdm

def calc_spectra(self: Radtrans, temp, abunds, gravity, mmw, sigma_lnorm=None, \
              fsed=None, Kzz=None, radius=None, \
              gray_opacity=None, Pcloud=None, \
              kappa_zero=None, \
              gamma_scat=None, \
              add_cloud_scat_as_abs=None, \
              Tstar=None, Rstar=None, semimajoraxis=None, \
              geometry='non-isotropic', theta_star=0, \
              hack_cloud_photospheric_tau=None):
    ''' Method to calculate the atmosphere's emitted intensity as a function of angles.
    Takes a list of temp, abunds and theta_star. All other input parameters are similar to pRTs calc_flux routine

        Args:
            temp:
                the atmospheric temperature in K, at each atmospheric layer
                (2-d numpy array, same length as pressure array).
            abunds:
                dictionary of mass fractions for all atmospheric absorbers.
                Dictionary keys are the species names.
                Every mass fraction array
                has same length as pressure array.
            gravity (float):
                Surface gravity in cgs. Vertically constant for emission
                spectra.
            mmw:
                the atmospheric mean molecular weight in amu,
                at each atmospheric layer
                (1-d numpy array, same length as pressure array).
            sigma_lnorm (Optional[float]):
                width of the log-normal cloud particle size distribution
            fsed (Optional[float]):
                cloud settling parameter
            Kzz (Optional):
                the atmospheric eddy diffusion coeffiecient in cgs untis
                (i.e. :math:`\\rm cm^2/s`),
                at each atmospheric layer
                (1-d numpy array, same length as pressure array).
            radius (Optional):
                dictionary of mean particle radii for all cloud species.
                Dictionary keys are the cloud species names.
                Every radius array has same length as pressure array.
            gray_opacity (Optional[float]):
                Gray opacity value, to be added to the opacity at all
                pressures and wavelengths (units :math:`\\rm cm^2/g`)
            Pcloud (Optional[float]):
                Pressure, in bar, where opaque cloud deck is added to the
                absorption opacity.
            kappa_zero (Optional[float]):
                Scattering opacity at 0.35 micron, in cgs units (cm^2/g).
            gamma_scat (Optional[float]):
                Has to be given if kappa_zero is definded, this is the
                wavelength powerlaw index of the parametrized scattering
                opacity.
            add_cloud_scat_as_abs (Optional[bool]):
                If ``True``, 20 % of the cloud scattering opacity will be
                added to the absorption opacity, introduced to test for the
                effect of neglecting scattering.
            Tstar (Optional[float]):
                The temperature of the host star in K, used only if the
                scattering is considered. If not specified, the direct
                light contribution is not calculated.
            Rstar (Optional[float]):
                The radius of the star in Solar radii. If specified,
                used to scale the to scale the stellar flux,
                otherwise it uses PHOENIX radius.
            semimajoraxis (Optional[float]):
                The distance of the planet from the star. Used to scale
                the stellar flux when the scattering of the direct light
                is considered.
            geometry (Optional[string]):
                if equal to ``'dayside_ave'``: use the dayside average
                geometry. if equal to ``'planetary_ave'``: use the
                planetary average geometry. if equal to
                ``'non-isotropic'``: use the non-isotropic
                geometry.
            theta_star (Optional[float]):
                Inclination angle of the direct light with respect to
                the normal to the atmosphere. Used only in the
                non-isotropic geometry scenario.
    '''

    self.hack_cloud_photospheric_tau = hack_cloud_photospheric_tau
    self.Pcloud = Pcloud
    self.kappa_zero = kappa_zero
    self.gamma_scat = gamma_scat
    self.gray_opacity = gray_opacity
    self.geometry = geometry
    if self.geometry!= 'non-isotropic':
        raise NotImplementedError('phase curve calculation is currently only valid non-isotropic geometry')
    self.fsed = fsed

    self.get_star_spectrum(Tstar, semimajoraxis, Rstar)

    spectra = []
    N_comp = len(theta_star)
    for i in tqdm(range(N_comp)):
        self.mu_star = np.cos(theta_star[i] * np.pi / 180.)

        if self.mu_star <= 0.:
            self.mu_star = 1e-8
        self.interpolate_species_opa(temp[i])
        self.mix_opa_tot(abunds[i], mmw, gravity, sigma_lnorm, fsed, Kzz, radius, \
                         add_cloud_scat_as_abs=add_cloud_scat_as_abs)

        self.calc_opt_depth(gravity)
        I_GCM = calc_RT_phase(self)

        spectra.append(I_GCM)

    return spectra


def calc_RT_phase(self: Radtrans):
    # Calculate the flux
    _, I_GCM = fs.feautrier_rad_trans_phase_curve(self.border_freqs, \
                                                      self.total_tau[:, :, 0, :], \
                                                      self.temp, \
                                                      mu, \
                                                      w_mu, \
                                                      self.w_gauss, \
                                                      self.photon_destruction_prob, \
                                                      self.reflectance, \
                                                      self.emissivity, \
                                                      self.stellar_intensity, \
                                                      self.geometry, \
                                                      self.mu_star,
                                                      self.do_scat_emis)

    return I_GCM