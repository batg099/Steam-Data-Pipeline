select
    *,
    rang_semaine_derniere - rang as progression
from {{ ref('stg_top') }}
where date_collecte = (select max(date_collecte) from {{ ref('stg_top') }})
