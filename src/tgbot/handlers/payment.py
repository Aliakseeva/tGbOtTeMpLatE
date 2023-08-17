from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, \
    CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class TestCallback(CallbackData, prefix='test'):
    is_test: bool


@router.message(Command("pay"))  # ~F.from_user.id.in_(settings.admin_list)
async def cmd_pay(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Оплатить', pay=True))
    builder.add(InlineKeyboardButton(text='Вторая кнопка', callback_data=TestCallback(is_test=True).pack()))
    builder.adjust(1)

    markup = builder.as_markup()

    inv = await message.answer_invoice(
        title=f'Title',
        is_flexible=False,          # True если опции доставки
        currency='rub',
        start_parameter='payment_done',     # Для отображения чека
        payload='payload',                  # Идентификация товара
        description='desc',
        prices=[LabeledPrice(label='name',
                             amount=100000)],
        provider_token='381764678:TEST:64202',
        reply_markup=markup)


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # обработка запроса на платеж
    await pre_checkout_query.answer(ok=True, error_message='Сообщение в случае ошибки')


@router.message(F.content_type.in_({'successful_payment', 'sticker'}))
async def process_successful_payment(message: Message):
    # в случае успешного платежа
    # message.successful_payment
    # SuccessfulPayment(currency='RUB',
    #                   total_amount=100000,
    #                   invoice_payload='payload',
    #                   telegram_payment_charge_id='some_id',
    #                   provider_payment_charge_id='some_id',
    #                   shipping_option_id=None,
    #                   order_info=None)
    pass


@router.callback_query(TestCallback.filter())
async def payment_second_button(callback: CallbackQuery):
    pass
