const util = ["login", "createuser", "write", "received_email", "sent_email", "read_s", "read_r", "changeinfo", "deleteuser"];
const $ = id => document.getElementById(id);

let authToken = localStorage.getItem("token") || null;
let authUsername = localStorage.getItem("username") || null;

const API_BASE = "https://test-v0kg.onrender.com";

function change(module) {
  if (module === "received_email") {
    doReadReceivedEmail();
  }

  if (module === "sent_email") {
    doReadSentEmail();
  }

  for (const u of util) {
    $(u).style.display = module === u ? "block" : "none";
  }
}


async function doLogin() {
  const user = $("username").value.trim();
  const pass = $("password").value;

  const formData = new URLSearchParams();
  formData.append("username", user);
  formData.append("password", pass);

  try {
    const res = await fetch(`${API_BASE}/users/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      $("loginerror").textContent = data.detail || "로그인에 실패했습니다.";
      return;
    }

    authToken = data.access_token;
    authUsername = user;

    localStorage.setItem("token", authToken);
    localStorage.setItem("username", authUsername);

    change("write");
  } catch (error) {
    $("loginerror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doLogout() {
  try {
    const res = await fetch(`${API_BASE}/users/logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    if (!res.ok) {
      const data = await res.json();
      $("logouterror").textContent = data.detail || "로그아웃에 실패했습니다.";
      return;
    }

    localStorage.removeItem("token");
    localStorage.removeItem("username");

    authToken = null;
    authUsername = null;
    change("login");
  } catch (error) {
    $("logouterror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doCreateUser() {
  const user = $("create_username").value.trim();
  const pass = $("create_password").value;

  if (user.length < 1) {
    $("createerror").textContent = "닉네임을 입력하세요";
    return;
  }

  if (pass.length < 8 || pass.length > 16) {
    $("createerror").textContent = "비밀번호는 8~16자여야 합니다";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/users`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: user,
        password: pass,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      $("createerror").textContent = data.detail || "회원가입에 실패했습니다.";
      return;
    }

    change("login");
  } catch (error) {
    $("createerror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doDeleteUser() {
  if ($("agree").value !== "동의") {
    $("error").textContent = "동의를 제대로 입력하세요";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/users`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    if (!res.ok) {
      const data = await res.json();
      $("deleteerror").textContent = data.detail || "회원 탈퇴에 실패했습니다.";
      return;
    }

    localStorage.removeItem("token");
    localStorage.removeItem("username");

    authToken = null;
    authUsername = null;
    change("login");
  } catch (error) {
    $("deleteerror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doUpdateUser() {
  const user = $("new_username").value.trim();
  const pass = $("new_password").value;

  if (pass.length > 0 && (pass.length < 8 || pass.length > 16)) {
    $("error").textContent = "비밀번호는 8~16자여야 합니다";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/users`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        name: user || null,
        password: pass || null,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      $("updateerror").textContent = data.detail || "회원 정보 수정에 실패했습니다.";
      return;
    }

    if (user) {
      authUsername = user;
      localStorage.setItem("username", user);
    }

    change("write");
  } catch (error) {
    $("updateerror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doWrite() {
  const receiver = $("write_name").value.trim();
  const title = $("write_title").value;
  const content = $("write_content").value;

  if (!receiver) {
    $("writeerror").textContent = "받는 사람을 입력하세요";
    return;
  }

  if (!title.trim()) {
    $("writeerror").textContent = "제목을 입력하세요";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        receiver_id: receiver,
        title,
        content,
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      $("writeerror").textContent = data.detail || "편지 전송에 실패했습니다.";
      return;
    }

    $("write_name").value = "";
    $("write_title").value = "";
    $("write_content").value = "";
  } catch (error) {
    $("writeerror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function readMessage(messageId, screenId, listItemId) {
  change(screenId);

  const listItem = document.getElementById(listItemId);
  if (listItem) {
    listItem.remove();
  }

  try {
    const res = await fetch(`${API_BASE}/messages/${messageId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      if (screenId == "read_s") { $("senterror").textContent = data.detail || "편지를 불러오지 못했습니다."; }
      if (screenId == "read_r") { $("receivederror").textContent = data.detail || "편지를 불러오지 못했습니다."; }
      return;
    }

    const email = document.createElement("div");
    email.id = data.id;

    for (const value of [
      data.sender_id,
      data.receiver_id,
      data.title,
      data.content,
    ]) {
      const field = document.createElement("div");
      field.textContent = value;
      email.appendChild(field);
    }

    $(screenId).appendChild(email);
  } catch (error) {
    if (screenId == "read_s") { $("senterror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요"; }
    if (screenId == "read_r") { $("receivederror").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요"; }
  }
}


function Read_S(messageId) {
  return readMessage(messageId, "read_s", messageId);
}


function Read_R(messageId) {
  return readMessage(messageId, "read_r", messageId);
}


async function doReadSentEmail() {
  document.querySelectorAll("._sent_email").forEach(e => e.remove());

  try {
    const res = await fetch(`${API_BASE}/messages/sent`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      $("error").textContent = data.detail || "보낸 편지를 불러오지 못했습니다.";
      return;
    }

    for (const message of data.messages) {
      const email = document.createElement("div");
      email.id = message.id;
      email.className = "_sent_email";
      email.textContent = `${message.title} - ${message.receiver_id}`;
      email.addEventListener("click", () => Read_S(message.id));
      $("sent_email").appendChild(email);
    }
  } catch (error) {
    $("error").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}


async function doReadReceivedEmail() {
  document.querySelectorAll("._received_email").forEach(e => e.remove());

  try {
    const res = await fetch(`${API_BASE}/messages/received`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      $("error").textContent = data.detail || "받은 편지를 불러오지 못했습니다.";
      return;
    }

    for (const message of data.messages) {
      const email = document.createElement("div");
      email.id = message.id;
      email.className = "_received_email";
      email.textContent = `${message.title} - ${message.sender_id}`;
      email.addEventListener("click", () => Read_R(message.id));
      $("received_email").appendChild(email);
    }
  } catch (error) {
    $("error").textContent = "서버 연결 실패 — 서버가 실행 중인지 확인하세요";
  }
}
