from pycbc.waveform import td_approximants, fd_approximants

def get_approximants(approximant_type, end):
    if type(end) is int and end > 0:
      if approximant_type == 'td':
          approximants = td_approximants()
          return approximants[:end]
      elif approximant_type == 'fd':
          approximants = fd_approximants()
          return approximants[:end]
      else:
          raise ValueError('Only td or fd approximants exist')
    else:
        raise ValueError('End is not Int or is > 0')