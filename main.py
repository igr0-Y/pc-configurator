from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import get_db
from models import CPU, GPU, RAM, Motherboard, PSU, Cooler, Case, Storage, Build, BuildRAM, BuildStorage, CoolerSocket
from schemas import BuildUpdate, RAMAdd, StorageAdd
from compatibility import check_compatibility, generate_verdict, get_build_rams, get_build_storages, get_cooler_sockets
from sqlalchemy.orm import Session


app = FastAPI()

@app.get("/", include_in_schema=False)
def read_frontend():
    return FileResponse("pcconfigurator_html.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_component_list(model, session, search=None, filters=None):
    query = session.query(model)

    if search:
        query = query.filter(model.name.ilike(f"%{search}%"))

    if filters:
        for field, values in filters.items():
            if values:
                query = query.filter(getattr(model, field).in_(values))

    items = query.all()
    result = []
    for item in items:
        item_dict = item.__dict__.copy()
        item_dict.pop("_sa_instance_state", None)
        result.append(item_dict)
    return result


@app.post("/", summary="Начать новую сборку 🖥️")
def build_create(session: Session = Depends(get_db)):
    new_build = Build()
    session.add(new_build)
    session.commit()
    build_id = new_build.id
    return {"message": "Черновик сборки создан!", "id": build_id}


@app.put("/{build_id}", summary="Изменить сборку 🖥️")
def build_change(build_id: int, build: BuildUpdate, session: Session = Depends(get_db)):
    change_build = session.query(Build).filter(Build.id == build_id).first()
    if change_build:
        update_data = build.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(change_build, field, value)
        session.commit()
        hard_checks, hard_details, soft_details = check_compatibility(change_build, session)
        is_fully_filled = (
            change_build.cpu_id is not None and
            change_build.motherboard_id is not None and
            change_build.gpu_id is not None and
            change_build.psu_id is not None and
            change_build.cooler_id is not None and
            change_build.case_chassis_id is not None and
            len(get_build_rams(change_build, session)) > 0 and
            len(get_build_storages(change_build, session)) > 0
        )

        verdict = generate_verdict(hard_details, soft_details) if is_fully_filled else None
        return {"message": "Изменения приняты!", "hard_checks": hard_checks, "verdict": verdict}
    else:
        return {"message": "Такой сборки нет!"}


@app.delete("/{build_id}", summary="Удалить сборку 🗑️")
def delete_build(build_id: int, session: Session = Depends(get_db)):
    build = session.query(Build).filter(Build.id == build_id).first()
    if build:
        session.delete(build)
        session.commit()
        return {"message": "Удалено! 🗑️"}
    else:
        return {"message": "Такой сборки нет!"}


@app.get("/cpu", summary="Список процессоров")
def get_cpus(
    session: Session = Depends(get_db),
    search: str = None,
    socket: list[str] = Query(None),
    cores: list[str] = Query(None),
    threads: list[int] = Query(None),
    has_integrated_graphics: bool = None
):
    filters = {}
    if socket:
        filters["socket"] = socket
    if cores:
        filters["cores"] = cores
    if threads:
        filters["threads"] = threads
    if has_integrated_graphics is not None:
        filters["has_integrated_graphics"] = [has_integrated_graphics]
    
    
    return get_component_list(CPU, session, search=search, filters=filters)


@app.get("/motherboard", summary="Список материнских плат")
def get_motherboards(
    session: Session = Depends(get_db), 
    search: str = None,
    socket: list[str] = Query(None),
    form_factor: list[str] = Query(None),
    ram_type: list[str] = Query(None),
    m2_slots: list[str] = Query(None),
    sata_slots: list[str] = Query(None)
):
    filters = {}
    if socket:
        filters["socket"] = socket
    if form_factor:
        filters["form_factor"] = form_factor
    if ram_type:
        filters["ram_type"] = ram_type
    if m2_slots:
        filters["m2_slots"] = m2_slots
    if sata_slots:
        filters["sata_slots"] = sata_slots

    return get_component_list(Motherboard, session, search=search, filters=filters)


@app.get("/ram", summary="Список оперативной памяти")
def get_rams(
    session: Session = Depends(get_db),
    search: str = None,
    ram_type: list[str] = Query(None),
    capacity_gb: list[str] = Query(None),
    module_capacity_gb: list[str] = Query(None),
    modules_count: list[str] = Query(None),
    speed_mhz: list[str] = Query(None),
    cas_latency: list[str] = Query(None)
):
    filters = {}
    if ram_type:
        filters["ram_type"] = ram_type
    if capacity_gb:
        filters["capacity_gb"] = capacity_gb
    if module_capacity_gb:
        filters["module_capacity_gb"] = module_capacity_gb
    if modules_count:
        filters["modules_count"] = modules_count
    if speed_mhz:
        filters["speed_mhz"] = speed_mhz
    if cas_latency:
        filters["cas_latency"] = cas_latency
    return get_component_list(RAM, session, search=search, filters=filters)


@app.get("/gpu", summary="Список видеокарт")
def get_gpus(
    session: Session = Depends(get_db),
    search: str = None,
    manufacturer: list[str] = Query(None),
    vram_gb: list[str] = Query(None)
):
    filters = {}
    if manufacturer:
        filters["manufacturer"] = manufacturer
    if vram_gb:
        filters["vram_gb"] = vram_gb
    return get_component_list(GPU, session, search=search, filters=filters)


@app.get("/psu", summary="Список блоков питания")
def get_psus(
    session: Session = Depends(get_db),
    search: str = None,
    wattage: list[str] = Query(None),
    certification: list[str] = Query(None),
    modularity: list[str] = Query(None)
):
    filters = {}
    if wattage:
        filters["wattage"] = wattage
    if certification:
        filters["certification"] = certification
    if modularity:
        filters["modularity"] = modularity
    return get_component_list(PSU, session, search=search, filters=filters)


@app.get("/cooler", summary="Список кулеров")
def get_coolers(
    session: Session = Depends(get_db),
    search: str = None,
    socket: list[str] = Query(None),
    max_tdp: list[str] = Query(None)
):
    query = session.query(Cooler)
    
    if search:
        query = query.filter(Cooler.name.ilike(f"%{search}%"))
    
    if socket:
        query = query.join(CoolerSocket).filter(CoolerSocket.socket.in_(socket))
    
    if max_tdp:
        query = query.filter(Cooler.max_tdp.in_(max_tdp))
    
    items = query.all()
    result = []
    for item in items:
        item_dict = item.__dict__.copy()
        item_dict.pop("_sa_instance_state", None)
        item_dict["compatible_sockets"] = get_cooler_sockets(item.id, session)
        result.append(item_dict)
    return result


@app.get("/case_chassis", summary="Список корпусов")
def get_cases(session: Session = Depends(get_db)):
    return get_component_list(Case, session)


@app.get("/storage", summary="Список накопителей")
def get_storages(session: Session = Depends(get_db)):
    return get_component_list(Storage, session)

@app.post("/{build_id}/add-ram", summary="Добавление оперативки")
def add_ram_to_build(build_id: int, data: RAMAdd, session: Session = Depends(get_db)):
    build = session.query(Build).filter(Build.id == build_id).first()
    if not build:
        return {"message": "Сборка не найдена"}

    new_ram_entry = BuildRAM(build_id=build_id, ram_id=data.ram_id, quantity=data.quantity)
    session.add(new_ram_entry)
    session.commit()
    return {"message": "Оперативка добавлена в сборку", "build_ram_id": new_ram_entry.id}

@app.delete("/{build_id}/remove-ram/{build_ram_id}", summary="Удаленние оперативки")
def remove_ram_from_build(build_id: int, build_ram_id: int, session: Session = Depends(get_db)):
    ram = session.query(BuildRAM).filter(BuildRAM.id == build_ram_id, BuildRAM.build_id == build_id).first()
    if ram:
        session.delete(ram)
        session.commit()
        return {"message": "Удалено! 🗑️"}
    else:
        return{"message": "Такого нет!"}

@app.post("/{build_id}/add-storage", summary="Добавление памяти")
def add_storage_to_build(build_id: int, data: StorageAdd, session: Session = Depends(get_db)):
    build = session.query(Build).filter(Build.id == build_id).first()
    if not build:
        return {"message": "Сборка не найдена"}

    new_storage = BuildStorage(build_id=build_id, storage_id=data.storage_id)
    session.add(new_storage)
    session.commit()
    return {"message": "Память добавлена в сборку", "new_storage": new_storage.id}

@app.delete("/{build_id}/remove-storage/{build_storage_id}", summary="Удаленние памяти")
def remove_storage_from_build(build_id: int, build_storage_id: int, session: Session = Depends(get_db)):
    storage = session.query(BuildStorage).filter(BuildStorage.id == build_storage_id, BuildStorage.build_id == build_id).first()
    if storage:
        session.delete(storage)
        session.commit()
        return {"message": "Удалено! 🗑️"}
    else:
        return{"message": "Такого нет!"}

@app.get("/{build_id}", summary="Показать сборку 🖥️")
def get_build(build_id: int, session: Session = Depends(get_db)):
    build = session.query(Build).filter(Build.id == build_id).first()
    if not build:
        return {"message": "Такой сборки нет!"}
    result = {
        "id": build.id,
        "name_build": build.name_build,
        "cpu_id": build.cpu_id,
        "motherboard_id": build.motherboard_id,
        "gpu_id": build.gpu_id,
        "psu_id": build.psu_id,
        "cooler_id": build.cooler_id,
        "case_chassis_id": build.case_chassis_id,
    }
    return result