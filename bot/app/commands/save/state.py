from aiogram.fsm.state import State, StatesGroup


class SaveState(StatesGroup):
    # waiting for the user to send the link
    waiting_input_link: State = State()
