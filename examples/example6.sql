Select AVG(wl.hours_worked) As avg_hours
From workload wl
Join workers w On wl.worker_id = w.id
Where w.isManager = 0;