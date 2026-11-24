import matplotlib.pyplot as plt

# Input Variables
T_prep = float(input("Prep time is: "))  # preparation time
vol_one_part = float(input("Total volume of one part: "))
sup_vol_one_part = float(input("Total support volume of one part: "))
sur_area_one_part = float(input("Total surface area of one part: "))
max_build_height = float(input("Max build height: "))
num_layers = float(input("Number of layers: "))
F_matchan = float(input("Do you change a material 0/1: "))
F_heat = float(input("Do you need heat treatment 0/1: "))
F_wc = float(input("Do you need wire cutting 0/1: "))
one_batch_num = int(input("what is the total number of a part in a chamber "))

# Constants
C_lab = 15.84  # $/h
F_inert = 1.25
T_setup = 1.5  # h
T_matchan = 2.0  # h
C_ecb = 0.0608  # 0.038$/kWh * 1.6 kWh
C_furn = 150  # $
C_ech = 0.057  # $
T_heat = 2  # h
T_wc = 2  # $
C_mwc = 150  # $
C_ecw = 0.0456  # 0.038$/kWh * 1.2 kWh
T_rem = 1.5  # h
C_pur = 600000
Y_life = 5 * 5400

# Material types and their costs
materials = {
    "ss316l": {"density": 7.93, "cost": 103.84 * 10e-6},
    "ti64": {"density": 4.42, "cost": 526.35 * 10e-6},
    "AlSi10Mg": {"density": 2.67, "cost": 263.738 * 10e-6}
}

cost_per_part_lists = {material: [] for material in materials}

# Generate num_parts_list for 200 parts with increments of 4
num_parts_list = list(range(one_batch_num, 201,one_batch_num))

for material, props in materials.items():
    
    cost_accumulated = 0
    build_count = 0

    for num_parts in num_parts_list:
        
        vol_total = vol_one_part * num_parts
        sup_vol_total = sup_vol_one_part * num_parts
        sur_area_total = sur_area_one_part * num_parts

        T_build = (
                            -55.14539374334845 + 11.2389 * num_parts + 0.0056 * vol_one_part + 0.0006 * sup_vol_one_part + -0.0003 * sur_area_one_part + 8.3892 * max_build_height + -0.2347 * num_layers) / 60

        if T_build > 10:
            C_inert = 381.09
        else:
            C_inert = 38.109

        C_SLM = (C_pur * T_build) / (num_parts * 0.9 * Y_life) #($/part)
        # C_SLM  = 0.164
        C_prep = T_prep * C_lab

        cost_part = props["cost"] * vol_total
        cost_sup = props["cost"] * sup_vol_total
        cost_scrap = cost_part * 0.15
        C_mat = cost_part + cost_sup + cost_scrap

        C_build = T_build * (C_SLM + C_inert) + C_mat

        C_setup = F_inert * (C_lab + C_SLM) * (T_setup + F_matchan * T_matchan) / num_parts
        C_heat = F_heat * T_heat * (C_lab + C_furn)
        C_wc = F_wc * T_wc * (C_lab + C_mwc)
        C_rem = F_inert * T_rem * (C_lab + C_SLM) / num_parts
        C_post = C_heat + C_wc + C_rem

        C_total = C_prep + C_setup + C_build + C_post

        # Accumulate cost for every 6 parts
        cost_accumulated += C_total


        # Check if a build job (consisting of 4 parts) is completed
        if num_parts % one_batch_num== 0:
            build_count += 1
            cost_per_part = cost_accumulated / (one_batch_num * build_count)  # Calculate cost per part
            cost_per_part_lists[material].append(cost_per_part)
            cost_accumulated = 0  # Reset accumulated cost

# Generate x-axis labels for the plot
x_labels = list(range(one_batch_num, 201, one_batch_num))  # Adjusted to match the length of cost_per_part_list

# Save T_build to a file (everytime it will be re-written based on inputs)
with open('T_build_value.txt', 'w') as f:
    T_build = round(T_build, 2)
    f.write(str(T_build))  # Save T_build as a string

# Plotting
plt.figure(figsize=(10, 4))
for material, cost_per_part_list in cost_per_part_lists.items():
    plt.plot(x_labels, cost_per_part_list, label=material)

plt.xlabel('Number of Parts', fontsize=14)
plt.ylabel('Cost per Part ($)', fontsize=17)
plt.title('Cost per Part vs. Number of Parts for Different Materials', fontsize=16)
plt.grid(True)

# Make axis number labels a little big bigger
plt.tick_params(axis='both', labelsize=10)

plt.legend(fontsize=15)
plt.savefig('diagram.jpeg', dpi=600)  
#plt.show()
print(T_build)