const $  = id => document.getElementById(id);
const API_BASE = "https://test-production-3a75.up.railway.app";

let authToken    = localStorage.getItem('token')    || null;
let authUsername = localStorage.getItem('username') || null;

function startGame() {
  alert("성공!");
}

async function doRegister() {
  const user = $('id').value.trim();
  const pass = $('password').value;
  $('error').textContent = '';
  if (user.length < 4) { $('error').textContent = '아이디는 4자 이상이어야 합니다'; return; }
  if (pass.length < 4) { $('error').textContent = '비밀번호는 4자 이상이어야 합니다'; return; }

  try {
    const res  = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password: pass })
    });

    const data = await res.json();
    if (!res.ok) { $('error').textContent = data.detail || '회원가입 실패'; return; }

    authToken    = data.token;
    authUsername = data.username;
    localStorage.setItem('token',    authToken);
    localStorage.setItem('username', authUsername);
    startGame();
  } catch(e) {
    $('error').textContent = '서버 연결 실패 — 서버가 실행 중인지 확인하세요';
  }
