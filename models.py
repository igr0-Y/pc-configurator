from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ComponentBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String)
    icon_path = Column(String)


class CPU(ComponentBase):
    __tablename__ = "cpu"
    socket = Column(String)
    power_consumption = Column(Integer)
    benchmark_score = Column(Integer)
    cores = Column(Integer)
    threads = Column(Integer)
    has_integrated_graphics = Column(Boolean)

class GPU(ComponentBase):
    __tablename__ = "gpu"
    manufacturer = Column(String)
    power_consumption = Column(Integer)
    benchmark_score = Column(Integer)
    vram_gb = Column(Integer)
    length_mm = Column(Integer)
    suggested_psu = Column(Integer)


class RAM(ComponentBase):
    __tablename__ = "ram"
    ram_type = Column(String)
    capacity_gb = Column(Integer)
    module_capacity_gb = Column(Integer)
    modules_count = Column(Integer)
    speed_mhz = Column(Integer)
    cas_latency = Column(Integer)


class Motherboard(ComponentBase):
    __tablename__ = "motherboard"
    socket = Column(String)
    ram_type = Column(String)
    max_ram_speed = Column(Integer)
    form_factor = Column(String)
    ram_slots = Column(Integer)
    m2_slots = Column(Integer)
    sata_slots = Column(Integer)
    vrm_phases = Column(Integer)

class PSU(ComponentBase):
    __tablename__ = "psu"
    wattage = Column(Integer)
    certification = Column(String)
    modularity = Column(String)


class Cooler(ComponentBase):
    __tablename__ = "cooler"
    max_tdp = Column(Integer)


class Case(ComponentBase):
    __tablename__ = "case_chassis"
    form_factor = Column(String)
    max_gpu_length_mm = Column(Integer)


class Storage(ComponentBase):
    __tablename__ = "storage"
    type = Column(String)
    capacity_gb = Column(Integer)
    interface = Column(String)
    read_speed_mbps = Column(Integer)

class Build(Base):
    __tablename__ = "build"
    id = Column(Integer, primary_key=True)
    name_build = Column(String)
    cpu_id = Column(Integer, ForeignKey("cpu.id"))
    motherboard_id = Column(Integer, ForeignKey("motherboard.id"))
    gpu_id = Column(Integer, ForeignKey("gpu.id"))
    psu_id = Column(Integer, ForeignKey("psu.id"))
    cooler_id = Column(Integer, ForeignKey("cooler.id"))
    case_chassis_id = Column(Integer, ForeignKey("case_chassis.id"))

class BuildRAM(Base):
    __tablename__ = "build_ram"
    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey("build.id"))
    ram_id = Column(Integer, ForeignKey("ram.id"))
    quantity = Column(Integer, default=1)


class BuildStorage(Base):
    __tablename__ = "build_storage"
    id = Column(Integer, primary_key=True)
    build_id = Column(Integer, ForeignKey("build.id"))
    storage_id = Column(Integer, ForeignKey("storage.id"))

class CoolerSocket(Base):
    __tablename__ = "cooler_socket"
    id = Column(Integer, primary_key=True)
    cooler_id = Column(Integer, ForeignKey("cooler.id"))
    socket = Column(String)    

