SELECT w.id, w.isim, w.soyisim, GROUP_CONCAT(c.sirketIsim) AS companies
FROM workers w
JOIN workload wl ON w.id = wl.worker_id
JOIN companies c ON c.id = wl.company_id
GROUP BY w.id;