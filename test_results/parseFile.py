import re
def parse_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"Performance counter stats for 'system wide':", content)
    data_list = []

    def clean_float(s):
        return float(s.replace('\u202F', '').replace(' ', '').replace(',', '.'))

    def clean_int(s):
        return int(s.replace('\u202F', '').replace(' ', ''))

    for block in blocks[1:]:
        pkg_match = re.search(r"([\d,]+) Joules power/energy-pkg/", block)
        core_match = re.search(r"([\d,]+) Joules power/energy-cores/", block)
        cycles_match = re.search(r"([\d\s\u202F]+) +cycles", block)
        instr_match = re.search(r"([\d\s\u202F]+) +instructions", block)
        cache_ref_match = re.search(r"([\d\s\u202F]+) +cache-references", block)
        cache_miss_match = re.search(r"([\d\s\u202F]+) +cache-misses", block)
        cs_match = re.search(r"([\d\s\u202F]+) +cs", block)
        migrations_match = re.search(r"([\d\s\u202F]+) +migrations", block)
        pf_match = re.search(r"([\d\s\u202F]+) +page-faults", block)

        data = {
            "energy_pkg": clean_float(pkg_match.group(1)),
            "energy_cores": clean_float(core_match.group(1)),
            "cycles": clean_int(cycles_match.group(1)),
            "instructions": clean_int(instr_match.group(1)),
            "cache_references": clean_int(cache_ref_match.group(1)),
            "cache_misses": clean_int(cache_miss_match.group(1)),
            "cs": clean_int(cs_match.group(1)),
            "migrations": clean_int(migrations_match.group(1)),
            "page_faults": clean_int(pf_match.group(1)),
        }
        data_list.append(data)

    return data_list

def aggregate_data(data_list):
    aggregated = { key: [] for key in data_list[0] } if data_list else {}

    for entry in data_list:
        for key, value in entry.items():
            aggregated[key].append(value)
    return aggregated

def compute_averages(aggregated):
    averages = {}
    for key, values in aggregated.items():
        averages[key] = sum(values) / len(values) if values else 0
    return averages


file_data = parse_file("leo_skeleton_base_group1_short_typing_test.txt")

print(file_data)

aggregated = aggregate_data(file_data)
averages = compute_averages(aggregated)
    
print("Aggregated Data (each metric as a list):\n")
for key, values in aggregated.items():
    print(f"{key} = {values}")
    
print("\nAverages for each metric:\n")
for key, avg in averages.items():
    print(f"Average {key} = {avg}")