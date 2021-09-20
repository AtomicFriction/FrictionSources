typeof = {'cutoff': float,
          'eta': float,
          'interact': str,
          'numba': str,
          'dt': float,
          'run': [float, float, int],
          'eig_proj': [int, int],
          'integ': str,
          'apply_agent': [int],
          'apply_damping': [int],
          'n_dump': int,
          'n_phonon': int,
          'data': str,
          'dim': int,
          'layers': int,
          'fix_layers': int,
          'num': int,
          'bound_cond': str,
          'latt_const': float,
          'cuto_const': float,
          'displace_type': str,
          'k': float,
          'k1': float,
          'k2': float,
          'k3': float,
          'mass': float,
          'shape': str,
          'sigma': float,
          'epsilon': float,
          'agent_pos': float,
          'slider_pos': float,
          'slider_vel': float,
          'eq_len': float,
          'constrain': str,
          'apply_thermo': [int],
          'thermo': str,
          'mode': str,
          'thickness': int,
          'tau': float,
          's': float,
          'q': float,
          'gamma': float
}

integtype = {('ec', 'eulercromer'): 'EulerCromer',
             ('vv', 'velocityverlet'): 'VelocityVerlet'
}

thermotype = {('vs', 'velrescale'): 'VelRescale',
              ('b', 'berendsen'): 'Berendsen',
              ('nh', 'nosehoover'): 'NooseHoover',
              ('l', 'langevin'): 'Langevin'
}
