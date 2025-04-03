SELECT c.sirketIsim, AVG(wl.hours_worked) AS avg_work_hours
from workload wl
JOIN companies c ON c.id = wl.company_id
GROUP BY c.sirketIsim;