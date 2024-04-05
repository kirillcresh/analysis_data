from math import floor

file_list: list[str] = [
    "ФСД дз4 - Лист1.csv",
    "ФСД дз4 - Лист2.csv",
    "ФСД дз4 - Лист3.csv",
]
map_results: list[dict[str, int]] = []


def map_f(file: str):
    with open(file, encoding="UTF-8") as f:
        caller = []
        duration = []
        lines = f.readlines()
        first_line = lines[0].split(",")
        for i in range(len(first_line)):
            if first_line[i] == "Вызывающий":
                pos_caller = i
            if first_line[i] == "Длительность":
                pos_duration = i
        for line in lines[1:]:
            line = line.split(",")
            if line[pos_caller] not in caller:
                caller.append(line[pos_caller])
                duration.append(line[pos_duration])
            else:
                static_duration = []
                static_duration.append(duration[caller.index(line[pos_caller])])
                static_duration.append(line[pos_duration])
                duration[caller.index(line[pos_caller])] = static_duration
        map_results.append(dict(zip(caller, duration)))


for file in file_list:
    map_f(file)
print("map_results-----------------------------------------")
print(map_results[0])
print(map_results[1])
print(map_results[2])
sort_arr: dict[str, list[str]] = {}


def result_shuffle(node_res):
    for key, val in node_res.items():
        values = sort_arr.get(key, [])
        values.append(val)
        sort_arr[key] = values


for node_res in map_results:
    result_shuffle(node_res)

print("sort result----------------------------------")
print(sort_arr)

result: dict[str, str] = {}


def reducer(key, grouped_values):
    group_sum_duration_sec = 0
    total_count_dur = 0
    for durations in grouped_values:
        sum_duration_sec = 0
        count_dur = 0
        if isinstance(durations, list):
            for duration in durations:
                if duration == "":
                    continue
                count_dur += 1
                split_dur = duration.split(":")
                minutes = split_dur[0]
                second = split_dur[1]
                min_to_sec = int(minutes) * 60
                duration_sec = int(second) + min_to_sec
                sum_duration_sec += duration_sec
        else:
            if durations == "":
                continue
            count_dur += 1
            split_dur = durations.split(":")
            minutes = split_dur[0]
            second = split_dur[1]
            min_to_sec = int(minutes) * 60
            duration_sec = int(second) + min_to_sec
            sum_duration_sec += duration_sec
        total_count_dur += count_dur
        group_sum_duration_sec += sum_duration_sec
    avg_dur = group_sum_duration_sec / total_count_dur
    avg_min = floor(avg_dur / 60)
    avg_sec = int(avg_dur - avg_min * 60)
    if avg_sec < 10:
        avg_sec = f"0{avg_sec}"
    grouped_values = f"{avg_min}:{avg_sec}"
    result[key] = grouped_values  # здесь среднее время звонка


for key, values in sort_arr.items():
    reducer(key, values)

print("reducer result -----------------------------")
print(result)
