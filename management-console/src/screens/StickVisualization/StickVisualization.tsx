import { CircularProgress, Typography } from "@mui/material";
import { StickEvent, useGetStickEvents } from "../../api/stick"
import { useCallback, useState } from "react";

const getPositionBackground = (currentPosition: number, position: number) => position === currentPosition ? "#96e996" : "lightgrey"

export const StickVisualization = () => {
  const [stickLog, setStickLog] = useState<string[]>([]);
  const [cellSequence, setCellSequence] = useState<number[]>([]);
  const [stickPosition, setStickPosition] = useState(5)
  const stickEventHandler = useCallback((msg: StickEvent) => {
    if (msg.type === "cellChange") {
      const newCell = parseInt(msg.value)
      setStickPosition(newCell)
      setCellSequence(prev => [...prev, newCell])
    }
    else if (msg.type === "wordEnded") {
      setStickLog(prev => [`Sequence recorded with cells ${msg.value}`, ...prev])
      setCellSequence([])
    }
    else if (msg.type === "playingWord")
      setStickLog(prev => [`Playing word ${msg.value}`, ...prev])
  }, [])

  const { connected } = useGetStickEvents(stickEventHandler);
  return (
    <div style={{ maxWidth: "50rem", gap: "1rem", display: "flex", flexDirection: "column", height: "100%", flexGrow: 1, alignItems: "center" }}>
      {
        connected ?
          (
            <div style={{ display: "grid", gridTemplateRows: "350px 1fr", height: "100%" }}>
              <div>
                <svg width="301" height="301" xmlns="http://www.w3.org/2000/svg">
                  <rect width="125" height="125" x="0" y="175" fill={getPositionBackground(stickPosition, 1)} stroke="black" /> {/* 1 */}
                  <rect width="50" height="100" x="125" y="200" fill={getPositionBackground(stickPosition, 2)} stroke="black" /> {/* 2 */}
                  <rect width="125" height="125" x="175" y="175" fill={getPositionBackground(stickPosition, 3)} stroke="black" /> {/* 3 */}
                  <rect width="100" height="50" x="0" y="125" fill={getPositionBackground(stickPosition, 4)} stroke="black" /> {/* 4 */}
                  <rect width="100" height="50" x="200" y="125" fill={getPositionBackground(stickPosition, 6)} stroke="black" /> {/* 6 */}
                  <rect width="125" height="125" x="0" y="0" fill={getPositionBackground(stickPosition, 7)} stroke="black" /> {/* 7 */}
                  <rect width="50" height="100" x="125" y="0" fill={getPositionBackground(stickPosition, 8)} stroke="black" /> {/* 8 */}
                  <rect width="125" height="125" x="175" y="0" fill={getPositionBackground(stickPosition, 9)} stroke="black" /> {/* 9 */}

                  <polygon points="125,75 175,75 225,125 225,175 175,225 125,225 75,175 75,125" fill={getPositionBackground(stickPosition, 5)} stroke="black" strokeWidth="2" /> {/* 5 */}
                  <text x="50" y="250"> 1 </text>
                  <text x="145" y="270"> 2 </text>
                  <text x="250" y="250"> 3 </text>
                  <text x="45" y="155"> 4 </text>
                  <text x="145" y="155"> 5 </text>
                  <text x="250" y="155"> 6 </text>
                  <text x="50" y="50"> 7 </text>
                  <text x="145" y="40"> 8 </text>
                  <text x="250" y="50"> 9 </text>
                </svg>
                <Typography variant="body1" textAlign="center">
                  current cell sequence: {cellSequence}
                </Typography>
                <Typography variant="h6">
                  Stick Events
                </Typography>
              </div>
              <div style={{ overflow: "scroll" }}>
                {stickLog.map(l => <Typography variant="body1">{l}</Typography>)}
              </div>
            </div>
          ) :
          <>
            <CircularProgress />
            <Typography style={{ textAlign: "center" }}>
              This might take a minute... <br />
              If the grid is not loaded after 1 minute, refresh the page to try again
            </Typography>
          </>
      }
    </div>
  )
}