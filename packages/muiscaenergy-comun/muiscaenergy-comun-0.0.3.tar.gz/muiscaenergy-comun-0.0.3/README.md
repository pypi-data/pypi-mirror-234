# muiscaenergy-comun
Common functions for Muisca energy projects


## Time Series

Example usage:
    from datetime import datetime
    from muiscaenergy_common.src.timeseries.base import get_timeseries


    ts_from = datetime(2023, 9, 30, 12, 0, 0)
    ts_to = datetime(2023, 10, 1, 11, 0, 0)
    freq = 'H'
    lat = 52.5200
    lon = 13.4050
    tz = 'America/Los_Angeles'

    # Get a TimeSeriesMessage object without notion of location
    ts1 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq)
    print(ts1.df)

    # Get a TimeSeriesMessage object with notion of location via lat and lon
    ts2 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq,
                     lat=lat,
                     lon=lon)
    print(ts2.df)

    # Get a TimeSeriesMessage object with notion of location via tz (timezone)
    ts3 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq,
                     tz=tz)
    print(ts3.df)



Pasos
1. Crear un nuevo repositorio en github
2. Clonar el repositorio en local
3. Crear un nuevo proyecto en Pycharm
4. Crear un nuevo entorno virtual en Pycharm

Gitiignore
1. abra el archivo .gitignore 
2. comente la linea con (*.egg-info/)... en mi version es liena 24

Pasos para crear un paquete
1. agregar nuevo folder con src (python directory) y otro ocn test (python directory)
2. crear los archivos de folder

Pasos para subir el paquete a pypi
1. crear el archivo setup.py 
2. python setup.py sdist bdist_wheel --> creates egg, build, dist
3. commit and push to github
4. 'pip install twine' if not installed
5. twine check dist/* --> check if the package is ok
6. twine upload dist/* --> upload to pypi
7. (alternativa) twine upload dist/muiscaenergy-comun-0.0.2.tar.gz*


