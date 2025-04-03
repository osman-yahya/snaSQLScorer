SELECT c.sirketIsim, SUM(wl.hours_worked) AS total_hours, AVG(wl.hours_worked) AS avg_hours
FROM workload wl
JOIN companies c ON c.id = wl.company_id
GROUP BY c.id
ORDER BY total_hours DESC;