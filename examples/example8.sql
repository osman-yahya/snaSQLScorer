SELECT SUM(wl.hours_worked) AS total_hours FROM workload wl WHERE wl.date BETWEEN '2025-03-01' AND '2025-03-31';