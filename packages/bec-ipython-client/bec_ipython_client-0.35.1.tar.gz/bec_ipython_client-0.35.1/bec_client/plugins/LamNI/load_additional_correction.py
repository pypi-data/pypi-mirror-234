def lamni_read_additional_correction():
    # "additional_correction_shift"
    # [0][] x , [1][] y, [2][] angle, [3][0] number of elements
    import numpy as np

    with open("correction_lamni_um_S01405_.txt", "r") as f:
        num_elements = f.readline()
        int_num_elements = int(num_elements.split(" ")[2])
        print(int_num_elements)
        corr_pos_x = []
        corr_pos_y = []
        corr_angle = []
        for j in range(0, int_num_elements * 3):
            line = f.readline()
            value = line.split(" ")[2]
            name = line.split(" ")[0].split("[")[0]
            if name == "corr_pos_x":
                corr_pos_x.append(value)
            elif name == "corr_pos_y":
                corr_pos_y.append(value)
            elif name == "corr_angle":
                corr_angle.append(value)
    return (corr_pos_x, corr_pos_y, corr_angle, num_elements)
