import json
import requests
example_vehicle_config = {
	"engine_type": "electric",
	"country":"Italy",
	"zone":"North",
	"fuel_capacity": 35.8,
	"consumption": 10.309,
	"cost_car": 24700,
}
if example_vehicle_config["engine_type"] == "electric":
	countries_code = json.loads(requests.get('https://api.electricitymap.org/v3/zones').content)
	for k, v in countries_code.items():
		if example_vehicle_config["zone"] == "":
			if v["zoneName"] == example_vehicle_config["country"]:
				code = k
				break
		elif "countryName" not in list(v.keys()):
			pass
		elif v['countryName'] == example_vehicle_config["country"] and v["zoneName"] == example_vehicle_config["zone"]:
			code = k
			break

	electric_production_emissions = requests.get('https://api.co2signal.com/v1/latest?countryCode='+code,
	                        headers={'auth-token': '658db0a8d45daedc'})
class Vehicle(object):
	def __init__(self, vehicle_config):
		self.engine_type = vehicle_config["engine_type"] #gasoline, diesel, lpg, gnc, electric
		self.consumption = vehicle_config["consumption"] #km/l, km/kWh
		self.capacity = vehicle_config["fuel_capacity"] #kWh (electric), Liter (gasoline,diesel,lpg), kilograms (gnc)
		self.cost_car = vehicle_config["cost_car"] # in €

		if self.engine_type == "gasoline":
			self.welltotank_emission = 90.4 #gCO2eq/MJ
			self.energy_content = 32 #MJ/L
			self.welltotank_energy = 0.24 #MJ/MJgasoline
			self.lower_heating_value = 43.2 #MJ/kg
			self.carbon_content = 86.4 #%
		elif self.engine_type == "diesel":
			self.welltotank_emission = 92.1 #gCO2eq/MJ
			self.energy_content = 36 #MJ/L
			self.welltotank_energy = 0.26 #MJ/MJdiesel
			self.lower_heating_value = 43.1  # MJ/kg
			self.carbon_content = 86.1  # %
		elif self.engine_type == "lpg":
			self.welltotank_emission = 73.2 #gCO2eq/MJ
			self.energy_content = 24  # MJ/L
			self.welltotank_energy = 0.12 #MJ/MJlpg
			self.lower_heating_value = 46  # MJ/kg
			self.carbon_content = 82.4  # %
		elif self.engine_type == "cng":
			self.welltotank_emission = 67.6 #gCO2eq/MJ
			self.energy_content = 44.4  # MJ/kg
			self.welltotank_energy = 0.15 #MJ/MJcng
			self.lower_heating_value = 46.6  # MJ/kg
			self.carbon_content = 71.3  # %
		elif self.engine_type == "electric":
			self.welltotank_emission = json.loads(electric_production_emissions.content)['data']['carbonIntensity'] #gCO2eq/Kwh
			self.welltotank_energy = 2.96 #MJ/MJelectricity


	def get_charging_time_from_perc(self, actual_level_perc, flow_amount, beta=100):
		# flow_amount is generalized to represent the amount of fuel
		# loaded in the vehicle per unit of time
		# electric: kW (3.3,7.4,11,22,43,50,120)
		# gasoline,diesel,lpg: liter/min (between 30-50)
		# gnc: kg/min (between 30-70)

		if self.engine_type == "electric":
			power_output = flow_amount / 1000
			capacity_left = ((beta - actual_level_perc) / 100) * self.capacity
			return (capacity_left / power_output) * 3600
		elif self.engine_type in ["gasoline", "diesel", "lpg","cng"]:
			flow_rate = flow_amount
			capacity_left = ((beta - actual_level_perc)/100) * self.capacity
			return (capacity_left/flow_rate) * 60

	def get_percentage_from_charging_time(self, charging_time, flow_amount):
		# flow_amount is generalized to represent the amount of fuel
		# loaded in the vehicle per unit of time
		# electric: kW (3.3,7.4,11,22,43,50,120)
		# gasoline,diesel,lpg: liter/min (between 30-50)
		# gnc: kg/min (between 30-70)

		if self.engine_type == "electric":
			power_output = flow_amount / 1000
			capacity_left = power_output * (charging_time / 3600)
			return 100 * (capacity_left / self.capacity)
		elif self.engine_type in ["gasoline", "diesel", "lpg", "cng"]:
			flow_rate = flow_amount
			capacity_left = (flow_rate * charging_time)/60
			return 100 * (capacity_left / self.capacity)

	def tanktowheel_energy_from_perc(self, percentage):
		if self.engine_type == "electric":
			tanktowheel_kwh = self.percentage_to_consumption(percentage)
		elif self.engine_type in ["gasoline", "diesel", "lpg", "cng"]:
			tanktowheel_kwh = (self.percentage_to_consumption(percentage) * self.energy_content) / 3.6
		return tanktowheel_kwh

	def welltotank_energy_from_perc(self, percentage):
		if self.engine_type == "electric":
			tanktowheel_mj = self.percentage_to_consumption(percentage) * 3.6
		elif self.engine_type in ["gasoline", "diesel", "lpg", "cng"]:
			tanktowheel_mj = self.percentage_to_consumption(percentage) * self.energy_content
		welltotank_kwh = (self.welltotank_energy * tanktowheel_mj) / 3.6
		return welltotank_kwh

	def from_kml_to_lkm(self):
		return 1 / self.consumption

	def from_kml_to_energyperkm(self):
		perkm_consumption = self.from_kml_to_lkm()
		return perkm_consumption * self.energy_content

	def consumption_to_percentage(self, consumption):
		# x:100 = consumption : capacity
		percentage = (consumption * 100) / self.capacity
		return percentage

	def percentage_to_consumption(self, percentage):
		# x:100 = consumption : capacity
		consumption = (percentage * self.capacity) / 100
		return consumption

	def distance_to_consumption(self, distance):
		perkm_consumption = self.from_kml_to_lkm()
		tot_consumption = perkm_consumption * distance
		return tot_consumption

	def distance_to_welltotank_emission(self,distance):
		if self.engine_type in ["gasoline", "diesel", "lpg", "cng"]:
			wtt_emissions_perkm = self.welltotank_emission * self.from_kml_to_energyperkm()
		elif self.engine_type == "electric":
			wtt_emissions_perkm = self.welltotank_emission / self.consumption
		tot_wtt_emissions = distance * wtt_emissions_perkm
		return tot_wtt_emissions

	def distance_to_tanktowheel_emission(self,distance):
		if self.engine_type in ["gasoline", "diesel", "lpg", "cng"]:
			ttw_energy_mj = self.distance_to_consumption(distance) * self.energy_content
			tot_ttw_emissions = (ttw_energy_mj / self.lower_heating_value * self.carbon_content / 100 / 12 * 44) * 1000  # gCO2
		elif self.engine_type == "electric":
			tot_ttw_emissions = 0
		return tot_ttw_emissions

# car = Vehicle(example_vehicle_config)
# distance = 130
# cons = car.distance_to_consumption(distance)
# print("Consumption = ", cons)
# print("Cons percentage = ", car.consumption_to_percentage(cons))
# print("Total emission Well to Wheel = ", car.distance_to_emission(distance))
# car.current_percentage -= car.consumption_to_percentage(cons)
# print(car.current_percentage)
# print("Charging time (s) = ",car.get_charging_time_from_perc(35,90))
# print("Charging perc = ", car.get_percentage_from_charging_time(15.119796755911661,35))

