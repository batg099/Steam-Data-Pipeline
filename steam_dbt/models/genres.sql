select
    genre,
    count(*) as nb_jeux,
    sum(pic_joueurs) as joueurs_total,
    round(avg(prix_eur), 2) as prix_moyen
from {{ ref('jeux_du_jour') }},
    unnest(split(genres, ', ')) as genre
where genres != ''
group by genre
