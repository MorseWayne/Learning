def parse_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    data_lines = data.strip().split('\n')
    
    abnormal_values = []
    kpi_data = {}
    current_abnormal = None
    
    for line in data_lines:
        if ':' in line:
            key, values = line.split(': ')
            if key == 'abnormal':
                current_abnormal = [float(x) for x in values.split()]
                abnormal_values.append(current_abnormal)
            elif key.startswith('kpi_'):
                if current_abnormal is not None:
                    kpi_values = [float(x) for x in values.split()]
                    kpi_data.setdefault(tuple(current_abnormal), []).append(kpi_values)
                else:
                    print("Warning: Found KPI data without corresponding Abnormal data.")
    
    return abnormal_values, kpi_data

file_path = 'data.txt'
abnormal, kpi_data = parse_data(file_path)
print("Abnormal values:", abnormal)
print("KPI data:")
for abnormal_values, kpi_values in kpi_data.items():
    print(f"Abnormal: {abnormal_values}")
    print(f"KPI values: {kpi_values}")