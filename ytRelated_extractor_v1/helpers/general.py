from datetime import datetime, timedelta, timezone, date # biblioteca para manipulação de datas

# Função para obter a data completa e o dia da extração:
def get_extraction_date():
    diff = timedelta(hours=-3)

    t_zone = timezone(diff)

    extraction_date = str(datetime.now(tz=t_zone))
    extraction_day = str(date.today())

    return extraction_date, extraction_day