typeof = {'cutoff': float,
          'interact': str,
          'numba': str,
          'dt': float,
          'run': [float, float, int],
          'integ': str,
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
          'mass': float,
          'shape': str,
          'sigma': float,
          'epsilon': float,
          'agent_pos': float,
          'slider_pos': float,
          'slider_vel': float,
          'eq_len': float,
          'constrain': str,
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

thermotype = {('vs', 'velrescale'): 'vs',
              ('b', 'berendsen'): 'b',
              ('l', 'langevin'): 'l'
}        
