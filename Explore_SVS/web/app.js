/**
 * SysInfo Web Dashboard Client Application
 * Live fetches /api/stats and updates DOM elements smoothly.
 */

(() => {
  let timerId = null;
  let currentInterval = 2000;
  let isFetching = false;

  // DOM Elements - Controls
  const intervalSelect = document.getElementById('interval-select');
  const btnRefresh = document.getElementById('btn-refresh');
  const spinIcon = btnRefresh.querySelector('.spin-icon');
  const connectionStatus = document.getElementById('connection-status');
  const pulseDot = document.querySelector('.pulse-dot');
  const lastUpdatedText = document.getElementById('last-updated-text');

  // Helper: Apply color class to progress bars based on percentage
  function getUsageColorClass(pct) {
    if (pct >= 85) return 'bar-high';
    if (pct >= 60) return 'bar-med';
    return '';
  }

  // Fetch API Stats
  async function fetchStats() {
    if (isFetching) return;
    isFetching = true;
    spinIcon.classList.add('spinning');

    try {
      const response = await fetch('/api/stats', {
        headers: { 'Cache-Control': 'no-cache' }
      });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      updateDashboard(data);

      connectionStatus.textContent = 'Live Connected';
      connectionStatus.style.color = '#34d399';
      pulseDot.style.background = '#10b981';
      pulseDot.style.display = 'inline-block';
    } catch (err) {
      console.error('Error fetching system stats:', err);
      connectionStatus.textContent = 'Reconnecting...';
      connectionStatus.style.color = '#f87171';
      pulseDot.style.background = '#ef4444';
    } finally {
      isFetching = false;
      spinIcon.classList.remove('spinning');
    }
  }

  // Master Dashboard Updater
  function updateDashboard(data) {
    if (!data) return;

    // 1. Quick Stats
    renderQuickStats(data);

    // 2. OS Overview
    renderOSInfo(data.os);

    // 3. CPU Details & Cores
    renderCPUInfo(data.cpu);

    // 4. Memory & Swap
    renderMemoryInfo(data.memory);

    // 5. Storage / Partitions
    renderDiskInfo(data.disk);

    // 6. Network Interfaces
    renderNetworkInfo(data.network);

    // 7. Battery & Power
    renderBatteryInfo(data.battery);

    // 8. Runtime Environment
    renderEnvironmentInfo(data.environment);

    // Footer timestamp
    if (data.timestamp) {
      lastUpdatedText.textContent = `Last update: ${data.timestamp}`;
    }
  }

  function renderQuickStats(data) {
    // Quick CPU
    const cpuPct = data.cpu?.usage_percent ?? 0;
    const quickCpuVal = document.getElementById('quick-cpu-val');
    const quickCpuSub = document.getElementById('quick-cpu-sub');
    const quickCpuBar = document.getElementById('quick-cpu-bar');

    quickCpuVal.textContent = `${cpuPct.toFixed(1)}%`;
    quickCpuSub.textContent = `${data.cpu?.physical_cores ?? '-'} Cores • ${data.cpu?.logical_cores ?? '-'} Threads`;
    quickCpuBar.style.width = `${Math.min(cpuPct, 100)}%`;
    quickCpuBar.className = `progress-bar-fill cpu-bg ${getUsageColorClass(cpuPct)}`;

    // Quick RAM
    const ram = data.memory?.ram;
    if (ram) {
      const ramPct = ram.percent ?? 0;
      const quickRamVal = document.getElementById('quick-ram-val');
      const quickRamSub = document.getElementById('quick-ram-sub');
      const quickRamBar = document.getElementById('quick-ram-bar');

      quickRamVal.textContent = `${ramPct.toFixed(1)}%`;
      quickRamSub.textContent = `${ram.used || '--'} used of ${ram.total || '--'}`;
      quickRamBar.style.width = `${Math.min(ramPct, 100)}%`;
      quickRamBar.className = `progress-bar-fill ram-bg ${getUsageColorClass(ramPct)}`;
    }

    // Quick Disk (Primary C:\ or first partition)
    const partitions = data.disk?.partitions ?? [];
    if (partitions.length > 0) {
      const p = partitions[0];
      const quickDiskVal = document.getElementById('quick-disk-val');
      const quickDiskSub = document.getElementById('quick-disk-sub');
      const quickDiskBar = document.getElementById('quick-disk-bar');

      quickDiskVal.textContent = `${p.percent}%`;
      quickDiskSub.textContent = `${p.device} (${p.free} free of ${p.total})`;
      quickDiskBar.style.width = `${Math.min(p.percent, 100)}%`;
      quickDiskBar.className = `progress-bar-fill disk-bg ${getUsageColorClass(p.percent)}`;
    }

    // Quick Net / Power
    const quickNetVal = document.getElementById('quick-net-val');
    const quickNetSub = document.getElementById('quick-net-sub');
    const quickBatteryTag = document.getElementById('quick-battery-tag');

    quickNetVal.textContent = data.network?.primary_ip || '127.0.0.1';
    const activeIfCount = (data.network?.interfaces || []).filter(i => i.is_up).length;
    quickNetSub.textContent = `${activeIfCount} active network adapter${activeIfCount === 1 ? '' : 's'}`;

    if (data.battery && data.battery.has_battery) {
      const powerState = data.battery.power_plugged ? '⚡ AC Plugged In' : '🔋 On Battery';
      quickBatteryTag.textContent = `${powerState} (${data.battery.percent}%)`;
      quickBatteryTag.style.display = 'inline-block';
    } else {
      quickBatteryTag.textContent = '🔌 Desktop / AC Powered';
    }
  }

  function renderOSInfo(os) {
    if (!os) return;
    document.getElementById('info-os-name').textContent = `${os.system} ${os.release} (Build ${os.version})`;
    document.getElementById('info-arch').textContent = os.architecture;
    document.getElementById('info-hostname').textContent = os.hostname;
    document.getElementById('info-user').textContent = os.username;
    document.getElementById('info-boot-time').textContent = os.boot_time;
    document.getElementById('info-uptime').textContent = os.uptime;
    document.getElementById('os-platform-badge').textContent = os.system || 'OS';
  }

  function renderCPUInfo(cpu) {
    if (!cpu) return;
    document.getElementById('cpu-brand-name').textContent = cpu.brand || 'Central Processing Unit';
    document.getElementById('cpu-physical-cores').textContent = cpu.physical_cores ?? '--';
    document.getElementById('cpu-logical-cores').textContent = cpu.logical_cores ?? '--';
    document.getElementById('cpu-max-freq').textContent = `${cpu.frequency_current || '--'} (Max: ${cpu.frequency_max || '--'})`;
    document.getElementById('cpu-freq-badge').textContent = cpu.frequency_current || 'Speed: N/A';

    const overallPct = cpu.usage_percent ?? 0;
    document.getElementById('cpu-overall-pct').textContent = `${overallPct.toFixed(1)}%`;
    const overallBar = document.getElementById('cpu-overall-bar');
    overallBar.style.width = `${Math.min(overallPct, 100)}%`;
    overallBar.className = `progress-bar-fill cpu-gradient ${getUsageColorClass(overallPct)}`;

    // Render Per-Core Grid
    const coresGrid = document.getElementById('cores-grid');
    const perCore = cpu.per_core_percent || [];

    // Match count or reconstruct
    if (coresGrid.children.length !== perCore.length) {
      coresGrid.innerHTML = '';
      perCore.forEach((val, idx) => {
        const coreNumStr = `C${String(idx).padStart(2, '0')}`;
        const card = document.createElement('div');
        card.className = 'core-card';
        card.id = `core-card-${idx}`;
        card.innerHTML = `
          <div class="core-card-header">
            <span class="core-num">${coreNumStr}</span>
            <span class="core-pct" id="core-val-${idx}">${val.toFixed(1)}%</span>
          </div>
          <div class="core-bar-bg">
            <div class="core-bar-fill" id="core-bar-${idx}" style="width: ${Math.min(val, 100)}%"></div>
          </div>
        `;
        coresGrid.appendChild(card);
      });
    } else {
      // Update in-place
      perCore.forEach((val, idx) => {
        const valElem = document.getElementById(`core-val-${idx}`);
        const barElem = document.getElementById(`core-bar-${idx}`);
        if (valElem) valElem.textContent = `${val.toFixed(1)}%`;
        if (barElem) {
          barElem.style.width = `${Math.min(val, 100)}%`;
          barElem.style.background = val >= 80 ? '#f43f5e' : val >= 50 ? '#f59e0b' : '#6366f1';
        }
      });
    }
  }

  function renderMemoryInfo(memory) {
    if (!memory) return;

    // RAM
    const ram = memory.ram;
    if (ram) {
      document.getElementById('ram-usage-text').textContent = `${ram.used} / ${ram.total}`;
      document.getElementById('ram-free-val').textContent = ram.available;
      document.getElementById('ram-pct-val').textContent = `${ram.percent}%`;
      const ramBar = document.getElementById('ram-progress-bar');
      ramBar.style.width = `${Math.min(ram.percent, 100)}%`;
      ramBar.className = `progress-bar-fill ram-gradient ${getUsageColorClass(ram.percent)}`;
    }

    // Swap / Pagefile
    const swap = memory.swap;
    const swapBlock = document.getElementById('swap-block');
    if (swap) {
      swapBlock.style.display = 'flex';
      const label = swap.label || 'Swap / Pagefile';
      document.getElementById('swap-title').textContent = label;
      document.getElementById('swap-usage-text').textContent = `${swap.used} / ${swap.total}`;
      document.getElementById('swap-free-val').textContent = swap.free || '--';
      document.getElementById('swap-pct-val').textContent = `${swap.percent}%`;
      const swapBar = document.getElementById('swap-progress-bar');
      swapBar.style.width = `${Math.min(swap.percent, 100)}%`;
      swapBar.className = `progress-bar-fill swap-gradient ${getUsageColorClass(swap.percent)}`;
    } else {
      swapBlock.style.display = 'none';
    }
  }

  function renderDiskInfo(disk) {
    if (!disk) return;

    // Disk I/O pill
    if (disk.io) {
      document.getElementById('disk-io-pill').textContent = `Read: ${disk.io.read} | Write: ${disk.io.write}`;
    }

    const container = document.getElementById('partitions-container');
    const partitions = disk.partitions || [];
    container.innerHTML = '';

    partitions.forEach(p => {
      const item = document.createElement('div');
      item.className = 'partition-item';
      item.innerHTML = `
        <div class="partition-header">
          <div class="partition-name-group">
            <span class="partition-mount">${p.mountpoint}</span>
            <span class="partition-type">${p.fstype}</span>
          </div>
          <span class="partition-stats">${p.percent}%</span>
        </div>
        <div class="progress-bar-bg small-bar">
          <div class="progress-bar-fill disk-bg ${getUsageColorClass(p.percent)}" style="width: ${Math.min(p.percent, 100)}%"></div>
        </div>
        <div class="partition-footer">
          <span>Used: <strong>${p.used}</strong></span>
          <span>Free: <strong>${p.free}</strong></span>
          <span>Total: <strong>${p.total}</strong></span>
        </div>
      `;
      container.appendChild(item);
    });
  }

  function renderNetworkInfo(net) {
    if (!net) return;

    document.getElementById('badge-primary-ip').textContent = `IP: ${net.primary_ip || 'N/A'}`;

    if (net.total_io) {
      document.getElementById('net-total-sent').textContent = net.total_io.bytes_sent || '--';
      document.getElementById('net-total-recv').textContent = net.total_io.bytes_recv || '--';
    }

    const container = document.getElementById('interfaces-container');
    const ifaces = net.interfaces || [];
    container.innerHTML = '';

    ifaces.forEach(i => {
      const card = document.createElement('div');
      card.className = 'interface-card';
      const statusClass = i.is_up ? 'up' : 'down';
      const statusText = i.is_up ? 'UP' : 'DOWN';
      const speedStr = i.speed_mbps > 0 ? ` (${i.speed_mbps} Mbps)` : '';

      card.innerHTML = `
        <div class="interface-header">
          <span class="if-name">${i.name}</span>
          <span class="if-status-badge ${statusClass}">[${statusText}]${speedStr}</span>
        </div>
        <div class="if-details">
          <span>IPv4: <strong>${i.ipv4 || 'N/A'}</strong></span>
          <span>MAC: <strong>${i.mac || 'N/A'}</strong></span>
        </div>
        <div class="if-details">
          <span>Sent: ${i.traffic_sent || '--'}</span>
          <span>Recv: ${i.traffic_recv || '--'}</span>
        </div>
      `;
      container.appendChild(card);
    });
  }

  function renderBatteryInfo(battery) {
    const container = document.getElementById('battery-container');
    if (!battery || !battery.has_battery) {
      container.innerHTML = `
        <div class="battery-header">
          <div class="battery-icon-label">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 12h-5M9 12H4M12 9v6"/>
            </svg>
            <span>Direct AC Power (No Battery Detected)</span>
          </div>
        </div>
        <div class="battery-meta-row" style="margin-top: 6px;">
          <span>System running on standard wall power outlet</span>
        </div>
      `;
      return;
    }

    document.getElementById('battery-pct').textContent = `${battery.percent}%`;
    const bar = document.getElementById('battery-bar');
    bar.style.width = `${Math.min(battery.percent, 100)}%`;
    bar.className = `progress-bar-fill battery-bg ${getUsageColorClass(100 - battery.percent)}`;

    const sourceText = battery.power_plugged ? 'Source: Plugged In (AC)' : 'Source: Discharged (Battery)';
    document.getElementById('battery-source').textContent = sourceText;
    document.getElementById('battery-remaining').textContent = `Remaining: ${battery.time_left || '--'}`;
  }

  function renderEnvironmentInfo(env) {
    if (!env) return;
    document.getElementById('py-version').textContent = env.python_version || '--';
    document.getElementById('py-processes').textContent = env.active_processes || '--';
    
    const pyExe = document.getElementById('py-executable');
    pyExe.textContent = env.python_executable || '--';
    pyExe.title = env.python_executable || '';

    const pyWork = document.getElementById('py-workdir');
    pyWork.textContent = env.working_directory || '--';
    pyWork.title = env.working_directory || '';
  }

  // Interval Controller
  function setupInterval(ms) {
    if (timerId) {
      clearInterval(timerId);
      timerId = null;
    }
    currentInterval = parseInt(ms, 10);
    if (currentInterval > 0) {
      timerId = setInterval(fetchStats, currentInterval);
    }
  }

  // Event Listeners
  btnRefresh.addEventListener('click', () => {
    fetchStats();
  });

  intervalSelect.addEventListener('change', (e) => {
    setupInterval(e.target.value);
  });

  // Initial Boot
  fetchStats();
  setupInterval(currentInterval);
})();
