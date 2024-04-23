import linecache

videodev2_h = "/usr/include/linux/videodev2.h"
now_line = 512


while True:
    line = linecache.getline(videodev2_h, now_line).strip()
    now_line += 1
    if line.startswith("/*") and line.endswith("*/"):
        continue
    elif len(line) == 0:
        continue
    elif "v4l2_fourcc" not in line:
        break

    if "/*" in line:
        line = line[: line.find("/*")]
    line = line.replace("\t", " ")
    _, name, value = line.split(" ", 2)
    value = value.replace("'", '"').strip()
    print(f"{name} = {value}")
