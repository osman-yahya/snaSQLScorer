SELECT w.id, w.isim, w.soyisim, SUM(wl.hours_worked) AS total_hours
FROM workers w
JOIN workload wl ON w.id = wl.worker_id
GROUP BY w.id
ORDER BY total_hours DESC
LIMIT 1;