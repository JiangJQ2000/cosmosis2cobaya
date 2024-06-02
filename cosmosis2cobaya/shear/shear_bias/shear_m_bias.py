from cosmosis2cobaya._base import base

class shear_m_bias(base):
    do_auto = True
    do_cross = True
    do_cmbcross = True

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        m_per_bin, cl_section, cal_section, cross_section, cmbcross_section, verbose=config
        ret = [cal_section,]
        if self.do_auto:
            ret += cl_section
        if self.do_cross:
            ret += cross_section
        if self.do_cmbcross:
            ret += cmbcross_section
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        m_per_bin, cl_section, cal_section, cross_section, cmbcross_section, verbose=config
        ret = []
        if self.do_auto:
            ret += cl_section
        if self.do_cross:
            ret += cross_section
        if self.do_cmbcross:
            ret += cmbcross_section
        return ret
