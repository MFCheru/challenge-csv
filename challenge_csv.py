import csv
import argparse
import counter_collection as cc

# Query update functions
def third_query_update(people_list, name, age, team, civil_status, acedemic_degree):
    
    if civil_status == "Casado" and acedemic_degree == "Universitario" and len(people_list) < 100:
        people_list.append([name, age, team])


def fourth_query_update(name_frequencies, team, name):

    if team == "River":
        name_frequencies.put(name)


def fifth_query_update(team_frequencies, team, age):

    team_frequencies.put(team)
    item = team_frequencies[team]

    if 'age_sum' in item.keys():
        new_age_sum = item['age_sum'] + age
        team_frequencies.update_item(team, 'age_sum', new_age_sum)
        
        if age < item['min_age']:
            team_frequencies.update_item(team, 'min_age', age)
        
        if age > item['max_age']:
            team_frequencies.update_item(team, 'max_age', age)

    else:
        team_frequencies.update_item(team, 'age_sum', age)
        team_frequencies.update_item(team, 'min_age', age)
        team_frequencies.update_item(team, 'max_age', age)


# Display functions
def display_first_query(line_count):
    print(
        "1) Cantidad de personas: ", line_count, '\n'
    )


def display_second_query(age_average):
    print(
        "2) Edad promedio: ", age_average, '\n'
    )


def display_third_query(third_query_collector):
    print(
        "3) Casados y con titulo universitario: ", '\n'
    )
    for person in third_query_collector:
        print(
            "Nombre: ", person[0], '\n'
            "Edad:   ", person[1], '\n'
            "Equipo: ", person[2], '\n'
        )


def display_fourth_query(name_frequencies):

    print("4) Los cinco nombres más frecuentes en hinchas de River son:", '\n')
    for name in name_frequencies.most_frequent(ascending_order=True):
        print(name)
    print()


def display_fifth_query(team_frequencies):

    print("5) Equipos con mas socios:", '\n')
    for team in team_frequencies.most_frequent(ascending_order=False):

        amount_of_fans = team_frequencies.frequency_of(team)
        age_sum = team_frequencies[team]['age_sum']
        min_age = team_frequencies[team]['min_age']
        max_age = team_frequencies[team]['max_age']
        age_average = age_sum / amount_of_fans
        print(team, age_average, min_age, max_age)


# Main script
def main():
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Relative path to the csv file", type=str)
    parser.add_argument("query", help="Number of the query that you want to be displayed", nargs='?', type=int, default=0)                 
    args = parser.parse_args()
    csv_path = args.csv_path
    query = args.query

    # Field names of the csv file
    field_names = ["Nombre", "Edad", "Equipo", "Estado Civil", "Nivel de Estudios"]

    # Perform queries
    with open(csv_path, newline='', encoding='latin3') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=field_names, delimiter=';')
        
        line_count = 0
        age_acum = 0

        third_query_collector = []
        fouth_query_collector = cc.CounterCollection(k_most_max_amount=5, k_most_fixed_amount=True)
        fifth_query_collector = cc.CounterCollection(k_most_fixed_amount=False)

        for row in csv_reader:
            name            = str(row["Nombre"])
            age             = int(row["Edad"])
            team            = str(row["Equipo"])
            civil_status    = str(row["Estado Civil"])
            academic_degree = str(row["Nivel de Estudios"])

            # First query acumulator
            line_count += 1
            # Second query acumulator
            age_acum   += age
            
            third_query_update(third_query_collector, name, age, team, civil_status, academic_degree)
            fourth_query_update(fouth_query_collector, team, name)
            fifth_query_update(fifth_query_collector, team, age)

    # Calulate second query
    age_average = age_acum / line_count

    # Sort third query
    third_query_collector.sort(key=lambda x: x[1])

    if   query == 1:
        display_first_query(line_count)
    
    elif query == 2:
        display_second_query(age_average)

    elif query == 3:
        display_third_query(third_query_collector)

    elif query == 4:
        display_fourth_query(fouth_query_collector)

    elif query == 5:
        display_fifth_query(fifth_query_collector)

    else:
        display_first_query(line_count)
        display_second_query(age_average)
        display_third_query(third_query_collector)
        display_fourth_query(fouth_query_collector)
        display_fifth_query(fifth_query_collector)


if __name__ == '__main__':
    main()