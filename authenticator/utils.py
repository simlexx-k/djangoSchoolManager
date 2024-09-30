from datetime import timedelta
from administrator.models import Term, WeekSchedule

def generate_weeks_for_term(term):
    current_date = term.start_date
    week_number = 1
    while current_date <= term.end_date:
        end_date = min(current_date + timedelta(days=6), term.end_date)
        WeekSchedule.objects.get_or_create(
            term=term,
            week_number=week_number,
            defaults={
                'start_date': current_date,
                'end_date': end_date
            }
        )
        current_date = end_date + timedelta(days=1)
        week_number += 1
