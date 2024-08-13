const initWebSocket = async (url: string): Promise<WebSocket> => new Promise((resolve, reject) => {
    console.log('Connecting to WebSocket:', url);
    const socket = new WebSocket(url);
    socket.binaryType = 'arraybuffer';

    socket.onopen = () => {
        console.log('WebSocket connected:', url);
        resolve(socket)
    };
    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error)
    };

    return socket;
})

export const useWebSocket = async (url: string, onMessage?: (data: any) => void) => {
    if (window.location.search === '') {
        window.location.replace(`${import.meta.env.VITE_SERVER_URL}/login`);
    }
    const socket = await initWebSocket(url + window.location.search);

    const send = (data: string) => {
        console.log('Sending:', data);
        socket.send(data);
    }

    const close = () => {
        console.log('Closing WebSocket:', url);
        socket.close();
    }

    socket.onmessage = (event) => {
        console.log('Received:', event.data);
        if (onMessage) {
            onMessage(event.data);
        }
    }

    return { send, close, socket };
}
