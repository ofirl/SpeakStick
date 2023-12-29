import { useEffect, useRef, useState } from "react"
import { websocketBaseUrl } from "./consts"

export type StickEvent = {
  type: "cellChange" | "wordEnded" | "playingWord"
  value: string
};

export const useGetStickEvents = (eventHandler: (msg: StickEvent) => void) => {
  const [connected, setConnected] = useState(false);
  const websocketRef = useRef<WebSocket>();
  const eventHandlerRef = useRef(eventHandler)

  // this is done to ensure consistent websocket connection, even if the calback changes the connection will persist
  useEffect(() => {
    eventHandlerRef.current = eventHandler
  }, [eventHandler])

  useEffect(() => {
    const websocket = new WebSocket(`${websocketBaseUrl}`)

    websocket.onopen = () => {
      setConnected(true);
      websocketRef.current = websocket;
      setInterval(() => {
        websocket.send("keep-alive")
      }, 10000)
    }

    websocket.onmessage = (msg: MessageEvent<string>) => {
      eventHandlerRef.current.call(this, JSON.parse(msg.data))
    }

    websocket.onclose = () => {
      setConnected(false);
    }

    return () => {
      websocket.close()
    }
  }, [])

  return { connected, websocket: websocketRef };
}