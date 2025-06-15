function sayHello() {
    alert("你好，这是从 index.js 触发的！");
}

function deleteNote(noteId) {
    fetch("/delete_note", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ noteId:noteId }),
    }).then((_res) => {
        window.location.href = "/";
    });
}