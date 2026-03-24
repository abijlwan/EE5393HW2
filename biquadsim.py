import subprocess
import re

def write_in_file(state, filename='biquad.in'):
    """Writes the current molecular state to the .in file."""
    with open(filename, 'w') as f:
        for mol, val in state.items():
            f.write(f"{mol} {int(val)} N\n")

def parse_output(output_text, molecules):
    """Extracts the final molecular counts from the aleae output."""
    final_state = {}
    
    for line in output_text.split('\n'):
        if line.startswith("avg ["):
            numbers = re.findall(r"[\d.]+", line)
            for i, mol in enumerate(molecules):
                final_state[mol] = float(numbers[i])
            break
            
    return final_state

if __name__ == '__main__':
    inputs = [100, 5, 500, 20, 250]
    molecules = ['X', 'A', 'F', 'H', 'C', 'E', 'Y', 'R1', 'R2']
    current_state = {mol: 0 for mol in molecules}
    
    print(f"{'Cycle':<7} | {'Input (X)':<10} | {'Output (Y)':<10}")
    print("-" * 35)
    
    for cycle, x_val in enumerate(inputs, 1):
        current_state['X'] = x_val
        write_in_file(current_state)
        
        cmd = ['./aleae', 'biquad.in', 'biquad.r', '1', '-1', '0']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        new_state = parse_output(result.stdout, molecules)
        
        output_y = int(new_state['Y'])
        print(f"{cycle:<7} | {x_val:<10} | {output_y:<10}")
        
        current_state['C'] = new_state['R1']
        current_state['E'] = new_state['R2']
        current_state['R1'] = 0
        current_state['R2'] = 0
        
        current_state['A'] = new_state['A']
        current_state['F'] = new_state['F']
        current_state['H'] = new_state['H']
        current_state['Y'] = 0