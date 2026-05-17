/* ═══════════════════════════════════════════════════════
   Inkwell — profile.js
   Covers: nav dropdown · tabs · edit modal · avatar
   preview · password strength · PATCH /users/me · PUT /users/me/password
═══════════════════════════════════════════════════════ */

const BASE_URL = "http://localhost:8000"

/* ─────────────────────────────────────────
   AUTH HEADER  (reads token from localStorage)
───────────────────────────────────────── */
function authHeaders(json = false) {
  const token = localStorage.getItem("token")
  const h = {}
  if (token) h["Authorization"] = `Bearer ${token}`
  if (json)  h["Content-Type"] = "application/json"
  return h
}

/* ─────────────────────────────────────────
   NAV DROPDOWN
───────────────────────────────────────── */
function toggleDropdown() {
  document.getElementById("navDropdown").classList.toggle("open")
}

document.addEventListener("click", e => {
  const btn = document.getElementById("navAvatarBtn")
  const dd  = document.getElementById("navDropdown")
  if (!btn.contains(e.target) && !dd.contains(e.target)) {
    dd.classList.remove("open")
  }
})

/* ─────────────────────────────────────────
   PROFILE TABS  (posts / followers / following / liked)
───────────────────────────────────────── */
function switchTab(name) {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    const active = btn.textContent.trim().toLowerCase().startsWith(name)
    btn.classList.toggle("active", active)
  })
  document.querySelectorAll(".tab-pane").forEach(pane => {
    pane.classList.toggle("active", pane.id === `tab-${name}`)
  })
}

/* ─────────────────────────────────────────
   EDIT MODAL  — open / close / overlay click
───────────────────────────────────────── */
function openEditModal(startTab = "info") {
  document.getElementById("editModal").classList.add("open")
  document.body.style.overflow = "hidden"
  switchModalTab(startTab)
}

function closeEditModal() {
  document.getElementById("editModal").classList.remove("open")
  document.body.style.overflow = ""
}

function closeOnOverlay(e) {
  if (e.target === document.getElementById("editModal")) closeEditModal()
}

document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeEditModal()
})

/* ─────────────────────────────────────────
   MODAL INNER TABS  (info / photo / password)
───────────────────────────────────────── */
function switchModalTab(name) {
  document.querySelectorAll(".modal-tab").forEach(t => {
    t.classList.toggle("active", t.textContent.trim().toLowerCase().includes(name))
  })
  document.querySelectorAll(".mpane").forEach(p => {
    p.classList.toggle("active", p.id === `mpane-${name}`)
  })
  // reset messages
  document.querySelectorAll(".msg").forEach(m => m.className = "msg")
}

/* ─────────────────────────────────────────
   BIO CHAR COUNT
───────────────────────────────────────── */
const bioTA = document.getElementById("f-bio")
if (bioTA) {
  bioTA.addEventListener("input", () => {
    const len = bioTA.value.length
    document.getElementById("bioCount").textContent = len
    document.getElementById("bioCount").style.color = len > 190 ? "#B83A2A" : ""
  })
}

/* ─────────────────────────────────────────
   SHOW MESSAGE  helpers
───────────────────────────────────────── */
function showMsg(id, text, type) {
  const el = document.getElementById(id)
  el.textContent = text
  el.className = `msg ${type}`
}

function setBtnLoading(id, on, label) {
  const btn = document.getElementById(id)
  if (!btn) return
  btn.disabled = on
  btn.classList.toggle("loading", on)
  const lbl = btn.querySelector(".btn-label")
  if (lbl) lbl.textContent = label
  else btn.childNodes[btn.childNodes.length - 1].textContent = " " + label
}

/* ─────────────────────────────────────────
   SAVE PROFILE INFO  →  PATCH /users/me
───────────────────────────────────────── */
async function saveInfo() {
  const fullName = document.getElementById("f-name").value.trim()
  const username = document.getElementById("f-username").value.trim().replace(/^@/, "")
  const email    = document.getElementById("f-email").value.trim()
  const bio      = document.getElementById("f-bio").value.trim()
  const location = document.getElementById("f-location").value.trim()

  if (!fullName || !email) {
    showMsg("msg-info", "Name and email are required.", "error")
    return
  }

  // split full name into first / last
  const parts     = fullName.split(" ")
  const firstName = parts[0] || ""
  const lastName  = parts.slice(1).join(" ") || ""

  setBtnLoading("saveInfoBtn", true, "Saving…")

  try {
    const res = await fetch(`${BASE_URL}/users/me`, {
      method: "PATCH",
      headers: authHeaders(true),
      body: JSON.stringify({
        first_name: firstName,
        last_name:  lastName,
        username,
        email,
        bio:     bio   || null,
        country: location || null,
      }),
    })

    const data = await res.json()

    if (res.ok) {
      // update visible profile fields instantly
      document.getElementById("displayName").textContent   = fullName
      document.getElementById("displayHandle").textContent = `@${username}`
      document.getElementById("displayBio").textContent    = bio
      document.getElementById("sidebarName").textContent   = fullName
      document.getElementById("sidebarLocation").textContent = location

      showMsg("msg-info", "Profile updated successfully!", "success")
    } else {
      const detail = Array.isArray(data.detail)
        ? data.detail.map(e => e.msg).join(" · ")
        : data.detail || "Update failed."
      showMsg("msg-info", detail, "error")
    }
  } catch {
    showMsg("msg-info", "Cannot reach the server.", "error")
  } finally {
    setBtnLoading("saveInfoBtn", false, "Save changes")
  }
}

/* ─────────────────────────────────────────
   AVATAR PREVIEW  (profile page inline click)
───────────────────────────────────────── */
function previewAvatar(input) {
  if (!input.files || !input.files[0]) return
  const url = URL.createObjectURL(input.files[0])
  setAvatarPreview(url)
}

function setAvatarPreview(url) {
  // main profile avatar
  const av = document.getElementById("profileAv")
  av.querySelector(".av-edit-hint")?.remove()
  let img = av.querySelector("img")
  if (!img) {
    img = document.createElement("img")
    av.appendChild(img)
  }
  img.src = url
  av.textContent = ""
  av.appendChild(img)
  const hint = document.createElement("div")
  hint.className = "av-edit-hint"
  hint.textContent = "Change"
  av.appendChild(hint)

  // modal large preview
  const large = document.getElementById("avatarLargePreview")
  if (large) {
    large.textContent = ""
    const img2 = document.createElement("img")
    img2.src = url
    large.appendChild(img2)
  }
}

/* ─────────────────────────────────────────
   MODAL AVATAR SELECT + DRAG-AND-DROP
───────────────────────────────────────── */
function handleAvatarSelect(input) {
  if (!input.files || !input.files[0]) return
  _stageAvatarFile(input.files[0])
}

function handleDragOver(e) {
  e.preventDefault()
  document.getElementById("uploadArea").classList.add("dragover")
}

function handleDrop(e) {
  e.preventDefault()
  document.getElementById("uploadArea").classList.remove("dragover")
  const file = e.dataTransfer.files[0]
  if (file) _stageAvatarFile(file)
}

let _stagedAvatarFile = null

function _stageAvatarFile(file) {
  if (!file.type.startsWith("image/")) {
    showMsg("msg-photo", "Please select a valid image file.", "error")
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    showMsg("msg-photo", "File must be under 5 MB.", "error")
    return
  }
  _stagedAvatarFile = file
  const url = URL.createObjectURL(file)
  // update modal preview
  const large = document.getElementById("avatarLargePreview")
  large.textContent = ""
  const img = document.createElement("img")
  img.src = url
  large.appendChild(img)
  // update upload area hint
  document.querySelector(".upload-title").textContent = file.name
}

/* ─────────────────────────────────────────
   SAVE PHOTO  →  POST /users/me/photo  (multipart)
───────────────────────────────────────── */
async function savePhoto() {
  if (!_stagedAvatarFile) {
    showMsg("msg-photo", "Please choose a photo first.", "error")
    return
  }

  setBtnLoading("savePhotoBtn", true, "Uploading…")

  try {
    const fd = new FormData()
    fd.append("file", _stagedAvatarFile)

    const res = await fetch(`${BASE_URL}/users/me/photo`, {
      method: "POST",
      headers: authHeaders(),   // no Content-Type — let browser set multipart boundary
      body: fd,
    })

    const data = await res.json()

    if (res.ok) {
      const photoUrl = data.profile_picture_url || URL.createObjectURL(_stagedAvatarFile)
      setAvatarPreview(photoUrl)
      _stagedAvatarFile = null
      showMsg("msg-photo", "Photo updated!", "success")
    } else {
      showMsg("msg-photo", data.detail || "Upload failed.", "error")
    }
  } catch {
    showMsg("msg-photo", "Cannot reach the server.", "error")
  } finally {
    setBtnLoading("savePhotoBtn", false, "Save photo")
  }
}

/* ─────────────────────────────────────────
   PASSWORD STRENGTH METER
───────────────────────────────────────── */
function checkStrength(val) {
  const bar   = document.getElementById("pwBar")
  const label = document.getElementById("pwLabel")
  if (!bar) return

  let score = 0
  if (val.length >= 8)              score++
  if (val.length >= 12)             score++
  if (/[A-Z]/.test(val))            score++
  if (/[0-9]/.test(val))            score++
  if (/[^A-Za-z0-9]/.test(val))     score++

  const levels = [
    { w: "0%",   color: "#E2DFD8", text: "—"      },
    { w: "25%",  color: "#B83A2A", text: "Weak"   },
    { w: "50%",  color: "#E07C2A", text: "Fair"   },
    { w: "75%",  color: "#C9943A", text: "Good"   },
    { w: "90%",  color: "#2A7A45", text: "Strong" },
    { w: "100%", color: "#2A7A45", text: "Great"  },
  ]

  const lvl = val.length === 0 ? levels[0] : levels[Math.min(score, 5)]
  bar.style.width      = lvl.w
  bar.style.background = lvl.color
  label.textContent    = lvl.text
  label.style.color    = lvl.color
}

/* ─────────────────────────────────────────
   SAVE PASSWORD  →  PUT /users/me/password
───────────────────────────────────────── */
async function savePassword() {
  const current = document.getElementById("f-curr-pw").value
  const newPw   = document.getElementById("f-new-pw").value
  const confirm = document.getElementById("f-confirm-pw").value

  if (!current || !newPw || !confirm) {
    showMsg("msg-pw", "All fields are required.", "error")
    return
  }
  if (newPw.length < 8) {
    showMsg("msg-pw", "New password must be at least 8 characters.", "error")
    return
  }
  if (newPw !== confirm) {
    showMsg("msg-pw", "Passwords don't match.", "error")
    return
  }

  setBtnLoading("savePwBtn", true, "Updating…")

  try {
    const res = await fetch(`${BASE_URL}/users/me/password`, {
      method: "PUT",
      headers: authHeaders(true),
      body: JSON.stringify({ current_password: current, new_password: newPw }),
    })

    const data = await res.json()

    if (res.ok) {
      showMsg("msg-pw", "Password updated successfully!", "success")
      document.getElementById("f-curr-pw").value  = ""
      document.getElementById("f-new-pw").value   = ""
      document.getElementById("f-confirm-pw").value = ""
      checkStrength("")
    } else {
      showMsg("msg-pw", data.detail || "Update failed.", "error")
    }
  } catch {
    showMsg("msg-pw", "Cannot reach the server.", "error")
  } finally {
    setBtnLoading("savePwBtn", false, "Update password")
  }
}