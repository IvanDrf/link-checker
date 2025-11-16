from aiogram.fsm.state import State, StatesGroup


class CsvState(StatesGroup):
    # waiting for user to exit from check state
    waiting_for_exit: State = State()
