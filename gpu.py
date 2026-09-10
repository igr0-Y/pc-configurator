from database import Session
from models import CPU

session = Session()

cpu_data = [
    {"name": "Ryzen 9 9950X3D", "socket": "AM5", "power_consumption": 170, "benchmark_score": 70106, "cores": 16, "threads": 32, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 9 9950X", "socket": "AM5", "power_consumption": 170, "benchmark_score": 65718, "cores": 16, "threads": 32, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 9 9900X", "socket": "AM5", "power_consumption": 120, "benchmark_score": 54330, "cores": 12, "threads": 24, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 7 9800X3D", "socket": "AM5", "power_consumption": 120, "benchmark_score": 39938, "cores": 8, "threads": 16, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 7 9700X", "socket": "AM5", "power_consumption": 65, "benchmark_score": 36965, "cores": 8, "threads": 16, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 5 9600X", "socket": "AM5", "power_consumption": 65, "benchmark_score": 30090, "cores": 6, "threads": 12, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 9 7950X3D", "socket": "AM5", "power_consumption": 120, "benchmark_score": 62301, "cores": 16, "threads": 32, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 9 7950X", "socket": "AM5", "power_consumption": 170, "benchmark_score": 62140, "cores": 16, "threads": 32, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 9 7900X", "socket": "AM5", "power_consumption": 170, "benchmark_score": 51234, "cores": 12, "threads": 24, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 7 7800X3D", "socket": "AM5", "power_consumption": 120, "benchmark_score": 34276, "cores": 8, "threads": 16, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 7 7700X", "socket": "AM5", "power_consumption": 105, "benchmark_score": 35494, "cores": 8, "threads": 16, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 5 7600X", "socket": "AM5", "power_consumption": 105, "benchmark_score": 28279, "cores": 6, "threads": 12, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Ryzen 5 7500F", "socket": "AM5", "power_consumption": 65, "benchmark_score": 26535, "cores": 6, "threads": 12, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_am5.png"},
    {"name": "Core i9-14900K", "socket": "LGA1700", "power_consumption": 125, "benchmark_score": 58247, "cores": 24, "threads": 32, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1700.png"},
    {"name": "Core i7-14700K", "socket": "LGA1700", "power_consumption": 125, "benchmark_score": 51952, "cores": 20, "threads": 28, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1700.png"},
    {"name": "Core i5-14600K", "socket": "LGA1700", "power_consumption": 125, "benchmark_score": 38402, "cores": 14, "threads": 20, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1700.png"},
    {"name": "Core i5-13400F", "socket": "LGA1700", "power_consumption": 65, "benchmark_score": 24906, "cores": 10, "threads": 16, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_lga1700.png"},
    {"name": "Core Ultra 9 285K", "socket": "LGA1851", "power_consumption": 125, "benchmark_score": 67263, "cores": 24, "threads": 24, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1851.png"},
    {"name": "Core Ultra 7 265K", "socket": "LGA1851", "power_consumption": 125, "benchmark_score": 58594, "cores": 20, "threads": 20, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1851.png"},
    {"name": "Core Ultra 5 245K", "socket": "LGA1851", "power_consumption": 125, "benchmark_score": 43051, "cores": 14, "threads": 14, "has_integrated_graphics": True, "icon_path": "/static/icons/cpu_lga1851.png"},
    {"name": "Ryzen 9 5950X", "socket": "AM4", "power_consumption": 105, "benchmark_score": 45267, "cores": 16, "threads": 32, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_am4.png"},
    {"name": "Ryzen 7 5800X3D", "socket": "AM4", "power_consumption": 105, "benchmark_score": 28288, "cores": 8, "threads": 16, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_am4.png"},
    {"name": "Ryzen 7 5700X", "socket": "AM4", "power_consumption": 65, "benchmark_score": 26563, "cores": 8, "threads": 16, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_am4.png"},
    {"name": "Ryzen 5 5600X", "socket": "AM4", "power_consumption": 65, "benchmark_score": 24000, "cores": 6, "threads": 12, "has_integrated_graphics": False, "icon_path": "/static/icons/cpu_am4.png"},
]

for cpu in cpu_data:
    new_cpu = CPU(**cpu)
    session.add(new_cpu)
    print(f"Добавлено: {cpu['name']}")

session.commit()
session.close()