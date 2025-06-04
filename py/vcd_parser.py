import re
from collections import defaultdict

def parse_vcd(filepath):
  try:
    with open(filepath, 'r') as f:
      lines = f.readlines()
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")
  except IOError as e:
    raise IOError(f"Error opening file '{filepath}': {e}")

  hierarchy_stack = []
  signal_map = {}                   # Symbol → {name, type, width}
  time_events = defaultdict(list)   # Timestamp → list of changes
  current_time = 0

  for line in lines:
    line = line.strip()
      
    if line.startswith('$scope'):
      tokens = line.split()
      if len(tokens) >= 3:
        module = tokens[2]
        hierarchy_stack.append(module)
      else:
        raise ValueError(f"Malformed $scope line: '{line}'")
      
    elif line.startswith('$upscope'):
      if hierarchy_stack:
        hierarchy_stack.pop()
      else:
        raise ValueError("Unexpected $upscope with empty hierarchy stack")
      
    elif line.startswith('$var'):
      tokens = line.split()
      if len(tokens) >= 6:
        symbol = tokens[4]
        signal_name = tokens[5]
        full_path = '.'.join(hierarchy_stack + [signal_name])
        signal_map[symbol] = {
            'name': full_path,
            'type': tokens[1],
            'width': int(tokens[2])
        }
      else:
        raise ValueError(f"Malformed $var line: '{line}'")
      
    elif re.match(r'#\d+', line):
      current_time = int(line[1:])
      
    elif line and not line.startswith('$') and not line.startswith('#'):
      if line[0] in '01xX':
        symbol = line[1:]
        value = line[0]
      elif line[0] == 'b':
        parts = line[1:].split()
        if len(parts) == 2:
          value, symbol = parts
        else:
          raise ValueError(f"Malformed binary line: '{line}'")
      else:
          continue
        
      signal = signal_map.get(symbol)
      if signal:
        time_events[current_time].append({
          'signal': signal['name'],
          'value': value
        })
      # else:
      #   raise ValueError(f"Unknown signal: '{symbol}'")

  return signal_map, time_events
