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
          'agent_select': str,
          'mass': float,
          'shape': str,
          'sigma': float,
          'epsilon': float,
          'normal_force': float,
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

integtype_agent = {('ec', 'eulercromer'): 'SimulateAgentEC',
             ('vv', 'velocityverlet'): 'SimulateAgentVV'
}

integtype_subs = {('ec', 'eulercromer'): 'SimulateSubsEC',
             ('vv', 'velocityverlet'): 'SimulateSubsVV'
}

thermotype = {('vs', 'velrescale'): 'VelRescale',
              ('b', 'berendsen'): 'Berendsen',
              ('nh', 'nosehoover'): 'NooseHoover',
              ('l', 'langevin'): 'Langevin'
}
