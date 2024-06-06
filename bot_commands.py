from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states import Form
import json


router = Router()
i = 0
right = 0

test = []


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    global i, test
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    test = data['test']
    await message.reply(f'Привет, давай пройдём тест на знание дат по истории, он состоит из {len(test)} вопросов')
    await message.reply(test[i]['question'])
    await state.set_state(Form.test_going)


@router.message(Command('stop'))
async def stop(message: Message, state: FSMContext):
    await message.reply(f'Всего доброго! Если хотите пройти тест заново, то нажмите /start')
    await state.set_state()
    i = 0
    right = 0


@router.message(Form.test_going)
async def start(message: Message, state: FSMContext):
    global i, right
    if message.text == test[i]['response']:
        right += 1
        i += 1
    if i < len(test):
        await message.reply(test[i]['question'])
    else:
        await message.reply(f'Молодец! Ты прошёл тест, ты ответил на {right} из {len(test)} вопросов')
        await message.reply(f'Если хочешь пройти тест ещё раз, нажми /start')
        await state.set_state()
        i = 0
        right = 0