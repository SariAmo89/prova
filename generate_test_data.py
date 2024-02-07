from backend.config import app,db,Pflanze

app.app_context().push()

pflanze = Pflanze(
    name = 'Schweigrohr',
    wissenschaft_name = 'Dieffenbachia',
    familie = 'Aronstabgewächse',
    vegetationszone = 'Tropen',
    will_sonne = 'hell',
    gefahr = 'kann Hautreizungen oder Vergiftungen verursachen'
)
db.session.add(pflanze)
db.session.commit()