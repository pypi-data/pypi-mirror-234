class DataStructures:
    class Users:
        account = {
            "username": None,
            "password": None,
            "first_name": None,
            "last_name": None
        }  # user name

        workshop = {
            "username": None,
            "workshop_name": None,
            "next_ids": {
                "printer": 0,
                "filament": 0
            },
            "stations": [],
            "controllers": [],
            "printers": [],
            "filament_changers": [],
            "filaments": []
        }  # workshop name

    class Devices:
        station = {
            "username": None,  # str
            "workshop_name": None,  # str
            "station_name": None,  # str
            "device_id": None,  # str(int)
            "machine_version": None,  # str
            "firmware_version": None,  # str
            "capacity": None,  # str(int)  # max amount of controllers
            "filament_changers": []  # ids of the filament changers
        }  # station name

        controller = {
            "username": None,  # str
            "workshop_name": None,  # str
            # "controller_name": None,  # str
            "device_id": None,  # str(int)
            "printer": None,  # str(int)  # printer id
            "bed": None,  # str(int)
            "filament_link": [None, None, None]  # [id of the filament changer, id of the channel, id of the filament]
        }

        filament_changer = {
            "username": None,  # str
            "workshop_name": None,  # str
            # "filament_changer_name": None,  # str
            "device_id": None,  # str(int)
            "capacity": None,  # str(int)  # max amount of channels
            "min_temp": None,  # str(int)
            "max_temp": None,  # str(int)
            "channels": {}
        }  # ids of the channels: ids of the filaments

        printer = {
            "username": None,  # str
            "workshop_name": None,  # str
            "printer_name": None,  # str
            "device_id": None,  # str(int)
            "model": None,  # str
            "manufacturer": None,  # str
            "firmware": None,  # str
            "bitrate": None,  # str(int)
            "build_size": [
                None,  # str(float)
                None,  # str(float)
                None  # str(float)
            ],
            "nozzle_diameter": None,  # str(float)
            "head_max_temp": None,  # str(int)
            "bed_max_temp": None,  # str(int)  # None/0 if there is no bed
            "min_layer_height": None,  # str(float)  # mm
            "max_layer_height": None,  # str(float)  # mm
            "max_velocity": [
                None,  # str(float)
                None,  # str(float)
                None  # str(float)
            ],
            "max_print_velocity": [
                None,  # str(float)
                None,  # str(float)
                None  # str(float)
            ],  # recommended
            "max_acceleration": [
                None,  # str(float)
                None,  # str(float)
                None  # str(float)
            ],
            "statistics": {
                "entire_life": None,  # str(float)  # hours
                "print_life_total": None,  # str(float)  # hours
                "print_life_success": None,  # str(float)  # hours
                "print_life_failure": None,  # str(float)  # hours
                "prints_total": None,  # str(int)
                "prints_success": None,  # str(int)
                "prints_failure": None,  # str(int)
            }
        }

        filament = {
            "id": None,  # str(int)
            "material": None,  # str
            "color": None,  # str  # color
            "min_temp": None,  # str(int)
            "max_temp": None,  # str(int)
            "opacity": None,  # str(float)  # 0 < x < 100
            "diameter": None,  # str(float)  # mm
            "density": None,  # str(float)  # g/cm^3
            "initial_weight": None,  # str(float)  # g
            "initial_length": None,  # str(float)  # mm
            "spool_weight": None,  # str(float)  # g
            "current_weight": None,  # str(float)  # g
            "current_length": None,  # str(float)  # mm
            "currency": None,  # str(float)  # $/g
        }
