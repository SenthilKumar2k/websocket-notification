<script>
    const notificationSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/notifications/'
    );

    notificationSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(data.message);
    };
</script>
Now, when you send a notification from the DRF view, it will be broadcasted to all connected clients.