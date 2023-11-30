import { useEffect, useRef, useState } from "react"
import { websocketBaseUrl } from "./consts"

type StickPosition = {
  cell: string;
}
export const useGetStickPosistion = () => {
  const [stickPosition, setStickPosition] = useState<StickPosition>();
  const [connected, setConnected] = useState(false);
  const websocketRef = useRef<WebSocket>();

  useEffect(() => {
    const websocket = new WebSocket(`${websocketBaseUrl}`)

    websocket.onopen = () => {
      setConnected(true);
      websocketRef.current = websocket;
    }

    websocket.onmessage = (msg) => {
      setStickPosition({ cell: msg.data });
    }

    websocket.onclose = () => {
      setConnected(false);
    }

    return () => {
      websocket.close()
    }
  }, [])

  return { stickPosition, connected, websocket: websocketRef };
}