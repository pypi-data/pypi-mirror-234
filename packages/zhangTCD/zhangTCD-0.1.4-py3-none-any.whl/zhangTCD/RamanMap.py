from .spcMap import spcMap

class RamanMap(spcMap):
    # Unit, labels and scalebar
    xy_unit = '$\mu$m'
    x_unit = 'cm$^{-1}$'
    x_label = 'Raman shift (' + x_unit + ')'
    y_unit = 'a.u.'
    y_label = 'Intensity (' + y_unit + ')'
    experiment = 'Raman spectroscopy'
    def __init__(self, rawdatafile):
        spcMap.__init__(self, rawdatafile)
    
    # -------------------------------------
    def update_units(self, **kwargs):
        '''
        Update units used in the work:
        xy_unit: length
        x_unit: wavenumber
        x_label: Raman shift (cm-1)
        y_unit: a.u.
        y_label: Intensity (a.u.)
        '''
    
        for field in kwargs:
            vars(self)[field] = kwargs[field]