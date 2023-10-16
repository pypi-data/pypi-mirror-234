import calendar

class Calendrier:

    @staticmethod
    def get_days_of_month_formatted(year: int, month: int) -> list:
        _, last_day = calendar.monthrange(year, month)
        return [f'{calendar.day_name[calendar.weekday(year, month, day)][:]} {day:02d} {calendar.month_name[month]} {year}' for day in range(1, last_day + 1)]
