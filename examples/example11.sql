SELECT w.id, w.isim, w.soyisim, AVG(wl.hours_worked) AS avg_hours, SUM(wl.hours_worked) AS total_hours
FROM workers w
JOIN workload wl ON w.id = wl.worker_id
WHERE w.id = 5  -- Örneğin, id'si 5 olan çalışan
GROUP BY w.id;