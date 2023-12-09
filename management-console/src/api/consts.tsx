// export const baseUrl = "http://speakstick.local/api"
export const baseUrl = window.location.hostname === "localhost" ? "http://speakstick.local/api" : "/api"
export const websocketBaseUrl = "ws://speakstick.local/ws/stick-position"
// export const baseUrl = "http://localhost:8090/api"