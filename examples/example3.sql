select w.id, w.isim, w.soyisim, w.email 
from workers w
join workload wl ON w.id = wl.worker_id
where wl.company_id = 3;