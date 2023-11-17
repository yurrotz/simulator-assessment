import pickle as pk

with open('levy_l_p_boxes.pk', 'rb') as f:
    file = pk.load(f)

print(file)