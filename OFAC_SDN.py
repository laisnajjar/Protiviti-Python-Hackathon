import pandas as pd
import random

file = "SDF_Data_List.csv"

#get 300 random samples for each variation
def get_random_samples(file_path, numSamples):
    df = pd.read_csv(file, names = ['Full Name','Entity Type'])
    individuals = df[df['Entity Type'] == 'individual']
    samples = individuals.sample(n = numSamples) #! change to 300
    name_splits = samples['Full Name'].str.split(', ', expand=True)
    samples['Last Name'] = name_splits[0]
    first_second_names = name_splits[1].str.split(' ', n=1, expand=True)
    samples['First Name'] = first_second_names[0]
    samples['Second Name'] = first_second_names[1].fillna('')
    return samples

# returns full name, FN + LN, 2N + FN + LN, LN + 2N + FN
def get_name_combinations(samples):
    samples['FN + LN'] = samples['First Name'] + ' ' + samples['Last Name']
    samples['LN + FN'] = samples['Last Name'] + ' ' + samples['First Name']
    samples['2N + FN + LN'] = samples['Second Name'] + ' ' + samples['First Name'] + ' ' + samples['Last Name']
    samples['LN + 2N + FN'] = samples['Last Name'] + ' ' + samples['Second Name'] + ' ' + samples['First Name']
    return samples[['Full Name', 'FN + LN', 'LN + FN', '2N + FN + LN', 'LN + 2N + FN']]

# for containment
def shorten_first_name(name):
    if len(name) < 4:
        return name
    else:
        shorten_length = random.randint(1, round(len(name) * 0.75))
        return name[:shorten_length]
#get containment of first names
def create_containment(data):
    # Shorten 'First Name' if necessary
    data['First Name'] = data['First Name'].apply(shorten_first_name)
    return data
#Stitching​
#Add a random amount (1-5) of hyphens somewhere in the name (cannot be leading). If the full name has more than 11 characters, anywhere from 1-5 hyphens are added. If the name <= 11 chars, either 1 or 2 hyphens are added​

#Return the Full Name
def add_hypens(name):
    num_chars = len(name)
    if num_chars > 11:
        num_hyphens = random.randint(1, 5)
    else:
        num_hyphens = random.randint(1, 2)
    hyphen_indices = random.sample(range(1, num_chars), num_hyphens)
    hyphen_indices.sort()
    for index in hyphen_indices:
        name = name[:index] + '-' + name[index:]
    return name

def create_stichting(data):
    data['Full Name'] = data['Full Name'].apply(add_hypens)
    return data

def master(file):
    numSamples = 300
    #name combos
    #get samples
    samples = get_random_samples(file, numSamples)
    print(samples)
    name_combos = get_name_combinations(samples)
    name_combos.to_csv('namecombos.csv', index = False)
    #containment names
    #new round of smaples
    samples = get_random_samples(file, numSamples)
    containment = create_containment(samples)
    containment.to_csv('containment.csv', index = False)
    #stitching
    #new round of samples
    samples = get_random_samples(file, numSamples)
    stitching = create_stichting(samples)
    stitching.to_csv('stitching.csv', index = False)

master(file)