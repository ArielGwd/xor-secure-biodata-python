const apiBase = "/api/biodata";

async function fetchAll() {
  const resp = await fetch(apiBase);
  if (!resp.ok) throw new Error("Failed to fetch");
  return await resp.json();
}

function rowHtml(item) {
  return `
    <tr class="py-3">
      <td class="py-3 pr-4">${escapeHtml(item.name)}</td>
      <td class="py-3 pr-4">${escapeHtml(item.email)}</td>
      <td class="py-3 pr-4">${escapeHtml(item.phone)}</td>
      <td class="py-3 pr-4">${escapeHtml(item.address)}</td>
      <td class="py-3 pr-4">${escapeHtml(item.gender || "")}</td>
      <td class="py-3 pr-4 flex gap-2">
        <button onclick='openEdit(${item.id})' class="px-3 py-1 bg-yellow-400 text-white rounded">Edit</button>
        <button onclick='remove(${item.id}, "${escapeHtml(item.name)}")' class="px-3 py-1 bg-red-500 text-white rounded">Delete</button>
      </td>
    </tr>
  `;
}

function escapeHtml(s) {
  if (!s) return "";
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function loadTable() {
  const body = document.getElementById("table-body");
  body.innerHTML = "<tr><td colspan='6' class='py-6 text-center text-slate-500'>Loading...</td></tr>";
  try {
    const data = await fetchAll();
    if (!Array.isArray(data) || data.length === 0) {
      body.innerHTML = "<tr><td colspan='6' class='py-6 text-center'>No data</td></tr>";
      return;
    }
    body.innerHTML = data.map(rowHtml).join("");
  } catch (e) {
    body.innerHTML = `<tr><td colspan='6' class='py-6 text-center text-red-500'>Error loading data</td></tr>`;
    console.error(e);
  }
}

const modal = document.getElementById("modal");
const form = document.getElementById("form");
document.getElementById("btn-add").addEventListener("click", () => openAdd());
document.getElementById("btn-cancel").addEventListener("click", () => closeModal());
document.getElementById("modal-close").addEventListener("click", () => closeModal());

function openAdd() {
  document.getElementById("modal-title").innerText = "Add Biodata";
  document.getElementById("edit-id").value = "";
  form.name.value = "";
  form.email.value = "";
  form.phone.value = "";
  form.address.value = "";
  form.gender.value = "";
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function openEdit(id) {
  fetch(`${apiBase}/${id}`)
    .then(async (r) => {
      if (!r.ok) throw new Error("Failed to load biodata");
      return await r.json();
    })
    .then((d) => {
      document.getElementById("modal-title").innerText = "Edit Biodata";
      document.getElementById("edit-id").value = d.id;
      form.name.value = d.name || "";
      form.email.value = d.email || "";
      form.phone.value = d.phone || "";
      form.address.value = d.address || "";
      form.gender.value = d.gender || "";

      modal.classList.remove("hidden");
      modal.classList.add("flex");

      console.log("name", d.name);
    })
    .catch((err) => {
      alert("Error loading data");
      console.error(err);
    });
}

function closeModal() {
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

// Submit (POST/PUT)
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = document.getElementById("edit-id").value;
  const payload = {
    name: form.name.value,
    email: form.email.value,
    phone: form.phone.value,
    address: form.address.value,
    gender: form.gender.value,
  };
  if (id) {
    await fetch(`${apiBase}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } else {
    await fetch(apiBase, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }
  closeModal();
  loadTable();
});

const deleteModal = document.getElementById("delete-modal");
const deleteText = document.getElementById("delete-text");
const deleteCancel = document.getElementById("delete-cancel");
const deleteConfirm = document.getElementById("delete-confirm");

let deleteId = null;

function remove(id, name) {
  deleteId = id;
  deleteText.innerText = `Yakin ingin menghapus biodata: "${name}"?`;
  deleteModal.classList.remove("hidden");
  deleteModal.classList.add("flex");
}

function closeDeleteModal() {
  deleteModal.classList.add("hidden");
  deleteModal.classList.remove("flex");
}

deleteCancel.addEventListener("click", closeDeleteModal);

deleteConfirm.addEventListener("click", async () => {
  if (!deleteId) return;

  await fetch(`${apiBase}/${deleteId}`, {
    method: "DELETE",
  });

  deleteId = null;
  closeDeleteModal();
  loadTable();
});

loadTable();
