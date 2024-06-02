from cosmosis2cobaya._base import base

class cl_to_xi_interface(base):

    def cosmosis_datablock_inputs(self):
        config = self.module.data
        xi_type, thetas, theta_edges, ell_max, legfacs, cl_section, output_section, save_name, bin_avg, e_plus_b_name = config
        ret = []
        if xi_type == "EB":
            ee_section, bb_section, e_plus_b_name = cl_section[0], cl_section[1], e_plus_b_name
            ret += [ee_section, bb_section]
            cl_section, bb_section = cl_section
        ret.append(cl_section)
        return ret
    
    def cosmosis_datablock_outputs(self):
        config = self.module.data
        xi_type, thetas, theta_edges, ell_max, legfacs, cl_section, output_section, save_name, bin_avg, e_plus_b_name = config
        if not isinstance(output_section, tuple):
            output_section = (output_section,)
        ret = list(output_section)
        if xi_type == "EB":
            p_section, m_section = e_plus_b_name + "_eplusb", e_plus_b_name + "_eminusb"
            ret += [p_section, m_section]
        for o in output_section:
            ret.append(f'_metadata.{o}.theta.unit')
            if theta_edges is not None:
                ret.append(f'_metadata.{o}.theta_edges.unit')
        return ret

class TwoPt_shear(cl_to_xi_interface):
    name = '2pt_shear'

class TwoPt_gal(cl_to_xi_interface):
    name = '2pt_gal'

class TwoPt_gal_shear(cl_to_xi_interface):
    name = '2pt_gal_shear'

class TwoPt_gal_cmbkappa(cl_to_xi_interface):
    name = '2pt_gal_cmbkappa'

class TwoPt_gal_cmbkappa_planck(cl_to_xi_interface):
    name = '2pt_gal_cmbkappa_planck'

class TwoPt_shear_cmbkappa(cl_to_xi_interface):
    name = '2pt_shear_cmbkappa'

class TwoPt_shear_cmbkappa_planck(cl_to_xi_interface):
    name = '2pt_shear_cmbkappa_planck'
