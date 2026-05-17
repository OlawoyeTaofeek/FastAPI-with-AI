// ── Constants ────────────────────────────────────────
const BASE_URL = 'http://localhost:8000'

// ── Auth state on page load ──────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const token    = localStorage.getItem('token')
  const name     = localStorage.getItem('user_name')
  const initials = localStorage.getItem('user_initials')

  if (token && name) {
    showLoggedIn(name, initials)
  } else {
    showLoggedOut()
  }

  // close dropdown when clicking outside
  document.addEventListener('click', e => {
    const menu = document.getElementById('navUserMenu')
    if (menu && !menu.contains(e.target)) {
      closeDropdown()
    }
  })
})

// ── Show / hide nav state ────────────────────────────
function showLoggedIn(name, initials) {
  document.getElementById('nav-guest').style.display = 'none'
  document.getElementById('nav-user').style.display  = 'flex'
  document.getElementById('navInitials').textContent    = initials || getInitials(name)
  document.getElementById('navDropdownName').textContent = name
}

function showLoggedOut() {
  document.getElementById('nav-guest').style.display = 'flex'
  document.getElementById('nav-user').style.display  = 'none'
}

function getInitials(name) {
  const parts = name.trim().split(' ')
  return parts.length > 1
    ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    : parts[0].slice(0, 2).toUpperCase()
}

// ── Dropdown ─────────────────────────────────────────
function toggleDropdown() {
  document.getElementById('navDropdown').classList.toggle('open')
}
function closeDropdown() {
  document.getElementById('navDropdown').classList.remove('open')
}

// ── Auth modal ────────────────────────────────────────
function openModal(tab) {
  document.getElementById('authModal').classList.add('open')
  switchTab(tab === 'register' ? 'register' : 'signin')
}
function closeModal() {
  document.getElementById('authModal').classList.remove('open')
  clearErrors()
}
function closeModalOnOverlay(e) {
  if (e.target === document.getElementById('authModal')) closeModal()
}
function switchTab(tab) {
  document.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'))
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'))
  document.getElementById('tab-' + tab).classList.add('active')
  document.getElementById('pane-' + tab).classList.add('active')
}
function clearErrors() {
  document.getElementById('signin-error').textContent   = ''
  document.getElementById('register-error').textContent = ''
}
function showError(id, msg) {
  document.getElementById(id).textContent = msg
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal()
})

// ── Sign in ───────────────────────────────────────────
async function handleSignIn() {
  const email    = document.getElementById('signin-email').value.trim()
  const password = document.getElementById('signin-password').value

  if (!email || !password) {
    showError('signin-error', 'Please fill in all fields.')
    return
  }

  try {
    // FastAPI OAuth2 expects form data, not JSON
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)

    const res  = await fetch(`${BASE_URL}/auth/login`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body:    form
    })
    const data = await res.json()

    if (res.ok) {
      localStorage.setItem('token',          data.access_token)
      localStorage.setItem('user_name',      data.user.full_name)
      localStorage.setItem('user_initials',  getInitials(data.user.full_name))
      localStorage.setItem('user_username',  data.user.username)
      showLoggedIn(data.user.full_name, getInitials(data.user.full_name))
      closeModal()
    } else {
      showError('signin-error', data.detail || 'Invalid email or password.')
    }
  } catch {
    showError('signin-error', 'Cannot reach server. Is FastAPI running?')
  }
}

// ── Register ──────────────────────────────────────────
async function handleRegister() {
  const name     = document.getElementById('reg-name').value.trim()
  const username = document.getElementById('reg-username').value.trim()
  const email    = document.getElementById('reg-email').value.trim()
  const password = document.getElementById('reg-password').value

  if (!name || !username || !email || !password) {
    showError('register-error', 'Please fill in all fields.')
    return
  }
  if (password.length < 8) {
    showError('register-error', 'Password must be at least 8 characters.')
    return
  }

  try {
    const res  = await fetch(`${BASE_URL}/auth/register`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ full_name: name, username, email, password })
    })
    const data = await res.json()

    if (res.ok) {
      localStorage.setItem('token',         data.access_token)
      localStorage.setItem('user_name',     data.user.full_name)
      localStorage.setItem('user_initials', getInitials(data.user.full_name))
      localStorage.setItem('user_username', data.user.username)
      showLoggedIn(data.user.full_name, getInitials(data.user.full_name))
      closeModal()
    } else {
      showError('register-error', data.detail || 'Registration failed.')
    }
  } catch {
    showError('register-error', 'Cannot reach server. Is FastAPI running?')
  }
}

// ── Sign out ──────────────────────────────────────────
function signOut() {
  localStorage.removeItem('token')
  localStorage.removeItem('user_name')
  localStorage.removeItem('user_initials')
  localStorage.removeItem('user_username')
  showLoggedOut()
  closeDropdown()
  window.location.href = '/'
}