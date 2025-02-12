####  Online banking (alif mobi) - PulNest
Описание: онлайн кошелек

#### Сущности
1. Пользователи users:
id int primary key 
email string unique
password string 
phone_number int unique
birth_date timestamp
fullname string
is_identified boolean 
created_at timestamp
updated_at timestamp
deleted_at timestamp

2. Кошельки wallets
id int primary key
user_id foreign key
balance float
created_at timestamp
updated_at timestamp
deleted_at timestamp
 
3. Карты cards
id int primary key
user_id foreign key
pan_number int unique
balance float 
expire_date timestamp
cvv int 
card_holder_name string
created_at timestamp
updated_at timestamp
deleted_at timestamp


4. Транзакции transactions
id int primary key
tran_type_id int foreign key
source_id int foreign key
destination_id int foreign key
amount float
currency default tjs


5. Тип транзакции transaction_types
id int primary key
tran_type int primary key
created_at timestamp
updated_at timestamp
deleted_at timestamp






#### Основной функционал:
Регистрация и авторизация
1. Регистрация по номеру телефона или email.
2. Подтверждение через Email.
3. Вход с паролем или PIN-кодом.

Баланс и управление средствами
1. Отображение текущего баланса.
2. История транзакций (дата, сумма, описание).
3. Пополнение баланса(через карту, перевод от другого пользователя).
4. Вывод средств(на банковскую карту или другой кошелёк).



Переводы между пользователями
1. Отправка денег по номеру телефона.

Оплата услуг
1. Оплата мобильной связи, интернета, ЖКХ.
2. Возможность настроить автоплатежи.

Дополнительные функции
1. Кэшбэк или бонусы за переводы и оплаты.
2. Категоризация расходов(еда, транспорт, развлечения).
3. Аналитика расходов за месяц.

Optional:
- Возможность запроса выписка за определнный период (в формате pdf)
- Возможность добавить комментарий к переводу.
- Запрос денег у другого пользователя.
- Оплата по QR
- Интеграция с AA.EDU



Стек: python, postgres, sqlAlchemy, jwt, fastAPI, swagger 2.0 or 3.0

##### Участники команды:
- Нуритдинов Фаррух
- Есипов Денис
- Бектошев Ислом
- Миркосимова Манижа
- Эргашев Хуршед
- Ганизода Сулаймон
- Ниезова Мехрона
- Джамшедзода Шохрух
- Хамроев Доро
- Бахшиев Муртазо
- Наврузов Фариддун