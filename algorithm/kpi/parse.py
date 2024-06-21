class DataParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.kpi_data = {}

    def parse_data(self):
        with open(self.file_path, 'r') as file:
            data = file.read()

        data_lines = data.strip().split('\n')

        current_abnormal = None

        index = 0
        for line in data_lines:
            if ':' in line:
                key, values = line.split(':')
                if key == 'abnormal':
                    index += 1
                    current_abnormal = [float(x) for x in values.split()]
                    self.kpi_data[index] = (current_abnormal, [])
                elif key.startswith('kpi_'):
                    if current_abnormal is not None:
                        kpi_value = [float(x) for x in values.split()]
                        self.kpi_data[index][1].append(kpi_value)
                    else:
                        print("Warning: Found KPI data without corresponding Abnormal data.")

    def print_data(self):
        print("KPI data:")
        for abnormal, kpi_values in self.kpi_data.values():
            print(f"Abnormal: {len(abnormal)}")
            for kpi in kpi_values:
                print(f"kpi len: \t{len(kpi)}")

    def get_kpi_data(self):
        return self.kpi_data


# file_path = 'kpi_test_data.txt'
# parser = DataParser(file_path)
# parser.parse_data()
# parser.print_data()
