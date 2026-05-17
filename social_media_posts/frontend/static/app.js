  const BASE_URL = "http://localhost:8000"
  let token = null

  // ── Tab switching ──────────────────────────────────────
  function setTab(el) {
    const tabs     = document.querySelectorAll('.tab')
    const isSignIn = tabs[0] === el
    
    
    tabs.forEach(t => t.classList.remove('active'))
    el.classList.add('active')

    document.getElementById('panel-signin').style.display   = isSignIn ? 'block' : 'none'
    document.getElementById('panel-register').style.display = isSignIn ? 'none'  : 'block'

    // clear messages when switching
    showMessage('login-message', '', '')
    showMessage('register-message', '', '')
  }

  // ── Message helper ─────────────────────────────────────
  function showMessage(id, text, type) {
    const el = document.getElementById(id)
    el.textContent = text
    el.className   = type  // "success" | "error" | ""
  }

  // ── Sign in ────────────────────────────────────────────
  async function login() {
    const username = document.getElementById('username').value.trim()
    const password = document.getElementById('password').value
    const btn      = document.getElementById('login-btn')

    if (!username || !password) {
      showMessage('login-message', 'Please enter your email and password.', 'error')
      return
    }

    btn.classList.add('loading')
    btn.textContent = 'Signing in…'

    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    try {
      const response = await fetch(`${BASE_URL}/login`, { method: 'POST', body: formData })
      const data     = await response.json()

      if (response.ok) {
        token = data.access_token
        localStorage.setItem('token', token)
        showMessage('login-message', 'Logged in successfully! Redirecting…', 'success')
        // window.location.href = "/dashboard"
      } else {
        showMessage('login-message', data.detail || 'Login failed. Please try again.', 'error')
      }
    } catch {
      showMessage('login-message', 'Cannot reach the server. Is FastAPI running on port 8000?', 'error')
    } finally {
      btn.classList.remove('loading')
      btn.textContent = 'Sign in to Inkwell'
    }
  }

  // ── Create account ─────────────────────────────────────
  async function register() {
    const fullname = document.getElementById('reg-fullname').value.trim()
    const email    = document.getElementById('reg-email').value.trim()
    const username = document.getElementById('reg-username').value.trim().replace(/^@/, '')
    const password = document.getElementById('reg-password').value
    const btn      = document.getElementById('register-btn')

    if (!fullname || !email || !username || !password) {
      showMessage('register-message', 'Please fill in all fields.', 'error')
      return
    }
    if (password.length < 8) {
      showMessage('register-message', 'Password must be at least 8 characters.', 'error')
      return
    }

    btn.classList.add('loading')
    btn.textContent = 'Creating account…'

    try {
      const response = await fetch(`${BASE_URL}/users`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ full_name: fullname, email, username, password })
      })
      const data = await response.json()

      if (response.ok) {
        showMessage('register-message', 'Account created! Redirecting to sign in…', 'success')

        // clear register fields
        ;['reg-fullname','reg-email','reg-username','reg-password'].forEach(id => {
          document.getElementById(id).value = ''
        })

        // switch to Sign in tab after 1.5 s
        setTimeout(() => {
          setTab(document.querySelectorAll('.tab')[0])
          showMessage('login-message', 'Account created — please sign in.', 'success')
        }, 1500)

      } else {
        const msg = Array.isArray(data.detail)
          ? data.detail.map(e => e.msg).join(', ')
          : (data.detail || 'Registration failed. Please try again.')
        showMessage('register-message', msg, 'error')
      }
    } catch {
      showMessage('register-message', 'Cannot reach the server. Is FastAPI running on port 8000?', 'error')
    } finally {
      btn.classList.remove('loading')
      btn.textContent = 'Create account'
    }
  }

  // ── Enter key submits whichever panel is active ────────
  document.addEventListener('keydown', e => {
    if (e.key !== 'Enter') return
    const registerVisible = document.getElementById('panel-register').style.display !== 'none'
    registerVisible ? register() : login()
  })