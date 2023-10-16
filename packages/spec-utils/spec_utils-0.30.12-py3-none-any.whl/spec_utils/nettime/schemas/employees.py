from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
from .base import Base


class BlockMinute(BaseModel):
    start: Optional[int]
    end: Optional[int]


class Block(BaseModel):
    id: int
    color: Optional[str]
    type: int
    minutes: Optional[List[BlockMinute]] = Field(alias="Minutos")


class Present(BaseModel):
    today: Optional[bool] = Field(alias="Today")
    blocks: Optional[List[Block]] = Field(alias="Bloques")


class DepartmentValidity(BaseModel):
    start_date: Optional[datetime] = Field(alias="StartDate")
    end_date: Optional[datetime] = Field(alias="EndDate")


class EmployeeDepartment(BaseModel):
    element: int = Field(alias="Elemento")
    validity: Optional[List[DepartmentValidity]] = Field(alias="Validez")


class Employee(Base):

    last_name: Optional[str] = Field(alias="LastName")
    name_employee: Optional[str] = Field(alias="nameEmployee")
    no_attendance: Optional[bool] = Field(alias="NoAttendance")
    fingers_quantity: Optional[int] = Field(alias="NumFingers")

    # TODO: split by ; char
    timetypes: Optional[str] = Field(alias="TimeTypesEmployee")

    readers: Optional[List[int]] = Field(alias="Readers")
    town: Optional[str] = Field(alias="Town")
    province: Optional[str] = Field(alias="Province")
    postal_code: Optional[str] = Field(alias="PostalCode")

    birth_date: Optional[datetime] = Field(alias="birthdate")
    register_system_date: Optional[datetime] = Field(alias="RegisterSystemDate")
    
    # TODO: Check to edit with periods
    active_days: Optional[str] = Field(
        alias="ActiveDays",
        description="Antiquity"
    )
    activedays: Optional[str] = Field(alias="Persona.DiasActivos")
    
    employee_departments: Optional[List[EmployeeDepartment]] = Field(
        alias="Departments"
    )

    calendar: Optional[int] = Field(alias="Calendar")
    portal_not_validation_required: Optional[bool] = Field(alias="Portal....")
    portal_can_not_edit: Optional[bool] = Field(alias="Portal.NoPuedeEditar")
    portal_can_use: Optional[bool] = Field(alias="Portal.UsaPortal")
    portal_results_template: Optional[int] = Field(
        alias="Portal.PlantillaResultados"
    )
    portal_disable_movs: Optional[bool] = Field(
        alias="Portal.DisableMovimientos"
    )
    portal_disable_resume_view: Optional[bool] = Field(
        alias="Portal.DisableVistaResumen"
    )

    present: Optional[Present] = Field(alias="Persona.Presente")
    is_present: Optional[bool] = Field(alias="IsPresent")
    departments: Optional[str] = Field(alias="Persona.Departaments")
    photo: Optional[str] = Field(alias="Photo")
    clockings: Optional[str] = Field(alias="Persona.Clockings")
    dni_name_lastname: Optional[str] = Field(alias="DNI_Apellidos_Nombre")
    name_lastname: Optional[str] = Field(alias="Apellidos_Nombre")
    anomaly: Optional[str] = Field(alias="Persona.Anomalia")
    shift: Optional[str] = Field(alias="Persona.Jornada")
    effective_calendar: Optional[str] = Field(alias="Persona.Calendario")
    base_calendar: Optional[str] = Field(alias="Persona.CalendarioBase")
    is_active: Optional[bool] = Field(alias="Persona.DeAlta")
    id_enroll: Optional[int] = Field(alias="idEnroll")
    enroll_active: Optional[int] = Field(alias="enrollActive")
    access_current_zone: Optional[int] = Field(alias="Accesos.Zona")
    access_profiles: Optional[str] = Field(alias="Accesos.Perfiles")
    phone: Optional[str] = Field(alias="Phone")
    cards: Optional[str] = Field(alias="Persona.Cards")

    employee_code: Optional[str] = Field(alias="employeeCode")
    company_code: Optional[str] = Field(alias="companyCode")
    professional_mobile: Optional[str] = Field(alias="Mobile")
    personal_phone: Optional[str] = Field(alias="PersonalPhone")
    personal_mobile: Optional[str] = Field(alias="PersonalMobile")

    weekly_theoretical_hours: Optional[int] = Field(
        alias="Persona.HorasTeoricasSemanales"
    )
    tree_node: Optional[str] = Field(alias="nodoArbol")
    nif: Optional[str] = Field(alias="nif")
    last_clocking: Optional[str] = Field(alias="LastMarcaje")
    last_clocking_reader: Optional[str] = Field(alias="LastMarcajeReader")
    exboss: Optional[bool] = Field(description="Assigned to me")
    managers: Optional[str] = Field(alias="Persona.ManagersAction")
    time_readers: Optional[str] = Field(alias="Persona.ValidReaders")
    today_planning: Optional[str] = Field(alias="Persona.PlanisToday")
    current_status: Optional[str] = Field(alias="CurrentStatus")
    current_status_wa: Optional[str] = Field(alias="CurrentStatusWA")
    current_status_wo: Optional[str] = Field(alias="CurrentStatusWO")
    first_day_clocking: Optional[str] = Field(alias="Persona.FirstClocking")
    last_day_clocking: Optional[str] = Field(alias="Persona.LastClocking")
    
    bio_data_enrolled: Optional[str] = Field(alias="Persona.BioDataEnrolled")
    total_docs: Optional[int] = Field(alias="Persona.totalDocs")

    use_remote_clocking: Optional[bool] = Field(alias="RemoteClocking")
    use_mobile_clocking: Optional[bool] = Field(alias="MobileClocking")
    mobile_id: Optional[str] = Field(alias="mobileId")
    proface_admin: Optional[bool] = Field(alias="ProfaceAdmin")

