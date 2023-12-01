import pandas as pd
import random
import openpyxl

def generate_parts_data():
    parts = [
        "Engine", "Transmission", "Suspension", "Brakes", "Steering",
        "Electrical System", "Fuel System", "Exhaust System", "Tires", "Wheels",
        "Radiator", "Air Conditioning", "Ignition System", "Battery", "Alternator",
        "Starter Motor", "Drive Belts", "Oil Filter", "Air Filter", "Fuel Filter",
        "Spark Plugs", "Brake Pads", "Shock Absorbers", "Struts", "Axles", 
        "Power Steering Pump", "Control Arms", "Wheel Bearings", "Throttle Body"
    ]
    return random.choices(parts, k=30)

def generate_subparts_data():
    subparts_data = []
    for _ in range(random.randint(2, 5)):
        subparts_data.append(f"Subpart {_ + 1}")
    return subparts_data

def generate_versions_data():
    versions_data = []
    for _ in range(random.randint(1, 3)):
        versions_data.append(f"Version {_ + 1}")
    return versions_data

def generate_complexity_data(subparts_data, versions_data):
    return len(versions_data) * len(subparts_data)

def generate_and_save_excel(file_name):
    df = pd.DataFrame(columns=['Part', 'Subpart', 'vehicle_version', '复杂度'])

    parts_data = generate_parts_data()

    for part in parts_data:
        subparts_data = generate_subparts_data()
        versions_data = generate_versions_data()
        complexity_data = generate_complexity_data(subparts_data, versions_data)
        df = pd.concat([df, pd.DataFrame({'Part': [part], 'Subpart': ['\n'.join(subparts_data)], 'vehicle_version': ['\n'.join(versions_data)], '复杂度': [complexity_data]})], ignore_index=True)

    total_complexity = df['复杂度'].sum()

    df.loc[len(df)] = ['Total Complexity', '', '', total_complexity]

    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        for row in worksheet.iter_rows(min_row=2, max_row=len(df)+1, min_col=2, max_col=3):
            for cell in row:
                cell.alignment = openpyxl.styles.Alignment(wrapText=True, vertical='top')

    print(f"Excel文件已生成：{file_name}")

for i in range(1, 6):
    file_name = f'PMT{i}.xlsx'
    generate_and_save_excel(file_name)
