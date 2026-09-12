/* ==========================================================================
   University Hostel Management System (HMS) - Interactive Controller
   Handles theme switching, modals, client-side table filters, tabs,
   toast notifications, and connected prototype mock interactions.
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initNotifications();
  initTabs();
  initModals();
  initSearchAndFilters();
  initAutoDismissFlashes();
  HMS_ChatWidget.init();
});

/* --------------------------------------------------------------------------
   Notification Bell
   -------------------------------------------------------------------------- */
function initNotifications() {
  const bellButton = document.querySelector('.header-bell-btn');
  if (!bellButton) return;

  const notificationCount = bellButton.dataset.count ? Number(bellButton.dataset.count) : 3;

  bellButton.addEventListener('click', () => {
    if (notificationCount > 0) {
      showToast(`You have ${notificationCount} new notification${notificationCount === 1 ? '' : 's'} to review.`, 'info');
      bellButton.dataset.count = '0';
      bellButton.classList.remove('has-new');
      return;
    }

    showToast('No new notifications.', 'info');
  });

  if (notificationCount > 0) {
    bellButton.classList.add('has-new');
  }
}

/* --------------------------------------------------------------------------
   1. Theme Management (Light / Dark Mode)
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const savedTheme = localStorage.getItem('hms-theme') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

  setTheme(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
      showToast(`Switched to ${newTheme === 'dark' ? 'Dark' : 'Light'} Mode`, 'info');
    });
  }
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('hms-theme', theme);
  const themeIcon = document.getElementById('theme-icon');
  if (themeIcon) {
    themeIcon.innerHTML = theme === 'dark'
      ? `<path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>`
      : `<path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" fill="currentColor"/>`;
  }
}

/* --------------------------------------------------------------------------
   2. Responsive Sidebar
   -------------------------------------------------------------------------- */
function initSidebar() {
  const toggleBtn = document.getElementById('sidebar-toggle');
  const closeBtn = document.getElementById('sidebar-close');
  const backdrop = document.getElementById('sidebar-backdrop');
  const sidebar = document.getElementById('app-sidebar');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('open');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = window.innerWidth <= 768 ? 'hidden' : '';
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (sidebar && sidebar.classList.contains('open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', closeSidebar);
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSidebar();
  });

  // Close sidebar on mobile when navigating
  document.querySelectorAll('.app-sidebar .nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        closeSidebar();
      }
    });
  });
}

/* --------------------------------------------------------------------------
   3. Tabs Switching
   -------------------------------------------------------------------------- */
function initTabs() {
  document.querySelectorAll('.tabs-nav').forEach(nav => {
    const buttons = nav.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-tab');
        if (!targetId) return;

        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const parent = nav.closest('.tabs-wrapper') || nav.parentElement;
        parent.querySelectorAll('.tab-content').forEach(content => {
          content.classList.remove('active');
        });

        const activeContent = document.getElementById(targetId);
        if (activeContent) {
          activeContent.classList.add('active');
        }
      });
    });
  });
}

/* --------------------------------------------------------------------------
   4. Modal Dialogs
   -------------------------------------------------------------------------- */
function initModals() {
  // Open modal buttons
  document.querySelectorAll('[data-modal-target]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = trigger.getAttribute('data-modal-target');
      openModal(targetId);
    });
  });

  // Close modal buttons and backdrop clicks
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        closeModal(backdrop.id);
      }
    });

    backdrop.querySelectorAll('.modal-close-btn, [data-modal-close]').forEach(btn => {
      btn.addEventListener('click', () => {
        closeModal(backdrop.id);
      });
    });
  });

  // Escape key closes modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.active').forEach(modal => {
        closeModal(modal.id);
      });
    }
  });
}

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    const firstInput = modal.querySelector('input, select, textarea');
    if (firstInput) firstInput.focus();
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

/* --------------------------------------------------------------------------
   5. Search and Dynamic Filtering on Data Tables
   -------------------------------------------------------------------------- */
function initSearchAndFilters() {
  document.querySelectorAll('.filter-bar').forEach(bar => {
    const searchInput = bar.querySelector('.table-search-input');
    const statusSelect = bar.querySelector('.table-status-filter');
    const categorySelect = bar.querySelector('.table-category-filter');
    const tableId = bar.getAttribute('data-target-table');
    const table = tableId ? document.getElementById(tableId) : bar.nextElementSibling?.querySelector('.data-table');

    if (!table) return;

    const filterRows = () => {
      const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
      const statusFilter = statusSelect ? statusSelect.value.toLowerCase() : 'all';
      const categoryFilter = categorySelect ? categorySelect.value.toLowerCase() : 'all';

      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const rowStatus = (row.getAttribute('data-status') || '').toLowerCase();
        const rowCategory = (row.getAttribute('data-category') || '').toLowerCase();

        const matchesQuery = !query || text.includes(query);
        const matchesStatus = statusFilter === 'all' || rowStatus === statusFilter || text.includes(statusFilter);
        const matchesCategory = categoryFilter === 'all' || rowCategory === categoryFilter || text.includes(categoryFilter);

        row.style.display = (matchesQuery && matchesStatus && matchesCategory) ? '' : 'none';
      });
    };

    if (searchInput) searchInput.addEventListener('input', filterRows);
    if (statusSelect) statusSelect.addEventListener('change', filterRows);
    if (categorySelect) categorySelect.addEventListener('change', filterRows);
  });
}

/* --------------------------------------------------------------------------
   6. Toast Notifications
   -------------------------------------------------------------------------- */
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-dot"></span>
    <div style="flex: 1;">${message}</div>
    <button type="button" style="background:none;border:none;color:inherit;cursor:pointer;opacity:0.6;font-size:1.1rem;">&times;</button>
  `;

  toast.querySelector('button').addEventListener('click', () => {
    toast.remove();
  });

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

function initAutoDismissFlashes() {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.opacity = '0';
      flash.style.transition = 'opacity 0.4s ease';
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });
}

/* --------------------------------------------------------------------------
   7. Prototype Mock Interactions (Connected Navigation & State)
   -------------------------------------------------------------------------- */
window.HMS = {
  openModal,
  closeModal,
  showToast,

  // Allocate bed action
  allocateBed: function(roomNo, bedNo) {
    const studentSelect = document.getElementById('alloc-student-select');
    const studentName = studentSelect ? studentSelect.options[studentSelect.selectedIndex].text : 'Selected Student';
    showToast(`Successfully allocated ${roomNo} (${bedNo}) to ${studentName}`, 'success');
    closeModal('modal-allocate-bed');
    setTimeout(() => location.reload(), 600);
  },

  // Record payment action
  recordPayment: function(invoiceNo) {
    showToast(`Payment recorded for Invoice #${invoiceNo}. Official receipt generated.`, 'success');
    closeModal('modal-record-payment');
    setTimeout(() => location.reload(), 600);
  },

  // Print receipt trigger
  printReceipt: function(receiptId) {
    openModal('modal-official-receipt');
  },

  // Approve outpass
  approveLeave: function(leaveId, studentName) {
    showToast(`Outpass application #${leaveId} for ${studentName} has been approved. Gate pass generated.`, 'success');
    const row = document.getElementById(`leave-row-${leaveId}`);
    if (row) {
      const badge = row.querySelector('.badge');
      if (badge) {
        badge.className = 'badge badge-success';
        badge.innerHTML = '<span class="badge-dot"></span> Approved';
      }
      const actions = row.querySelector('.row-actions');
      if (actions) actions.innerHTML = '<span class="badge badge-neutral">Processed</span>';
    }
  },

  // Reject outpass
  rejectLeave: function(leaveId, studentName) {
    showToast(`Outpass application #${leaveId} for ${studentName} was rejected.`, 'error');
    const row = document.getElementById(`leave-row-${leaveId}`);
    if (row) {
      const badge = row.querySelector('.badge');
      if (badge) {
        badge.className = 'badge badge-danger';
        badge.innerHTML = '<span class="badge-dot"></span> Rejected';
      }
      const actions = row.querySelector('.row-actions');
      if (actions) actions.innerHTML = '<span class="badge badge-neutral">Processed</span>';
    }
  },

  // Check out visitor
  checkoutVisitor: function(visitorId, visitorName) {
    showToast(`Checked out ${visitorName}. Visitor pass closed.`, 'info');
    const row = document.getElementById(`visitor-row-${visitorId}`);
    if (row) {
      const badge = row.querySelector('.badge');
      if (badge) {
        badge.className = 'badge badge-neutral';
        badge.innerHTML = '<span class="badge-dot"></span> Checked Out';
      }
      const actionBtn = row.querySelector('.btn-checkout');
      if (actionBtn) actionBtn.remove();
    }
  },

  // Mark all present in roll call
  markAllAttendance: function(status) {
    document.querySelectorAll('.attendance-select').forEach(sel => {
      sel.value = status;
    });
    showToast(`All listed students marked as ${status} for today's roll call.`, 'success');
  },

  // Assign maintenance technician
  assignTechnician: function(complaintId) {
    const techSelect = document.getElementById('tech-select');
    const techName = techSelect ? techSelect.value : 'Technician';
    showToast(`Complaint #${complaintId} assigned to ${techName}. Status set to In Progress.`, 'success');
    closeModal('modal-assign-tech');
    setTimeout(() => location.reload(), 600);
  }
};

/* --------------------------------------------------------------------------
   Floating Chatbot Widget Controller
   -------------------------------------------------------------------------- */
const HMS_ChatWidget = {
  isOpen: false,

  init: function() {
    const btn = document.getElementById('floating-chatbot-btn');
    const panel = document.getElementById('floating-chat-panel');
    const closeBtn = document.getElementById('chat-panel-close-btn');
    const form = document.getElementById('floating-chat-form');
    const input = document.getElementById('floating-chat-input');
    const chips = document.querySelectorAll('.chat-chip');

    if (!btn || !panel) return;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggle();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.close();
      });
    }

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = input ? input.value.trim() : '';
        if (!text) return;
        input.value = '';
        this.sendMessage(text);
      });
    }

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        if (query) {
          this.sendMessage(query);
        }
      });
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    });

    // Close on clicking outside on mobile or desktop
    document.addEventListener('click', (e) => {
      if (this.isOpen && !panel.contains(e.target) && !btn.contains(e.target)) {
        this.close();
      }
    });
  },

  toggle: function() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  },

  open: function() {
    const panel = document.getElementById('floating-chat-panel');
    const btn = document.getElementById('floating-chatbot-btn');
    const input = document.getElementById('floating-chat-input');

    if (panel) {
      panel.classList.add('active');
      panel.setAttribute('aria-hidden', 'false');
    }
    if (btn) {
      btn.classList.add('panel-open');
    }
    this.isOpen = true;
    if (input) {
      setTimeout(() => input.focus(), 150);
    }
  },

  close: function() {
    const panel = document.getElementById('floating-chat-panel');
    const btn = document.getElementById('floating-chatbot-btn');

    if (panel) {
      panel.classList.remove('active');
      panel.setAttribute('aria-hidden', 'true');
    }
    if (btn) {
      btn.classList.remove('panel-open');
    }
    this.isOpen = false;
  },

  appendMessage: function(sender, text, isUser = false) {
    const container = document.getElementById('floating-chat-messages');
    if (!container) return;

    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-bot'}`;

    const senderDiv = document.createElement('div');
    senderDiv.className = 'chat-bubble-sender';
    senderDiv.textContent = sender;

    const textDiv = document.createElement('div');
    textDiv.className = 'chat-bubble-text';
    textDiv.textContent = text;

    bubble.appendChild(senderDiv);
    bubble.appendChild(textDiv);
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
  },

  sendMessage: async function(text) {
    if (!text) return;
    this.appendMessage('You', text, true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await response.json();
      this.appendMessage('Assistant', data.reply || 'No reply.', false);
    } catch (err) {
      this.appendMessage('Assistant', 'Unable to reach the assistant right now. Please try again.', false);
    }
  }
};
