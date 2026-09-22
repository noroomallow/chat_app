// =====================================
// TempChat JavaScript
// =====================================


let lastMessageCount = 0;
let lastFileCount = 0;


// =====================================
// Room Link
// =====================================

const roomLinkInput = document.getElementById("room-link");

if (roomLinkInput) {

    roomLinkInput.value =
        window.location.origin +
        "/chat/" +
        ROOM_CODE +
        "?username=Guest";
}


// =====================================
// Copy Room Link
// =====================================

function copyRoomLink() {

    const input =
        document.getElementById("room-link");

    navigator.clipboard.writeText(
        input.value
    );

    alert("Room link copied!");
}


// =====================================
// Format Time
// =====================================

function formatTime(dateString) {

    const date = new Date(
        dateString + "Z"
    );

    return date.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}


// =====================================
// Load Messages
// =====================================

async function loadMessages() {

    try {

        const response = await fetch(
            "/api/messages/" + ROOM_CODE
        );

        const data = await response.json();

        if (!data.success) {

            alert("This room has expired.");

            window.location.href = "/";

            return;
        }


        const container =
            document.getElementById("messages");


        if (
            data.messages.length ===
            lastMessageCount
        ) {
            return;
        }


        lastMessageCount =
            data.messages.length;


        container.innerHTML = "";


        data.messages.forEach(
            function(message) {

                const wrapper =
                    document.createElement("div");

                wrapper.className = "message";


                if (
                    message.username ===
                    USERNAME
                ) {

                    wrapper.classList.add(
                        "mine"
                    );

                }


                const name =
                    document.createElement("div");

                name.className =
                    "message-name";

                name.textContent =
                    message.username;


                const bubble =
                    document.createElement("div");

                bubble.className =
                    "message-bubble";

                bubble.textContent =
                    message.message;


                const time =
                    document.createElement("div");

                time.className =
                    "message-time";

                time.textContent =
                    formatTime(
                        message.created_at
                    );


                wrapper.appendChild(name);

                wrapper.appendChild(bubble);

                wrapper.appendChild(time);

                container.appendChild(wrapper);

            }
        );


        container.scrollTop =
            container.scrollHeight;

    }

    catch (error) {

        console.log(
            "Message error:",
            error
        );

    }
}


// =====================================
// Send Message
// =====================================

async function sendMessage() {

    const input =
        document.getElementById(
            "message-input"
        );

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    input.disabled = true;


    try {

        const response = await fetch(
            "/api/messages/" + ROOM_CODE,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    username: USERNAME,
                    message: message
                })
            }
        );


        const data =
            await response.json();


        if (data.success) {

            input.value = "";

            await loadMessages();

        }

        else {

            alert(
                data.error ||
                "Unable to send message."
            );

        }

    }

    catch (error) {

        alert(
            "Unable to connect to server."
        );

    }


    input.disabled = false;

    input.focus();
}


// =====================================
// Send Button
// =====================================

const sendButton =
    document.getElementById(
        "send-button"
    );


if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendMessage
    );

}


// =====================================
// Enter Key
// =====================================

const messageInput =
    document.getElementById(
        "message-input"
    );


if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );

}


// =====================================
// Upload File
// =====================================

const fileInput =
    document.getElementById(
        "file-input"
    );


if (fileInput) {

    fileInput.addEventListener(
        "change",
        uploadFile
    );

}


async function uploadFile() {

    const file =
        fileInput.files[0];


    if (!file) {
        return;
    }


    if (file.size > 10 * 1024 * 1024) {

        alert(
            "Maximum file size is 10 MB."
        );

        fileInput.value = "";

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    formData.append(
        "username",
        USERNAME
    );


    try {

        const response =
            await fetch(
                "/upload/" + ROOM_CODE,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (data.success) {

            alert(
                "File uploaded successfully."
            );

            loadFiles();

        }

        else {

            alert(
                data.error ||
                "File upload failed."
            );

        }

    }

    catch (error) {

        alert(
            "Unable to upload file."
        );

    }


    fileInput.value = "";
}


// =====================================
// Load Files
// =====================================

async function loadFiles() {

    try {

        const response =
            await fetch(
                "/api/files/" + ROOM_CODE
            );


        const data =
            await response.json();


        if (!data.success) {
            return;
        }


        if (
            data.files.length ===
            lastFileCount
        ) {
            return;
        }


        lastFileCount =
            data.files.length;


        const container =
            document.getElementById(
                "file-list"
            );


        container.innerHTML = "";


        data.files.forEach(
            function(file) {

                const card =
                    document.createElement("div");

                card.className =
                    "file-card";


                const name =
                    document.createElement("span");

                name.textContent =
                    "📎 " +
                    file.filename +
                    " — " +
                    file.username;


                const link =
                    document.createElement("a");

                link.href =
                    file.url;

                link.textContent =
                    "Download";


                card.appendChild(name);

                card.appendChild(link);

                container.appendChild(card);

            }
        );

    }

    catch (error) {

        console.log(
            "File error:",
            error
        );

    }
}


// =====================================
// Countdown
// =====================================

function updateCountdown() {

    const countdown =
        document.getElementById(
            "countdown"
        );


    const expiry =
        new Date(
            EXPIRES_AT + "Z"
        );


    const now =
        new Date();


    const difference =
        expiry - now;


    if (difference <= 0) {

        countdown.textContent =
            "Expired";

        alert(
            "This temporary room has expired."
        );

        window.location.href = "/";

        return;
    }


    const hours =
        Math.floor(
            difference /
            (1000 * 60 * 60)
        );


    const minutes =
        Math.floor(
            (
                difference %
                (1000 * 60 * 60)
            ) /
            (1000 * 60)
        );


    const seconds =
        Math.floor(
            (
                difference %
                (1000 * 60)
            ) /
            1000
        );


    countdown.textContent =
        "Expires in " +
        hours +
        "h " +
        minutes +
        "m " +
        seconds +
        "s";

}


// =====================================
// Start
// =====================================

loadMessages();

loadFiles();

updateCountdown();


// Check every 2 seconds
setInterval(
    loadMessages,
    2000
);


// Check files every 3 seconds
setInterval(
    loadFiles,
    3000
);


// Countdown every second
setInterval(
    updateCountdown,
    1000
);