select
    date_collecte,
    appid,
    nom,
    rang,
    pic_joueurs,
    lag(pic_joueurs) over (partition by appid order by date_collecte) as pic_joueurs_veille
from {{ ref('stg_top') }}
