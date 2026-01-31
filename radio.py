
import json
import math
import random
import matplotlib.pyplot as plt
import numpy as np

avogadros_constant = 6.022e23

with open('isotopes.json', 'r') as file: 
    data = json.load(file)

def to_seconds(value, unit): 
    if(unit == "years"): 
        return value * 365 * 24 * 3600 
    if(unit == "days"): 
        return value * 24 * 3600 
    if(unit == "minutes"): 
        return value * 60
    if(unit == "seconds"): 
        return value


# for x in my_dict: -> automatically prints out the keys in the dictionary  
def print_isotopes(data):
    print("Available isotopes: ")
    for isotope, info in data.items():
        name = info["name"]
        print(f"{isotope}, {name}")


#do smth so that it maybe prints out the element in a nice way
def print_isotope_info(isotope):
    if isotope in data: 
        info = data[isotope]
        name = info["name"]
        proton_num = info["Z"]
        nucleon_num = info["A"]
        print(" ")
        print("Your choice: ")
        print(f"{name}, {proton_num}, {nucleon_num}" )
    else: 
        print("This isotope isnt found in the dataset")


def moles(isotope, mass): 
    if isotope in data: 
        info = data[isotope]
        A = info["A"]
    else: 
        print("Error")
    
    return mass / A


def get_inputs(isotope):
    print("Enter the mass in grams: ")
    grams = float(input())
    mols = moles(isotope, grams)

    print("Enter the amount of time:")
    time_input = float(input())
    print("Specify the unit ")
    print("- seconds ")
    print("- years ")
    print("- days ")
    print("- minutes ")
    unit = input()
    time = to_seconds(time_input, unit)
  
    return mols, time, grams


def simulate_decay(isotope, total_time, moles, dt = 1): 
    if isotope in data: 
        info = data[isotope]

    half_life = to_seconds(info["half_life"], info["unit"])

    num_atoms = int(moles * avogadros_constant)
    decay_constant_lambda = math.log(2) / half_life    
    
    times = []
    counts = []

    #probability per step
    p = decay_constant_lambda * dt 

    time = 0
    
    
    while time <= total_time and num_atoms > 0:

        decayed = 0


        # Fast Monte Carlo: binomial sampling
        decayed = np.random.binomial(num_atoms, p)

        #for i in range(num_atoms):
             #if random.random() < p:
                #decayed += 1 

        num_atoms -= decayed
        counts.append(num_atoms)
        times.append(time)
        time += dt
    

    return times, counts


def plot_decay(isotope, times, counts):

    plt.xlabel("Time (seconds)")
    plt.ylabel("Number of atoms")
    plt.title(f"Radioactive Decay of {isotope}")


    plt.plot(times, counts)
    plt.show()

    




print(" ")
print("======= Choose an isotope to see the decay for ========")
print("               (Please enter the name)")
print(" ")
print_isotopes(data)
isotope = input()
print_isotope_info(isotope)
mols, time, grams = get_inputs(isotope)

times = []
counts = []
times, counts = simulate_decay(isotope, time, mols, 1)

plot_decay(isotope, times, counts)

