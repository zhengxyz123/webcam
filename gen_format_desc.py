import linecache

videodev2_h = "/usr/include/linux/videodev2.h"
now_line = 512

while True:
    line = linecache.getline(videodev2_h, now_line).strip()
    now_line += 1
    if line.startswith("#define") and "v4l2_fourcc" in line:
        pass
    elif "struct" in line:
        break
    else:
        continue

    if "/*" in line:
        line = line.replace("\t", " ")[: line.find("/*")]
    _, name, value = line.split(" ", 2)
    value = value.replace("'", '"').strip()
    print(f"{name} = {value}")
