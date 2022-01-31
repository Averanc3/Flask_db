import csv
import random

from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()
fake.add_provider(VehicleProvider)

file_path = '/Users/nikitafadeenko/PycharmProjects/FlaskProj/'
file_name = 'car_names.csv'
full_path = file_path + file_name

car_info = []
for i in range(30):
    car = []
    car.append(fake.vehicle_make())
    car.append(fake.vehicle_model())
    car.append(random.randint(1, 30))
    car.append(random.randint(1, 30))
    car_info.append(car)
print(car_info)

with open(full_path, "w") as cf:
    writer = csv.writer(cf)
    writer.writerow(['car_name', 'car_model', 'color_id', 'speed_id'])
    writer.writerows(car_info)


