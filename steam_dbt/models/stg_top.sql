select
    cast(date_collecte as date) as date_collecte,
    rang,
    rang_semaine_derniere,
    appid,
    nom,
    gratuit,
    case when gratuit then 0 else prix_eur end as prix_eur,
    reduction_pct,
    genres,
    pic_joueurs
from {{ source('steam', 'raw_top') }}
