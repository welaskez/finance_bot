from database import Database

db = Database()


def get_today_wastes_msg():
    today_wastes, total_today_wastes = db.get_today_wastes()
    msg = ""
    for category, amount in today_wastes.items():
        msg += f'\n{category} - {amount} тг'

    msg += f'\n\nВсего трат за сегодня: {total_today_wastes} тг'
    return msg


