from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    dream = State()
    test = State()
    problems = State()
    promise = State()
    input_contact=State()
    input_cancel=State()
    add_service=State()
    input_new_service = State()
    input_service_to_remove = State()

