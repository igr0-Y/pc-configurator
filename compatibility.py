from models import CPU, GPU, RAM, Motherboard, PSU, Cooler, Case, Storage, BuildRAM, BuildStorage, CoolerSocket

# ====================================================== Жесткие проверки ====================================================== #

def cpu_integrated_graphics_check(has_integrated_graphics, gpu_selected): # Проверка встроенной графики у процессора
    if not has_integrated_graphics and not gpu_selected:
        long_text = "У процессора нет встроенной графики — без видеокарты изображение не выведется"
        return "🔴 Требуется видеокарта", long_text
    return None

def cpu_motherboard(cpu_socket, motherboard_socket): # Проверка совместимости сокета процессора и материнской платы
    if cpu_socket == motherboard_socket:
        return ("🟢 Совместимо с материнской платой", None), ("🟢 Совместимо с процессором", None)
    else:
        long_text = "Сокет процессора несовместим с сокетом материнской платы."
        return ("🔴 Не совместимо с материнской платой", long_text), ("🔴 Не совместимо с процессором", None)

def get_cooler_sockets(cooler_id, session): # Получение списка сокетов кулеров
    sockets = session.query(CoolerSocket).filter(CoolerSocket.cooler_id == cooler_id).all()
    return [s.socket for s in sockets]

def compatibility_cooler_cpu(cpu_socket, cooler_compatible_sockets): # Проверка совместимости сокета процессора и кулера
    if cpu_socket in cooler_compatible_sockets:
        return ("🟢 Совместимо с кулером", None), ("🟢 Совместимо с процессором", None)
    else:
        long_text = "Сокет кулера не подходит под процессор."
        return ("🔴 Не совместимо с кулером", long_text), ("🔴 Не совместимо с процессором", None)

def compatibility_cooling_cpu(cpu_power_consumption, cooler_max_tdp): # Проверка достаточности охлаждения процессора кулером
    if cpu_power_consumption < cooler_max_tdp:
        return ("🟢 Охлаждения достаточно", None), ("🟢 Достаточно для процессора", None)
    else:
        long_text = "Охлаждения от кулера недостаточно, процессор будет идти на износ."
        return ("🔴 Охлаждения недостаточно", long_text), ("🔴 Недостаточно для процессора", None)

def gpu_case_capacity(gpu_length_mm, case_max_gpu_length_mm): # Проверка вместимости видеокарты в корпус
    if gpu_length_mm < case_max_gpu_length_mm:
        return ("🟢 Спокойно влезет в корпус", None), ("🟢 Совместимо с видеокартой", None)
    else:
        long_text = "Видеокарта физически не поместится в корпус"
        return ("🔴 Не влезет в корпус", long_text), ("🔴 Не совместимо с видеокартой", None)

def psu_compatibility(cpu_power_consumption, gpu_power_consumption, psu_wattage): # Проверка совместимости мощности блока питания 
    if cpu_power_consumption + gpu_power_consumption + 150 < psu_wattage:
        return "🟢 Совместимо", None
    else:
        return "🔴 Не совместимо", "Мощности блока питания недостаточно для этой связки процессора и видеокарты, рекомендуется выбрать более мощный блок питания."

def motherboard_case_form_factor(motherboard_form_factor, case_form_factor): # Проверка вместимости материнской платы в корпус
    FORM_FACTOR_SIZES = {"ATX": 3, "mATX": 2, "ITX": 1}
    mb_size = FORM_FACTOR_SIZES.get(motherboard_form_factor, 0)
    case_size = FORM_FACTOR_SIZES.get(case_form_factor, 0)
    if mb_size <= case_size:
        return ("🟢 Совместимо с корпусом", None), ("🟢 Совместимо с материнской платой", None)
    else:
        long_text = "Материнская плата не поместится в этот корпус, нужен корпус побольше или материнка поменьше."
        return ("🔴 Не совместимо с корпусом", long_text), ("🔴 Не совместимо с материнской платой", None)

def ram_motherboard_type(ram_type, motherboard_ram_type): # Проверка совместимости оперативной памяти с материнской платой
    if ram_type == motherboard_ram_type:
        return ("🟢 Совместимо с материнской платой", None), ("🟢 Совместимо с оперативной памятью", None)
    else:
        long_text = "Тип оперативной памяти не подходит к материнской плате."
        return ("🔴 Не совместимо с материнской платой", long_text), ("🔴 Не совместимо с оперативной памятью", None)

def ram_slots(total_modules, motherboard_ram_slots): # Проверка слотов RAM
    if total_modules <= motherboard_ram_slots:
        return f"🟢 В пределах нормы ({total_modules}/{motherboard_ram_slots})", None
    else:
        return "🔴 Превышено количество слотов", f"Выбрано {total_modules} модулей RAM, а слотов на материнке только {motherboard_ram_slots}, лишние модули некуда ставить."

def storage_slots(m2_count, sata_count, motherboard_m2_slots, motherboard_sata_slots): # Проверка слотов памяти
    if m2_count <= motherboard_m2_slots and sata_count <= motherboard_sata_slots:
        return "🟢 В пределах нормы", None
    else:
        return "🔴 Превышено количество слотов", "Выбрано больше накопителей, чем слотов на материнке, часть накопителей физически некуда подключить."
    
# ============================================================================================================================== #

# ====================================================== Мягкие проверки ======================================================= #

def cpu_score(cpu_score): # Процент мощности процессора
    CPU_MAX_SCORE = 70106
    cpu_percent = cpu_score / CPU_MAX_SCORE * 100
    return cpu_percent

def gpu_score(gpu_score): # Процент мощности видеокарты 
    GPU_MAX_SCORE = 38970
    gpu_percent = gpu_score / GPU_MAX_SCORE * 100
    return gpu_percent

def balance_cpu_gpu(cpu_percent, gpu_percent): # Проверка баланса процессора и видеокарты между собой
    difference = abs(cpu_percent - gpu_percent)
    if 0 <= difference <= 15:
        return None
    elif 15 < difference <= 30:
        if cpu_percent > gpu_percent:
            return "Легкий дисбаланс мощности процессора по отношению к видеокарте, это почти никак не влияет, но мощность процессора не будет полностью раскрыта."
        else:
            return "Легкий дисбаланс мощности видеокарты по отношению к процессору, это почти никак не влияет, но мощность видеокарты не будет полностью раскрыта."
    else:
        if cpu_percent > gpu_percent:
            return "Сильный дисбаланс мощности процессора по отношению к видеокарте. Процессор почти не раскроет свой потенциал, нужно поменять видеокарту на более мощную или выбрать процессор послабее."
        else:
            return "Сильный дисбаланс мощности видеокарты по отношению к процессору. Видеокарта почти не раскроет свой потенциал, нужно поменять процессор на более мощный или выбрать видеокарту послабее."

def balance_vram_gpu(gpu_vram_gb, gpu_percent): # Проверка баланса VRAM по соотношению мощности видеокарты
    if gpu_vram_gb < 8:
        return "Небольшой объём видеопамяти — для большинства игр этого достаточно, но в требовательных проектах на высоких настройках может не хватить."
    elif gpu_vram_gb > 12 and gpu_percent < 50:
        return "Слишком много видеопамяти для такой видеокарты, большинство памяти просто не будет использоваться, рекомендуется поменять видеокарту с более меньшим количеством VRAM."
    else:
        return None

def ram_capacity(total_capacity_gb): # Проверка количетсва оперативной памяти
    if total_capacity_gb < 16:
        return "Маловато оперативной памяти, рекомендуется от 16 ГБ для современных задач."
    return None

def ram_motherboard_speed(ram_speed_mhz, motherboard_max_speed): # Проверка поддерживаемой скорости материнской платы и оперативной памяти
    if ram_speed_mhz > motherboard_max_speed:
        return "Материнка не поддерживает такую частоту памяти, работать будет медленнее заявленной скорости."
    return None

def latency_ram(speed_mhz, cas_latency): # Проверка задержки оперативной памяти
    true_latency_ns = (cas_latency / (speed_mhz / 2)) * 1000
    if true_latency_ns <= 10:
        return None
    elif true_latency_ns <= 13:
        return "Средняя задержка оперативной памяти, не критично, но есть варианты быстрее."
    else:
        return "Высокая реальная задержка памяти, несмотря на частоту работать будет ощутимо медленнее аналогов с лучшими таймингами."

def ram_dual_channel(total_modules): # Проверка двухканального режима оперативной памяти
    if total_modules == 1:
        return "Один модуль оперативной памяти не позволяет использовать двухканальный режим, рекомендуется взять два модуля меньшего объёма вместо одного большого — скорость работы памяти заметно вырастет."
    return None

def storage_type(storage_types): # Проверка памяти
    if "NVMe" in storage_types:
        return None
    return "Рекомендуется добавить NVMe для системы, загрузка будет заметно быстрее."    

# ============================================================================================================================== #

def get_build_rams(build, session):
    build_rams = session.query(BuildRAM).filter(BuildRAM.build_id == build.id).all()
    result = []
    for br in build_rams:
        ram = session.query(RAM).filter(RAM.id == br.ram_id).first()
        result.append({"ram": ram, "quantity": br.quantity})
    return result


def get_build_storages(build, session):
    build_storages = session.query(BuildStorage).filter(BuildStorage.build_id == build.id).all()
    result = []
    for bs in build_storages:
        storage = session.query(Storage).filter(Storage.id == bs.storage_id).first()
        result.append(storage)
    return result

def save_hard_check(key, result, hard_checks, hard_details):
    short, long = result
    hard_checks[key] = short
    if long:
        hard_details[key] = long

def save_soft_check(key, text, soft_details):
    if text:
        soft_details[key] = text

def check_compatibility(build, session):
    hard_checks = {}
    hard_details = {}
    soft_details = {}

    cpu = session.query(CPU).filter(CPU.id == build.cpu_id).first()
    gpu = session.query(GPU).filter(GPU.id == build.gpu_id).first()
    motherboard = session.query(Motherboard).filter(Motherboard.id == build.motherboard_id).first()
    psu = session.query(PSU).filter(PSU.id == build.psu_id).first()
    cooler = session.query(Cooler).filter(Cooler.id == build.cooler_id).first()
    case = session.query(Case).filter(Case.id == build.case_chassis_id).first()

# ====================================================== Жесткие проверки ====================================================== #

    if build.cpu_id is not None: # Проверка встроенной графики у процессора
        result = (cpu_integrated_graphics_check(cpu.has_integrated_graphics, build.gpu_id is not None))
        if result:
            save_hard_check("cpu_integrated_graphics_check", result, hard_checks, hard_details)
    
    if build.cpu_id is not None and build.motherboard_id is not None: # Проверка совместимости сокета процессора и материнской платы
        cpu_side, mb_side = cpu_motherboard(cpu.socket, motherboard.socket)
        save_hard_check("cpu_socket_vs_motherboard", cpu_side, hard_checks, hard_details)
        save_hard_check("motherboard_socket_vs_cpu", mb_side, hard_checks, hard_details)

    if build.cpu_id is not None and build.cooler_id is not None:
        cooler_sockets = get_cooler_sockets(cooler.id, session) # Получаем список сокетов кулера из новой таблицы
        cpu_side, cooler_side = compatibility_cooler_cpu(cpu.socket, cooler_sockets) # Проверка совместимости сокета процессора и кулера
        save_hard_check("cpu_socket_vs_cooler", cpu_side, hard_checks, hard_details)
        save_hard_check("cooler_socket_vs_cpu", cooler_side, hard_checks, hard_details)

        cpu_side, cooler_side = compatibility_cooling_cpu(cpu.power_consumption, cooler.max_tdp) # Проверка достаточности охлаждения процессора кулером
        save_hard_check("cpu_cooling_check", cpu_side, hard_checks, hard_details)
        save_hard_check("cooler_cooling_check", cooler_side, hard_checks, hard_details)

    if build.case_chassis_id is not None and build.gpu_id is not None: # Проверка вместимости видеокарты в корпус
        gpu_side, case_side = gpu_case_capacity(gpu.length_mm, case.max_gpu_length_mm)
        save_hard_check("gpu_case_check", gpu_side, hard_checks, hard_details)
        save_hard_check("case_gpu_check", case_side, hard_checks, hard_details)

    if build.cpu_id is not None and build.gpu_id is not None and build.psu_id is not None: # Проверка совместимости мощности блока питания
        save_hard_check("psu_compatibility", psu_compatibility(cpu.power_consumption, gpu.power_consumption, psu.wattage), hard_checks, hard_details)

    if build.motherboard_id is not None and build.case_chassis_id is not None: # Проверка вместимости материнской платы в корпус
        mb_side, case_side = motherboard_case_form_factor(motherboard.form_factor, case.form_factor)
        save_hard_check("motherboard_case_check", mb_side, hard_checks, hard_details)
        save_hard_check("case_motherboard_check", case_side, hard_checks, hard_details)

    build_rams = get_build_rams(build, session)
    if len(build_rams) > 0 and build.motherboard_id is not None:
        first_ram = build_rams[0]["ram"]
        total_modules = sum(item["quantity"] for item in build_rams)
        ram_side, mb_side = ram_motherboard_type(first_ram.ram_type, motherboard.ram_type) # Проверка совместимости оперативной памяти с материнской платой
        save_hard_check("ram_type_check", ram_side, hard_checks, hard_details)
        save_hard_check("motherboard_ram_check", mb_side, hard_checks, hard_details)
        save_hard_check("ram_slots", ram_slots(total_modules, motherboard.ram_slots), hard_checks, hard_details) # Проверка слотов RAM

    build_storages = get_build_storages(build, session)
    if len(build_storages) > 0 and build.motherboard_id is not None:
        m2_count = sum(1 for s in build_storages if s.interface == "M.2")
        sata_count = sum(1 for s in build_storages if s.interface == "SATA")
        save_hard_check("storage_slots", storage_slots(m2_count, sata_count, motherboard.m2_slots, motherboard.sata_slots), hard_checks, hard_details) # Проверка слотов памяти

# ============================================================================================================================== #

# ====================================================== Мягкие проверки ======================================================= #

    if build.cpu_id is not None and build.gpu_id is not None: # Проверка баланса процессора и видеокарты между собой
        save_soft_check("balance_cpu_gpu", balance_cpu_gpu(cpu_score(cpu.benchmark_score), gpu_score(gpu.benchmark_score)), soft_details)

    if build.gpu_id is not None: # Проверка баланса VRAM по соотношению мощности видеокарты
        save_soft_check("balance_vram_gpu", balance_vram_gpu(gpu.vram_gb, gpu_score(gpu.benchmark_score)), soft_details)

    if len(build_rams) > 0:
        first_ram = build_rams[0]["ram"]
        total_capacity = sum(item["ram"].capacity_gb * item["quantity"] for item in build_rams)
        save_soft_check("ram_capacity", ram_capacity(total_capacity), soft_details) # Проверка количетсва оперативной памяти
        save_soft_check("latency_ram", latency_ram(first_ram.speed_mhz, first_ram.cas_latency), soft_details) # Проверка задержки оперативной памяти
        if build.motherboard_id is not None:
            save_soft_check("ram_motherboard_speed", ram_motherboard_speed(first_ram.speed_mhz, motherboard.max_ram_speed), soft_details) # Проверка поддерживаемой скорости материнской платы и оперативной памяти
            save_soft_check("ram_dual_channel", ram_dual_channel(total_modules), soft_details) # Проверка двухканального режима оперативной памяти

    if len(build_storages) > 0: # Проверка SSD
        save_soft_check("storage_type", storage_type([s.type for s in build_storages]), soft_details)


# ============================================================================================================================== #
    

    return hard_checks, hard_details, soft_details

def generate_verdict(hard_details, soft_details):
    parts = []

    if hard_details:
        parts.append("⚠️ Сначала обрати внимание: " + " ".join(hard_details.values()))

    if soft_details:
        parts.append("Помимо этого: " + " ".join(soft_details.values()))
    elif not hard_details:
        parts.append("🏆 Отличная сборка! Все компоненты хорошо сочетаются между собой.")

    return " ".join(parts)