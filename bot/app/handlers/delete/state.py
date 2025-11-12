from aiogram.fsm.state import State, StatesGroup


class DeleteState(StatesGroup):
    # waiting for the user to delete the link
    waiting_input_link: State = State()
